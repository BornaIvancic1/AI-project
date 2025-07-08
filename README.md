AI-driven Document Insight Service
Upload PDF or image documents, extract their text, and use AI (Gemini) to answer questions about document content. Includes OCR, QA, Docker, and optional NER and Streamlit UI.

🚀 Features
Document Upload: Upload PDFs and images for processing.

Text Extraction: Uses EasyOCR and PyMuPDF to extract text from documents.

AI Question Answering: Answers user questions about uploaded documents using Gemini (Google Generative AI API).

Dockerized: Fully containerized for easy deployment.

Test Documents: Includes sample PDFs/images for demo.

(Optional) NER: Highlights named entities in answers.

(Optional) Streamlit UI: User-friendly web interface.

🛠️ Setup Instructions
Manual Installation
Clone the repository:


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
Upload Documents
Endpoint:
POST /upload

Description:
Upload one or more files (PDF, image, text, DOCX, or CSV) for processing and storage.

Example Request (using curl)
bash
curl -X POST "http://localhost:8000/upload" \
  -F "files=@/path/to/document1.pdf" \
  -F "files=@/path/to/image1.png" \
  -F "files=@/path/to/notes.txt"
Example Request (using Python)
python
import requests

files = [
    ("files", ("document1.pdf", open("document1.pdf", "rb"), "application/pdf")),
    ("files", ("image1.png", open("image1.png", "rb"), "image/png")),
    ("files", ("notes.txt", open("notes.txt", "rb"), "text/plain"))
]
response = requests.post("http://localhost:8000/upload", files=files)
print(response.json())
Example Success Response
json
{
  "uploaded": [
    {
      "filename": "document1.pdf",
      "text_excerpt": "This is the first 200 characters of the extracted text from document1.pdf..."
    },
    {
      "filename": "image1.png",
      "text_excerpt": "This is the first 200 characters of the extracted text from image1.png..."
    },
    {
      "filename": "notes.txt",
      "text_excerpt": "This is the first 200 characters of the extracted text from notes.txt..."
    }
  ]
}
Example Error Responses
Unsupported File Type:

json
{
  "detail": "Unsupported file type"
}
Text Extraction Failure:

json
{
  "detail": "Text extraction failed: <detailed error message>"
}
File Save Failure:

json
{
  "detail": "Failed to save file: <detailed error message>"
}
Extracted Text is Empty or Invalid:

json
{
  "detail": "Extracted text is empty or invalid."
}
Notes
You can upload multiple files in a single request.

Supported file types: .pdf, .png, .jpg, .jpeg, .txt, .docx, .csv.

Each successful upload returns the filename and a 200-character excerpt of the extracted text.

Errors are returned with a detail field describing the issue.

Example request: Use Swagger UI or Postman to upload files.

Ask a Question
Endpoint:
POST /ask

Description:
Ask a question about the uploaded documents. The response includes the answer and any extracted entities.

Example Request (using curl)
bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "Who is the client in the agreement?"}'
Example Request (using Python)
python
import requests

payload = {"question": "Who is the client in the agreement?"}
response = requests.post("http://localhost:8000/ask", json=payload)
print(response.json())
2. Example Success Response
json
{
  "answer": "The client in the agreement is ACME Corporation.",
  "entities": [
    {
      "entity_group": "ORG",
      "word": "ACME Corporation",
      "start": 28,
      "end": 44,
      "score": 0.997
    }
  ]
}
3. Example Error Responses
No Documents Uploaded:

json
{
  "detail": "No documents uploaded yet."
}
Other Errors (e.g., Internal Server Error):

json
{
  "detail": "Internal server error."
}
4. Notes
The request must be a JSON object with a "question" field.

The response contains the "answer" string and a list of "entities" (if any are found).

Each entity includes its group, word, start/end positions, and confidence score.

If no documents are indexed, the endpoint returns an error with "No documents uploaded yet."

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
streamlit run streamlit_app.py
Then open http://localhost:8501.

