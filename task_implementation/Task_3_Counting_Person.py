# Description: This script counts the mentions of each person in the processed sentences.
# The PersonMentionCounter class preprocesses the input data and counts the mentions of each person.
# The results are saved to a JSON file.

import json
import os
from typing import List, Dict, Any
from utils.helper_Task2 import save_to_json,load_preprocessed_data, preprocess_data


class PersonMentionCounter:
    def __init__(
            self,
            data_file: str = None,
            sentences_path: str = None,
            people_path: str = None,
            stopwords_path: str = None,
            preprocess: bool = False
    ):
        """
        Initialize the PersonMentionCounter class.

        :param data_file: Path to the preprocessed JSON file (optional).
        :param sentences_path: Path to the sentences CSV file.
        :param people_path: Path to the people CSV file.
        :param stopwords_path: Path to the stopwords CSV file.
        :param preprocess: Flag indicating if preprocessing is required.
        """
        self.preprocess = preprocess

        if self.preprocess and (not sentences_path or not people_path or not stopwords_path):
            raise ValueError("Sentences, people, and stopwords paths must be provided if preprocessing is enabled.")

        self.data = (
            self.load_preprocessed_data(data_file)
            if data_file and not preprocess
            else preprocess_data(sentences_path, people_path, stopwords_path)
        )

    def count_person_mentions(self) -> Dict[str, int]:
        """
        Count mentions of each person in the processed sentences.

        :return: A dictionary where keys are names and values are counts of mentions.
        """
        mention_counts = {}
        sentences = self.data["Processed Sentences"]
        people = self.data["Processed Names"]

        for person in people:
            main_name = person[0]  # Main name
            alternate_names = person[1:]  # Alternate names

            # Build a set of all names for the person (main + alternate)
            all_names = set([main_name] + alternate_names)

            # Count mentions for all names in the sentences
            count = 0
            for sentence in sentences:
                for word in sentence:
                    if word in all_names:
                        count += 1

            if count > 0:
                mention_counts[main_name] = count

        return mention_counts

    def generate_results(self) -> None:
        """Generate the final results for person mentions."""
        mention_counts = self.count_person_mentions()
        sorted_mentions = sorted(mention_counts.items(), key=lambda x: x[0])  # Sort by name alphabetically

        results = {
            "Question 3": {
                "Name Mentions": [[name, count] for name, count in sorted_mentions]
            }
        }
        print(json.dumps(results, indent=4))


# Example usage
if __name__ == "__main__":
    data_file = "/path/to/preprocessed_data.json"
    sentences_file = "examples_new/Q1_examples/example_1/sentences_small_1.csv"
    people_file = "examples_new/Q1_examples/example_1/people_small_1.csv"
    stopwords_file = "data/REMOVEWORDS.csv"
    output_file = "examples_new/Q1_examples/example_1/generated_Q1_result.json"

    # Check if required files exist
    for file_path in [sentences_file, people_file, stopwords_file, output_file]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Required file not found: {file_path}")

    counter = PersonMentionCounter(
        data_file=None,
        sentences_path=sentences_file,
        people_path=people_file,
        stopwords_path=stopwords_file,
        preprocess=True
    )

    # Use the helper function to save the processed data
    save_to_json(output_path=output_file, process_function=counter.generate_results)
    print(f"JSON results saved to {output_file}")
