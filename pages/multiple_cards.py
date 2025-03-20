import os
from PIL import Image
import ast
import pymysql
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from pymysql import IntegrityError

load_dotenv()

st.set_page_config(page_title='Multiple Cards')
st.header('Generate Details From Multiple Cards')

conn=pymysql.connect(
    host='localhost',
    user='root',
    password=os.getenv('MYSQL_PASSWORD'),
    database='visiting_card_details'
)

mycursor = conn.cursor()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

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

The output must be in JSON format for easy storage in a database. If any field is missing, use None (as in the python None datatype for its value.

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

input_path=st.text_input('Enter file path (Please remove the inverted commas and make sure you don\'t have duplicate images in the directory): ')
# input_path=r'D:\Visiting Card (Gemini)\images'
image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff','.webp']

input_images=[]

for filename in os.listdir(input_path):
    if os.path.splitext(filename)[1] in image_extensions:
        input_images.append(os.path.join(input_path, filename))

btn=st.button('Submit')

if btn:
    if input_path:
        if len(input_images)>0:

            for filename in input_images:
                image=Image.open(filename)
                response=model.generate_content([prompt,image])
                data = response.text
                # print(data)
                data= data.replace('json', '')
                print(data)
                data= data.replace('```', '')
                data=ast.literal_eval(data)
                print(data)

                try:
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

                    mycursor.execute(query, values)
                    conn.commit()

                    st.write('User entered')

                except IntegrityError:
                    st.error('User already exists')

            st.success('Successfully generated')

        else:
            st.error('There are no more images in the given directory')