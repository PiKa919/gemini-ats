import base64
from dotenv import load_dotenv
# Load environment variables from a .env file
load_dotenv()

import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
import io

# Configure the Google Generative AI API with the API key from environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    """
    Calls the Gemini Generative AI model to generate a response based on the input prompt and PDF content.
    
    Parameters:
    - input (str): The input text prompt for the model.
    - pdf_content (list): A list of dictionaries, each containing the base64 encoded data of the PDF pages.
    - prompt (str): Additional prompt information for the model.
    
    Returns:
    - str: The text response from the model.
    """
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content(input, pdf_content, prompt)
    return response.text

def input_pdf_setup(uploaded_file):
    """
    Converts the first page of a PDF file to a JPEG image and encodes it in base64.
    
    Parameters:
    - uploaded_file: The uploaded file object.
    
    Returns:
    - list: A list containing a dictionary with the mime type and base64 encoded data of the first page.
    
    Raises:
    - FileNotFoundError: If no file is uploaded.
    """
    if uploaded_file is not None:
        #convert the pdf to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page=images[0]
        
        #converting to bytes
        img_bytes_arr = io.BytesIO()
        first_page.save(img_bytes_arr, format='JPEG')
        img_bytes_arr = img_bytes_arr.getvalue()
        
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_bytes_arr).decode('utf-8')
            }
        ]
        return pdf_parts
    
    else:
        raise FileNotFoundError("File not found")
    

# Streamlit App Configuration
st.set_page_config(page_title="Gemini ATS", page_icon=":robot:", layout="wide")
st.header("Gemini ATS tracking system")
input_text = st.text_area("Job Description", "Please enter the job description here", key="input")
uploaded_file = st.file_uploader("Upload resume in PDF file", type=["pdf"])

# Streamlit UI Elements
if uploaded_file is not None:
    st.write("File uploaded successfully")
    
submit1 = st.button("Tell me about the RESUME")
submit2 = st.button("HR Round analysis")

# Input prompts for the Gemini model
input_prompt1 = """You are an experienced ATS (Applicant Tracking System) specialist tasked with analyzing resumes for keyword matching and overall suitability for a specific job opening. 


**Analyze the resume and provide the following information:**

* **ATS Match Score:** Estimate the percentage match between the resume and the job description based on keywords and relevant skills. (0.0 - 1.0)
* **Missing Keywords:** Identify a list of keywords that are not present in the resume.
* (Optional) **Overused Keywords:** If applicable, identify keywords that appear too frequently in the resume compared to the resume

**Additional Notes:**

* Consider common resume formats and ATS parsing limitations.
* Focus on identifying relevant skills and experience beyond just keyword matching.
* Prioritize keywords that are more specific to the job requirements."""


input_prompt2 = """You are an experienced technical HR manager reviewing resumes 

 Scrutinize the following resume:

Analyze the resume for:

    Technical Skills: Identify and assess the candidate's technical skills relevant to the job description (e.g., programming languages, frameworks, tools).
    Experience Depth: Evaluate the depth and breadth of the candidate's experience in applying those skills to solve technical problems.
    Quantifiable Achievements: Look for quantifiable results and accomplishments demonstrating the impact of their technical contributions.
    Red Flags: Identify any potential red flags in the resume, such as gaps in employment or unclear technical skills descriptions.

Additional Notes:

    Consider industry best practices and current trends in the technical skillset required for the role.
    Look for keywords that showcase the candidate's technical proficiency.."""
    
# Handling button clicks and displaying responses
if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content,input_text)
        st.subheader("The response is:")
        st.write(response)
    else:
        st.write("Please upload the resume first") 
        
elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content,input_text)
        st.subheader("The response is:")
        st.write(response)
    else:
        st.write("Please upload the resume first")