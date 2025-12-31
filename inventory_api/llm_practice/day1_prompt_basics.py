
# Week 6 - Day 1: LLM Basics & Prompt Engineering

# Concepts covered:
# 1. What is an LLM?
# 2. Zero-shot prompting
# 3. Few-shot prompting
# 4. Tokens basic understanding

# Note:
# This file is for learning and experimentation.
# No API calls yet.



def zero_shot_prompt():
    """
    Zero-shot prompting:
    Asking the model to do a task without giving examples.
    """
    prompt = "Explain what an API is in simple words."
    print("ZERO-SHOT PROMPT:")
    print(prompt)
    print("-" * 50)


def few_shot_prompt():
    """
    Few-shot prompting:
    Giving examples before asking the task.
    """
    prompt = """
Example:
Input: What is Python?
Output: Python is a programming language.

Example:
Input: What is Flask?
Output: Flask is a Python web framework.

Now answer:
Input: What is Django?
Output:
"""
    print("FEW-SHOT PROMPT:")
    print(prompt)
    print("-" * 50)



if __name__ == "__main__":
    zero_shot_prompt()
    few_shot_prompt()
