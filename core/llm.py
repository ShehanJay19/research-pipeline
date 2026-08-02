import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client =Groq()

def call_llm(prompt: str, model: str = "llama-3.3-70b-versatile", max_tokens: int = 1000) ->str:
    """Send a prompt to the LLM and return the response."""
    response = client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content, response.usage
