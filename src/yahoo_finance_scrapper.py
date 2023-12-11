import yfinance as yf
import pandas as pd
import shutil, os
import datetime
import requests

from bs4 import BeautifulSoup
from typing import Tuple

from utility import find_the_adjusted_final_trading_date_of_the_quarter
from config import Config


class YahooFinanceScrapper:
    def __init__(self, config: Config) -> None:
        self.config = config
    
    
    def scrap_stock_finance(self) -> pd.DataFrame:
        the_final_trading_date_of_the_quarter, the_date_before_the_final_trading_date_of_the_quarter = find_the_adjusted_final_trading_date_of_the_quarter()
        stock_list, stock_finance = self.config.stock_list, []
        
        for symbol in stock_list:
            stock = yf.Ticker(symbol)
            hist_data = stock.history(start=the_date_before_the_final_trading_date_of_the_quarter, end=the_final_trading_date_of_the_quarter, interval='1d')
            hist_data.reset_index(inplace=True)
            
            hist_data['Symbol'] = symbol
            hist_data['Date'] = pd.to_datetime(hist_data['Date'])
            hist_data['Date'] = hist_data['Date'].dt.date
        
            stock_finance.append(hist_data[['Symbol', 'Date', 'Close', 'Volume']])
            
        return pd.concat(stock_finance, ignore_index=True)
    
    
    def scrap_stock_profile(self) -> pd.DataFrame:
        stock_list, stock_profile = self.config.stock_list, dict()
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        
        for symbol in stock_list:
            url = f'https://finance.yahoo.com/quote/{symbol}/profile?p={symbol}'
            
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            company_profile = soup.find('p', class_='D(ib) Va(t)')
        
            profile_data, current_key = {}, None
        
            for child in company_profile.children:
                if child.name == 'span' and not 'Fw(600)' in child.get('class', []):
                    current_key = child.get_text().strip()
                elif current_key and child.name == 'span' and 'Fw(600)' in child.get('class', []):
                    profile_data[current_key] = child.get_text().strip()
                
            stock_profile[symbol] = profile_data
            print(f'{symbol} scraped correctly')
        
        stock_profile_df = pd.DataFrame.from_dict(stock_profile, orient='index')
        stock_profile_df.reset_index(inplace=True)
        stock_profile_df.rename(columns={'index': 'Symbol'}, inplace=True)
        
        return stock_profile_df
    
    
    def save_stock_info(self) -> None:
        stock_finance_df = self.scrap_stock_finance()
        stock_profile_df = self.scrap_stock_profile()
        
        pd.merge(stock_finance_df, stock_profile_df, on='Symbol').to_csv(self.config.stock_info_filepath, index=False)
        print('Stock information data saved successfully.')


def main():
    config = Config()
    
    if os.path.isdir(config.stock_info_folder_path):
        shutil.rmtree(config.stock_info_folder_path)
        
    os.mkdir(config.stock_info_folder_path)
    
    yahoo_finance_scrapper = YahooFinanceScrapper(config)
    yahoo_finance_scrapper.save_stock_info()
    

if __name__ == '__main__':
    main()
