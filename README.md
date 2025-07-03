AI-driven Document Insight Service
Upload PDF or image documents, extract their text, and use AI (Gemini) to answer questions about document content. Includes OCR, QA, Docker, and optional NER and Streamlit UI.

🚀 Features
Document Upload: Upload PDFs and images for processing.

Text Extraction: Uses EasyOCR and PyMuPDF to extract text from documents.

AI Question Answering: Answers user questions about uploaded documents using Gemini (Google Generative AI API).

Dockerized: Fully containerized for easy deployment.

Test Documents: Includes sample PDFs/images for demo and grading.

(Optional) NER: Highlights named entities in answers.

(Optional) Streamlit UI: User-friendly web interface.

🛠️ Setup Instructions
Manual Installation
Clone the repository:

bash
git clone https://github.com/<YOUR_USERNAME>/<YOUR_REPO>.git
cd <YOUR_REPO>
Create and activate a virtual environment:

bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
Install dependencies:

bash
pip install -r requirements.txt
Set up your Gemini API key:
Create a .env file in the project root:

text
GEMINI_API_KEY=your_actual_api_key_here
Run the FastAPI app:

bash
uvicorn app.main:app --reload
Visit http://localhost:8000/docs for the API docs.

Docker Installation
Build the Docker image:

bash
docker build -t ai-doc-insight .
Run the Docker container:

bash
docker run -p 8000:8000 ai-doc-insight
Access the API at:
http://localhost:8000/docs

📄 Example API Usage
Upload Documents
POST /upload

Upload one or more PDF/image files.

Example request: Use Swagger UI or Postman to upload files.

Ask a Question
POST /ask

Request body:

json
{
  "question": "What is the invoice total?"
}
Example response:

json
{
  "answer": "The invoice total is $1,200.",
  "entities": [
    {"entity_group": "MONEY", "word": "$1,200", "start": 24, "end": 30, "score": 0.99}
  ]
}
💡 Approach & Tools
Backend: FastAPI

OCR: EasyOCR (images), PyMuPDF (PDFs)

AI/LLM: Gemini (Google Generative AI API)

NER: Hugging Face Transformers pipeline (optional)

UI: Streamlit (optional)

Containerization: Docker

Why Gemini?
Gemini provides robust, scalable, and multimodal LLM capabilities via API, making it ideal for document QA.

📝 Test Documents
Sample PDFs and images are included in the test_docs/ folder for demonstration and grading.

🖥️ (Optional) Streamlit UI
To run the Streamlit demo:

bash
streamlit run streamlit_app/streamlit_app.py
Then open http://localhost:8501.

