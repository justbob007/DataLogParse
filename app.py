import streamlit as st #https://docs.streamlit.io/
import pandas as pd #https://pandas.pydata.org/docs/
import io #https://docs.python.org/3/library/io.html

st.title("CSV to Excel Converter")

uploaded_file = st.file_uploader("Upload your CSV", type="csv") #UI for upload button

if uploaded_file is not None:
    content = uploaded_file.getvalue().decode('utf-8')
    lines = content.splitlines()
    rows = [line.split(',', 3) for line in lines[1:]]
    rows = [r for r in rows if len(r) == 4]  # skip any malformed rows
    df = pd.DataFrame(rows, columns=['Timestamp', 'Source', 'Level', 'Line'])
    
    #FILE PARSING AND FILTERING
    df = df.drop(columns=['Source', 'Level']) #Remove redundant columns
    df = df.rename(columns = {'Line':'Temperature'})
    
    df = df[df['Temperature'].astype(str).str.match(r'^""\d{2}\.\d{2},\d{2}\.\d{2}"')]

    extracted = df['Temperature'].str.extract(r'(\d{2}\.\d{2}),(\d{2}\.\d{2})')
    df['Temp1'] = extracted[0].astype(float)
    df['Temp2'] = extracted[1].astype(float)
    df = df.drop(columns=['Temperature'])
    df['Timestamp'] = df['Timestamp'].str.extract(r'(\d{2}:\d{2}:\d{2})') #Truncate timestamps for readability
    
    #farenheit conversion
    df['Temp1'] = df['Temp1'] * 9/5
    df['Temp1'] = df['Temp1'] + 32
    df['Temp2'] = df['Temp2'] * 9/5
    df['Temp2'] = df['Temp2'] + 32
    
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