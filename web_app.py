import streamlit as st
from utils import (
    load_pdf_text, 
    split_text,
    create_faiss_vector_store,
    retrieve_relevant_chunks, 
    ask_question_groq
)
from dotenv import load_dotenv
import tempfile

load_dotenv()

st.set_page_config(page_title="PDF Q&A Bot", layout="centered")
st.title("Chat with your PDF")

uploaded_file = st.file_uploader("Upload a pdf",type="pdf")

if uploaded_file:
    with st.spinner("Reading and splitting pdf..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(uploaded_file.read())
            pdf_path = temp_pdf.name
        
        raw_text = load_pdf_text(pdf_path)
        chunks = split_text(raw_text)
        st.success(f"PDF loaded.Total chunks: {len(chunks)}")

        vector_store = create_faiss_vector_store(chunks)

    #adding chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    user_question = st.text_input("Ask a question about this PDF: ",key="input")



    if user_question:
        with st.spinner("Retrieving relevant context...."):
            context = retrieve_relevant_chunks(vector_store, user_question)

        with st.spinner("Asking Groq..."):
            answer = ask_question_groq(context, user_question)
        
        st.session_state.chat_history.append((user_question, answer))
        st.markdown("chat history")
        for q, a in reversed(st.session_state.chat_history):
            st.markdown(f"You: {q}")
            st.markdown(f"Bot:{a}")

            