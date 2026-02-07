from data_pipeline.textChunking import chunk_documents
from data_pipeline.readPDF import process_document_bucket
from data_pipeline.embedding import embed_and_save
from llm import query_llm

INPUT_FILE = "raw_text/extracted_text.txt"
OUTPUT_DIR = "chunks"
MAX_SIZE = 2000

def ask_question():
    user_prompt = input("\n\nAsk a question: ")
    response = query_llm(user_prompt)
    print(response)

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