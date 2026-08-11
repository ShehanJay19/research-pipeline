from pydantic import BaseModel,Field
from core.llm import call_llm_structured_async
from core.tools import web_search

class Finding(BaseModel):
    claim:str
    source_url:str
    confidence: str=Field(description="high, medium, or low")
    
class SearcherOutput(BaseModel):
    findings: list[Finding]

SEARCHER_PROMPT = """You are a research assistant. Below are web search results for
the question: "{question}"

Search results:
{results_block}

Extract 3-5 distinct factual findings that help answer the question. For each finding:
- State the claim in your own words (do not copy text verbatim)
- Reference the source_url it came from — you MUST only use URLs that appear above, never invent one
- Rate your confidence: "high" if directly stated, "medium" if inferred, "low" if uncertain

Respond with a JSON object in this exact shape:
{{"findings": [{{"claim": "...", "source_url": "...", "confidence": "..."}}]}}
"""

async def search(question: str) -> SearcherOutput:
    """Search the web for a sub-question and return structured, sourced findings."""
    results = web_search(question)  # Tavily's client is sync — fine for now, thread it later if it's a bottleneck
    results_block = "\n\n".join(
        f"[{r['title']}]({r['url']})\n{r['content']}" for r in results
    )
    prompt = SEARCHER_PROMPT.format(question=question, results_block=results_block)
    return await call_llm_structured_async(prompt, schema=SearcherOutput)


if __name__ == "__main__":
    import asyncio
    import sys

    async def main():
        question = sys.argv[1] if len(sys.argv) > 1 else "What is the current state of solid-state battery commercialization?"
        result = await search(question)
        for f in result.findings:
            print(f"[{f.confidence}] {f.claim}")
            print(f"    source: {f.source_url}\n")

    asyncio.run(main())