# Description: Implementation of Task 3: Counting Person Mentions.
# This script counts the mentions of each person in a given text.
# The PersonMentionCounter class preprocesses the input data if necessary and counts the mentions of each person.


import json
from collections import defaultdict
from typing import Dict, Any
from task_implementation.Task_1_Preprocessing import Preprocessing


class PersonMentionCounter:
    def __init__(
            self,
            question_num: int = 3,
            data_file: str = None,
            sentences_path: str = None,
            people_path: str = None,
            stopwords_path: str = None,
            preprocess: str = None,
    ):
        """
        Initialize the PersonMentionCounter class.

        :param data_file: Path to the preprocessed JSON file (if available).
        :param sentences_path: Path to the sentences CSV file.
        :param people_path: Path to the people CSV file.
        :param stopwords_path: Path to the stopwords CSV file.
        :param preprocess: Flag indicating if preprocessing is required.
        """
        self.question_num = question_num

        # If there is a preprocess flag, load data directly from the preprocessed file
        if preprocess == "--p":
            if not data_file:
                raise ValueError("A data file must be provided when preprocess=True.")
            with open(data_file, "r") as file:
                self.data = json.load(file)

        # If there is no preprocess flag, preprocess the raw input files
        else:
            if not sentences_path or not people_path or not stopwords_path:
                raise ValueError("Sentences, people, and stopwords paths must be provided when preprocess=None.")
            self.data = Preprocessing.preprocess_other_tasks(
                sentences_path=sentences_path,
                people_path=people_path,
                stopwords_path=stopwords_path
            )

    @property
    def count_mentions(self) -> Dict[str, int]:
        """
        Count the mentions of each person in the processed sentences.
        :return: A dictionary with person names as keys and their mention counts as values.
        """
        # If the data is preprocessed, load the processed sentences and people
        processed_sentences = (self.data.get("Question 1", {}).get("Processed Sentences", [])
                               if "Question 1" in self.data
                               else self.data.get("Processed Sentences", []))

        processed_people = (self.data.get("Question 1", {}).get("Processed Names", [])
                            if "Question 1" in self.data
                            else self.data.get("Processed Names", []))

        # If the data is not preprocessed, preprocess the sentences and people
        if not processed_sentences or not processed_people:
            raise ValueError("The provided data does not contain valid 'Processed Sentences' or 'Processed Names'.")

        mention_counts = defaultdict(int)

        # Create a dictionary of main names to their nicknames
        name_to_nicknames = {
            " ".join(person[0]).lower(): {  # Main name
                                             " ".join(name).lower() for name in person[1]
                                         } | {" ".join(person[0]).lower()}  # Add main name to nicknames set
            for person in processed_people
        }

        # Count mentions of each main name and its nicknames in sentences
        for sentence in processed_sentences:
            sentence_partials = [partial.lower() for partial in sentence]

            for main_name, all_names in name_to_nicknames.items():
                count_for_main_name = 0
                for name_variant in all_names:
                    name_partials = name_variant.split()

                    # Count full matches of name_variant in the sentence
                    for i in range(len(sentence_partials) - len(name_partials) + 1):
                        if sentence_partials[i:i + len(name_partials)] == name_partials:
                            count_for_main_name += 1

                    # Count partial matches (each word in the name_variant)
                    for partial in name_partials:
                        count_for_main_name += sentence_partials.count(partial)

                mention_counts[main_name] += count_for_main_name

        # Filter out names with zero mentions and sort alphabetically
        filtered_counts = {name: count for name, count in mention_counts.items() if count > 0}
        return dict(sorted(filtered_counts.items(), key=lambda x: x[0]))

    def generate_results(self) -> Dict[str, Any]:
        """
        Generate the final results for the task.
        :return: A dictionary containing the task results.
        """
        mention_counts = self.count_mentions
        return {
            f"Question {self.question_num}": {
                "Name Mentions": [[name, count] for name, count in mention_counts.items()]
            }
        }

