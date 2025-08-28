# Description: Helper functions for Tasks 2-9.
# In order to maintain a clean software.

from typing import List, Dict, Any
from collections import defaultdict
import json
import os
import sys
from task_implementation.Task_1_Preprocessing import Preprocessing


# Used in Tasks: 2, 3, 4, 5, 6, 9
def preprocess_init(preprocess_path: str = None,
                    sentences_path: str = None,
                    people_path: str = None,
                    stopwords_path: str = None) -> dict[str, list[list[str]] | list[list[list[str]]]]:
    """
    Initialize data processing if preprocess flag is present or not.
    :param preprocess_path: Path to the preprocessed JSON file (optional).
    :param sentences_path: Path to the sentences CSV file.
    :param people_path: Path to the people CSV file.
    :param stopwords_path: Path to the stopwords CSV file.
    :return: a list containing processed sentences and/or processed names.
    """

    # Load from preprocessed JSON if provided
    if preprocess_path:
        # Check if the preprocessed file exists and is not empty
        if not os.path.exists(preprocess_path) or os.path.getsize(preprocess_path) == 0:
            print(f"Error: The preprocessed file at {preprocess_path} is missing or empty.")
            sys.exit(1)
        try:
            with open(preprocess_path, "r") as file:
                preprocess = json.load(file)
                return {
                    "Processed Sentences": preprocess.get("Question 1", {}).get("Processed Sentences", []),
                    "Processed Names": preprocess.get("Question 1", {}).get("Processed Names", [])
                }
        except Exception as e:
            print(f"Error loading preprocessed file: {e}")
            sys.exit(1)

    # Preprocess from raw data using Preprocessing class
    preprocessor = Preprocessing(sentences_path=sentences_path,
                                 people_path=people_path,
                                 stopwords_path=stopwords_path)

    results = {}
    if sentences_path:
        results["Processed Sentences"] = preprocessor.preprocess_sentences()
    if people_path:
        results["Processed Names"] = preprocessor.preprocess_people()

    return results  # A dictionary containing processed sentences and/or processed names.


# Used in Task 4, 5 and 9
def map_n_grams(sentences: List[List[str]], N: int or None) -> defaultdict[Any, set]:
    """
    Map n-grams (word sequences) to the sentences they appear in.
    :param N: Length of the n-gram (optional).
    :param sentences: A list of sentences  each sentence is a list.
    :return: A dictionary which the keys are n-grams and the values are the sentences they appear in.
    """

    # Create a dictionary mapping n-grams (word sequences) to the sentences they appear in, enabling O(1) lookup
    n_grams = defaultdict(set)  # Maps n-grams (keys) to the set of sentences (values)

    for sentence in sentences:
        sentence_text = " ".join(sentence)  # Combine the sentence tokens into a single string for easier processing
        words = sentence_text.split()

        if not N:
            # Generate all possible n-grams (1-word to full sentence)
            for k in range(len(words)):
                for i in range(k + 1, len(words) + 1):  # Generate n-grams of different lengths
                    ngram = " ".join(words[k:i])  # Create an n-gram from words[k] to words[i-1]
                    n_grams[ngram].add(tuple(sentence))  # Map n-gram to sentence (stored as a tuple)
        else:
            # Generate n-grams up to N from the sentence
            for k in range(1, N + 1):  # k is the length of the n-gram (1-word, 2-words, ... N-words)
                for i in range(len(words) - k + 1):  # Avoids out-of-bounds errors
                    ngram = " ".join(words[i:i + k])  # Convert tuple to a string for JSON compatibility
                    n_grams[ngram].add(tuple(sentence))  # Store the sentence that contains the k-seq

    return n_grams
