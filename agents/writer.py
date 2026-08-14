from core.llm import call_llm
from agents.searcher import Finding

WRITER_PROMPT="""You are a research report writer. Write a clear, well-organized report
answering the question below, using ONLY the verified findings provided. Do not use any
outside knowledge — if the findings don't cover something, don't invent it.

Question: {question}

Verified findings (numbered — cite them inline like [1], [2] where you use them):
{numbered_findings}

{gaps_section}

Write the report in markdown. Structure:
1. A short introductory paragraph
2. 2-4 sections with headers covering the main themes in the findings
3. Cite every factual claim inline with its number, e.g. "Prices have fallen 40% since 2023 [2]."
4. End with a "## Sources" section listing every numbered source as a markdown link

Be honest about uncertainty — if findings disagree or coverage is thin, say so rather than
overstating confidence.
"""
def write_report(question: str, verified_findings: list[Finding], unresolved_gaps: list[str] | None = None) -> str:
    numbered_findings = "\n".join(
        f"[{i}] {f.claim} (source: {f.source_url})"
        for i, f in enumerate(verified_findings, 1)
    )

    gaps_section = ""
    if unresolved_gaps:
        gaps_list = "\n".join(f"- {g}" for g in unresolved_gaps)
        gaps_section = f"Note: these areas remain uncertain or under-covered — mention this limitation in the report where relevant:\n{gaps_list}"

    prompt = WRITER_PROMPT.format(
        question=question,
        numbered_findings=numbered_findings,
        gaps_section=gaps_section
    )
    return call_llm(prompt, max_tokens=2000)