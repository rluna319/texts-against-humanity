from datasets import load_dataset # type: ignore
from transformers import AutoTokenizer # type: ignore

model_name = "andrijdavid/MeanGirl"

# Load dataset from a CSV file
dataset = load_dataset("text", data_files="dark_humor_prompts.txt")
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Check sequence length
def check_sequence_lengths(dataset, tokenizer, num_samples):
    sum = 0
    for i in range(num_samples):
        text = dataset["train"][i]["text"]  # Adjust this field based on your dataset
        tokens = tokenizer(text, return_tensors="pt")["input_ids"]
        print(f"Sample {i + 1} ({len(tokens[0])} tokens): {dataset['train'][i]['text']}")
        sum += len(tokens[0])
    print(f"Average sequence length: {sum / num_samples}")

num_samples = 1000
check_sequence_lengths(dataset, tokenizer, num_samples)