import os
    
class Config:
    def __init__(self):
        self.openai_api_key = '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'
        
        
        # Url and local folder path to store stock info, company recommendations, and explanations
        self.stock_list = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA',
            'META', 'TSLA', 'TSM', 'AVGO', 'ORCL',
            'ADBE', 'ASML','BABA', 'CRM', 'ACN',
             'NFLX', 'AMD', 'SAP', 'INTC', 'QCOM']
        self.stock_info_filepath = '/Users/zhuochen_henry/Desktop/Project/yahoo_data/stock_info.csv'
        
        self.recommended_companies_and_explanations_filepath = '/Users/zhuochen_henry/Desktop/Project/yahoo_data/company_recommendations.csv'
        
        
        # Url and local folder path to access template resumes
        self.resume_template_base_url = 'https://www.overleaf.com/latex/templates?q=technical+resume'
        self.resume_template_images_folder_path = '/Users/zhuochen_henry/Desktop/Project/resume_template_images'
        self.resume_template_images_metadata_folder_path = '/Users/zhuochen_henry/Desktop/Project/resume_template_images/metadata'
        self.resume_template_images_metadata_filepath = os.path.join(self.resume_template_images_metadata_folder_path, 'resume_template_image_metadata.csv')
