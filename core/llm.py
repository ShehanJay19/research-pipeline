import os
import json
import re
from typing import Type, TypeVar
from core.budget import budget


from dotenv import load_dotenv
from groq import Groq, AsyncGroq, RateLimitError
from pydantic import BaseModel, ValidationError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

load_dotenv()

client = Groq()
async_client = AsyncGroq()

T = TypeVar("T", bound=BaseModel)

JSON_INSTRUCTION = (
    "Respond with ONLY valid JSON. No markdown code fences, "
    "no preamble, no explanation — just the raw JSON object."
)


# ---------- Sync ----------

@retry(
    retry=retry_if_exception_type(RateLimitError),
    wait=wait_exponential(multiplier=1, min=2, max=60),
    stop=stop_after_attempt(5)
)
def call_llm(prompt: str, model: str = "llama-3.3-70b-versatile", max_tokens: int = 1000) -> str:
    """Send a prompt to the LLM and return the text response. Retries on rate limits."""
    response = client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}]
    )
    budget.record_llm_call(response.usage.prompt_tokens, response.usage.completion_tokens)

    return response.choices[0].message.content


def call_llm_json(prompt: str, model: str = "llama-3.3-70b-versatile", max_tokens: int = 1000) -> dict:
    """Call the LLM and parse the response as JSON, stripping markdown fences if present."""
    raw = call_llm(f"{JSON_INSTRUCTION}\n\n{prompt}", model=model, max_tokens=max_tokens)
    cleaned = re.sub(r"^```(?:json)?\s*", "", raw.strip())
    cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"Model did not return valid JSON.\nRaw output: {raw}") from e


def call_llm_structured(prompt: str, schema: Type[T], model: str = "llama-3.3-70b-versatile", max_tokens: int = 1000) -> T:
    """Call the LLM, parse JSON, and validate it against a Pydantic schema."""
    data = call_llm_json(prompt, model=model, max_tokens=max_tokens)
    try:
        return schema.model_validate(data)
    except ValidationError as e:
        raise ValueError(f"Model output didn't match expected schema.\nRaw data: {data}\nErrors: {e}") from e


# ---------- Async ----------

@retry(
    retry=retry_if_exception_type(RateLimitError),
    wait=wait_exponential(multiplier=1, min=2, max=60),
    stop=stop_after_attempt(5)
)
async def call_llm_async(prompt: str, model: str = "llama-3.3-70b-versatile", max_tokens: int = 1000) -> str:
    """Async version of call_llm — used by agents that run concurrently."""
    response = await async_client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


async def call_llm_json_async(prompt: str, model: str = "llama-3.3-70b-versatile", max_tokens: int = 1000) -> dict:
    """Async version of call_llm_json."""
    raw = await call_llm_async(f"{JSON_INSTRUCTION}\n\n{prompt}", model=model, max_tokens=max_tokens)
    cleaned = re.sub(r"^```(?:json)?\s*", "", raw.strip())
    cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"Model did not return valid JSON.\nRaw output: {raw}") from e


async def call_llm_structured_async(prompt: str, schema: Type[T], model: str = "llama-3.3-70b-versatile", max_tokens: int = 1000) -> T:
    """Async version of call_llm_structured."""
    data = await call_llm_json_async(prompt, model=model, max_tokens=max_tokens)
    try:
        return schema.model_validate(data)
    except ValidationError as e:
        raise ValueError(f"Model output didn't match expected schema.\nRaw data: {data}\nErrors: {e}") from e