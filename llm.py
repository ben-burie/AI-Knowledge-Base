from dotenv import load_dotenv
from google import genai
from google.genai import types
from data_pipeline.embedding import search
import os

load_dotenv()

client = genai.Client(api_key=os.getenv('API-KEY'))

def query_llm(user_prompt):

    relevant_chunks = search(user_prompt, 3) # (user_prompt, top_k chunks)
    context = "\n\n".join(relevant_chunks)
    #print("RELEVANT CHUNKS: ", relevant_chunks)
    #print("CONTEXT: ", context)

    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are a helpful assistant to IT helpdesk workers."
                    "Answer the question using the provided context."
                    "The answer may not explicitly be in the context, MAKE SURE to use the context to infer the answer."
                    "Please give 3 of the most relevant ticket numbers of the relevant tickets used in the answer. Format them like this: 'Relevant ticket numbers:\n 1. IT-12345, 2. IT-67890, 3. IT-24680' If there are no relevant tickets, say 'There are no relevant tickets.'"
                )
            ),
            contents=[
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": f"""
                            Context:
                            {context}

                            Question:
                            {user_prompt}
                            """
                        }
                    ]
                }
            ]
        )

        return response.text
    except Exception as e:
        print(f"An error occured when formulating response: {e}")