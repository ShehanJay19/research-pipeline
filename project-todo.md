# Multi-Agent Research Pipeline — Master To-Do List

**Stack (100% free):** Groq (LLM, free forever, no card) · Tavily (search, 1,000 free/mo) · Streamlit (UI, free) · Python

**Status legend:** ⬜ not started · 🟨 in progress · ✅ done

---

## 📍 Current step: Phase 0 — Accounts & Setup

---

## Phase 0 — Accounts & Environment Setup
- ⬜ Create Groq account, generate API key
- ⬜ Create Tavily account, generate API key
- ⬜ Create project folder + virtual environment
- ⬜ Install core packages (`groq`, `tavily-python`, `python-dotenv`, `pydantic`)
- ⬜ Create `.env` with both API keys + `.gitignore`
- ⬜ Verify: one successful test call to Groq

## Phase 1 — Core LLM Wrapper
- ⬜ Build `core/llm.py`: wraps Groq client, one function to call the model and get text back
- ⬜ Add retry logic for rate-limit errors (Groq free tier has RPM/TPM caps)
- ⬜ Add a helper that forces/parses JSON output from the model
- ⬜ Validate JSON output with a Pydantic model
- ⬜ **Milestone:** call `llm.py` directly, get validated structured output

## Phase 2 — Planner Agent
- ⬜ Write planner prompt: research question → 3–5 sub-questions
- ⬜ Build `agents/planner.py` using `core/llm.py`
- ⬜ **Milestone:** `python -m agents.planner "question"` prints a clean sub-question list

## Phase 3 — Search Tool + Searcher Agent
- ⬜ Build `core/tools.py`: wraps Tavily search
- ⬜ Build `agents/searcher.py`: sub-question → structured findings (`claim`, `source_url`, `snippet`)
- ⬜ **Milestone:** one searcher call returns 3–5 sourced findings for one sub-question

## Phase 4 — Parallel Execution
- ⬜ Convert searcher to async
- ⬜ Run all searchers concurrently with `asyncio.gather()`
- ⬜ Add a semaphore to respect Groq/Tavily rate limits
- ⬜ **Milestone:** all sub-questions searched in parallel, total time ≈ slowest single search

## Phase 5 — Critic Agent + Feedback Loop
- ⬜ Write critic prompt: findings → verified / contradictions / gaps
- ⬜ Build `agents/critic.py`
- ⬜ Implement re-search loop for gaps/contradictions (capped at 2 iterations)
- ⬜ **Milestone:** critic catches a deliberately-planted contradiction in test data

## Phase 6 — Writer Agent
- ⬜ Write writer prompt: verified findings only → report with inline citations [1][2] + source list
- ⬜ Build `agents/writer.py`
- ⬜ **Milestone:** full pipeline runs end-to-end, produces a cited markdown report

## Phase 7 — Rate/Budget Controller
- ⬜ Build `core/budget.py`: tracks requests + tokens used per run against Groq/Tavily free-tier caps
- ⬜ Add pre-call checks that block/queue when near a cap
- ⬜ Add graceful degradation rule (e.g. skip re-search loop if near limit)
- ⬜ Print a usage summary at end of each run
- ⬜ **Milestone:** deliberately spam the pipeline, watch it throttle itself instead of crashing

## Phase 8 — Tracing & Logging
- ⬜ Log every agent call (name, input, output, tokens, duration) to a JSONL file
- ⬜ **Milestone:** can reconstruct exactly what happened in a run from the log alone

## Phase 9 — Streamlit UI
- ⬜ Basic UI: text input for question → button → spinner → final report displayed
- ⬜ Show live progress: which agent is running, sub-questions found, sources gathered
- ⬜ Show the source list as clickable links
- ⬜ Show token/cost-equivalent usage from the budget controller
- ⬜ Polish styling (layout, colors, report formatting)
- ⬜ **Milestone:** a non-technical person can use it without reading code

## Phase 10 — Deploy & Portfolio Polish
- ⬜ Push to GitHub (public repo)
- ⬜ Deploy free on Streamlit Community Cloud
- ⬜ Write README: architecture diagram, screenshots, how to run locally
- ⬜ Add 2–3 example runs saved in the repo
- ⬜ Record a short demo GIF/video for the README

---

## 🧠 Concepts learned along the way
*(filled in as you ask questions — not project steps, just your personal reference)*

-
