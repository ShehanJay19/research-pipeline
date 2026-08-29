import asyncio
import sys
from agents.pipeline import run_pipeline
from core.budget import budget,BudgetExceeded


async def main():
    question = sys.argv[1] if len(sys.argv) > 1 else "What is the current state of solid-state battery commercialization?"
    print(f"Researching: {question}\n")
    try:
        report = await run_pipeline(question)
        print(report)
    except BudgetExceeded as e:
        print(f"\n⚠️  Budget exhausted before a report could be produced: {e}")
        print("Raise the limits in core/budget.py if this keeps happening on normal questions.")
    finally:
        print("\n" + budget.summary())


if __name__ == "__main__":
    asyncio.run(main())