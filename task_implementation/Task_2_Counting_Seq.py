# Description:
# This file contains the implementation of counting sequences of words from a text input.
# The class CountingSequences uses the input data and saves the results to a JSON file.
import json
from collections import defaultdict
from typing import Dict, Any, List
from task_implementation.Task_1_Preprocessing import Preprocessing


def load_data(data_file: str) -> Dict[str, Any]:
    """
    Load preprocessed data from a JSON file.

    :param data_file: Path to the preprocessed JSON file.
    :return: The loaded data as a dictionary.
    """
    try:
        with open(data_file, "r") as file:
            return json.load(file)
    except Exception as e:
        raise FileNotFoundError(f"Error loading data file: {e}")


class SequenceCounter:
    def __init__(
            self,
            question_num: int = 2,
            data_file: str = None,
            sentences_path: str = None,
            stopwords_path: str = None,
            preprocess: bool = None,
            N: int = None
    ):
        """
        Initialize the PersonMentionCounter class.

        :param data_file: Path to the preprocessed JSON file (optional).
        :param sentences_path: Path to the sentences CSV file.
        :param stopwords_path: The path for a file with a list of common words to remove CSV file.
        :param preprocess: Flag indicating if preprocessing is required.
        :param N: Maximum size of the sequences to create.
        """
        self.question_num = question_num
        self.N = N if N is not None else 3
        self.preprocess = preprocess

        # If preprocess is True, load data directly from the preprocessed file
        if preprocess:
            if not data_file:
                raise ValueError("A data file must be provided when preprocess=True.")
            self.data = load_data(data_file)

        # If preprocess is False, preprocess the raw input files
        else:
            if not sentences_path or not stopwords_path:
                raise ValueError("Sentences, people, and stopwords paths must be provided when preprocess=False.")
            self.data = Preprocessing.preprocess_other_tasks(sentences_path, stopwords_path)

    @property
    def count_sequences(self) -> Dict[str, List[list[str, int]]]:
        """
        Count the occurrence of sequences (1-grams, 2-grams, 3-grams) in the processed sentences.

        :return: A dictionary with sequence sizes as keys and their counts as values.
        """
        # Handle data structure differences between raw and preprocessed inputs
        processed_sentences = (
            self.data.get("Question 1", {}).get("Processed Sentences", [])
            if "Question 1" in self.data
            else self.data.get("Processed Sentences", [])
        )

        if not processed_sentences:
            raise ValueError(
                "The provided data does not contain valid 'Processed Sentences'. Please check the input data.")

        sequence_counts = {f"{i}-Seq Counts": defaultdict(int) for i in range(1, self.N + 1)}

        # Extract sentences and count occurrences of each sequence
        for sentence in processed_sentences:
            for seq_size in range(1, self.N + 1):
                for i in range(len(sentence) - seq_size + 1):
                    seq = tuple(sentence[i:i + seq_size])
                    sequence_counts[f"{seq_size}-Seq Counts"][seq] += 1

        # Convert defaultdict to regular dict and sort alphabetically
        sorted_counts = {
            k: sorted([(" ".join(key), value) for key, value in v.items()], key=lambda x: x[0])
            for k, v in sequence_counts.items()
        }

        return sorted_counts

    def generate_results(self) -> dict[str, dict[str, list[list[str, int]]]]:
        """
        Generate results for the counted sequences.

        :return: A dictionary containing the results.
        """
        sequence_counts = self.count_sequences
        return {
            f"Question {self.question_num}": sequence_counts
        }


if __name__ == "__main__":
    counter = SequenceCounter(
        question_num=2,
        data_file="examples_new/Q1_examples/example_1/generated_Q1_result.json",
        preprocess=True,
        N=3
    )

    # counter = SequenceCounter(
    #     question_num=2,
    #     sentences_path="examples_new/Q2_examples/example_1/sentences_small_1.csv",
    #     stopwords_path="Data/REMOVEWORDS.csv",
    #     preprocess=False,
    #     N=3
    # )

    print(counter.generate_results())
