import streamlit as st
import PyPDF2
import io
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

# Function to analyze text using Gemini
def analyze_with_gemini(text):
    # Create a prompt for Gemini that guides it to analyze the technical report
    prompt = f"""
    Analyze the following technical report text and provide:
    1. A clear summary of what the report is about
    2. Key findings or conclusions
    3. Main topics covered
    4. Technical terminology explained in simpler terms
    5. Potential applications or implications

    Here is the text to analyze:
    {text}

    Try to be concise and straight to the point. Only write one paragraph for each. 
    """
    
    # Generate response from Gemini
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)
    return response.text

# App title and description
st.title("Technical Report Analyzer")
st.write("Upload a PDF technical report to get an AI-powered summary and analysis.")

# File uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Display a spinner while processing
    with st.spinner("Processing PDF..."):
        # Extract text from the PDF
        pdf_bytes = io.BytesIO(uploaded_file.getvalue())
        text = extract_text_from_pdf(pdf_bytes)
        
        # Show text extraction success
        st.success(f"Successfully extracted text from {uploaded_file.name}")
        
        # Option to show raw text
        if st.checkbox("Show extracted text"):
            st.text_area("Extracted Text", text, height=200)
        
        # Analyze with Gemini API
        with st.spinner("Analyzing with Gemini..."):
            analysis = analyze_with_gemini(text)
            
        # Display the analysis
        st.subheader("Analysis Results")
        st.markdown(analysis)
        
        # Add a download button for the analysis
        st.download_button(
            label="Download Analysis",
            data=analysis,
            file_name="report_analysis.txt",
            mime="text/plain"
        )

# Information about API key setup
st.sidebar.title("Setup")

# Add instructions
st.sidebar.title("Instructions")
st.sidebar.markdown(
    """
    1. Upload a PDF technical report
    2. Wait for text extraction and analysis
    3. View the AI-generated summary
    4. Optionally download the analysis
    """
)

# Add app footer
st.markdown("---")
st.markdown("Powered by Google Gemini API | Created with Streamlit | Made by Maitreya Singh")