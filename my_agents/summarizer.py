import re
from .unified_ai import ai_complete

PROMPT_TEMPLATE = """
You are an AI assistant generating a user-friendly README description for a GitHub project.
The following is a code file. Analyze what the project does and describe it clearly and concisely for a GitHub README file.
Avoid mentioning temporary file paths or including AI reasoning like <think> or "we are given...".

{code}
"""

def clean_ai_output(text):
    # Remove <think>...</think> blocks and strip leading/trailing whitespace
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    return text.strip()

def summarize_files(analysis, tone="Professional"):
    summaries = {}
    for fname, info in analysis.items():
        if "code" in info:
            prompt = PROMPT_TEMPLATE.format(code=info["code"])
            ai_response = ai_complete(prompt, tone=tone)
            summaries[fname] = clean_ai_output(ai_response)
        else:
            summaries[fname] = "[Error: Could not analyze file]"
    return summaries
