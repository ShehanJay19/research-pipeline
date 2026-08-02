import os
from dotenv import load_dotenv
from groq import Groq
from tenacity import retry, stop_after_attempt, wait_random_exponential, retry_if_exception_type 

load_dotenv()
client =Groq()
@retry(
    stop=stop_after_attempt(5),
    wait=wait_random_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type(RateLimitError)
)

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
