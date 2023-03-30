import streamlit as st
import pandas as pd
from io import BytesIO
import numpy as np


st.write(
    """
# 📊 FB Post Rawdata Cleaning
Upload your files
"""
)


def merge_files(data1, data2):
    return pd.merge(data1, data2, how='left', left_on='Campaign Hashtag', right_on='#Hashtag')

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

def listing_splitter(text, target):
    #Try except to handle np.nans in input
    try:
        #Extract the list of flags
        flags = [l for l in target if l in text]
        #If any flags were extracted then return the list
        if flags:
            return flags
        #Otherwise return np.nan
        else:
            return np.nan
    except AttributeError:
        return np.nan

#Allow only .csv .xlsx files to be uploaded
uploaded_file1 = st.file_uploader('Facebook Raw Data', type='csv')

if uploaded_file1 is not None:
    #Loading data
    key_metrics = pd.read_csv(uploaded_file1)
    
    #Sorting columns
    key_metrics = key_metrics[['Post ID', 'Page ID', 'Page name', 'Description', 'Duration (sec)', 
                           'Publish time', 'Permalink', 'Post type', 'Impressions', 'People Reached', 
                           'Engagements', 'Shares', 'Likes', 'Comments', 'Seconds Viewed', '60-Second Video Views', 
                           '3-Second Video Views', 'Average Seconds Viewed', 'Total clicks', 'Other Clicks', 'Photo Views', 
                           'Link Clicks', 'Clicks to Play', 'Article Average Time Spent', 'Article Daily Scroll Depth', '3-Second Viewers', 
                           'Unique Video 60-Second Views', '60-Second Views From Recommendations', '60-Second Views From Shares', '60-Second Views From Followers', 
                           '60-Second Views From Boosted posts', 'Seconds Viewed From Recommendations', 'Seconds Viewed From Shares', 'Seconds Viewed From Followers', 
                           'Seconds Viewed From Boosted posts', 'Average Seconds Viewed From Recommendations', 'Average Seconds Viewed From Shares', 
                           'Average Seconds Viewed From Followers', 'Average Seconds Viewed From Boosted posts', 'Engaged users', 'Overall negative feedback', 
                           'Unique negative feedback from users', 'Unique negative feedback from users: Hide all', 'Unique negative feedback from users: Hide', 
                           'Estimated earnings (USD)', 'Ad CPM (USD)', 'Ad Impressions', 'Estimated stars earnings (USD)', 'Views by top audience (13-17, F)', 
                           'Views by top audience (13-17, M)', 'Views by top audience (18-24, F)', 'Views by top audience (18-24, M)', 'Views by top audience (25-34, F)', 
                           'Views by top audience (25-34, M)', 'Views by top audience (35-44, F)', 'Views by top audience (35-44, M)', 'Views by top audience (45-54, F)', 
                           'Views by top audience (45-54, M)', 'Views by top audience (55-64, F)', 'Views by top audience (55-64, M)', 'Views by top audience (65+, F)', 
                           'Views by top audience (65+, M)', 'Returning Viewers', '60-Second Video Views by Returning Viewers', 'Seconds Viewed by Returning Viewers', 
                           'Average Seconds Viewed by Returning Viewers']]
    #Preview
    st.subheader('Facebook Key Metric Data Preview:')
    st.dataframe(key_metrics.head())


#Allow only .csv .xlsx files to be uploaded
uploaded_file2 = st.file_uploader('Master Data', type='xlsx')

if uploaded_file2 is not None:
    #Loading data
    master_data = pd.read_excel(uploaded_file2, sheet_name='MasterData', skiprows=[0])

    #Sorting columns
    master_data = master_data[['Campaign name', '#Hashtag', 'Budget code', 'Page', 'Year']]
    #Preview
    st.subheader('Master Data Preview:')
    st.dataframe(master_data.head())


if st.button('Ba-dum Tss'):
    if (uploaded_file1 is not None) & (uploaded_file2 is not None):
        df_merge['Hashtags'] = key_metrics['Description'].str.findall(r'#.*?(?=\s|$)')
        df_merge['Hashtags'] = [', '.join(i) if isinstance(i, list) else i for i in df_merge['Hashtags']]
        target = master_data['#Hashtag'].values.tolist()
        df_merge['Campaign Hashtag'] = df_merge['Hashtags'].apply(lambda x: listing_splitter(x, target))
        df_merge['Campaign Hashtag'] = [','.join(i) if isinstance(i, list) else i for i in df_merge['Campaign Hashtag']]
        df = merge_files1(df_merge, master_data)
        df.drop(['Campaign Hashtag', 'Hashtags'], axis=1, inplace=True)
        df_xlsx = to_excel(df)
        st.download_button(label='📥 Get me the data!',
                                    data=df_xlsx ,
                                    file_name= 'FB_Post_Completed.xlsx')
