# DSCI_560_Final_Project
1. yahoo_finance_scrapper.py visits yahoo finance, scraps, formats, and stores stock information (of company symbols in ```config.stock_list```) to the given filepath ```config.stock_info_filepath```
<br/>
2. prompt_training_recommender.py prompt-trains GPT-4 based on the stock information data, recommends several companies that are likely to hired (with short descriptions of each), and stores the recommendations to the given filepath ```config.recommended_companies_and_descriptions_filepath```
<br/>
3. prompt_training_recommender_for_international_students.py prompt-trains GPT-4 based on the stock information data & previous years h-1b sponsorships, recommends several companies that are likely to provide h-1b sponsorships (with short descriptions of each), and stores the recommendations to the given filepath ```config.recommended_companies_and_descriptions_for_international_students_filepath```
<br/>
4. resume_template_image_scrapper.py random downloads a few resume templates from ```config.resume_template_base_url```, transfers them as images, and stores them into ```config.resume_template_images_folder_path```
<br/>
5. Please keep 2 config.py the same (1 in the folder, another inside /src)
<br/>
6. ```main.py``` initiates a streamlit interface. To see further details, visit
   <br/> https://youtu.be/DRdQT6L7uoQ
<br/>
7. To initiate the program, run the command line in the project directory
   <br/>```sh commands.sh```
<br/>
8. Please include model bins in the local directory and adjust line 62 in main.py
   <br/>```llm = CTransformers(model='local_models/gpt2.bin', model_type='gpt2')```
   <br/> and adjust word embeddings accordingly
<br/>
9. You need to make the dataset historical_h1b_sponsorships_2018_2023.csv yourself from
   <br/> https://www.uscis.gov/tools/reports-and-studies/h-1b-employer-data-hub
