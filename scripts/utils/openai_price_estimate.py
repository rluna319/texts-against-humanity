import openai
import tiktoken  # OpenAI's tokenizer library
import json

# Load OpenAI's tokenizer for GPT-4o Mini
tokenizer = tiktoken.get_encoding("cl100k_base")  # Same tokenizer used for GPT-4o Mini

# Pricing per 1,000 tokens (GPT-4o Mini)
INPUT_COST_PER_1K = 0.00015  # $0.15 per 1M tokens → $0.00015 per 1K
OUTPUT_COST_PER_1K = 0.0006  # $0.60 per 1M tokens → $0.0006 per 1K

# Pricing per 1,000,000 tokens (GPT-4o)
INPUT_COST_PER_1M = 3.75  # $3.75 per 1M tokens
OUTPUT_COST_PER_1M = 15.00  # $15.00 per 1M tokens


# Load dataset (Adjust file name if needed)
with open("cah-all-full.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Extract black (prompts) and white (responses) cards from all sets
all_prompts = []
all_responses = []

for pack in data:
    if "black" in pack:
        all_prompts.extend([card["text"] for card in pack["black"]])
    if "white" in pack:
        all_responses.extend([card["text"] for card in pack["white"]])

# Function to count tokens in a given text
def count_tokens(text):
    return len(tokenizer.encode(text))

# Count total tokens
total_prompt_tokens = sum(count_tokens(prompt) for prompt in all_prompts)
total_response_tokens = sum(count_tokens(response) for response in all_responses)

# Estimate output tokens (assuming responses expand by ~20%)
estimated_output_tokens = total_response_tokens * 1.2  # Adjustable factor

# Compute costs
input_cost = (total_prompt_tokens + total_response_tokens) / 1000000 * INPUT_COST_PER_1M
output_cost = estimated_output_tokens / 1000000 * OUTPUT_COST_PER_1M
total_cost = input_cost + output_cost

# Print results
print(f"Total Black Cards (Prompts): {len(all_prompts)}")
print(f"Total White Cards (Responses): {len(all_responses)}")
print(f"Total Prompt Tokens: {total_prompt_tokens}")
print(f"Total Response Tokens: {total_response_tokens}")
print(f"Estimated Output Tokens (After GPT-4o Processing): {int(estimated_output_tokens)}")
print(f"Estimated Cost for Input Processing: ${input_cost:.4f}")
print(f"Estimated Cost for Output Processing: ${output_cost:.4f}")
print(f"Total Estimated Cost: ${total_cost:.4f}")
