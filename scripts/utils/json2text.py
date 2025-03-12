import json

# Load JSON Against Humanity dataset
with open("cah-all-full.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Extract black (prompt) cards from all packs
black_cards = []
for pack in data:
    black_cards.extend(pack["black"])

# Format into training sentences
training_data = "\n".join([card["text"].replace("_", "...") for card in black_cards])

# Save to a text file
with open("dark_humor_prompts.txt", "w", encoding="utf-8") as f:
    f.write(training_data)

print("Dataset formatted and saved!")
