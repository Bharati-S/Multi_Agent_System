# agents/json_agent.py

from pydantic import BaseModel, ValidationError
from typing import Optional

class InvoiceSchema(BaseModel):
    invoice_id: str
    sender: str
    receiver: str
    amount: float
    due_date: str
    currency: Optional[str] = "USD"

def process_json_file(file_path):
    import json

    with open(file_path, 'r') as f:
        data = json.load(f)

    try:
        invoice = InvoiceSchema(**data)
        return invoice.dict(), []
    except ValidationError as e:
        return None, e.errors()
