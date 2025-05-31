import os
import json
import sqlite3
import uuid
from datetime import datetime, timezone
from agents.pdf_agent import extract_pdf_info
from agents.json_agent import process_json_file
from agents.email_agent import extract_email_info

DB_PATH = "shared_memory.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id TEXT PRIMARY KEY,
            source TEXT,
            type TEXT,
            intent TEXT,
            extracted_values TEXT,
            thread_id TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_entry(source, file_type, intent, extracted_values, thread_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO memory (id, source, type, intent, extracted_values, thread_id, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (str(uuid.uuid4()), source, file_type, intent, extracted_values, thread_id, datetime.now(timezone.utc).isoformat()))
    conn.commit()
    conn.close()

def classify_format(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.json':
        return "JSON"
    elif ext == '.pdf':
        return "PDF"
    elif ext in ['.txt', '.eml']:
        return "Email"
    else:
        return "Unknown"

def classify_intent(text):
    text = text.lower()
    if 'invoice' in text:
        return "Invoice"
    elif 'quote' in text or 'rfq' in text:
        return "RFQ"
    elif 'complaint' in text:
        return "Complaint"
    elif 'regulation' in text:
        return "Regulation"
    else:
        return "Unknown"

def read_file_content(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.json':
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.dumps(json.load(f))
    elif ext == '.pdf':
        # For PDFs, return empty string since PDF agent will handle content extraction
        return ""
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

def main():
    init_db()

    file_path = input("Enter the full path of the file to process: ").strip()

    if not os.path.isfile(file_path):
        print("❌ File does not exist. Please check the path and try again.")
        return

    fmt = classify_format(file_path)
    raw_content = read_file_content(file_path)
    intent = classify_intent(raw_content)
    thread_id = str(uuid.uuid4())[:8]

    print(f"Processing file: {file_path}")
    print(f"Detected Format: {fmt}")
    print(f"Detected Intent: {intent}")
    print(f"Thread ID: {thread_id}\n")

    if fmt == "JSON":
        result, errors = process_json_file(file_path)
        if result:
            print("✅ Valid JSON detected:")
            print(json.dumps(result, indent=2))
            log_entry(file_path, fmt, intent, json.dumps(result), thread_id)
        else:
            print("❌ JSON Validation errors:")
            for error in errors:
                print(f" - {error['loc']}: {error['msg']}")
            log_entry(file_path, fmt, "ValidationError", json.dumps(errors), thread_id)

    elif fmt == "Email":
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        result, detected_intent = extract_email_info(content)
        print("📧 Email parsed info:")
        print(json.dumps(result, indent=2))
        log_entry(file_path, fmt, detected_intent, json.dumps(result), thread_id)

    elif fmt == "PDF":
        result, warnings = extract_pdf_info(file_path)
        print("📄 PDF parsed info:")
        print(json.dumps(result, indent=2))
        if warnings:
            print("\n⚠️ PDF Warnings:")
            for w in warnings:
                print(f" - {w}")
        log_entry(file_path, fmt, intent, json.dumps(result), thread_id)

    else:
        print("❌ Unsupported file format. Only JSON, PDF, and Email (.txt/.eml) are supported.")
        log_entry(file_path, "Unknown", intent, "Could not classify file format", thread_id)

if __name__ == "__main__":
    main()
