import asyncio
from agents.planner import plan
from agents.searcher import search,Finding
from agents.critic import critique,CriticOutput
from agents.writer import write_report
MAX_ITERATIONS = 2

async def gather_findings(questions:list[str])->list[Finding]:
    """Run searcher concurrently for all questions ,return combined findings
    """
    tasks = [search(q) for q in questions]
    results = await asyncio.gather(*tasks)
    
    all_findings = []
    for r in results:
        all_findings.extend(r.findings)
    return all_findings


def build_followup_queries(critic_output:CriticOutput)->list[str]:
   """Turn gaps and contradictions into new searcher queries
   """
   queries =[]
   for c in critic_output.contradictions:
        queries.append(f"{c.topic}: find an authoritative source to resolve conflicting claims: {', '.join(c.conflicting_claims)}")
        
   return queries


async def research_with_critic_loop(question: str) -> CriticOutput:
    plan_result = plan(question)
    all_findings = await gather_findings(plan_result.sub_questions)
    critic_output = critique(all_findings)

    iteration = 1
    while (critic_output.gaps or critic_output.contradictions) and iteration < MAX_ITERATIONS:
        followup_queries = build_followup_queries(critic_output)
        print(f"\n--- Re-search iteration {iteration}: {len(followup_queries)} follow-up quer{'y' if len(followup_queries)==1 else 'ies'} ---")
        for q in followup_queries:
            print(f"  - {q}")

        new_findings = await gather_findings(followup_queries)
        all_findings.extend(new_findings)
        critic_output = critique(all_findings)
        iteration += 1

    return critic_output    
async def run_pipeline(question: str) -> str:
    """Full pipeline: plan -> parallel search -> critic loop -> write report."""
    critic_output = await research_with_critic_loop(question)
    report = write_report(
        question=question,
        verified_findings=critic_output.verified,
        unresolved_gaps=critic_output.gaps
    )
    return report

async def run_pipeline(question: str) -> str:
    """Full pipeline: plan -> parallel search -> critic loop -> write report."""
    critic_output = await research_with_critic_loop(question)
    report = write_report(
        question=question,
        verified_findings=critic_output.verified,
        unresolved_gaps=critic_output.gaps
    )
    return report

