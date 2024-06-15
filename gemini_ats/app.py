from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content(input, pdf_content, prompt)
    return response.text

def input_pdf_setup():
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
    
