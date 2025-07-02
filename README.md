# resume_bot
Resume Bot is an intelligent web app built with Streamlit and Gemini Pro (Google Generative AI) that helps users tailor their resumes to specific job descriptions. Users upload a PDF of their resume and paste a job description. The bot analyzes and:

Calculates a Resume Match Score (0-100) indicating how well the resume fits the job.

Identifies missing skills from the job description that are absent in the resume.

Suggests improvements to optimize the resume for better alignment with the job posting.

This tool helps job seekers quickly customize resumes for Applicant Tracking Systems (ATS) and hiring managers.
dependencies:
pip install streamlit google-generativeai PyPDF2 streamlit-option-menu python-dotenv
