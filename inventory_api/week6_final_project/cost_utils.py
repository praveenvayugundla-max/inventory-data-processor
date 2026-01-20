# approximate cost for gpt-4o-mini
INPUT_COST_PER_1K = 0.00015
OUTPUT_COST_PER_1K = 0.00060


def calculate_cost(prompt_tokens: int, completion_tokens: int) -> float:
    
    #Calculate approximate cost based on token usage.
    
    input_cost = (prompt_tokens / 1000) * INPUT_COST_PER_1K
    output_cost = (completion_tokens / 1000) * OUTPUT_COST_PER_1K
    return round(input_cost + output_cost, 6)
