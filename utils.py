import os
import requests
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def load_pdf_text(file_path):
    reader = PdfReader(file_path)
    raw_text = ''
    for page in reader.pages:
        raw_text += page.extract_text()
    return raw_text

def split_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200
    )
    return splitter.split_text(text)

def create_faiss_vector_store(chunks):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)
    return vector_store

def retrieve_relevant_chunks(vector_store, question, top_k=5):
    retriever = vector_store.as_retriever(search_kwargs={"k":top_k})
    results = retriever.invoke(question)
    return "\n".join([doc.page_content for doc in results])

def ask_question_groq(context,question):
    api_key = os.getenv("GROQ_API_KEY")
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role":"system","content":"You are a helpful assistant.Answer based only on the provided context"},
            {"role":"user","content":f"Context:\n{context}\n\nQuestion:\n{question}"}
        ],
        "temperature":0.3
    }
    response = requests.post(url, headers=headers,json=data)
    
    if not response.ok:
        print("Groq API returned error:",response.status_code)
        print("Details:",response.text)
        response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]

def load_pdf_text(file_path):
    reader = PdfReader(file_path)
    raw_text = ''
    for page in reader.pages:
        raw_text += page.extract_text()
    return raw_text

def split_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200
    )
    chunks = splitter.split_text(text)
    return chunks

# pdf_path = "sample.pdf"
# raw_text = load_pdf_text(pdf_path)
# text_chunks = split_text(raw_text)

# print(f"Extractec {len(text_chunks)} text chunks.")
