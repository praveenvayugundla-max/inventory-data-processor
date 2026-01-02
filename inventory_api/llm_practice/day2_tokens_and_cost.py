# Day 2: Tokens & cost calculation (Simple estimation)

def estimate_tokens(text: str) -> int:
    """
    Rough token estimation.
    Rule of thumb: 1token ≈ 4 characters in English
    """
    return max(1, len(text) // 4)


def calculate_cost(tokens: int, cost_per_1k_tokens: float) -> float:
    """
    Calculate cost based on token usage
    """
    return (tokens / 1000) * cost_per_1k_tokens


def run_demo():
    prompt = "explain REST APIs in simple terms."

    # Example pricing (approx, for learning purpose)
    cost_per_1k_tokens = 0.002  # $0.002 per 1K tokens

    tokens = estimate_tokens(prompt)
    cost = calculate_cost(tokens, cost_per_1k_tokens)

    print("Prompt:", prompt)
    print("estimated Tokens:", tokens)
    print("estimated Cost ($):", round(cost, 6))


if __name__ == "__main__":
    run_demo()
