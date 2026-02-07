import re
from data_pipeline.textChunking import chunk_documents
from data_pipeline.readPDF import process_document_bucket
from data_pipeline.embedding import embed_and_save
from llm import query_llm
import os
import json

INPUT_FILE = "raw_text/extracted_text.txt"
OUTPUT_DIR = "chunks"
MAX_SIZE = 2000

def ask_question():
    user_prompt = input("\n\nAsk a question: ")
    response = query_llm(user_prompt)
    print(response)

def find_ticket_by_id(ticket_id, json_filepath='document_bucket/tickets_export.json'):
    if not os.path.exists(json_filepath):
        print(f"Error: JSON file '{json_filepath}' not found!")
        return None
    
    try:
        with open(json_filepath, 'r', encoding='utf-8') as f:
            tickets = json.load(f)
        
        for ticket in tickets:
            if ticket['ticket_id'] == ticket_id:
                return ticket
        
        print(f"Ticket ID '{ticket_id}' not found in the JSON file.")
        return None
    
    except json.JSONDecodeError:
        print(f"Error: Could not parse JSON file '{json_filepath}'")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
    
def extract_ticket_ids(response_text):
    ticket_pattern = r'(?:The\s+)?(?:most\s+)?relevant ticket numbers?\s*(?:are|is)?[:\s]*\n?(?:\d+\.\s*IT-\d+\s*\n?)+'
    
    ticket_ids = re.findall(r'IT-\d+', response_text)

    cleaned_response = re.sub(ticket_pattern, '', response_text, flags=re.IGNORECASE).strip()
    
    print(f"Extracted ticket IDs: {ticket_ids}")
    print(f"Cleaned response: {cleaned_response}")
    return cleaned_response, ticket_ids
    
if __name__ == "__main__":

    choice = 0

    while choice != 1 or choice != 2 or choice != 3:
        print("Welcome to the IT Ticket Knowledge Base AI Assistant!")
        print("\nOptions: ")
        print("1. Process Data")
        print("2. Use the Assistant")
        print("3. Exit")
        choice = int(input("Choose your action: "))

        if choice == 1:
            process_document_bucket()
            chunk_documents(INPUT_FILE, OUTPUT_DIR, MAX_SIZE)
            embed_and_save()
            print("\n")
        elif choice == 2:
            ask_question()
            print("\n")
        elif choice == 3:
            break
        else:
            print("Invalid choice.\n")