# Description:
# This file contains the implementation of Task 4: Search Engine.
# The SearchEngine class is responsible for building a search index
# mapping each K-seq to the sentences in which it appears.
# The implementation is using a dictionary as the primary data structure
# to enable O(1) search complexity for the K-seqs.

import json
from typing import Dict, Any, List
from collections import defaultdict
from task_implementation.Task_1_Preprocessing import Preprocessing
from utils.helper import map_n_grams


class SearchEngine:
    def __init__(
            self,
            question_num: int,
            data_file: str = None,
            sentences_path: str = None,
            stopwords_path: str = None,
            preprocess: str = None,
            k_seq_path: str = None

    ):
        """
        Initialize the SearchEngine class.

        :param question_num: The task reference number.
        :param data_file: Path to the preprocessed JSON file (optional).
        :param sentences_path: Path to the sentences CSV file.
        :param stopwords_path: Path to the stopwords file.
        :param preprocess: Flag indicating if preprocessing is required.
        :param k_seq_path: Path to the K-seq JSON file.

        """
        self.question_num = question_num
        self.k_seq_path = k_seq_path

        # Load the K-seq list from the JSON file
        with open(k_seq_path, "r") as file:
            self.k_seq_list = json.load(file)

        # If there is a preprocess flag, load data directly from the preprocessed file
        if preprocess == "--p":
            if not data_file:
                raise ValueError("A data file must be provided when preprocess=True.")
            with open(data_file, "r") as file:
                self.data = json.load(file)

        # If there is no preprocess flag, preprocess the raw input files
        else:
            if not sentences_path or not stopwords_path:
                raise ValueError("Sentences, people, and stopwords paths must be provided when preprocess=False.")
            self.data = Preprocessing.preprocess_other_tasks(sentences_path, stopwords_path)

    def build_search_index(self) -> Dict[str, List[List[str]]]:
        """
        Build a search index mapping each K-seq to the sentences in which it appears.
        Uses a hash map for O(1) lookup.
        """
        processed_sentences = (
            self.data.get("Question 1", {}).get("Processed Sentences", [])
            if "Question 1" in self.data
            else self.data.get("Processed Sentences", [])
        )

        if not processed_sentences:
            raise ValueError("The provided data does not contain valid 'Processed Sentences'.")

        # Create a dictionary mapping sentences to their text for O(1) lookup
        sentence_index = map_n_grams(processed_sentences, N=None)

        # Match K-seqs in O(1) Lookup
        search_index = defaultdict(list)
        for k_seq_key, k_seq_value in self.k_seq_list.items():
            if isinstance(k_seq_value, list) and isinstance(k_seq_value[0], list):  # Nested lists
                for inner_seq in k_seq_value:
                    k_seq_text = " ".join(inner_seq)
                    if k_seq_text in sentence_index:  # O(1) lookup
                        search_index[k_seq_text].extend(sentence_index[k_seq_text])
            else:
                k_seq_text = " ".join(k_seq_value)
                if k_seq_text in sentence_index:  # O(1) lookup
                    search_index[k_seq_text].extend(sentence_index[k_seq_text])

        # Convert results and sort sentences alphabetically
        for k_seq_text in search_index:
            search_index[k_seq_text] = sorted(search_index[k_seq_text], key=lambda x: " ".join(x))

        return search_index

    def generate_results(self) -> Dict[str, Any]:
        """
        Generate the final results for the task.
        :return: A dictionary containing the task results.
        """
        search_index = self.build_search_index()

        # Convert search index to the required format
        k_seq_matches = [[k_seq, search_index[k_seq]] for k_seq in sorted(search_index.keys())]

        return {
            f"Question {self.question_num}": {
                "K-Seq Matches": k_seq_matches
            }
        }


if __name__ == "__main__":
    # Example usage
    search_engine = SearchEngine(
        question_num=4,
        k_seq_path="examples 27.1/Q4_examples/example_4/kseq_query_keys_4.json",
        # data_file="examples 27.1/Q1_examples/example_1/Q1_result1.json",
        sentences_path="examples 27.1/Q4_examples/example_4/sentences_small_4.csv",
        stopwords_path="Data 27.1/REMOVEWORDS.csv",
        # preprocess="--p"
    )

    # Generate results
    results = search_engine.generate_results()

    # Print results
    print(json.dumps(results, indent=4))

    # Save results to a file
    output_file = "examples 27.1/Q4_examples/example_4/Gen_result_Q4_4.json"
    with open(output_file, "w") as file:
        json.dump(results, file, indent=4)
    print(f"JSON results saved to {output_file}")
