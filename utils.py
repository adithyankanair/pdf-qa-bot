from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter


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

pdf_path = "sample.pdf"
raw_text = load_pdf_text(pdf_path)
text_chunks = split_text(raw_text)

print(f"Extractec {len(text_chunks)} text chunks.")
