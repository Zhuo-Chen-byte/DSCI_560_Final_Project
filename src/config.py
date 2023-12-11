import os
    
class Config:
    def __init__(self):
        self.openai_api_key = 'my_openai_api_key'
        
        
        # Url and local folder path to store stock info, company recommendations, and explanations
        self.stock_list = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA',
            'META', 'TSLA', 'TSM', 'AVGO', 'ORCL',
            'ADBE', 'ASML','BABA', 'CRM', 'ACN',
             'NFLX', 'AMD', 'SAP', 'INTC', 'QCOM']
        self.stock_info_folder_path = '/Users/zhuochen_henry/Desktop/DSCI_560_Final_Project/stock_info_and_recommendations'
        self.stock_info_filepath = os.path.join(self.stock_info_folder_path, 'stock_info.csv')
        self.recommended_companies_and_explanations_filepath = os.path.join(self.stock_info_folder_path, 'recommended_companies_and_explanations_filepath.csv')
        
        
        # Url and local folder path to access template resumes
        self.resume_template_base_url = 'https://www.overleaf.com/latex/templates?q=technical+resume'
        self.resume_template_images_folder_path = '/Users/zhuochen_henry/Desktop/DSCI_560_Final_Project/resume_template_images'
        
        self.resume_template_images_metadata_folder_path = os.path.join(self.resume_template_images_folder_path, 'metadata')
        self.resume_template_images_metadata_filepath = os.path.join(self.resume_template_images_metadata_folder_path, 'resume_template_image_metadata.csv')
