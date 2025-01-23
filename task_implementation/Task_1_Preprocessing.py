# Description:
# This file contains the implementation of the preprocessing task for the text analyzer project.
# Includes functionality for cleaning sentences and processing names.
import csv
import re
from typing import List, Dict, Any
from utils.helper_functions import load_stopwords


class Preprocessing:
    def __init__(self, question_num: int, sentences_path: str, people_path: str, stopwords_path: str) -> None:
        """
        Initialize the preprocessor with file paths.
        Args:
            question_num (int): The task number. (1 in this case).
            sentences_path (str): Path to the sentences CSV file.
            people_path (str): Path to the people CSV file.
            stopwords_path (str): Path to the stopwords CSV file.
        """
        self.question_num = question_num
        self.sentences_path = sentences_path
        self.people_path = people_path
        self.stopwords = load_stopwords(stopwords_path)

    def preprocess_sentences(self) -> List[List[str]]:
        """
        Preprocess sentences by removing punctuation, stopwords, and whitespaces.
        Returns:
            List[List[str]]: A list of cleaned sentences.
        """
        processed_sentences = []
        with open(self.sentences_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                sentence = row['sentence'].lower()
                sentence = re.sub(r'[^a-z0-9\s]', ' ', sentence)  # Remove punctuation
                words = [word for word in sentence.split() if word not in self.stopwords]  # Remove stopwords,
                # whitespaces
                if words:  # Skips empty sentences
                    processed_sentences.append(words)
        return processed_sentences

    def preprocess_people(self) -> List[Dict[str, Any]]:
        """
        Preprocess people by cleaning names and their nicknames.
        Returns:
            List[Dict[str, Any]]: A list of dictionaries with main names and nicknames.
        """
        processed_people = []
        seen_names = set()

        with open(self.people_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                main_name = row['Name'].strip().lower()
                main_name = re.sub(r'[^a-z0-9\s]', ' ', main_name)  # Remove punctuation
                main_name = re.sub(r'\s+', ' ', main_name).strip()  # Remove consecutive whitespaces and trim

                if main_name in seen_names:
                    continue  # Skip duplicate names
                seen_names.add(main_name)

                other_names = [name.strip().lower() for name in row['Other Names'].split(',')]
                other_names = [re.sub(r'[^a-z0-9\s]', ' ', name) for name in other_names]  # Remove punctuation
                other_names = [re.sub(r'\s+', ' ', name).strip() for name in
                               other_names]  # Remove consecutive whitespaces and trim
                other_names = [name for name in other_names if name]  # Remove empty names

                processed_people.append({"name": main_name, "other_names": other_names})

        return processed_people

    def preprocess(self) -> Dict[str, Any]:
        """
        Run the complete preprocessing pipeline.
        Returns:
            Dict[str, Any]: A dictionary containing processed sentences and people.
        """
        return {
            "Processed Sentences": self.preprocess_sentences(),
            "Processed Names": self.preprocess_people()
        }


# Example Usage
if __name__ == "__main__":
    # Replace with actual file paths
    sentences_path = "sentences.csv"
    people_path = "people.csv"
    stopwords_path = "stopwords.csv"

    preprocessor = Preprocessing(sentences_path, people_path, stopwords_path)
    result = preprocessor.preprocess()

    # Print the result in JSON format
    import json

    print(json.dumps(result, indent=2))
