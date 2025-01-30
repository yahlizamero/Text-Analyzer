# Description: Helper functions for Tasks 2-9.
#   In order to maintain a clean software.

from typing import List, Dict, Any
from collections import defaultdict
import json
from task_implementation.Task_1_Preprocessing import Preprocessing


# Used in Task 4 and 5
def map_n_grams(sentences: List[List[str]], N: int) -> Dict[str, List[str]]:
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
        words = sentence_text.split()  # Split into words to generate n-grams

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


# Used in Task 7

def preprocess_init(self,
                    data_file: str = None,
                    sentences_path: str = None,
                    people_path: str = None,
                    stopwords_path: str = None,
                    preprocess: str = None) -> dict[str, Any] or None:
    """
    :param data:
    :param self:
    :param data_file:
    :param sentences_path:
    :param people_path:
    :param stopwords_path:
    :param preprocess:
    :return: None
    """

    # If preprocess flag is set, load data directly from the preprocessed file
    if preprocess == "--p":
        if not data_file:
            raise ValueError("A data file must be provided when preprocess=True.")
        with open(data_file, "r") as file:
            self.data = json.load(file)

    # Otherwise, preprocess the raw input files
    elif preprocess is None:
        if not people_path:
            if not sentences_path or not stopwords_path:
                raise ValueError("Sentences and stopwords paths must be provided when preprocess=False.")
            self.data = Preprocessing.preprocess_other_tasks(
                sentences_path=sentences_path, stopwords_path=stopwords_path
            )
            return self.data
        if not sentences_path or not stopwords_path:
            raise ValueError("Sentences, people, and stopwords paths must be provided when preprocess=False.")
        self.data = Preprocessing.preprocess_other_tasks(
            sentences_path=sentences_path, stopwords_path=stopwords_path, people_path=people_path
        )
        return self.data
    else:
        raise ValueError("Invalid arguments provided for preprocessing.")


