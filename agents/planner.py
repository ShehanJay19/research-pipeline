from pydantic import BaseModel,Field
from core.llm import call_llm_structured

class PlannerOutput(BaseModel):
    sub_questions:list[str]=Field(min_length=3,max_length=5)
    
    
    
PLANNER_PROMPT ="""Your are a research planner.Break the following research question into 3 to 5 focused sub-questions that, together, would let someone answer the original question thoroughly.
Rules:
-Each sub-question should cover a distinct angle-no overlap between them
-Sub-question should be specific enough to search for directly
-Do not answer the question,only decompse it

Research Question: {question}

Response with JSON object in this exact shape:
{{"sub_questions":["...","...","..."]}}

"""
def plan(question:str)->PlannerOutput:
    prompt=PLANNER_PROMPT.format(question=question)
    return call_llm_structured(prompt,schema=PlannerOutput)

if __name__=="__main__":
    import sys
    question =sys.argv[1] if len(sys.argv) > 1 else "What is the current state of solid-state battery commercialization?"
    result = plan(question)
    for i,sq in enumerate(result.sub_questions,1):
        print(f"{i}. {sq}") 