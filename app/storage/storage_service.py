document_texts = {}

def store_text(filename, text):
    document_texts[filename] = text

def get_all_texts():
    return list(document_texts.values())
