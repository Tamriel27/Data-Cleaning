import streamlit as st
import pandas as pd
from io import BytesIO
import numpy as np
from datetime import datetime

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
    # 🔴 Youtube Video Rawdata Cleaning
    Upload your files
    """
    )

    uploaded_file = st.file_uploader('Youtube Video Rawdata', type='xlsx')
    uploaded_file1 = st.file_uploader('Master Data', type='xlsx')
    if not uploaded_file:
        return None
    
    yv = pd.read_excel(uploaded_file)
    yv['Permalink'] = 'https://www.youtube.com/watch?v=' + yv['Video'] + '&ab_channel=Unitel'
    yv.rename({'Video title' : 'Post Message', 
           'Video publish time' : 'Posted', 
           'Impressions' : 'Total Impressions', 
           'Likes' : 'Like', 
           'Comments added' : 'Comment', 
           'Shares' : 'Share', 
           'Views' : 'Total Video Views', 
           'Average view duration' : 'Average time video viewed', 
           'Watch time (hours)' : 'Seconds Viewed'}, axis=1, inplace=True)
    yv['Posted'] = pd.to_datetime(yv['Posted'])
    yv['Average time video viewed'] = yv['Average time video viewed'].apply(lambda x: datetime.strptime(x,'%H:%M:%S'))
    yv['Average time video viewed'] = yv['Average time video viewed'].apply(lambda x: x.second + x.minute*60 + x.hour*3600)
    yv['Seconds Viewed'] = yv['Seconds Viewed'] * 3600
    yv['Video length'] = yv['Seconds Viewed'] / yv['Total Video Views'] / yv['Average percentage viewed (%)']
    yv = yv[['Permalink', 'Post Message', 'Posted', 'Total Impressions', 
         'Impressions click-through rate (%)', 'Like', 'Dislikes', 
         'Comment', 'Share', 'Subscribers gained', 
         'Subscribers lost', 'Subscribers', 'Total Video Views', 
         'Average percentage viewed (%)', 'Average time video viewed', 
         'Seconds Viewed', 'Video length']]
    yv['Hashtags'] = yv['Post Message'].str.findall(r'#.*?(?=\s|$)')
    yv['Hashtags'] = [', '.join(i) if isinstance(i, list) else i for i in yv['Hashtags']]
    
    st.text('Yotube Video Rawdata Preview:')
    st.dataframe(yv.head())
    
    if not uploaded_file1:
        return None
    
    master_data = pd.read_excel(uploaded_file1, sheet_name='MasterData', skiprows=[0])
    master_data = master_data[['#Hashtag', 'Budget code', 'Page', 'Year']]
    st.text('Master Data Preview:')
    st.dataframe(master_data.head())
    
    target = master_data['#Hashtag'].values.tolist()
    yv['Campaign Name'] = yv['Hashtags'].apply(lambda x: ';'.join([m for m in target if m in x]))
    df = pd.merge(yv, master_data, how='left', left_on='Campaign Name', right_on='#Hashtag')
    df.rename({'Page': 'Brand'}, axis=1, inplace=True)
    df.drop(['Hashtags', '#Hashtag'], axis=1, inplace=True)
    
    df_xlsx = to_excel(df)
    st.download_button(label='📥 Download Result',
                                    data=df_xlsx ,
                                    file_name= 'Youtube_Video_Completed.xlsx')
    
if __name__ == '__main__':
    main_loop()
