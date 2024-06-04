''' Create the Personal Functions for clean and transform Data'''

import pandas as pd
import os

class PersonalFunctions:
    
    def __init__(self):
        self.dir_path = os.path.dirname(os.path.abspath(__file__))
        
    def clean_columns(self, df:pd.DataFrame):
        
        # list to replaced characters
        characters = ['á','ú','é','í','ó',' ','ç','ã']
        characters_to_replace = ['a','u','e','i','o','_','c','a']
        
        # apply the clean inside the dataframe
        for char, replacement in zip(characters, characters_to_replace):
            df.columns = df.columns.str.replace(char, replacement)
        
        df.columns = df.columns.str.lower()
        
        return df
    
    def change_type(self, df:pd.DataFrame, column, type:str):
        df[column] = df[column].astype(type)
        return df
    
    def replace_str(self, df: pd.DataFrame, columns: list, old_str: str, new_str: str) -> pd.DataFrame:
        for column in columns:
            if column in df.columns:
                df[column] = df[column].str.replace(old_str, new_str)
        return df
