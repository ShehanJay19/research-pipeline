from pydantic import BaseModel
from core.llm import call_llm_structured

class Capital(BaseModel):
    city: str
    country: str
    
result = call_llm_structured(
    "Give me a JSON object with key 'city' and 'country' for capital of Japan",
    schema=Capital
)

print(result)
print(result.city)  # Should print "Tokyo"
print(type(result))
