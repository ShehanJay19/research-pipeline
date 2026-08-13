from agents.searcher import Finding
from agents.critic import critique

fake_findings = [
    Finding(claim="Solid-state batteries are expected to reach mass production by 2027",
            source_url="https://example.com/a", confidence="high"),
    Finding(claim="Solid-state batteries are not expected to reach mass production before 2030",
            source_url="https://example.com/b", confidence="high"),
    Finding(claim="Toyota has announced plans to commercialize solid-state batteries",
            source_url="https://example.com/c", confidence="medium"),
]

result = critique(fake_findings)
print("VERIFIED:", len(result.verified))
print("CONTRADICTIONS:", result.contradictions)
print("GAPS:", result.gaps)