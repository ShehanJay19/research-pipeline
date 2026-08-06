from pydantic import BaseModel,Field
from core.llm import call_llm_structured

class PlannerOutput(BaseModel):
    sub_questions:list[str]=Field(min_length=3,max_length=5)