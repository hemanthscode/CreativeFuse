import requests
from app.config import OPENROUTER_API_KEY

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

def generate_idea(domain: str, keywords: str, style: str) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    system_prompt = "You are a helpful assistant that generates creative ideas."
    user_prompt = (
        f"Generate a {style} idea for the domain '{domain}'."
        + (f" Include these keywords: {keywords}." if keywords else "")
        + " Provide a concise, creative description."
    )

    payload = {
        "model": "x-ai/grok-4-fast:free",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.8,
        "max_tokens": 150,
        "n": 1,
    }

    response = requests.post(OPENROUTER_API_URL, json=payload, headers=headers)
    if response.status_code != 200:
        raise RuntimeError(f"OpenRouter request failed: {response.status_code} {response.text}")

    res_json = response.json()
    return res_json['choices'][0]['message']['content'].strip()
