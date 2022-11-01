import streamlit as st
import pandas as pd
from io import BytesIO
import numpy as np

def to_excel(ga):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        ga.to_excel(writer, index=False, sheet_name='Sheet1')
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        format1 = workbook.add_format({'num_format': '0.00'}) 
        worksheet.set_column('A:A', None, format1)  
        writer.save()
        processed_data = output.getvalue()
        return processed_data
    
def main_loop():
    st.write(
    """
    # 📈 Google Analytics Rawdata Cleaning
    Upload your files
    """
    )
    
    uploaded_file = st.file_uploader('Google Analytics Rawdata', type='xlsx')
    uploaded_file1 = st.file_uploader('Master Data', type='xlsx')
    
    if not uploaded_file:
        return None
    
    ga = pd.read_excel(uploaded_file, sheet_name='Dataset1')
    ga = ga[ga['Page'].str.contains('/pagead/') == False]
    ga['Page'] = ga['Page'].str.split('?').str[0].str.replace(' ', '')
    ga = ga[['Page', 'Source / Medium', 'Device Category', 'Users', 
         'New Users', 'Sessions', 'Avg. Session Duration', 
         'Pages / Session', 'Number of Sessions per User', 'Bounces', 
         'Bounce Rate', 'Pageviews', 'Unique Pageviews', 
         'Avg. Time on Page', ' AVG Server Connection Time (sec)', 
         'AVG Server Response Time (sec)']]
    
    st.text('Google Analytics Rawdata Preview:')
    st.dataframe(ga.head())
    
    if not uploaded_file1:
        return None
    
    master_data = pd.read_excel(uploaded_file1, sheet_name='MasterData', skiprows=[0])
    master_data = master_data[['Campaign name', 'Budget code', 'Year', 'Page', 'News link', 'Promotion link']]
    master_data.rename({'Page': 'Brand'}, axis=1, inplace=True)
    
    st.text('Master Data Preview:')
    st.dataframe(master_data.head())
    
    df = pd.merge(ga, master_data, how='left', left_on='Page', right_on=['News link' and 'Promotion link'])
    df['Source'] = df['Source / Medium'].str.split('/').str[0].str.replace(' ', '')
    df['Medium'] = df['Source / Medium'].str.split('/').str[1].str.replace(' ', '')
    df['Link'] = 'https://www.unitel.mn' + df['Promotion link']
    
    df_xlsx = to_excel(df)
    st.download_button(label='📥 Download Result',
                                    data=df_xlsx ,
                                    file_name= 'Google_Analytics_Completed.xlsx')
    
if __name__ == '__main__':
    main_loop()
    
    
