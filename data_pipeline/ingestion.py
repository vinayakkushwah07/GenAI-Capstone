import fitz  # PyMuPDF
import hashlib
def compute_file_hash(file_bytes):
    return hashlib.sha256(file_bytes).hexdigest()[:10]

def extract_pdf(file_path):
    doc = fitz.open(file_path)
    pages = []

    for i, page in enumerate(doc):
        text = page.get_text()
        pages.append({
            "page_number": i + 1,
            "text": text
        })

    return pages

# def extract_docx(file_path):
#     doc = Document(file_path)
#     text = "\n".join([para.text for para in doc.paragraphs])
    
#     return [{
#         "page_number": 1,
#         "text": text
#     }]

def extract_file(file_path):
    if file_path.endswith(".pdf"):
        return extract_pdf(file_path)
    # elif file_path.endswith(".docx"):
    #     return extract_docx(file_path)
    else:
        raise ValueError("Unsupported file type")
