
import os
import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
from streamlit_option_menu import option_menu


# configure API key
genai.configure(api_key= "YOUR_API_KEY")
def get_gemini_pro():
    return genai.GenerativeModel('gemini-1.5-flash')

# Function to extract text from PDF resume
def pdf_to_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += str(page.extract_text())
    return text

# Construct prompt for resume match score
def construct_resume_score_prompt(resume, job_description):
    prompt = f'''
Act as an HR Manager with 20 years of experience. Compare the resume provided below with the job description given below. Check for key skills in the resume that are related to the job description. Rate the resume out of 100 based on the matching skill set. Assess the score with high accuracy.
Here is the Resume text: {resume}
Here is the Job Description: {job_description}
Return the response as a single string in the following structure: score:%
'''
    return prompt

# Construct prompt for missing skills
def construct_skills_prompt(resume, job_description):
    prompt = f'''
Act as an HR Manager with 20 years of experience. Compare the resume provided below with the job description given below. Identify key skills or qualifications mentioned in the job description that are missing from the resume. Provide a concise list of missing skills.
Here is the Resume text: {resume}
Here is the Job Description: {job_description}
Return the response as a list of missing skills in the format: Missing Skills: [skill1, skill2, ...]
'''
    return prompt

# Construct prompt for resume improvement suggestions
def construct_improvement_prompt(resume, job_description):
    prompt = f'''
Act as an HR Manager with 20 years of experience. Analyze the resume and job description provided below. Suggest specific improvements to the resume to better align it with the job description. Provide actionable suggestions, such as rephrasing accomplishments, adding specific keywords, or highlighting relevant skills.
Here is the Resume text: {resume}
Here is the Job Description: {job_description}
Return the response as a list of suggestions in the format: Suggestions: [suggestion1, suggestion2, ...]
'''
    return prompt

# Function to get response from Gemini model
def get_result(input_prompt):
    model = get_gemini_pro()
    response = model.generate_content(input_prompt)
    return response.text

# Streamlit app
st.title("Resume Bot - Optimize Your Resume")

# Sidebar for navigation
with st.sidebar:
    selected = option_menu(
        "Resume Analysis",
        ["Score Check", "Missing Skills", "Improvement Suggestions"],
        icons=["📊", "🔍", "✍️"],
        default_index=0
    )

# File uploader for resume
uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

# Text area for job description
job_description = st.text_area("Paste the Job Description")

# Submit button
submit = st.button("Analyze Resume")

if submit:
    if job_description == '':
        st.error("Please enter a job description.")
    elif uploaded_file is None:
        st.error("Please upload your resume.")
    else:
        # Extract resume text
        resume_text = pdf_to_text(uploaded_file)

        if selected == "Score Check":
            # Get resume match score
            score_prompt = construct_resume_score_prompt(resume_text, job_description)
            score_result = get_result(score_prompt)
            st.subheader("Resume Match Score")
            st.write(score_result)

        elif selected == "Missing Skills":
            # Get missing skills
            skills_prompt = construct_skills_prompt(resume_text, job_description)
            skills_result = get_result(skills_prompt)
            st.subheader("Missing Skills")
            st.write(skills_result)

        elif selected == "Improvement Suggestions":
            # Get improvement suggestions
            improvement_prompt = construct_improvement_prompt(resume_text, job_description)
            improvement_result = get_result(improvement_prompt)
            st.subheader("Improvement Suggestions")
            st.write(improvement_result)

