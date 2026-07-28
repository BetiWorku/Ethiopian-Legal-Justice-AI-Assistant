import requests
import json

# Make sure your FastAPI server is running (uvicorn app:app --reload) before running this script.

url = "http://127.0.0.1:8000/chat"

# Test question (Amharic)
payload = {"question": "የእኩልነት መብት ምንድነው?"}
headers = {"Content-Type": "application/json; charset=utf-8"}

print("Sending request to API...")

try:
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status() # Raise an exception for HTTP errors
    
    # Print with ensure_ascii=False to see Amharic characters properly in terminal
    print("\nAPI Response:")
    print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    
except requests.exceptions.RequestException as e:
    print(f"\nError connecting to API: {e}")
    print("Please ensure the FastAPI server is running on port 8000.")