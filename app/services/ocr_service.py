import easyocr
import fitz

def extract_text_from_image(image_path):
    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(image_path, detail=0)
    return "\n".join(result)

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text() for page in doc])
    doc.close()
    return text
