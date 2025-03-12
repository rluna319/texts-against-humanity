#!/usr/bin/env python3
"""
CAH to Text Messages Converter

This script converts Cards Against Humanity (CAH) cards into natural, realistic,
and humorous text-message formats suitable for an online texting-themed game.

It uses OpenAI's GPT-4o API to transform:
- Black cards (prompt cards with fill-in-the-blanks) into realistic initial text messages
- White cards (response cards) into humorous, standalone text message replies
"""

import json
import os
import time
import argparse
import logging
from typing import List, Dict, Any, Tuple
from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("cah_conversion.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_cah_cards(file_path: str) -> Tuple[List[Dict[str, Any]], List[str]]:
    """
    Load CAH cards from a JSON file.
    
    Args:
        file_path: Path to the JSON file containing CAH cards
        
    Returns:
        Tuple containing lists of black cards and white cards
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data['black'], data['white']
    except Exception as e:
        logger.error(f"Error loading CAH cards: {e}")
        raise

def batch_cards(cards: List[Any], batch_size: int) -> List[List[Any]]:
    """
    Split a list of cards into batches.
    
    Args:
        cards: List of cards to batch
        batch_size: Size of each batch
        
    Returns:
        List of batches, where each batch is a list of cards
    """
    return [cards[i:i + batch_size] for i in range(0, len(cards), batch_size)]

def convert_black_cards(black_cards: List[Dict[str, Any]], batch_size: int = 10) -> List[str]:
    """
    Convert black cards to natural text messages using OpenAI's API.
    
    Args:
        black_cards: List of black cards to convert
        batch_size: Number of cards to process in each API call
        
    Returns:
        List of converted text messages
    """
    logger.info(f"Converting {len(black_cards)} black cards to text messages...")
    converted_messages = []
    batches = batch_cards(black_cards, batch_size)
    
    for batch_idx, batch in enumerate(tqdm(batches, desc="Processing black card batches")):
        prompt_texts = []
        for card in batch:
            text = card['text']
            pick = card['pick']
            prompt_texts.append(f"Card: '{text}' (requires {pick} response{'s' if pick > 1 else ''})")
        
        try:
            # Prepare the system message with detailed instructions
            system_message = """
            Convert Cards Against Humanity black cards (prompt cards with blanks) into natural, realistic, 
            and humorous text messages that could be the first message in a conversation.
            
            Guidelines:
            1. Replace the blanks (_) with natural language that flows in the message
            2. Make it sound like a real text someone might send to a friend
            3. Keep the humor and adult themes but make it sound natural
            4. Don't use placeholders or mention Cards Against Humanity
            5. Each output should be a standalone text message without quotation marks
            6. Maintain the original humor and edginess of CAH
            7. For cards with multiple blanks, integrate them naturally into a single message
            
            Format your response as a simple list, one message per line, without numbering or bullet points.
            """
            
            # Make the API call
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": "Please convert these Cards Against Humanity black cards into natural text messages:\n\n" + "\n".join(prompt_texts)}
                ],
                temperature=0.7,
                max_tokens=2048
            )
            
            # Process the response
            result = response.choices[0].message.content.strip().split('\n')
            converted_messages.extend([msg.strip() for msg in result if msg.strip()])
            
            # Avoid rate limiting
            if batch_idx < len(batches) - 1:
                time.sleep(1)
                
        except Exception as e:
            logger.error(f"Error in batch {batch_idx}: {e}")
            # Continue with the next batch instead of failing completely
            time.sleep(5)  # Wait longer before retrying
    
    return converted_messages

def convert_white_cards(white_cards: List[str], batch_size: int = 20) -> List[str]:
    """
    Convert white cards to natural text message replies using OpenAI's API.
    
    Args:
        white_cards: List of white cards to convert
        batch_size: Number of cards to process in each API call
        
    Returns:
        List of converted text message replies
    """
    logger.info(f"Converting {len(white_cards)} white cards to text message replies...")
    converted_replies = []
    batches = batch_cards(white_cards, batch_size)
    
    for batch_idx, batch in enumerate(tqdm(batches, desc="Processing white card batches")):
        try:
            # Prepare the system message with detailed instructions
            system_message = """
            Convert Cards Against Humanity white cards (response cards) into natural, realistic, 
            and humorous text message replies.
            
            Guidelines:
            1. Make each card into a standalone text message reply
            2. Make it sound like a real text someone might send to a friend
            3. Keep the humor and adult themes but make it sound natural
            4. Don't use placeholders or mention Cards Against Humanity
            5. Each output should be a standalone text message without quotation marks
            6. Maintain the original humor and edginess of CAH
            7. Feel free to add emojis, text abbreviations, or other elements that make it feel like a real text
            
            Format your response as a simple list, one message per line, without numbering or bullet points.
            """
            
            # Make the API call
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": "Please convert these Cards Against Humanity white cards into natural text message replies:\n\n" + "\n".join(batch)}
                ],
                temperature=0.7,
                max_tokens=2048
            )
            
            # Process the response
            result = response.choices[0].message.content.strip().split('\n')
            converted_replies.extend([msg.strip() for msg in result if msg.strip()])
            
            # Avoid rate limiting
            if batch_idx < len(batches) - 1:
                time.sleep(1)
                
        except Exception as e:
            logger.error(f"Error in batch {batch_idx}: {e}")
            # Continue with the next batch instead of failing completely
            time.sleep(5)  # Wait longer before retrying
    
    return converted_replies

def save_to_file(messages: List[str], output_file: str):
    """
    Save converted messages to a text file.
    
    Args:
        messages: List of messages to save
        output_file: Path to the output file
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for message in messages:
                f.write(message + '\n')
        logger.info(f"Successfully saved {len(messages)} messages to {output_file}")
    except Exception as e:
        logger.error(f"Error saving to file {output_file}: {e}")

def estimate_cost(num_black_cards: int, num_white_cards: int, black_batch_size: int, white_batch_size: int):
    """
    Estimate the cost of API calls based on current OpenAI pricing.
    
    Args:
        num_black_cards: Number of black cards to process
        num_white_cards: Number of white cards to process
        black_batch_size: Batch size for black cards
        white_batch_size: Batch size for white cards
        
    Returns:
        Estimated cost in USD
    """
    # GPT-4o pricing (as of script creation)
    input_price_per_1k = 0.01  # $0.01 per 1K input tokens
    output_price_per_1k = 0.03  # $0.03 per 1K output tokens
    
    # Rough token estimates
    avg_input_tokens_per_black_card = 30
    avg_output_tokens_per_black_card = 50
    avg_input_tokens_per_white_card = 10
    avg_output_tokens_per_white_card = 30
    
    # System message tokens (rough estimate)
    system_message_tokens = 300
    
    # Calculate number of batches
    black_batches = (num_black_cards + black_batch_size - 1) // black_batch_size
    white_batches = (num_white_cards + white_batch_size - 1) // white_batch_size
    
    # Calculate total tokens
    total_input_tokens = (
        black_batches * system_message_tokens + 
        num_black_cards * avg_input_tokens_per_black_card +
        white_batches * system_message_tokens + 
        num_white_cards * avg_input_tokens_per_white_card
    )
    
    total_output_tokens = (
        num_black_cards * avg_output_tokens_per_black_card +
        num_white_cards * avg_output_tokens_per_white_card
    )
    
    # Calculate cost
    input_cost = (total_input_tokens / 1000) * input_price_per_1k
    output_cost = (total_output_tokens / 1000) * output_price_per_1k
    total_cost = input_cost + output_cost
    
    return total_cost

def main():
    """Main function to run the script."""
    parser = argparse.ArgumentParser(description='Convert CAH cards to text messages')
    parser.add_argument('--black-cards', type=str, default='cah-all-compact.json',
                        help='Path to the JSON file containing black cards')
    parser.add_argument('--white-cards', type=str, default='cah-all-compact.json',
                        help='Path to the JSON file containing white cards')
    parser.add_argument('--black-output', type=str, default='text_prompts.txt',
                        help='Path to the output file for converted black cards')
    parser.add_argument('--white-output', type=str, default='text_responses.txt',
                        help='Path to the output file for converted white cards')
    parser.add_argument('--black-batch-size', type=int, default=10,
                        help='Batch size for processing black cards')
    parser.add_argument('--white-batch-size', type=int, default=20,
                        help='Batch size for processing white cards')
    parser.add_argument('--black-limit', type=int, default=None,
                        help='Limit the number of black cards to process')
    parser.add_argument('--white-limit', type=int, default=None,
                        help='Limit the number of white cards to process')
    parser.add_argument('--estimate-only', action='store_true',
                        help='Only estimate the cost without making API calls')
    
    args = parser.parse_args()
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        logger.error("OPENAI_API_KEY environment variable is not set. Please set it in your .env file.")
        return
    
    # Load black and white cards
    black_cards, white_cards = load_cah_cards(args.black_cards)
    
    # Apply limits if specified
    if args.black_limit:
        black_cards = black_cards[:args.black_limit]
    if args.white_limit:
        white_cards = white_cards[:args.white_limit]
    
    # Estimate cost
    estimated_cost = estimate_cost(
        len(black_cards), len(white_cards), 
        args.black_batch_size, args.white_batch_size
    )
    
    logger.info(f"Estimated cost: ${estimated_cost:.2f}")
    
    if args.estimate_only:
        logger.info("Estimate-only mode. Exiting without making API calls.")
        return
    
    # Confirm with user
    confirmation = input(f"Estimated cost is ${estimated_cost:.2f}. Do you want to proceed? (y/n): ")
    if confirmation.lower() != 'y':
        logger.info("Operation cancelled by user.")
        return
    
    # Convert black cards
    converted_black = convert_black_cards(black_cards, args.black_batch_size)
    save_to_file(converted_black, args.black_output)
    
    # Convert white cards
    converted_white = convert_white_cards(white_cards, args.white_batch_size)
    save_to_file(converted_white, args.white_output)
    
    logger.info("Conversion completed successfully!")

if __name__ == "__main__":
    main() 