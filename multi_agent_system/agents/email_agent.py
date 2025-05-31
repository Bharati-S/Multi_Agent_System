""" # agents/email_agent.py

import re

def extract_email_info(content):
    sender = None
    urgency = "Normal"
    intent = "Unknown"

    # Extract sender
    match = re.search(r"From:\s*(.*)", content, re.IGNORECASE)
    if match:
        sender = match.group(1).strip()
    else:
        # Try getting from signature
        lines = content.strip().split('\n')
        sender = lines[-1].strip()

    # Determine urgency
    urgency_keywords = ['urgent', 'asap', 'immediately', 'high priority']
    if any(word in content.lower() for word in urgency_keywords):
        urgency = "High"

    # Determine intent (very simple keyword match)
    if 'quote' in content.lower():
        intent = "RFQ"
    elif 'complaint' in content.lower():
        intent = "Complaint"
    elif 'invoice' in content.lower():
        intent = "Invoice"
    elif 'regulation' in content.lower():
        intent = "Regulation"

    crm_format = {
        "sender": sender,
        "intent": intent,
        "urgency": urgency,
        "summary": content[:150].strip().replace('\n', ' ') + "..."
    }

    return crm_format, intent
 """


# agents/email_agent.py

def extract_email_info(email_text):
    # Very simple keyword-based extraction
    lines = email_text.strip().split('\n')
    sender = ""
    urgency = "Normal"

    for line in lines:
        if 'from:' in line.lower():
            sender = line.split(':', 1)[1].strip()
        if 'urgent' in line.lower():
            urgency = "High"

    # Basic intent detection
    email_text_lower = email_text.lower()
    if 'invoice' in email_text_lower:
        intent = "Invoice"
    elif 'quote' in email_text_lower or 'rfq' in email_text_lower:
        intent = "RFQ"
    elif 'complaint' in email_text_lower:
        intent = "Complaint"
    elif 'regulation' in email_text_lower:
        intent = "Regulation"
    else:
        intent = "Unknown"

    return {
        "sender": sender,
        "urgency": urgency,
        "body_preview": email_text[:100]  # Show only first 100 chars
    }, intent
