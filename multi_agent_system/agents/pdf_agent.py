""" # agents/pdf_agent.py

import fitz  # PyMuPDF

def extract_pdf_info(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()

    # Example extraction logic
    preview = text[:300].strip().replace('\n', ' ')
    return {
        "page_count": len(doc),
        "preview": preview
    }
 """

def extract_pdf_info(file_path):
    import fitz  # PyMuPDF

    doc = fitz.open(file_path)
    page_count = doc.page_count
    text_preview = doc[0].get_text()[:500]  # preview of first page text

    result = {
        "page_count": page_count,
        "text_preview": text_preview
    }

    warnings = []
    if page_count == 0:
        warnings.append("Empty PDF file.")
    elif len(text_preview) < 100:
        warnings.append("Text preview may be too short.")

    return result, warnings
