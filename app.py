import os
from dotenv import load_dotenv
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

#test
from utils import load_pdf_text, split_text, ask_question_groq

pdf_path = "sample.pdf"

text = load_pdf_text(pdf_path)
print("Raw text loaded.")

chunks = split_text(text)

context = "\n".join(chunks[:5])

question = input("Ask your question about the pdf: ")

answer = ask_question_groq(context, question)
print("\n Answer:\n",answer)


# print(f"{len(chunks)} chunks created.")
# retriever =  create_vector_store(chunks,openai_api_key)

# print("Vector store created and ready for questions")