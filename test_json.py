from core.llm import call_llm_json
result = call_llm_json(
    "Give me a JSON object with keys 'city' and 'country' for the capital of Japan."
)
print(result)
print(type(result))