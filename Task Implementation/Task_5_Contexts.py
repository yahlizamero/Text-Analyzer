# Description: Implementation of Task 5 - Person Contexts and K-Sequences.
# This script finds the contexts in which people are mentioned and extracts associated k-sequences.
# The PersonContexts class preprocesses the input preprocess if necessary and generates the final results for Task 5.

from typing import Dict, Any
import sys
from collections import defaultdict
from Utilities.helper import map_n_grams, preprocess_init


class PersonContexts:
    def __init__(
            self,
            question_num: int = 5,
            sentences_path: str = None,
            people_path: str = None,
            stopwords_path: str = None,
            preprocess_path: str = None,
            N: int = None
    ):
        """
        Initialize the PersonContexts class.

        :param question_num: The task reference number.
        :param sentences_path: Path to the sentences CSV file.
        :param people_path: Path to the people CSV file.
        :param stopwords_path: Path to the stopwords file.
        :param preprocess_path: Path to the preprocessed JSON file (optional).
        :param N: Maximum size of the k-seqs to create.
        """
        self.question_num = question_num
        self.sentences_path = sentences_path
        self.people_path = people_path
        self.stopwords_path = stopwords_path
        self.preprocess_path = preprocess_path
        self.N = N
        if self.N is None or self.N < 0:
            print("Error: Make sure you provided a non negative int for --maxk.")
            sys.exit(1)

        # Load the preprocessed data weather from a preprocessed file or preprocess it from raw data
        self.data = preprocess_init(preprocess_path, sentences_path, people_path, stopwords_path)

    def contexts_and_k_seqs(self) -> list[list[list[Any] | Any]]:
        """
        Find the contexts in which people are mentioned and extract associated k-seqs.
        :return: A dictionary where keys are person names and values are lists of k-seqs.
        """

        # Extract processed data
        processed_sentences = self.data.get("Processed Sentences", [])
        processed_people = self.data.get("Processed Names", [])

        # If N is 0, return names with empty k-seq lists
        if self.N == 0:
            return [[" ".join(person[0]), []] for person in processed_people]

        # Generate k_seqs
        n_grams_dict = map_n_grams(processed_sentences, self.N)

        # Construct name-to-main-name mapping with aliases
        name_to_main_name = {}  # {main_name: (main_name, alias1, alias2, ...)}
        for person in processed_people:
            main_name = " ".join(person[0])  # Main name is the full name
            aliases = {" ".join(alias) for alias in person[1]}  # Convert aliases to strings

            # Add partial name matches (e.g., "Harry Potter" → "Harry", "Potter")
            partial_names = set()
            for full_name in [main_name]:
                words = full_name.split()
                partial_names.update(words)  # Add individual words as aliases

            all_names = (main_name,) + tuple(aliases) + tuple(partial_names)  # Include all names
            name_to_main_name[main_name] = all_names

        # Reverse mapping of k_seqs to names
        name_to_k_seqs = defaultdict(set)

        for sentence_tokens in processed_sentences:
            sentence = " ".join(sentence_tokens)  # Convert tokens to a sentence

            # Get k-seqs (actual n-grams) for this sentence
            k_seqs = set()
            for key, val in n_grams_dict.items():
                if tuple(sentence_tokens) in val:
                    k_seqs.add(key)  # Store the n-gram (k_seq) instead of full sentences

            # Check if any name (or its alias/partial name) appears in the sentence
            for main_name, aliases in name_to_main_name.items():
                for name in aliases:
                    if name in sentence:
                        name_to_k_seqs[main_name].update(list(k_seqs))

        # Convert k_seqs to a list of lists for JSON compatibility and sort alphabetically
        return [
            [name, sorted([k_seq.split() for k_seq in sorted(k_seqs)])]  # Ensure k-seqs are lists of words
            for name, k_seqs in sorted(name_to_k_seqs.items())  # Sort names alphabetically
        ]

    def generate_results(self) -> Dict[str, Any]:
        """
        Generate the final results for the task.

        :return: A dictionary containing the task results.
        """
        person_contexts_and_kseqs = self.contexts_and_k_seqs()

        return {
            f"Question {self.question_num}": {
                "Person Contexts and K-Seqs": person_contexts_and_kseqs
            }
        }
