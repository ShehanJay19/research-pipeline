import asyncio
import sys
from agents.pipeline import run_pipeline
from core.budget import budget

async def main():
    question = sys.argv[1] if len(sys.argv) > 1 else "What is the current state of solid-state battery commercialization?"
    print(f"Researching: {question}\n")
    report = await run_pipeline(question)
    print(report)
    print("\n" + budget.summary())


if __name__ == "__main__":
    asyncio.run(main())