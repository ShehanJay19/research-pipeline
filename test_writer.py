from agents.searcher import Finding
from agents.writer import write_report

fake_findings = [
    Finding(claim="Solid-state batteries are expected to reach mass production by 2027",
            source_url="https://example.com/a", confidence="high"),
    Finding(claim="Toyota has announced plans to commercialize solid-state batteries",
            source_url="https://example.com/c", confidence="medium"),
]

report = write_report(
    question="What is the current state of solid-state battery commercialization?",
    verified_findings=fake_findings,
    unresolved_gaps=["Cost per kWh compared to lithium-ion batteries"]
)
print(report)