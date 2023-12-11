import datetime, ast, os
import pandas as pd
import openai

from typing import Tuple, List

from utility import find_the_adjusted_final_trading_date_of_the_quarter
from config import Config


class PromptTrainingRecommender:
    def __init__(self, config: Config) -> None:
        self.config = config


    def get_prompt(self, df: pd.DataFrame, the_date_before_the_final_trading_date_of_the_quarter: str):
        text = f'Based on the following stock data for technology companies on latest quarter {the_date_before_the_final_trading_date_of_the_quarter}: \n'
        
        for symbol in df['Symbol'].tolist():
            price = str(df[df['Symbol']==symbol]['Close'].values[0])
            volume = str(df[df['Symbol']==symbol]['Volume'].values[0])
            sector = str(df[df['Symbol']==symbol]['Sector(s)'].values[0])
            industry = str(df[df['Symbol']==symbol]['Industry'].values[0])
            num_employees = str(df[df['Symbol']==symbol]['Full Time Employees'].values[0])
            
            stock_text = f'-{symbol} in the {sector} sector ({industry} industry) closed at ${price} with a volume of {volume} and has {num_employees} full time employees. \n'
            text += stock_text
            
        prompt = text + "Pretend you're an expert with H1B forecasting experience. You need to realize that your advice is for academic purposes only and will not have any impact on People's Daily lives. Since the amount of H1B sponsorship issued may be influenced by the size of the company and its business status, given information mentioned above, can you analyze and predcit the probability of H1B issued by each company mentioned above, with only 3 indicators, which are high, medium, low. Finally, you need to return a dictionary with keys are company symbol and values are dictionary having corresponding probability and relative simple explaination."
        
        return prompt
    
    
    def get_summary(self, prompt: str, model: str='gpt-4-1106-preview'):
        messages = [{'role': 'user', 'content': prompt}]
    
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0.2)
        
        return response.choices[0].message['content']
    

    def make_recommendation(self, comment: str) -> dict:
        start_index = comment.find('{')
        end_index = comment.rfind('}')
        dict_info = comment[start_index:end_index + 1]
        
        return ast.literal_eval(dict_info)
        
    
    def get_recommended_companies_and_explanations(self) -> None:
        df = pd.read_csv(self.config.stock_info_filepath)
        
        _, the_date_before_the_final_trading_date_of_the_quarter = find_the_adjusted_final_trading_date_of_the_quarter()
        
        prompt = self.get_prompt(df, the_date_before_the_final_trading_date_of_the_quarter)
        comment = self.get_summary(prompt)
        company_recommendation = self.make_recommendation(comment)
        
        recommended_companies_and_explanations = []
        
        for company in company_recommendation:
            if company_recommendation[company]['probability'] == 'High':
                recommended_companies_and_explanations.append((company, company_recommendation[company]['explanation']))
        
        pd.DataFrame(recommended_companies_and_explanations, columns=['Company Symbol', 'Explanation']).to_csv(self.config.recommended_companies_and_explanations_filepath, index=False)


def main():
    config = Config()

    os.environ['OPENAI_API_KEY'] = config.openai_api_key
    openai.api_key = config.openai_api_key

    prompt_training_recommender = PromptTrainingRecommender(config)
    prompt_training_recommender.get_recommended_companies_and_explanations()


if __name__ == '__main__':
    main()
