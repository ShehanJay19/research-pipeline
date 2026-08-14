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
