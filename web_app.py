import streamlit as st
from utils import load_pdf_text, split_text, ask_question_groq
from dotenv import load_dotenv
import tempfile

load_dotenv()

st.set_page_config(page_title="PDF Q&A Bot", layout="centered")
st.title("PDF Question Answering Bot")

uploaded_file = st.file_uploader("Upload a pdf",type="pdf")

if uploaded_file:
    with st.spinner("Reading and splitting pdf..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(uploaded_file.read())
            pdf_path = temp_pdf.name
        
        raw_text = load_pdf_text(pdf_path)
        chunks = split_text(raw_text)
        st.success(f"PDF loaded.Total chunks: {len(chunks)}")

    question = st.text_input("Ask a question about this pdf: ")

    if question:
        with st.spinner("Asking Groq..."):
            context = "\n".join(chunks[:5])
            answer = ask_question_groq(context, question)
            st.success("Here's the answer: ")
            st.write(answer)

            