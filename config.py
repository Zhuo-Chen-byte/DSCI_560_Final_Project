import os
    
class Config:
    def __init__(self):
        self.openai_api_key = 'my_openai_api_key'
        
        # Url and local folder path to store stock info, company recommendations, and explanations
        self.stock_list = ['AAPL', 'ACN', 'ADBE', 'AMD', 'AMZN',
            'ASML', 'AVGO', 'BABA', 'CRM', 'GOOGL',
            'INTC', 'META', 'MSFT', 'NFLX', 'NVDA',
            'ORCL', 'QCOM', 'SAP', 'TSLA', 'TSM']
        self.stock_id_to_company_name = {'AAPL': 'Apple', 'ACN': 'Accenture', 'ADBE': 'Adobe', 'AMD': 'Advanced Micro Devices',
            'AMZN': 'Amazon', 'ASML': 'ASML', 'AVGO': 'Broadcom', 'BABA': 'Alibaba',
            'CRM': 'Salesforce', 'GOOGL': 'Google', 'INTC': 'Intel', 'META': 'Meta',
            'MSFT': 'Microsoft', 'NFLX': 'Netflix', 'NVDA': 'Nividia', 'ORCL': 'Oracle',
            'QCOM': 'Qualcomm', 'SAP': 'SAP', 'TSLA': 'Tesla', 'TSM': 'Taiwan Semiconductor'}
        
        self.stock_info_folder_path = '/Users/zhuochen_henry/Desktop/DSCI_560_Final_Project/stock_info_and_recommendations'
        self.stock_info_filepath = os.path.join(self.stock_info_folder_path, 'stock_info.csv')
        self.recommended_companies_and_descriptions_filepath = os.path.join(self.stock_info_folder_path, 'recommended_companies_and_descriptions.csv')
        
        self.historical_h1b_sponsorships_and_recommendations_folder_path = '/Users/zhuochen_henry/Desktop/DSCI_560_Final_Project/historical_h1b_sponsorships_and_recommendations'
        self.historical_h1b_sponsorships_filepath = os.path.join(self.historical_h1b_sponsorships_and_recommendations_folder_path, 'historical_h1b_sponsorships_2018_2023.csv')
        self.recommended_companies_and_descriptions_for_international_students_filepath = os.path.join(self.historical_h1b_sponsorships_and_recommendations_folder_path, 'recommended_companies_and_descriptions_for_international_students.csv')
        
        # Url and local folder path to access template resumes
        self.resume_template_base_url = 'https://www.overleaf.com/latex/templates?q=technical+resume'
        self.resume_template_images_folder_path = '/Users/zhuochen_henry/Desktop/DSCI_560_Final_Project/resume_template_images'
        
        self.resume_template_images_metadata_folder_path = os.path.join(self.resume_template_images_folder_path, 'metadata')
        self.resume_template_images_metadata_filepath = os.path.join(self.resume_template_images_metadata_folder_path, 'resume_template_image_metadata.csv')
