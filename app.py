import streamlit as st
import google.generativeai as genai

import os
import PyPDF2 as pdf 

from dotenv import load_dotenv

load_dotenv() ## laod all the evironment variables

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


## GEmini Pro Response
def get_gemini_response(input):
    
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(input)
    
    return response.text


def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in reader(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
        
    return text


## prompt Template

input_prompt= """
Hey Act like a skiled or very experience ATS(Application Tracking System) with a deep understanding of tech field, software engineering, data science, data analyst and big data engineer. Your task is
to evaluate the resume based on the given job description. You must considerr the job marker is very competitive and you should provide best assistance for improving the resumes.
Assign the percentage matching based on Jd and the missing keywords with high accuracy
resume:{text}
description:{jd}
I want the response in one single string having the structure
{{"JD match": "%", "MissingKeywords: []", "Profile Summary: ""}}
"""



## streamlit app
st.title("Smart Applications Tracking System(ATS)")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste your Job Description")
uploaded_file=st.file_uploader("Upload your Resume", type="pdf", help="Please upload your resume")

submit = st.button("Submit")


if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt)
        st.subheader(response)
        