import time


class BudgetExceeded(Exception):
    pass


class Budget:
    def __init__(self, max_llm_calls: int = 25, max_search_calls: int = 15):
        self.llm_calls = 0
        self.llm_input_tokens = 0
        self.llm_output_tokens = 0
        self.search_calls = 0
        self.start_time = time.time()
        self.max_llm_calls = max_llm_calls
        self.max_search_calls = max_search_calls

    def record_llm_call(self, input_tokens: int, output_tokens: int):
        self.llm_calls += 1
        self.llm_input_tokens += input_tokens
        self.llm_output_tokens += output_tokens

    def record_search_call(self):
        self.search_calls += 1

    def summary(self) -> str:
        elapsed = time.time() - self.start_time
        return (
            f"--- Budget summary ---\n"
            f"LLM calls: {self.llm_calls}/{self.max_llm_calls} "
            f"(in: {self.llm_input_tokens} tok, out: {self.llm_output_tokens} tok)\n"
            f"Search calls: {self.search_calls}/{self.max_search_calls}\n"
            f"Elapsed: {elapsed:.1f}s"
        )


# One shared instance for the whole run
budget = Budget()