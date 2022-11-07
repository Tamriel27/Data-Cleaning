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
    # 🟥 Youtube Post Rawdata Cleaning
    Upload your files
    """
    )

    uploaded_file = st.file_uploader('Youtube Post Rawdata', type='xlsx')
    uploaded_file1 = st.file_uploader('Master Data', type='xlsx')
    if not uploaded_file:
        return None
    
    yp = pd.read_excel(uploaded_file)
    yp['Permalink'] = 'https://www.youtube.com/channel/UCDbhUL64n8X8I6SGZTg4TrA/community?lb=' + yp['Post']
    yp.rename({'Post text' : 'Post Message', 'Post publish time' : 'Posted', 'Post impressions' : 'Total Impressions', 'Post likes' : 'Like', 'Post votes' : 'Votes'}, axis=1, inplace=True)
    yp['Hashtags'] = yp['Post Message'].str.findall(r'#.*?(?=\s|$)')
    yp['Hashtags'] = [', '.join(i) if isinstance(i, list) else i for i in yp['Hashtags']]
    st.text('Yotube Post Rawdata Preview:')
    st.dataframe(yp.head())
    
    if not uploaded_file1:
        return None
    
    master_data = pd.read_excel(uploaded_file1, sheet_name='MasterData', skiprows=[0])
    master_data = master_data[['#Hashtag', 'Budget code', 'Page', 'Year']]
    st.text('Master Data Preview:')
    st.dataframe(master_data.head())
    
    target = master_data['#Hashtag'].values.tolist()
    yp['Campaign Name'] = yp['Hashtags'].apply(lambda x: ';'.join([m for m in target if m in x])).replace('', np.nan)
    df = pd.merge(yp, master_data, how='left', left_on='Campaign Name', right_on='#Hashtag')
    df.rename({'Page': 'Brand'}, axis=1, inplace=True)
    df = df[['Permalink', 'Post Message', 'Posted', 'Total Impressions', 
         'Like', 'Votes', 'Campaign Name', 'Budget code', 'Year', 'Brand']]
    df['Posted'] = pd.to_datetime(df['Posted'])
    
    df_xlsx = to_excel(df)
    st.download_button(label='📥 Download Result',
                                    data=df_xlsx ,
                                    file_name= 'Youtube_Post_Completed.xlsx')
    
if __name__ == '__main__':
    main_loop()
