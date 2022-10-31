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
    # 📊 Twitter Post Rawdata Cleaning
    Upload your files
    """
    )

    uploaded_file = st.file_uploader('Twitter Post Rawdata', type='csv')
    uploaded_file1 = st.file_uploader('Master Data', type='xlsx')
    if not uploaded_file:
        return None

    tw = pd.read_csv(uploaded_file, infer_datetime_format=True)
    tw.loc[:, tw.columns.str.contains('promoted')] = tw.loc[:, tw.columns.str.contains('promoted')].replace('-', '0', regex=True)
    tw.loc[:, tw.columns.str.contains('promoted')] = tw.loc[:, tw.columns.str.contains('promoted')].apply(pd.to_numeric)
    tw['Total Impressions'] = tw['promoted impressions'] + tw['impressions']
    tw['Total Engagements'] = tw['retweets'] + tw['replies'] + tw['likes'] + tw['url clicks'] + tw['hashtag clicks'] + tw['detail expands'] + tw['promoted retweets'] + tw['promoted replies'] + tw['promoted likes'] + tw['promoted url clicks'] + tw['promoted hashtag clicks'] + tw['promoted detail expands']
    tw['Total Video views'] = tw['media views'] + tw['promoted media views']
    tw['Organic Engagements'] = tw['retweets'] + tw['replies'] + tw['likes'] + tw['url clicks'] + tw['hashtag clicks'] + tw['detail expands']
    tw['Paid Engagements'] = tw['promoted retweets'] + tw['promoted replies'] + tw['promoted likes'] + tw['promoted url clicks'] + tw['promoted hashtag clicks'] + tw['promoted detail expands']
    tw['Total Retweets'] = tw['retweets'] + tw['promoted retweets']
    tw['Total Replies'] = tw['replies'] + tw['promoted replies']
    tw['Total Like'] = tw['likes'] + tw['promoted likes']
    tw['Total Url clicks'] = tw['url clicks'] + tw['promoted url clicks']
    tw['Total Hashtag clicks'] = tw['hashtag clicks'] + tw['promoted hashtag clicks']
    tw['Total Detail expands'] = tw['detail expands'] + tw['promoted detail expands']
    
    post = []
    for row in tw['Tweet text']:
        if row.startswith('@') : post.append('Mention')
        else : post.append('Tweet')
    tw['Post type'] = post
    
    tw = tw[['Tweet id', 'Tweet permalink', 'Tweet text', 'time', 
         'impressions', 'media views', 'promoted impressions', 
         'promoted media views', 'Total Impressions', 'Total Engagements', 
         'Total Video views', 'Organic Engagements', 'Paid Engagements', 
         'Total Retweets', 'Total Replies', 'Total Like', 'Total Url clicks', 
         'Total Hashtag clicks', 'Total Detail expands', 'Post type']]
    
    tw['Hashtags'] = tw['Tweet text'].str.findall(r'#.*?(?=\s|$)')
    tw['Hashtags'] = [', '.join(i) if isinstance(i, list) else i for i in tw['Hashtags']]
    st.text('Twitter Post Completed Preview:')
    st.dataframe(tw.head())
    
    if not uploaded_file1:
        return None
    
    master_data = pd.read_excel(uploaded_file1, sheet_name='MasterData', skiprows=[0])
    master_data = master_data[['#Hashtag', 'Budget code', 'Page', 'Year']]
    st.text('Master Data Preview:')
    st.dataframe(master_data.head())
    
    target = master_data['#Hashtag'].values.tolist()
    tw['Campaign Name'] = tw['Hashtags'].apply(lambda x: ';'.join([m for m in target if m in x])).replace('', np.nan)
    
    df = pd.merge(tw, master_data, how='left', left_on='Campaign Name', right_on='#Hashtag')
    df.rename({'Page': 'Brand'}, axis=1, inplace=True)
    df.drop(['Hashtags', '#Hashtag'], axis=1, inplace=True)
    
    df_xlsx = to_excel(df)
    st.download_button(label='📥 Download Result',
                                    data=df_xlsx ,
                                    file_name= 'Twitter_Post_Completed.xlsx')
    
if __name__ == '__main__':
    main_loop()
    
