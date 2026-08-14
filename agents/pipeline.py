import asyncio
from agents.planner import plan
from agents.searcher import search,Finding
from agents.critic import critique,CriticOutput

MAX_ITERATIONS = 2

async def gathe_findings(questions:list[str])->list[Finding]:
    """Run searcher concurrently for all questions ,return combined findings
    """
    tasks = [search(q) for q in questions]
    results = await asyncio.gather(*tasks)
    
    all_findings = []
    for r in results:
        all_findings.extend(r.findings)
    return all_findings



    