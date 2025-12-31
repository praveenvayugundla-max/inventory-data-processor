#Day 3: Basic OpenAI API usage + cost calculation

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4o-mini"
COST_PER_1K_TOKENS = 0.002  # USD


def calculate_cost(total_tokens: int) -> float:
    return (total_tokens / 1000) * COST_PER_1K_TOKENS


def run_demo():
    prompt = "Explain what REST API is in very simple words."

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    answer = response.choices[0].message.content
    usage = response.usage.total_tokens

    cost = calculate_cost(usage)

    print("Prompt:", prompt)
    print("-" * 40)
    print("LLM Response:")
    print(answer)
    print("-" * 40)
    print("Tokens used:", usage)
    print("Estimated cost (USD):", round(cost, 6))


if __name__ == "__main__":
    run_demo()
