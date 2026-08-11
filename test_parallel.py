import asyncio
import time
from agents.planner import plan
from agents.searcher import search

async def search_sequential(sub_questions: list[str]):
    """One searcher at a time -the 'before' version"""
    results=[]
    for q in sub_questions:

        result=await search(q)
        results.append(result)
    return results


async def search_parallel(sub_questions:list[str]):
    """All searchers at onece - the 'after'version """
    tasks=[search(q) for q in sub_questions]
    results=await asyncio.gather(*tasks)
    return results
    
async def main():
    question="What is the current state of solid-state battery commercialization?" 
    
    plan_result=plan(question)
    sub_questions=plan_result.sub_questions
    
    print (f"Sub-questions ({len(sub_questions)}):")
    for sq in sub_questions:
        print(f"  - {sq}")
    
    print("\n---- Sequential Search ---")
    start_time=time.time()
    seq_results=await search_sequential(sub_questions)
    print(f"Sequential took {time.time() - start_time:.2f}s")
    
    print("\n --- Parallel Search ---")
    start =time.time()
    par_results=await search_parallel(sub_questions)
    print(f"Parallel took {time.time() - start:.2f}s")
    
    total_findings=sum(len(r.findings) for r in par_results)
    print(f"\nTotal findings: {total_findings}")
    
if __name__=="__main__":
    asyncio.run(main())     