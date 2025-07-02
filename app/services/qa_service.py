import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

def answer_question(question: str, context: str) -> str:

    prompt = f"""Given the following document:

{context}

Answer the following question concisely and accurately:
{question}
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text.strip()
