import os
from dotenv import load_dotenv
from groq import Groq, RateLimitError
from tenacity import retry, stop_after_attempt, wait_random_exponential, retry_if_exception_type 
import json
import re

load_dotenv()
client =Groq()
def call_llm_json(prompt: str, model: str = "llama-3.3-70b-versatile", max_tokens: int = 1000) -> dict:
    """Send a prompt and parse the reponse as JSON,stripping markdown fences if presented."""
    system_instruction= "Respond with ONLY valid JSON. No markdwon code fences,no preamble,no explanation - jsut the raw JSON object."
    full_prompt=f"{system_instruction}\n\n{prompt}"
    
    raw, _usage=call_llm(full_prompt,model=model,max_tokens=max_tokens)
    
    cleaned=raw.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    
    try: 
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"Model did not return valid JSON.\nRaw output: {raw}") from e
    
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
