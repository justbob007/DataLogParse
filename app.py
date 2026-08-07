import streamlit as st #https://docs.streamlit.io/
import pandas as pd #https://pandas.pydata.org/docs/
import io #https://docs.python.org/3/library/io.html

st.title("CSV to Excel Converter")

uploaded_file = st.file_uploader("Upload your CSV", type="csv") #UI for upload button

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file) #create csv object as a pandas dataframe (2x2)
    
    #FILE PARSING AND FILTERING
    df = df.drop(columns=['Source', 'Level']) #Remove redundant columns
    df = df.rename(columns = {'Line':'Temperature'})
    
    df = df[df['Temperature'].astype(str).str.match(r'^\d{2}\.\d{2}"')] #Remove all log entries that are not temperature readings - don't follow the "##.##" formula
    
    df['Temperature'] = df['Temperature'].str.extract(r'(\d{2}\.\d{2})').astype(float) #Trim column down to just the number
    df['Timestamp'] = df['Timestamp'].str.extract(r'(\d{2}:\d{2}:\d{2})') #Truncate timestamps for readability
    
    #farenheit conversion
    df['Temperature'] = df['Temperature'] * 9/5
    df['Temperature'] = df['Temperature'] + 32
    
    df = df.reset_index(drop=True) #reset entries to be properly numbered
    st.dataframe(df)  #table preview
    buffer = io.BytesIO()
    df.to_excel(buffer, index=True, engine='openpyxl') #convert pandas object to excel sheet
    buffer.seek(0) #reset cursor

    st.download_button( #UI for download button
        label="Download as Excel",
        data=buffer,
        file_name="output.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )