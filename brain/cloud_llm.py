"""
Cloud LLM — Mistral via OpenRouter with Jarvis personality, retry logic,
and conversation history injection.
"""

import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "mistralai/mistral-7b-instruct")

_JARVIS_SYSTEM = (
    "You are JARVIS — Just A Rather Very Intelligent System. "
    "You are an advanced AI assistant with worldwide knowledge. "
    "You speak confidently and concisely, like Tony Stark's AI. "
    "You understand Indian English, casual phrasing, and imperfect grammar perfectly. "
    "You give direct, actionable, and intelligent answers. "
    "If asked about current events, acknowledge your knowledge cutoff and provide the best available context. "
    "Keep responses under 3 paragraphs unless a longer answer is required."
)


def ask_cloud(prompt: str, history: list = None, retries: int = 2) -> str:
    """Call cloud LLM with retry logic and Jarvis personality."""
    if not OPENROUTER_API_KEY:
        return "Cloud LLM not configured. Please set OPENROUTER_API_KEY in your .env file."

    messages = [{"role": "system", "content": _JARVIS_SYSTEM}]

    # Inject short-term conversation history
    if history:
        for turn in history[-4:]:  # last 4 turns for context
            messages.append({"role": "user", "content": turn.get("user", "")})
            messages.append({"role": "assistant", "content": turn.get("assistant", "")})

    messages.append({"role": "user", "content": prompt})

    url = f"{OPENROUTER_BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/local-jarvis",
        "X-Title": "JARVIS Local Agent",
    }
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": messages,
        "temperature": 0.6,
        "max_tokens": 512,
    }

    for attempt in range(retries + 1):
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=30)
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"].strip()
            else:
                if attempt < retries:
                    time.sleep(2 ** attempt)
                    continue
                return f"Cloud error ({resp.status_code}): {resp.text[:200]}"
        except requests.Timeout:
            if attempt < retries:
                time.sleep(2)
                continue
            return "Cloud LLM timed out. Try again in a moment."
        except Exception as e:
            return f"Cloud connection error: {e}"

    return "Cloud LLM unavailable after retries."