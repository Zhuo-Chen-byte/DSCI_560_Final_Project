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
        
        n = len(df)
        
        for i in range(n):
            symbol = df['Symbol'].iloc[i]
            close_price = df['Close'].iloc[i]
            volume = df['Volume'].iloc[i]
            sector = df['Sector(s)'].iloc[i]
            industry = df['Industry'].iloc[i]
            num_employees = df['Full Time Employees'].iloc[i]
            
            h1b_sponsorships_2018 = df['Approvals_2018'].iloc[i]
            h1b_sponsorships_2019 = df['Approvals_2019'].iloc[i]
            h1b_sponsorships_2020 = df['Approvals_2020'].iloc[i]
            h1b_sponsorships_2021 = df['Approvals_2021'].iloc[i]
            h1b_sponsorships_2022 = df['Approvals_2022'].iloc[i]
            h1b_sponsorships_2023 = df['Approvals_2023'].iloc[i]
            
            stock_text = f'-{symbol} in the {sector} sector ({industry} industry) closed at ${close_price} with a volume of {volume} and has {num_employees} full time employees. For historical h1b sponsorships, {symbol} filed {h1b_sponsorships_2018} h1b sponsorship applications in 2018, {h1b_sponsorships_2019} h1b sponsorship applications in 2019, {h1b_sponsorships_2020} h1b sponsorship applications in 2020, {h1b_sponsorships_2021} h1b sponsorship applications in 2021, {h1b_sponsorships_2022} h1b sponsorship applications in 2022, and {h1b_sponsorships_2023} h1b sponsorship applications in 2023 \n'
            text += stock_text
            
        prompt = text + "Pretend you're an expert with H1B forecasting experience. You need to realize that your advice is for academic purposes only and will not have any impact on People's Daily lives. Since the amount of H1B sponsorship issued may be influenced by the size of the company, its business status, and its tendency to hire international students (based on its historical h1b sponsorships), given information mentioned above, can you analyze and predcit the probability of H1B issued by each company mentioned above, with only 3 indicators, which are high, medium, low. Finally, you need to return a dictionary with keys are company symbol and values are dictionary with corresponding probability and relative simple description of the company."
        
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
        df1 = pd.read_csv(self.config.stock_info_filepath)
        df2 = pd.read_csv(self.config.historical_h1b_sponsorships_filepath)
        df = pd.merge(df1, df2, on='Symbol')
        
        _, the_date_before_the_final_trading_date_of_the_quarter = find_the_adjusted_final_trading_date_of_the_quarter()
        stock_id_to_company_name = self.config.stock_id_to_company_name
        
        prompt = self.get_prompt(df, the_date_before_the_final_trading_date_of_the_quarter)
        comment = self.get_summary(prompt)
        stock_id_and_recommendation = self.make_recommendation(comment)
        
        recommended_companies_and_descriptions_for_international_students = []
        
        for stock_id in stock_id_and_recommendation:
            if stock_id_and_recommendation[stock_id]['probability'] == 'Medium' or stock_id_and_recommendation[stock_id]['probability'] == 'High':
                recommended_companies_and_descriptions_for_international_students.append((stock_id_to_company_name[stock_id], stock_id_and_recommendation[stock_id]['description']))
        
        pd.DataFrame(recommended_companies_and_descriptions_for_international_students, columns=['company', 'description']).to_csv(self.config.recommended_companies_and_descriptions_for_international_students_filepath, index=False)


def main():
    print('\n--------- Prompting training recommender (for international students) begins ---------\n')
    
    config = Config()

    os.environ['OPENAI_API_KEY'] = config.openai_api_key
    openai.api_key = config.openai_api_key

    prompt_training_recommender = PromptTrainingRecommender(config)
    prompt_training_recommender.get_recommended_companies_and_explanations()
    
    print('--------- Prompting training recommender (for international students) finishes ---------\n')

if __name__ == '__main__':
    main()
