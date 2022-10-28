import streamlit as st
import pandas as pd
from io import BytesIO
import numpy as np

def to_excel(df):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Sheet1')
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
    # 📊 Instagram Story Rawdata Cleaning
    Upload your files
    """
    )

    uploaded_file = st.file_uploader('Instagram Story Rawdata', type='xlsx')
    if not uploaded_file:
        return None
    
    df = pd.read_excel(uploaded_file, sheet_name='Worksheet')
    df = df[['Date', 'Impressions', 'Reach', 'Completions', 
         'Exits', 'Replies', 'Taps Back', 
         'Taps Forward', 'Url', 'Campaign name', 
         'Budget code', 'Year', 'Brand']]
    df['Post type'] = 'Story'
    df['Date'] = pd.to_datetime(df['Date'])
    st.text('Instagram Story Completed Preview:')
    st.dataframe(df.head())
    
    df_xlsx = to_excel(df)
    st.download_button(label='📥 Download Result',
                                    data=df_xlsx ,
                                    file_name= 'Instagram_Story_Completed.xlsx')

if __name__ == '__main__':
    main_loop()
