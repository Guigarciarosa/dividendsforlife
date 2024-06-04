'''
    Create a Streamlit app to Test 
'''

# framework
import streamlit as st
# data manipulation
import pandas as pd
# database
import sqlite3
from routines.extract import Extract


class main:
    
    def __init__(self):
        pass
    
    
    def dashboard(self):
        st.markdown('<h3> Insira o Codigo da Ação </h3>',unsafe_allow_html=True)
        get_stock = st.text_input('   ')
        
        if get_stock:
            ext_inst = Extract()
            html_content = ext_inst.extract_fundamentus_html(stock=get_stock)
            final_data = ext_inst.transform_html(html_content)
        
            st.markdown(self.create_html_cards(final_data),unsafe_allow_html=True)
 
        
    
    def create_html_cards(self, data):
        # Convert the DataFrame to a list of dictionaries for easier iteration
        records = data.to_dict(orient='records')
        
        # HTML and CSS for the card layout
        for record in records:
            style = """
            <style>
            .card {
                box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
                transition: 0.3s;
                width: 100%;
                border-radius: 5px;
                margin: 10px 0;
            }

            .card:hover {
                box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
            }

            .container {
                padding: 2px 16px;
            }

            .title {
                font-size: 18px;
                font-weight: bold;
            }
            </style>
            """
            div_ = f"""
            <div class="card">
                <div class="container">
                    <p class="title">Stock: {record.get('papel', 'N/A')}</p>
                    <p>Price: R${record.get('cotacao', 'N/A')}</p>
                    <p>Setor: {record.get('setor', 'N/A')}</p>
                    <p>Max 52 weeks: {record.get('max_52_sem', 'N/A')}</p>
                    <!-- Add more fields as necessary -->
                </div>
            </div>
            """
            card_html = style + div_
        return card_html


if __name__ == '__main__':
    main_inst = main()
    main_inst.dashboard()