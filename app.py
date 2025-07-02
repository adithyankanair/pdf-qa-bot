import os
from dotenv import load_dotenv
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

#test
from utils import load_pdf_text, split_text

pdf_path = "sample.pdf"

raw_text = load_pdf_text(pdf_path)
print("Raw text loaded.")

chunks = split_text(raw_text)
print(f"{len(chunks)} chunks created.")