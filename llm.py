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
    print("CONTEXT: ", context)

    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are a helpful assistant."
                    "Answer the question using the provided context."
                    "The answer may not explicitly be in the context, MAKE SURE to use the context to infer the answer."
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