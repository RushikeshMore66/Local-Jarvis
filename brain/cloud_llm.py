import requests
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")

def ask_cloud(prompt: str) -> str:
    if not OPENROUTER_API_KEY:
        return "cloud API key not configured."

    url = f"{OPENROUTER_BASE_URL}/chat/completions"

    headers ={
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a helpful AI assistant that understands Indian English, "
                    "casual phrasing, and imperfect grammar. Interpret intent correctly."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.5
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code != 200:
            return f"Cloud error: {response.text}"
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error connecting to cloud LLM: {e}"

    