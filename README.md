# CAH Dataset Generator

A tool to convert Cards Against Humanity cards into a natural text message conversation dataset using GPT-4. This dataset can be used to train AI models for generating humorous text message conversations in the style of Cards Against Humanity.

## Project Structure

```
cah-dataset-generator/
│
├── raw/                     # Original CAH JSON files
│   ├── cah-all-compact.json
│   ├── cah-all-full.json
│   └── dark_humor_prompts.txt
│
├── processed/              # Generated datasets
│   ├── text_prompts.txt
│   ├── text_responses.txt
│   └── training_examples.json
│
└── scripts/               # Processing scripts
    ├── conversion/       # CAH to text conversion
    ├── preprocessing/    # Data preprocessing
    └── utils/           # Utility scripts

```

## Features

- Convert CAH black cards into natural conversation starters
- Transform CAH white cards into witty text message replies
- Maintain the humor and edge of the original game
- Estimate token usage and API costs
- Generate training data for AI models

## Requirements

- Python 3.6+
- OpenAI API key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/cah-dataset-generator.git
   cd cah-dataset-generator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment:
   ```bash
   cp .env.example .env
   # Add your OpenAI API key to .env
   ```

## Usage

### Converting Cards to Text Messages

```bash
python scripts/conversion/cah_to_text_messages.py
```

### Estimating Costs

```bash
python scripts/utils/openai_price_estimate.py
```

### Checking Token Count

```bash
python scripts/utils/check_token_count.py
```

## Output Format

The generator produces three main files:

1. `text_prompts.txt`: Conversation starters derived from black cards
2. `text_responses.txt`: Witty replies derived from white cards
3. `training_examples.json`: Formatted training data for AI models

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Cards Against Humanity](https://cardsagainsthumanity.com/) for the original card game
- [JSON Against Humanity](https://github.com/crhallberg/json-against-humanity) for the card dataset
- OpenAI for the GPT-4 API 