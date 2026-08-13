from pydantic import BaseModel
from core.llm import call_llm_structured 
from agents.searcher import Findings

class Contradiction(BaseModel):
    topic:str
    conficting_class: list[str]
    
    
class Criticoutput(BaseModel):
    verified:list[Findings] 
    contradictions:list[Contradiction]
    gaps: list[str]   