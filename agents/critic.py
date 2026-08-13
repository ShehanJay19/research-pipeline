from pydantic import BaseModel
from core.llm import call_llm_structured 
from agents.searcher import Finding

class Contradiction(BaseModel):
    topic:str
    conflicting_claims: list[str]
    
    
class CriticOutput(BaseModel):
    verified:list[Finding] 
    contradictions:list[Contradiction]
    gaps: list[str]   
    
CRITIC_PROMPT = """You are a fact-checking critic reviewing research findings before theygo into the report.Below are findings gathered from multiple searches, each with source URL.

Findings:
{findings_block}

Your job:
1. VERIFIED: finding that are credible and not contradicted elsewhere - pass these through as-is.
2. CONTRADICTIONS: group fiindings that disagree with each other on the same topic,quoting both claims.
3. GAPS: importnt aspects of the topic that these findings do not cover well enough to write a through report.

Be skeptical.A single source making claim is not automatically verified if it's a strong or surprising claim with no corroboration - use judgment.

Respond with a JSON object in this exact shape:
{{"verified": [{{"claim": "...", "source_url": "...", "confidence": "..."}}],
  "contradictions": [{{"topic": "...", "conflicting_claims": ["...", "..."]}}],
  "gaps": ["...", "..."]}}
"""    

def critique(all_findings: list[Finding]) -> CriticOutput:
    findings_block = "\n".join(
        f"- {f.claim} (source: {f.source_url}, confidence: {f.confidence})"
        for f in all_findings
    )
    prompt = CRITIC_PROMPT.format(findings_block=findings_block)
    return call_llm_structured(prompt, schema=CriticOutput)