from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
NOVITA_API_KEY = os.getenv("NOVITA_API_KEY")
NOVITA_API_URL = "https://api.novita.ai/v3/openai"
MODEL_NAME = "deepseek/deepseek-r1-0528"

client = OpenAI(base_url=NOVITA_API_URL, api_key=NOVITA_API_KEY)

def ai_complete(prompt, tone="professional"):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": f"You are a helpful assistant. Your tone should be {tone}."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
