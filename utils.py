from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

#create embeddings for each chunk using OpenAIEmbeddings, store them in a FAISS vector store, return the retriever
from langchain_community.vectorstores import FAISS
# from langchain_embeddings import OpenRouterEmbeddings

#for groq
import requests
import os

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

# def create_vector_store(chunks,openai_api_key):
#     embeddings  = OpenRouterEmbeddings(
#             openai_api_key = openai_api_key,
#             model = "openai/text-embedding-ada-002"
#         )
#     vector_store = FAISS.from_texts(chunks, embedding=embeddings)
#     retriever = vector_store.as_retriever(search_kwargs={"k":3})
#     return retriever




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
