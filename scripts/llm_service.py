from google import genai
import os
from dotenv import load_dotenv


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


MODEL_NAME = "gemini-3.1-flash-lite"



def generate_response(prompt):

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text