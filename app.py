import streamlit as st
import fitz
from dotenv import load_dotenv
from groq import Groq
import os

# Load environment variables
load_dotenv()

# Configure Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Streamlit title
st.title("AI Resume Review Agent")

# Upload PDF
uploaded_file = st.file_uploader(
    "Upload your resume PDF",
    type=["pdf"]
)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):

    text = ""

    pdf = fitz.open(
        stream=pdf_file.read(),
        filetype="pdf"
    )

    for page in pdf:
        text += page.get_text()

    return text


# Process uploaded file
if uploaded_file:

    # Extract resume text
    resume_text = extract_text_from_pdf(uploaded_file)

    # Limit text size
    resume_text = resume_text[:3000]

    st.subheader("Resume Review")

    # Prompt
    prompt = f"""
    You are an expert ATS resume reviewer.

    Review the following resume and provide:

    1. Overall ATS score out of 100
    2. Strengths
    3. Weaknesses
    4. Missing skills
    5. Improvement suggestions
    6. Final recommendation

    Resume:
    {resume_text}
    """

    # AI Processing
    with st.spinner("Analyzing Resume..."):

        try:

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama-3.1-8b-instant",
            )

            st.write(
                chat_completion.choices[0].message.content
            )

        except Exception as e:
            st.error(f"Error: {e}")