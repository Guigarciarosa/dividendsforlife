''' File to Extract the Stock Data from website.fundamentus'''

# packages
# data manipulation
import pandas as pd
import datetime as dt
import os 

# using the scrapping libs
import re
import requests
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse

# lib to passe cookies
import http.cookiejar

# database
import sqlite3
from .clean_data_functions import PersonalFunctions


class Extract:
    def __init__(self):
        self.dir_path = os.path.dirname(os.path.abspath(__file__))
        self.conn = sqlite3.connect(
            fr'{self.dir_path}/../../database/database.sqlite3'
        )
    
    def extract_fundamentus_html(self, stock: str) -> str:
        # create a token to pass the cookies
        cookie_jar = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
        opener.addheaders = [
            ('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201'),
            ('Accept', 'text/html, text/plain, text/css, text/sgml, */*;q=0.01')
        ]
        
        url = f'https://www.fundamentus.com.br/detalhes.php?papel={stock}'
        html = opener.open(url)
        html_content = html.read().decode('ISO-8859-1')
        return html_content
    
    def transform_html(self, html_content: str) -> pd.DataFrame:
        # create the pattern
        pattern = re.compile('<table class="w728">.*</table>', re.DOTALL)
        final_soup = re.findall(pattern, html_content)[0]
        soup = BeautifulSoup(final_soup, 'lxml')

        data = []
        for dt in soup.find_all("span", attrs={'class':'txt'}):
            data.append(dt.text)
        
        column_names = [data[0:len(data):2]]
        column_names_clean = [column[:9] for column in column_names]
        
        rows = [data[1:len(data):2]]
        rows_clean = [str(row[:9]) for row in rows]
        
        rows_clean = eval(rows_clean[0])
        
        final_data = pd.DataFrame([rows_clean], columns=column_names_clean)
        final_data.columns = final_data.columns.map(''.join)
        
        pf = PersonalFunctions()
        final_data = pf.clean_columns(final_data)
        
        if 'cotacao' not in final_data.columns:
            print("Warning: 'cotacao' column not found in the data")
        
        final_data = pf.replace_str(final_data, ['cotacao'], ',', '.')
        
        return final_data
        
    def insert_into_database(self, df:pd.DataFrame):
        
        df.to_sql('stock_prices_daily',
                  con=self.conn,
                  schema=None,
                  if_exists='append',
                  index=False)
        print('\n Data Insert into DB')
        self.conn.close()


if __name__ == '__main__':
    # Create a instance
    pf = PersonalFunctions()
    
    # Create an instance of extract
    ex_inst = Extract()

    #Extract HTML content
    html_content = ex_inst.extract_fundamentus_html()
    
    # Transform HTML content into structured data
    final_data = ex_inst.transform_html(html_content)
   
    ex_inst.insert_into_database(df=final_data)