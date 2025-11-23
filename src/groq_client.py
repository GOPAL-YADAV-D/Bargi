# Groq API wrapper
# Pure LLM communication layer
from dotenv import load_dotenv
load_dotenv()

import os
import requests


def groq_chat(messages, model="openai/gpt-oss-120b", temperature=0.4):
    """
    Send messages to Groq API and get a response.
    """

    # Load API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable not set")

    # Groq OpenAI-compatible endpoint
    url = "https://api.groq.com/openai/v1/chat/completions"

    # Headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Payload
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)

        # If bad request, show Groq's detailed error
        if response.status_code >= 400:
            raise Exception(
                f"Groq API error {response.status_code}: {response.text}"
            )

        data = response.json()

        # Extract Groq response safely
        return data["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        raise Exception(f"Groq network error: {e}")

    except (KeyError, IndexError):
        raise Exception(
            f"Unexpected Groq response format: {response.text}"
        )
