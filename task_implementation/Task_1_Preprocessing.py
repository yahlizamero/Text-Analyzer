# Description: This script preprocesses the input data for Task 1: Preprocessing.
# Includes functionality for cleaning sentences and processing names.


import csv
import os
import sys
import re
from typing import *


# Helper functions for preprocessing
def clean_text(text: str, unwanted_words: Set[str]) -> str:
    """
    Clean a string by removing punctuation, unwanted words, and excessive whitespace.
    :param: text (str): The text to clean.
    :param: unwanted_words (Set[str]): A set of words to remove from the text.
    :return: str: The cleaned text.
    """
    text = re.sub(r'[^a-z0-9\s]', ' ', text.lower())  # Remove punctuation and convert to lowercase
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra whitespaces
    return ' '.join(word for word in text.split() if word not in unwanted_words)


def check_file_validity(file_type: str, path: str):
    if not os.path.exists(path):
        print(f"FileNotFoundError: The file for {file_type.replace('_', ' ')} was not found at: {path}")
        sys.exit(1)
    if os.path.getsize(path) == 0:
        print(f"Error: The file for {file_type.replace('_', ' ')} at {path} is empty.")
        sys.exit(1)

    # Check for correct headers in sentences and people files
    if file_type == "sentences_path":
        with open(path, 'r') as file:
            header = file.readline().strip()
            if header != "sentence":
                print(
                    f"Error: The sentences file at {path} is not in the correct format. Expected header 'sentence'.")
                sys.exit(1)
    elif file_type == "people_path":
        with open(path, 'r') as file:
            header = file.readline().strip()
            if header != "Name,Other Names":
                print(
                    f"Error: The people file at {path} is not in the correct format. Expected header 'Name,Other Names'.")
                sys.exit(1)


class Preprocessing:
    def __init__(self,
                 question_num: int = None,
                 sentences_path: str = None,
                 people_path: str = None,
                 stopwords_path: str = None) -> None:

        # Initialize the Preprocessing class with the required data paths
        self.question_num = question_num
        self.sentences_path = sentences_path
        self.people_path = people_path
        self.stopwords = self.load_stopwords_file(stopwords_path)

        if not stopwords_path:  # Stopwords are required for preprocessing
            print("Error: Stopwords file path must be provided when preprocessing raw data.")
            sys.exit(1)

        preprocessing_args = {
            "sentences_path": sentences_path,
            "people_path": people_path,
            "stopwords_path": stopwords_path
        }

        # Check if files exist, are not empty, and have the correct format
        for key, path in preprocessing_args.items():
            if path:
                check_file_validity(key, path)

    @staticmethod
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
            print(f"Error loading stopwords file: {e}")
            sys.exit(1)

    def preprocess_sentences(self) -> List[List[str]]:
        """
        Preprocess the sentences from the sentences CSV file.
        :param: sentences_path (str): Path to the sentences CSV file.
        :param: stopwords (Set[str]): A set of stopwords to remove from the sentences.
        :return: A list of processed sentences.
        """
        processed_sentences = []
        try:
            # Load the sentences CSV file and clean the sentences
            with open(self.sentences_path, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    sentence = clean_text(row['sentence'], self.stopwords)
                    if sentence:  # Skip empty sentences
                        processed_sentences.append(sentence.split())
            return processed_sentences
        except Exception as e:
            print(f"Error loading sentences file: {e}")
            sys.exit(1)

    def preprocess_people(self) -> List[List[List[str]]]:
        """
        Preprocess the people from the people CSV file.
        :param: people_path (str): Path to the people CSV file.
        :param: stopwords (Set[str]): A set of stopwords to remove from the people names.
        :return: A list of processed people.
        """
        processed_people = []
        seen_names = set()

        try:
            # Load the people CSV file and clean the names
            with open(self.people_path, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    main_name = clean_text(row['Name'], self.stopwords)
                    if not main_name:  # Skip empty names
                        continue

                    # Split and clean other names
                    raw_other_names = row['Other Names'].strip().split(',') if row['Other Names'].strip() else []
                    raw_other_names = [name.strip() for name in raw_other_names]
                    other_names = [clean_text(name, self.stopwords) for name in raw_other_names]
                    other_names = [name for name in other_names if name]

                    main_name_split = main_name.split()
                    other_names_split = [name.split() if " " in name else [name] for name in other_names]

                    # Skip duplicates or overlaps
                    if main_name in seen_names or any(nickname in seen_names for nickname in other_names):
                        continue

                    seen_names.add(main_name)
                    seen_names.update(other_names)

                    # Add cleaned data as lists, ensure empty nickname lists if none exist
                    processed_people.append([main_name_split, other_names_split if other_names_split else []])
            return processed_people
        except Exception as e:
            print(f"Error loading people file: {e}")
            sys.exit(1)

    def generate_results(self) -> Dict[str, Any]:
        """
        Generate the final results for the task.
        :param: preprocess_sentences: List of preprocessed sentences.
        :param: preprocess_people: List of preprocessed people.
        :param: stopwords: Set of stopwords.
        :return: A dictionary containing the task results.
        """
        return {
            f"Question {self.question_num}": {
                "Processed Sentences": self.preprocess_sentences(),
                "Processed Names": self.preprocess_people()
            }
        }
