import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO


st.write(
    """
# 📊 FB Page Rawdata Cleaning
Upload your files
"""
)

#Allow only .xlsx file to be uploaded
uploaded_file = st.file_uploader('FB Page Data', type='xlsx')

#Check if file was uploaded
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, sheet_name='Key Metrics', skiprows=[1])
    # Work with the dataframe
    st.text('Data preview:')
    st.dataframe(df.head())

    df = df[df.columns.drop(list(df.filter(regex=r'(Weekly|28 Days|30-Second)')))]
    df = df.iloc[:, np.r_[:13, 31:36, 37]]

    st.text('Completed Data:')
    st.dataframe(df.head())

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

    df_xlsx = to_excel(df)
    st.download_button(label='📥 Download Current Result',
                                    data=df_xlsx ,
                                    file_name= 'FB_Page_Completed.xlsx')