import asyncio
from agents.pipeline import research_with_critic_loop

async def main():
    result = await research_with_critic_loop(
        "What is the current state of solid-state battery commercialization?"
    )
    print(f"\nFINAL — verified: {len(result.verified)}, contradictions: {len(result.contradictions)}, gaps: {len(result.gaps)}")

asyncio.run(main())