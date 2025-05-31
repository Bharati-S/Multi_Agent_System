
# shared/memory.py

import sqlite3
from pathlib import Path

DB_PATH = Path("shared_memory.db")

def init_memory():
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
    import uuid
    from datetime import datetime, timezone
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO memory (id, source, type, intent, extracted_values, thread_id, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        str(uuid.uuid4()), source, file_type, intent,
        extracted_values, thread_id,
        datetime.now(timezone.utc).isoformat()
    ))
    conn.commit()
    conn.close()
