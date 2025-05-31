import os
import json

def detect_format(file_path):
    if file_path.endswith('.pdf'):
        return "PDF"
    elif file_path.endswith('.json'):
        return "JSON"
    elif file_path.endswith('.txt'):
        return "Email"
    else:
        return "Unknown"

def detect_intent(text):
    text = text.lower()
    if "invoice" in text:
        return "Invoice"
    elif "request for quote" in text or "rfq" in text:
        return "RFQ"
    elif "complaint" in text:
        return "Complaint"
    elif "regulation" in text:
        return "Regulation"
    else:
        return "Unknown"

def classify(file_path):
    fmt = detect_format(file_path)
    with open(file_path, "r", encoding='utf-8', errors='ignore') as f:
        content = f.read()
    intent = detect_intent(content)
    return fmt, intent, content
