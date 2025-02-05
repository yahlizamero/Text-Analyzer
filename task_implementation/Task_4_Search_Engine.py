# Description: Implementation of Task 4: Search Engine.
# This file contains the implementation of Task 4: Search Engine.
# The SearchEngine class is responsible for building a search index
# mapping each K-seq to the sentences in which it appears.
# The implementation is using a dictionary as the primary data structure
# to enable O(1) search complexity for the K-seqs.

import json
import sys
from typing import Dict, Any, List
from collections import defaultdict
from utils.helper import map_n_grams, preprocess_init


class SearchEngine:
    def __init__(
            self,
            question_num: int = 4,
            sentences_path: str = None,
            stopwords_path: str = None,
            preprocess_path: str = None,
            k_seq_path: str = None

    ):
        """
        Initialize the SearchEngine class.

        :param question_num: The task reference number.
        :param sentences_path: Path to the sentences CSV file.
        :param stopwords_path: Path to the stopwords file.
        :param preprocess_path: Path to the preprocessed JSON file (optional).
        :param k_seq_path: Path to the K-seq JSON file.

        """
        self.question_num = question_num
        self.k_seq_path = k_seq_path
        if k_seq_path is None:
            print("K-seq query path must be provided for Task 4.")
            sys.exit(1)

        # Load the K-seq list from the JSON file
        try:
            with open(k_seq_path, "r") as file:
                self.k_seq_list = json.load(file)
                if not isinstance(self.k_seq_list, dict):
                    print("Error: K-seq list must be a dictionary.")
                    sys.exit(1)
        except json.JSONDecodeError:
            print("Error: Failed to decode query keys JSON. Please provide it with the correct format.")
            sys.exit(1)
        except FileNotFoundError:
            print("Error: K-seq query file not found.")
            sys.exit(1)

        # Load the preprocessed data weather from a preprocessed file or preprocess it from raw data
        self.data = preprocess_init(preprocess_path, sentences_path, None, stopwords_path)

    def build_search_index(self) -> Dict[str, List[List[str]]] or List:
        """
        Build a search index mapping each K-seq to the sentences in which it appears.
        Uses a dictionary for O(1) lookup.
        :returns: A dictionary mapping K-seqs to the sentences in which they appear.
        """

        # Create a dictionary mapping sentences to their text for O(1) lookup
        sentence_index = map_n_grams(self.data.get("Processed Sentences", []), N=None)

        # Match K-seqs in O(1) Lookup
        search_index = defaultdict(list)
        added_kseqs = set()  # Keep track of added K-seqs to avoid duplicates
        if not self.k_seq_list.get("keys"):
            return {}

        else:
            for k_seq_value in self.k_seq_list.get("keys", []):
                if isinstance(k_seq_value, list) and k_seq_value:  # Ensure non-empty list
                    k_seq_text = " ".join(k_seq_value)  # Convert to text
                    if k_seq_text in sentence_index and k_seq_text not in added_kseqs:  # O(1) lookup and duplicate
                        # check
                        search_index[k_seq_text].extend([list(seq) for seq in sentence_index[k_seq_text]])
                        added_kseqs.add(k_seq_text)
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

        # Convert search index to the required format if it is a dictionary
        if isinstance(search_index, dict):
            k_seq_matches = [[k_seq, search_index[k_seq]] for k_seq in sorted(search_index.keys())]

        # We have an empty list because there was no info in the k_seq_query
        else:
            k_seq_matches = []

        return {
            f"Question {self.question_num}": {
                "K-Seq Matches": k_seq_matches
            }
        }

