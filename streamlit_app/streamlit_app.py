import streamlit as st
import requests

st.set_page_config(
    page_title="Document Insight Service",
    page_icon="🧾",
    layout="wide"
)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.title("Document Insight Service")
    st.write("Upload PDF or image documents, then ask questions about their contents. The AI will extract text and answer your questions!")

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
        if st.button("Upload Documents", key="upload_btn"):
            with st.spinner("Uploading and processing..."):
                response = requests.post("http://localhost:8000/upload", files=files)
                if response.status_code == 200:
                    st.success("Files uploaded and processed successfully!")
                else:
                    st.error(f"Upload failed: {response.text}")

    question = st.text_input("Ask a question about the uploaded documents:", key="question_input")

    if st.button("Get Answer", key="answer_btn") and question:
        with st.spinner("Finding answer..."):
            payload = {"question": question}
            response = requests.post("http://localhost:8000/ask", json=payload)
            if response.status_code == 200:
                answer = response.json().get("answer", "")
                st.success(f"**Answer:** {answer}")
            else:
                st.error("Failed to get answer. Make sure you have uploaded documents first.")

st.markdown("---")
