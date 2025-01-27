import json
import os
from typing import List, Dict, Any
from utils.helper_functions import load_file, save_to_json, print_results
from task_implementation.Task_1_Preprocessing import preprocess_sentences


class SearchEngine:
    def __init__(
            self,
            kseq_path: str,
            sentences_path: str = None,
            remove_path: str = None,
            preprocessed_data: Dict[str, Any] = None,
            preprocess: bool = False
    ):
        """
        Initialize the SearchEngine class.

        :param kseq_path: Path to the JSON file containing K-sequences.
        :param sentences_path: Path to the sentences CSV file.
        :param remove_path: Path to the stopwords CSV file.
        :param preprocessed_data: Preprocessed data as a dictionary (optional).
        :param preprocess: Flag to indicate whether preprocessing is required.
        """
        self.kseq_path = kseq_path

        if preprocess and (not sentences_path or not remove_path):
            raise ValueError("Sentences and stopwords paths must be provided if preprocessing is enabled.")

        self.sentences = (
            self.load_preprocessed_sentences(preprocessed_data)
            if preprocessed_data
            else self.preprocess_sentences(sentences_path, remove_path)
        )
        self.kseqs = self.load_kseqs()


    def load_preprocessed_sentences(self, preprocessed_data: Dict[str, Any]) -> List[List[str]]:
        """Load preprocessed sentences from provided data."""
        return preprocessed_data["Processed Sentences"]

    def preprocess_sentences(self, sentences_path: str, remove_path: str) -> List[List[str]]:
        """Preprocess the sentences from the CSV file."""
        return preprocess_sentences(sentences_path, remove_path)

    def load_kseqs(self) -> List[str]:
        """Load K-sequences from the provided JSON file."""
        with open(self.kseq_path, "r") as file:
            return json.load(file)["keys"]

    def preprocess_sentences_to_dict(self) -> Dict[str, List[List[str]]]:
        """
        Preprocess the sentences into a dictionary for O(1) K-seq lookups.
        :return: A dictionary where keys are K-sequences and values are lists of sentences containing them.
        """
        kseq_dict = {}

        for sentence in self.sentences:
            sentence_str = " ".join(sentence)
            words = sentence

            # Extract all possible K-sequences for this sentence
            for k in range(1, len(words) + 1):  # For 1-seq to N-seq
                for i in range(len(words) - k + 1):
                    kseq = " ".join(words[i:i + k])
                    if kseq not in kseq_dict:
                        kseq_dict[kseq] = []
                    kseq_dict[kseq].append(sentence_str)

        return kseq_dict

    def find_kseq_matches(self) -> Dict[str, List[List[str]]]:
        """
        Find sentences matching each K-sequence using a dictionary for O(1) lookups.
        :return: A dictionary where keys are K-sequences and values are lists of sentences containing those K-sequences.
        """
        kseq_matches = {}

        for kseq in self.kseqs:
            if kseq in self.kseq_dict:
                kseq_matches[kseq] = sorted(self.kseq_dict[kseq])  # Sort the matching sentences

        return kseq_matches

    def generate_results(self) -> Dict[str, Any]:
        """Generate the final results for K-sequence matches."""
        kseq_matches = self.find_kseq_matches()
        sorted_kseq_matches = sorted(kseq_matches.items(), key=lambda x: x[0])

        result = {
            "Question 4": {
                "K-Seq Matches": [
                    [kseq, matches] for kseq, matches in sorted_kseq_matches
                ]
            }
        }
        print_results(result)


# Example usage
if __name__ == "__main__":
    kseq_file = "examples_new/Q4_examples/example_1/kseq_query_keys_1.json"
    sentences_file = "examples_new/Q4_examples/example_1/sentences_small_1.csv"
    stopwords_file = "data/REMOVEWORDS.csv"
    output_file = "examples_new/Q4_examples/example_1/generated_Q4_result.json"

    # Check if required files exist
    for file_path in [kseq_file, sentences_file, stopwords_file, output_file]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Required file not found: {file_path}")

    search_engine = SearchEngine(
        kseq_path=kseq_file,
        sentences_path=sentences_file,
        remove_path=stopwords_file,
        preprocess=True
    )

    # Use the helper function to save the processed data
    save_to_json(output_path=output_file, process_function=search_engine.generate_results)
    print(f"JSON results saved to {output_file}")
