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
    return pd.merge(data1, data2, on='Permalink', how='left')

def merge_files1(data1, data2):
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
uploaded_file1 = st.file_uploader('Facebook Insights Data', type='xlsx')

if uploaded_file1 is not None:
    #Loading data
    key_metrics = pd.read_excel(uploaded_file1, sheet_name='Key Metrics', skiprows=[1])
    act = pd.read_excel(uploaded_file1, sheet_name='Lifetime Post Stories by act...')
    cons = pd.read_excel(uploaded_file1, sheet_name='Lifetime Post Consumers by type')
    
    #Sorting columns
    key_metrics = key_metrics[['Post ID', 'Permalink', 'Post Message', 
                           'Type', 'Posted', 'Lifetime Post Total Reach', 
                           'Lifetime Post organic reach', 'Lifetime Post Paid Reach', 
                           'Lifetime Post Total Impressions', 'Lifetime Post Organic Impressions', 
                           'Lifetime Post Paid Impressions', 'Lifetime Engaged Users', 
                           'Lifetime Post Impressions by people who have liked your Page', 
                           'Lifetime Post reach by people who like your Page', 
                           'Lifetime Organic views to 95%.1', 'Lifetime Paid views to 95%.1', 
                           'Lifetime Organic Video Views.1', 'Lifetime Paid Video Views.1', 
                           'Lifetime Average time video viewed', 'Lifetime Video length']]
    act = act[['Permalink', 'like', 'comment', 'share']]
    cons = cons[['Permalink', 'other clicks', 'photo view', 'link clicks', 'video play']]
    #Preview
    st.subheader('Facebook Insights Key Metric Data Preview:')
    st.dataframe(key_metrics.head())
    st.subheader('Facebook Insights Action Data Preview:')
    st.dataframe(act.head())
    st.subheader('Facebook Insights Consumption Data Preview:')
    st.dataframe(cons.head())


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


#Allow only .csv .xlsx files to be uploaded
uploaded_file3 = st.file_uploader('Video Data', type='csv')

if uploaded_file3 is not None:
    #Loading data
    video = pd.read_csv(uploaded_file3)

    #Sorting columns
    video = video[['Permalink', 'Seconds Viewed', 'Seconds Viewed From Recommendations', 
               'Seconds Viewed From Shares', 'Seconds Viewed From Followers', 
               'Seconds Viewed From Boosted posts']]
    #Preview
    st.subheader('Video Data Preview:')
    st.dataframe(video.head())

if st.button('Ba-dum Tss'):
    if (uploaded_file1 is not None) & (uploaded_file2 is not None) & (uploaded_file3 is not None):
        df_merge1 = merge_files(key_metrics, act)
        df_merge2 = merge_files(df_merge1, cons)
        df_merge3 = merge_files(df_merge2, video)
        df_merge3['Hashtags'] = key_metrics['Post Message'].str.findall(r'#.*?(?=\s|$)')
        df_merge3['Hashtags'] = [', '.join(i) if isinstance(i, list) else i for i in df_merge3['Hashtags']]
        target = master_data['#Hashtag'].values.tolist()
        df_merge3['Campaign Hashtag'] = df_merge3['Hashtags'].apply(lambda x: listing_splitter(x, target))
        df_merge3['Campaign Hashtag'] = [','.join(i) if isinstance(i, list) else i for i in df_merge3['Campaign Hashtag']]
        df = merge_files1(df_merge3, master_data)
        df.drop(['Campaign Hashtag', 'Hashtags'], axis=1, inplace=True)
        df_xlsx = to_excel(df)
        st.download_button(label='📥 Get me the data!',
                                    data=df_xlsx ,
                                    file_name= 'FB_Post_Completed.xlsx')
