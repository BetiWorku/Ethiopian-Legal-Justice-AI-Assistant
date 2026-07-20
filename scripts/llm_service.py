from pathlib import Path
from google import genai
from dotenv import load_dotenv
import os

project_root = Path(__file__).resolve().parents[1]
load_dotenv(project_root / ".env")


def get_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key in {"your_key", ""}:
        return None
    return genai.Client(api_key=api_key)


def generate_response(prompt):
    client = get_client()
    if client is None:
        return (
            "The Gemini API key is missing or not configured. "
            "Please set GEMINI_API_KEY in the .env file."
        )

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text
    except Exception as exc:
        error_message = str(exc).lower()
        if "429" in error_message or "quota" in error_message or "resource_exhausted" in error_message:
            return (
                "The Gemini API is temporarily unavailable because the free-tier quota has been exceeded. "
                "Please wait a while or use a paid API plan / a different API key."
            )
        return f"The Gemini API request failed: {exc}"


def main():
    prompt = "What are the requirements for a valid contract?"
    print(generate_response(prompt))


if __name__ == "__main__":
    main()