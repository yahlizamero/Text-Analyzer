# Description: Implementation of Task 5 - Person Contexts and K-Sequences.
# This script finds the contexts in which people are mentioned and extracts associated k-sequences.
# The PersonContexts class preprocesses the input preprocess if necessary and generates the final results for Task 5.

import json
from typing import Dict, Any, List
from collections import defaultdict
from task_implementation.Task_1_Preprocessing import Preprocessing
from utils.helper import map_n_grams, preprocess_init


class PersonContexts:
    def __init__(
            self,
            question_num: int,
            sentences_path: str = None,
            people_path: str = None,
            stopwords_path: str = None,
            preprocess: str = None,
            N: int = None
    ):
        """
        Initialize the PersonContexts class.

        :param question_num: The task reference number.
        :param sentences_path: Path to the sentences CSV file.
        :param people_path: Path to the people CSV file.
        :param stopwords_path: Path to the stopwords file.
        :param preprocess: Path to the preprocessed JSON file (optional).
        :param N: Maximum size of the k-seqs to create.
        """
        self.question_num = question_num
        self.sentences_path = sentences_path
        self.people_path = people_path
        self.stopwords_path = stopwords_path
        self.preprocess = preprocess
        self.N = N

        # If preprocess flag is set, load preprocess directly from the preprocessed file
        if preprocess:
            with open(preprocess, "r") as file:
                self.preprocess = json.load(file)

        # Otherwise, preprocess the raw input files
        elif preprocess is None:
            if not sentences_path or not stopwords_path or not people_path:
                raise ValueError("Sentences, people, and stopwords paths must be provided when preprocess=False.")
            self.preprocess = Preprocessing.preprocess_other_tasks(
                sentences_path=sentences_path, stopwords_path=stopwords_path, people_path=people_path
            )
        else:
            raise ValueError("Invalid arguments provided for preprocessing.")

    def contexts_and_k_seqs(self) -> list[str, list[str]]:
        """
        Find the contexts in which people are mentioned and extract associated k-seqs.

        :return: A dictionary where keys are person names and values are lists of k-seqs.
        """
        processed_sentences = (
            self.preprocess.get("Question 1", {}).get("Processed Sentences", [])
            if "Question 1" in self.preprocess
            else self.preprocess.get("Processed Sentences", [])
        )

        processed_people = (
            self.preprocess.get("Question 1", {}).get("Processed Names", [])
            if "Question 1" in self.preprocess
            else self.preprocess.get("Processed Names", [])
        )

        if not processed_sentences or not processed_people:
            raise ValueError("The provided preprocess does not contain valid 'Processed Sentences' or 'Processed "
                             "Names'.")

        # Generate k_seqs
        n_grams_dict = map_n_grams(processed_sentences, self.N)

        # Step 1: Construct name-to-main-name mapping with aliases
        name_to_main_name = {}
        for person in processed_people:
            main_name = " ".join(person[0])
            aliases = {" ".join(alias) for alias in person[1]}

            # Add partial name matches (e.g., "Harry Potter" → "Harry", "Potter")
            partial_names = set()
            for full_name in [main_name]:
                words = full_name.split()
                partial_names.update(words)  # Add individual words as aliases

            all_names = (main_name,) + tuple(aliases) + tuple(partial_names)
            name_to_main_name[main_name] = all_names

        # Step 2: Reverse mapping of k_seqs to names
        name_to_k_seqs = defaultdict(set)

        for sentence_tokens in processed_sentences:
            sentence = " ".join(sentence_tokens)

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

        # Convert k_seqs to a list of lists for JSON compatibility
        # Convert results and sort sentences alphabetically

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

