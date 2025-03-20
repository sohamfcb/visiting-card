import google.generativeai as genai
import pandas as pd
import os
import streamlit as st
from PIL import Image
import json
import ast
import pymysql
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

st.set_page_config(page_title='Text Extractor')
st.header('Text Extractor')

conn=pymysql.connect(
            host='localhost',
            user='root',
            password=os.getenv('MYSQL_PASSWORD'),
            database='visiting_card_details'
        )
my_cursor=conn.cursor()

file=st.file_uploader('Upload the Image',type=['jpg','png','jpeg','webp'])
model=genai.GenerativeModel('gemini-1.5-pro-exp-0801')

prompt='''
    You are an AI assistant tasked with extracting structured information from images of business cards. 

Given an image of a business card, extract and format the following details:
1. Full Name of the individual.
2. Company Name.
3. Job Role (for example, "Graphic Designer").
4. Address (including street, city, state, and postal code if available).
5. Phone Number(s) (including any extensions or country codes). If you find 2 phone numbers, put the second number in the phone2 field.
6. Email Address.
7. Website URL (if present).

The output must be in JSON format for easy storage in a database. If any field is missing, use None for its value.

Example output format:
{
    "name": "John Doe",
    "company": "Tech Solutions Inc.",
    "job_role": "Graphic Designer",
    "address": "123 Innovation Drive, San Francisco, CA 94107",
    "phone": "+1-555-123-4567",
    "phone2": "+1-555-123-4567" (if there are more than 1 phone numbers in the card) else return None.
    "email": "john.doe@techsolutions.com",
    "website": "https://www.techsolutions.com"
}
Ensure accuracy and structure in the output.
'''

if file:
    st.image(file,width=500)

    image=Image.open(file)
    response=model.generate_content([prompt,image])
    data=response.text
    print(data)
    data=data.replace('json','')
    data=data.replace('```','')
    print(data)
    data=ast.literal_eval(data)
    print(data)

    # try:
    query = """
    INSERT INTO details (name, company, job_role, address, phone,phone2, email, website)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        data['name'],
        data['company'],
        data['job_role'],
        data['address'],
        data['phone'],
        data['phone2'],
        data['email'],
        data['website']
    )

    my_cursor.execute(query, values)
    conn.commit()

    st.success('User entered!')

    # except:
    #     st.error('User already exists')



