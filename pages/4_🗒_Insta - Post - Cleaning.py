import streamlit as st
import pandas as pd
from io import BytesIO
import numpy as np

def listing_splitter(text, target):
    # Try except to handle np.nans in input
    try:
        # Extract the list of flags
        flags = [l for l in target if l in text]
        # If any flags were extracted then return the list
        if flags:
            return flags
        # Otherwise return np.nan
        else:
            return np.nan
    except AttributeError:
        return np.nan

def merge_files(data1, data2):
    return pd.merge(data1, data2, how='left', left_on='Campaign Name', right_on='#Hashtag')

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
    # 📊 Instagram Post Rawdata Cleaning
    Upload your files
    """
    )

    uploaded_file = st.file_uploader('Instagram Post Rawdata', type='xlsx')
    uploaded_file1 = st.file_uploader('Master Data', type='xlsx')
    if not uploaded_file:
        return None

    insta = pd.read_excel(uploaded_file, sheet_name='Worksheet')
    insta = insta[['Instagram URL', 'Caption', 'Date', 'Type', 
         'Reach', 'Reach organic', 'Reach paid', 
         'Impressions', 'Impressions organic', 'Impressions paid', 
         'Likes', 'Likes organic', 'Likes paid', 
         'Comments', 'Comments organic', 'Comments paid', 
         'Saves', 'Video views', 'Media Direct URL']]
    st.text('Instagram Post Rawdata Preview:')
    st.dataframe(insta.head())
    
    post = []
    for row in insta['Type']:
        if row == 'carousel' or 'photo' : post.append('Post')
        elif row == 'video': post.append('Video')
        else : post.append('')
    insta['Post type'] = post

    insta['Campaign'] = insta['Caption'].str.findall(r'#.*?(?=\s|$)')
    insta['Campaign'] = [', '.join(i) if isinstance(i, list) else i for i in insta['Campaign']]
    
    if not uploaded_file1:
        return None
    
    master_data = pd.read_excel(uploaded_file1, sheet_name='MasterData', skiprows=[0])
    master_data = master_data[['#Hashtag', 'Budget code', 'Page', 'Year']]
    st.text('Master Data Preview:')
    st.dataframe(master_data.head())
    
    master_data = master_data[['#Hashtag', 'Budget code', 'Page', 'Year']]
    target = master_data['#Hashtag'].values.tolist()
    insta['Campaign Name'] = insta['Campaign'].apply(lambda x: listing_splitter(x, target))
    insta['Campaign Name'] = [','.join(i) if isinstance(i, list) else i for i in insta['Campaign Name']]
    insta['Campaign Name'] = insta['Campaign'].str.replace('#unitel,', '').str.replace('#unitell,', '')
    df = merge_files(insta, master_data)
    df['Total Engagement'] = df['Likes'] + df['Comments'] + df['Saves']
    df['EngRate%'] = (df['Likes'] + df['Comments'] + df['Saves']) / df['Reach']
    df.rename({'Page': 'Brand'}, axis=1, inplace=True)
    df.drop(['Campaign', '#Hashtag'], axis=1, inplace=True)
    df_xlsx = to_excel(df)
    st.download_button(label='📥 Download Result',
                                    data=df_xlsx ,
                                    file_name= 'Instagram_Post_Completed.xlsx')


if __name__ == '__main__':
    main_loop()

