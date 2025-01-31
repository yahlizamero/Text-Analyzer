
# Description: This script preprocesses the input data for Task 1: Preprocessing.
# This file contains the implementation of the preprocessing task for the text analyzer project.
# Includes functionality for cleaning sentences and processing names.

import json
import csv
import os
from typing import *
from utils.helper_Task1 import clean_text, is_duplicate_or_overlap, split_name


def load_stopwords_file(stopwords_path: str) -> Set[str]:
    """
    Load stopwords file from a file into a set.
    Args:
        stopwords_path (str): Path to the stopwords file.
    Returns:
        Set[str]: A set of stopwords.
    """
    try:
        with open(stopwords_path, 'r') as file:
            return set(line.strip().lower() for line in file)
    except Exception as e:
        raise FileNotFoundError(f"Error loading data file: {e}")


class Preprocessing:
    def __init__(self, question_num: int, sentences_path: str, people_path: str, stopwords_path: str) -> None:
        self.question_num = question_num
        self.sentences_path = sentences_path
        self.people_path = people_path
        self.stopwords = load_stopwords_file(stopwords_path)

    def preprocess_sentences(self, stopwords_path) -> List[List[str]]:
        processed_sentences = []
        try:
            with open(self.sentences_path, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    sentence = clean_text(row['sentence'], self.stopwords)
                    if sentence:  # Skip empty sentences
                        processed_sentences.append(sentence.split())
            return processed_sentences
        except Exception as e:
            raise FileNotFoundError(f"Error loading sentence file: {e}")

    def preprocess_people(self) -> List[List[List[Any]]]:
        processed_people = []
        seen_names = set()

        try:
            with open(self.people_path, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    main_name = clean_text(row['Name'], self.stopwords)
                    if not main_name:  # Skip empty names
                        continue

                    raw_other_names = row['Other Names'].strip().split(',') if row['Other Names'].strip() else []
                    raw_other_names = [name.strip() for name in raw_other_names]
                    other_names = [clean_text(name, self.stopwords) for name in raw_other_names]
                    other_names = [name for name in other_names if name]

                    main_name_split = split_name(main_name)
                    other_names_split = [split_name(name) if " " in name else [name] for name in other_names]

                    if is_duplicate_or_overlap(main_name, other_names, seen_names):
                        continue

                    seen_names.add(main_name)
                    seen_names.update(other_names)

                    # Add cleaned data as lists, ensure empty nickname lists if none exist
                    processed_people.append([main_name_split, other_names_split if other_names_split else []])
            return processed_people
        except Exception as e:
            raise FileNotFoundError(f"Error loading people file: {e}")

    def generate_results(self) -> Dict[str, Any]:
        """
        Generate the final results for the task.
        :return: A dictionary containing the task results.
        """
        return {
            f"Question {self.question_num}": {
                "Processed Sentences": self.preprocess_sentences(self.stopwords),
                "Processed Names": self.preprocess_people()
            }
        }

    def print_results(self) -> None:
        """Print the results in JSON format."""
        results = self.generate_results()
        print(json.dumps(results, indent=4))

    def save_to_json(self, output_path: str) -> None:  # Extra function not necessary for the task, only pre-checks
        processed_data = self.generate_results()
        with open(output_path, "w") as file:
            json.dump(processed_data, file, indent=4)

    # Helper function for preprocessing for other tasks

    def preprocess_other_tasks(
            sentences_path: str = None,
            stopwords_path: str = None,
            people_path: str = None)\
            -> Dict[str, Any]:
        """
        Preprocess data from sentences, people, and stopwords files.
        Useful for other tasks that require preprocessing.

        :param sentences_path: Path to the sentences CSV file.
        :param people_path: Path to the people CSV file.
        :param stopwords_path: Path to the stopwords CSV file.
        :return: A dictionary containing processed sentences and/or processed names.
        """
        if not stopwords_path or not os.path.exists(stopwords_path):
            raise FileNotFoundError(f"Stopwords file not found: {stopwords_path}")

        results = {}

        if sentences_path:
            if not os.path.exists(sentences_path):
                raise FileNotFoundError(f"Sentences file not found: {sentences_path}")
            preprocessor_instance = Preprocessing(
                question_num=0,
                sentences_path=sentences_path,
                people_path=people_path,
                stopwords_path=stopwords_path
            )
            results["Processed Sentences"] = preprocessor_instance.preprocess_sentences(stopwords_path)

        if people_path:
            if not os.path.exists(people_path):
                raise FileNotFoundError(f"People file not found: {people_path}")
            preprocessor_instance = Preprocessing(
                question_num=0,
                sentences_path=sentences_path,
                people_path=people_path,
                stopwords_path=stopwords_path
            )
            results["Processed Names"] = preprocessor_instance.preprocess_people()

        return results


