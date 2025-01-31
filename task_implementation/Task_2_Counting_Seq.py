# Description: Implementation of Task 2: Counting Sequences.
# This file contains the implementation of counting sequences of words from a text input.
# The SequenceCounter class is responsible for counting the occurrence of sequences
# of up to length N in the processed sentences.

import json
import os
from collections import defaultdict
from typing import Dict, Any, List
from task_implementation.Task_1_Preprocessing import Preprocessing


class SequenceCounter:
    def __init__(
            self,
            question_num: int = 2,
            data_file: str = None,
            sentences_path: str = None,
            stopwords_path: str = None,
            preprocess: str = None,
            N: int = None
    ):
        """
        Initialize the PersonMentionCounter class.

        :param data_file: Path to the preprocessed JSON file (optional).
        :param sentences_path: Path to the sentences CSV file.
        :param stopwords_path: The path for a file with a list of common words to remove CSV file.
        :param preprocess: Path to JSON with preprocessed data
        :param N: Maximum size of the sequences to create.
        """
        self.question_num = question_num
        self.N = N if N is not None else 3
        self.preprocess = preprocess

        # If there is a preprocess flag, load data directly from the preprocessed file
        if self.preprocess:
            with open(self.preprocess, "r") as file:
                self.preprocess = json.load(file)

        # If there is no preprocess flag, preprocess the raw input files
        else:
            if not sentences_path or not stopwords_path:
                raise ValueError("Sentences, and stopwords paths must be provided when preprocess=False.")
            self.data = Preprocessing.preprocess_other_tasks(sentences_path, stopwords_path)

    @property
    def count_sequences(self) -> List[List[Any]]:
        """
        Count the occurrence of sequences of up to length of N in the processed sentences.
        :return: A list of lists where each inner list contains a sequence type (e.g., "1_seq") and its key-value pairs.
        """
        processed_sentences = (
            self.data.get("Question 1", {}).get("Processed Sentences", [])
            if "Question 1" in self.data
            else self.data.get("Processed Sentences", [])
        )

        if not processed_sentences:
            raise ValueError(
                "The provided data does not contain valid 'Processed Sentences'. Please check the input data.")

        sequence_counts = {f"{i}_seq": defaultdict(int) for i in range(1, self.N + 1)}

        for sentence in processed_sentences:
            for seq_size in range(1, self.N + 1):
                for i in range(len(sentence) - seq_size + 1):
                    seq = tuple(sentence[i:i + seq_size])
                    sequence_counts[f"{seq_size}_seq"][seq] += 1

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
