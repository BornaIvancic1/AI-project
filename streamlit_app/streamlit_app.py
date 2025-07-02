import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.title("📄 Document Insight Service")
st.write(
    "Upload PDF or image documents, then ask questions about their contents. "
    "The AI will extract text and answer your questions!"
)

uploaded_files = st.file_uploader(
    "Upload PDF or image files",
    type=["pdf", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files:
    files = [
        ("files", (file.name, file.getvalue(), file.type))
        for file in uploaded_files
    ]
    if st.button("Upload Documents"):
        with st.spinner("Uploading and processing..."):
            response = requests.post(f"{API_URL}/upload", files=files)
            if response.status_code == 200:
                st.success("Files uploaded and processed successfully!")
            else:
                st.error(f"Upload failed: {response.text}")

question = st.text_input("Ask a question about the uploaded documents:")

if st.button("Get Answer") and question:
    with st.spinner("Finding answer..."):
        payload = {"question": question}
        response = requests.post(f"{API_URL}/ask", json=payload)
        if response.status_code == 200:
            answer = response.json().get("answer", "")
            st.success(f"**Answer:** {answer}")
        else:
            st.error("Failed to get answer. Make sure you have uploaded documents first.")

st.markdown("---")
st.caption("Powered by FastAPI, Streamlit, EasyOCR, PyMuPDF, and Transformers.")
