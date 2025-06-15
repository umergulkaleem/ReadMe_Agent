import os
import openai

# Load the Novita key from env or Streamlit secrets
NOVITA_API_KEY = os.getenv("NOVITA_API_KEY")  # or st.secrets["NOVITA_API_KEY"]
NOVITA_API_BASE = "https://api.novita.ai/v1"  # or as given in their docs

openai.api_key = NOVITA_API_KEY
openai.api_base = NOVITA_API_BASE

def ai_complete(prompt, model="gpt-3.5-turbo"):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=1024
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"
