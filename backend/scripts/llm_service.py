from google import genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Gemini configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# FIX: Changed to a valid Gemini model name
MODEL_NAME = os.getenv("LLM_MODEL", "gemini-1.5-flash")

TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))
MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "512"))

# Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

def generate_response(prompt):
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config={
                "temperature": TEMPERATURE,
                "max_output_tokens": MAX_TOKENS
            }
        )

        if not response or not response.text:
            return fallback_response("Empty response returned from Gemini")

        answer = response.text.strip()

        # Remove unnecessary Gemini formatting
        cleanup_headers = [
            "Answer:",
            "Answer | መልስ:",
            "መልስ:"
        ]

        for header in cleanup_headers:
            answer = answer.replace(header, "")

        return answer.strip()

    except Exception as e:
        print("Gemini API Error:", e)
        return fallback_response("Gemini service unavailable")

def fallback_response(reason):
    return f"""
Answer:
The answer is not available in the retrieved legal documents.

Relevant Sources:
No sufficiently relevant legal source was retrieved.

Important Note:
This response is provided for general legal information only 
and does not replace advice from a qualified legal professional.

System Message:
{reason}
"""