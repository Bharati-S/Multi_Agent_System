Name:- Bharati Sharma 
 

# TOPIC:- MultiAgent AI System 
   This project is a multiagent system built in Python that classifies and processes incoming data in PDF, JSON, or Email (text) format using dedicated agents. It maintains a shared memory context to enable chaining, traceability, and persistent storage.



1. Objective :- To build a modular system with the following capabilities:
                - Accept inputs in PDF, JSON, or Email formats.
                - Detect the format and intent (Invoice, RFQ, Complaint, etc.).
                - Route input to the appropriate agent for processing.
                - Store classification and extracted data in a shared memory module for context and traceability.



2. System Architecture

 1) Classifier Agent
    - Accepts raw input.
    - Detects format (PDF / JSON / Email).
    - Infers intent using keyword methods.
    - Routes data to the appropriate agent.
    - Logs classification in shared memory.

 2) JSON Agent
    - Accepts structured JSON payloads.
    - Extracts fields into a target schema.
    - Flags anomalies or missing fields.

 3) Email Agent
    - Accepts plaintext email content.
    - Extracts sender, urgency, and inferred intent.
    - Prepares data for CRM or workflow tools.

 4) Shared Memory Module
    - Uses SQLite to store and share:
       - Input source
       - Format and intent
       - Extracted values
       - Thread ID and timestamp
       - Accessible by all agents.

3. Tech Stack:- 
   - Python
   - SQLite (for shared memory)
   - Regex / Keyword Matching
