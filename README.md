1. Field to input the job description
2. Upload PDF
3. PDF to image --> OCR -- >> Google gemini pro
4. Prompts template

prompts to generate the prompt template
1. generate a 100 word prompt template for an LLM's prompt template to review a given Resume and analyse it through the PoV of a Technical Human Resource Manager & scrutinise the resume
2. generate a 100 word prompt template for an LLM's prompt template to review a given Resume 
3. generate me a prompt template for a resume ats checker llm model's prompt template

## Make sure to install Poppler before running the app
https://poppler.freedesktop.org/
https://github.com/oschwartz10612/poppler-windows/releases
https://stackoverflow.com/questions/18381713/how-to-install-poppler-on-windows

## To run the app
1. Install the requirements
Use poetry to install the dependencies
'''poetry install --no-root'''

2. Run the app
streamlit run app.py