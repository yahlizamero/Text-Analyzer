# Description: Implementation of Task 3: Counting Person Mentions.
# This script counts the mentions of each person in a given text.
# The PersonMentionCounter class preprocesses the input data if necessary and counts the mentions of each person.


from collections import defaultdict
from typing import Dict, Any
from utils.helper import preprocess_init


class PersonMentionCounter:
    def __init__(
            self,
            question_num: int = 3,
            sentences_path: str = None,
            people_path: str = None,
            stopwords_path: str = None,
            preprocess_path: str = None,
    ):
        """
        Initialize the PersonMentionCounter class.
        :param question_num: The question number for the task.
        :param sentences_path: Path to the sentences CSV file.
        :param people_path: Path to the people CSV file.
        :param stopwords_path: Path to the stopwords CSV file.
        :param preprocess_path: Path to the preprocessed JSON file (if available).
        """
        # Initialize the class attributes
        self.question_num = question_num

        # Load the preprocessed data weather from a preprocessed file or preprocess it from raw data
        self.data = preprocess_init(preprocess_path, sentences_path, people_path, stopwords_path)

    @property
    def count_mentions(self) -> Dict[str, int]:
        """
        Count the mentions of each person in the processed sentences.
        :return: A dictionary with person names as keys and their mention counts as values.
        """

        mention_counts = defaultdict(int)

        # Create a dictionary of main names to their nicknames
        name_to_nicknames = {
            " ".join(person[0]).lower(): {  # Main name
                                             " ".join(name).lower() for name in person[1]
                                         } | {" ".join(person[0]).lower()}  # Add main name to nicknames set
            for person in self.data.get("Processed Names", [])
        }

        # Count mentions of each main name and its nicknames in sentences
        for sentence in self.data.get("Processed Sentences", []):
            sentence_partials = [partial.lower() for partial in sentence]

            for main_name, all_names in name_to_nicknames.items():  # all names include main name and nicknames

                # Count full matches and partial matches separately
                full_match_count = 0
                partial_match_count = 0

                for name_variant in all_names:
                    name_partials = name_variant.split()

                    # Count full matches of name_variant in the sentence
                    for i in range(len(sentence_partials) - len(name_partials) + 1):
                        if sentence_partials[i:i + len(name_partials)] == name_partials: # Full match
                            full_match_count += 1

                    # Count partial matches (each word in the name_variant)
                    for partial in name_partials:
                        partial_match_count += sentence_partials.count(partial)

                # Adjust count: total partial matches plus full matches minus overlaps
                count_for_main_name = partial_match_count + full_match_count - full_match_count

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
