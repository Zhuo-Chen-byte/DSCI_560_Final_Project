import pandas as pd
import numpy as np
import shutil, os
import requests
import random
import time
import cv2

from pdf2image import convert_from_path
from selenium import webdriver
from bs4 import BeautifulSoup
from typing import List

from config import Config


class ResumeTemplateImageScrapper:
    def __init__(self, config: Config, chrome_driver) -> None:
        self.config = config
        self.chrome_driver = chrome_driver
    
    
    def add_border_to_image(self, image: np.ndarray):
        return cv2.copyMakeBorder(
            image, 3, 3, 3, 3,
            cv2.BORDER_CONSTANT,
            value=[0, 0, 0])
    
    
    def convert_pdfs_to_images(self) -> List[str]:
        resume_template_images_folder_path = self.config.resume_template_images_folder_path
        pdf_filepaths = os.listdir(resume_template_images_folder_path)
        resume_template_image_filepaths = []
        
        for filename in pdf_filepaths:
            if not filename.endswith('.pdf'):
                continue
                
            pdf_filepath = os.path.join(resume_template_images_folder_path, filename)
            
            images = convert_from_path(pdf_filepath)
            os.remove(pdf_filepath)
            
            image_filepaths, cv2_images, n = [], [], len(images)
            
            for i in range(n):
                image_filepath = pdf_filepath[:-4] + '_page' + str(i) + '.jpg'
                image_filepaths.append(image_filepath)
                
                images[i].save(image_filepath, 'JPEG')
            
            for i in range(n):
                cv2_images.append(cv2.imread(image_filepaths[i]))
                os.remove(image_filepaths[i])
                
            combined_image = self.add_border_to_image(cv2.vconcat(cv2_images))
            combined_image_name = pdf_filepath[:-4] + '.jpg'
            
            cv2.imwrite(combined_image_name, combined_image)
            resume_template_image_filepaths.append(combined_image_name)
        
        return resume_template_image_filepaths
    
    
    def download_resume_templates(self, resume_template_urls: List[str]) -> None:
        resume_template_images_folder_path = self.config.resume_template_images_folder_path
        
        for url in resume_template_urls:
            pdf_name = url.split('/')[-1]
            pdf_data = requests.get(url).content
        
            with open(os.path.join(resume_template_images_folder_path, pdf_name), 'wb') as file:
                file.write(pdf_data)


    def scrape_resume_templates_randomly(self) -> List[str]:
        chrome_driver = self.chrome_driver
        resume_template_base_url = self.config.resume_template_base_url
        
        chrome_driver.get(resume_template_base_url)
        time.sleep(15)

        web_html = chrome_driver.page_source
        soup = BeautifulSoup(web_html, 'html.parser')
        search_hits = soup.find_all('div', class_='search-hit')
        
        resume_template_urls = []
        
        for hit in search_hits:
            pdf_div = hit.find('div', class_='search-image')
            
            if not pdf_div is None and not pdf_div.a is None:
                pdf_url = pdf_div.a.get('href')
                
                if not pdf_url is None:
                    if not pdf_url.startswith('http'):
                        pdf_url = resume_template_base_url + pdf_url
            
                resume_template_urls.append(pdf_url + '.pdf')
        
        url_count = len(resume_template_urls)
        random.shuffle(resume_template_urls)
        
        self.download_resume_templates(resume_template_urls)
        chrome_driver.quit()
        
        for i in range(url_count):
            resume_template_urls[i] = resume_template_urls[i][:-4]
            
        return resume_template_urls


def main():
    print('\n--------- Resume template image scrapper begins ---------\n')
    
    config = Config()

    if os.path.isdir(config.resume_template_images_folder_path):
        shutil.rmtree(config.resume_template_images_folder_path)

    os.mkdir(config.resume_template_images_folder_path)
    os.mkdir(config.resume_template_images_metadata_folder_path)

    chrome_driver = webdriver.Chrome()
    
    resume_template_image_scrapper = ResumeTemplateImageScrapper(config, chrome_driver)
    resume_template_urls = resume_template_image_scrapper.scrape_resume_templates_randomly()
    resume_template_image_filepaths = resume_template_image_scrapper.convert_pdfs_to_images()

    pd.DataFrame(zip(resume_template_image_filepaths, resume_template_urls), columns=['filepath', 'url']).to_csv(config.resume_template_images_metadata_filepath, index=False)

    print('\n--------- Resume template image scrapper finishes ---------\n')


if __name__ == '__main__':
    main()
