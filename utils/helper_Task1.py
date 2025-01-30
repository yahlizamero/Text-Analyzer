# Description: Helper functions for the first Task.
#   In order to maintain a clean software.
from typing import Set, List, Dict, Any
import json
from collections import defaultdict


# Used in Task 1
def clean_text(text: str, unwanted_words: Set[str]) -> str:
    """
    Clean a string by removing punctuation, unwanted words, and excessive whitespace.
    Args:
        text (str): The text to clean.
        unwanted_words (Set[str]): A set of words to remove from the text.
    Returns:
        str: The cleaned text.
    """
    import re
    text = re.sub(r'[^a-z0-9\s]', ' ', text.lower())  # Remove punctuation and convert to lowercase
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra whitespaces
    return ' '.join(word for word in text.split() if word not in unwanted_words)


def is_duplicate_or_overlap(name: str, other_names: List[str], seen_names: Set[str]) -> bool:
    """
    Check if a name or its nicknames already exist in the seen names.
    Args:
        name (str): The main name.
        other_names (List[str]): A list of nicknames.
        seen_names (Set[str]): A set of all previously seen names and nicknames.
    Returns:
        bool: True if there's a duplicate or overlap; False otherwise.
    """
    return name in seen_names or any(nickname in seen_names for nickname in other_names)


def split_name(name: str) -> List[str]:
    return name.split()
