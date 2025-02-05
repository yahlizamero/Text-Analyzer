# Description: Implementation of Task 2: Counting Sequences.
# This file contains the implementation of counting sequences of words from a text input.
# The SequenceCounter class is responsible for counting the occurrence of sequences
# of up to length N in the processed sentences.

from collections import defaultdict
import sys
from typing import Dict, Any
from utils.helper import preprocess_init


class SequenceCounter:
    def __init__(
            self,
            question_num: int = 2,
            sentences_path: str = None,
            stopwords_path: str = None,
            preprocess_path: str = None,
            N: int = None
    ):
        """
        Initialize the PersonMentionCounter class.

        :param sentences_path: Path to the sentences CSV file.
        :param stopwords_path: The path for a file with a list of common words to remove CSV file.
        :param preprocess_path: Path to the preprocessed JSON file (optional).
        :param N: Maximum size of the sequences to create.
        """
        # Initialize the class attributes
        self.question_num = question_num
        self.N = N
        if N is None or N < 1:
            print("Error: N value must be provided and greater than 0.")
            sys.exit(1)

        self.preprocess_path = preprocess_path

        # Load the preprocessed data weather from a preprocessed file or preprocess it from raw data
        self.data = preprocess_init(preprocess_path, sentences_path, None, stopwords_path)

    @property
    def count_sequences(self) -> list[list[str | list[list[str | int]]]]:
        """
        Count the occurrence of sequences of up to length of N in the processed sentences.
        :return: A list of lists where each inner list contains a sequence type (e.g., "1_seq") and its key-value pairs.
        """

        # Initialize a dictionary to store the counts of sequences of different lengths
        sequence_counts = {f"{i}_seq": defaultdict(int) for i in range(1, self.N + 1)}

        # Count the sequences of different lengths in the processed sentences
        for sentence in self.data.get("Processed Sentences", []):
            for seq_size in range(1, self.N + 1):
                for i in range(len(sentence) - seq_size + 1):  # Loop over the sentence
                    seq = tuple(sentence[i:i + seq_size])  # Create a sequence of length seq_size
                    sequence_counts[f"{seq_size}_seq"][seq] += 1  # Increment the count of the sequence

        # Convert default dict to a sorted list of lists
        sorted_counts = [
            [seq_type, sorted([[" ".join(key), value] for key, value in counts.items()], key=lambda x: x[0])]
            for seq_type, counts in sequence_counts.items()
        ]

        return sorted_counts

    def generate_results(self) -> Dict[str, Any]:
        """
        Generate results for the counted sequences in the desired JSON format.
        :return: A dictionary containing the results.
        """
        sequence_counts = self.count_sequences
        return {
            f"Question {self.question_num}": {
                f"{self.N}-Seq Counts": sequence_counts
            }
        }
