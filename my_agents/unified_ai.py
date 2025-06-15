import os
import requests
from dotenv import load_dotenv

load_dotenv()

NOVITA_API_KEY = os.getenv("NOVITA_API_KEY")
NOVITA_API_URL = "https://api.novita.ai/v3/openai"
MODEL_NAME = "deepseek/deepseek-r1-0528"

def ai_complete(prompt, tone="professional"):
    headers = {
        "Authorization": f"Bearer {NOVITA_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": f"You are a helpful assistant. Your tone should be {tone}."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(f"{NOVITA_API_URL}/chat/completions", headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
