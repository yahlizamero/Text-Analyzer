
import json
import csv
import os
from typing import List, Dict, Any, Set
from utils.helper_functions import load_stopwords, clean_text, is_duplicate_or_overlap, split_name


# Preprocessing class
class Preprocessing:
    def __init__(self, question_num: int, sentences_path: str, people_path: str, stopwords_path: str) -> None:
        self.question_num = question_num
        self.sentences_path = sentences_path
        self.people_path = people_path
        self.stopwords = load_stopwords(stopwords_path)

    def preprocess_sentences(self) -> List[List[str]]:
        processed_sentences = []
        with open(self.sentences_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                sentence = clean_text(row['sentence'], self.stopwords)
                if sentence:  # Skip empty sentences
                    processed_sentences.append(sentence.split())
        return processed_sentences

    def preprocess_people(self) -> List[List[List[Any]]]:
        processed_people = []
        seen_names = set()

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

    def preprocess(self) -> Dict[str, Any]:
        return {
            f"Question {self.question_num}": {
                "Processed Sentences": self.preprocess_sentences(),
                "Processed Names": self.preprocess_people()
            }
        }

    def save_to_json(self, output_path: str) -> None:
        processed_data = self.preprocess()
        with open(output_path, "w") as file:
            json.dump(processed_data, file, indent=4)


# Example usage
if __name__ == "__main__":
    sentences_file = "/Users/YAHLIZ/Library/CloudStorage/GoogleDrive-yahli.zamero@mail.huji.ac.il/My Drive/Intro to CS/text_analyzer/examples/Q1_examples/example_2/sentences_small_2.csv"
    people_file = "/Users/YAHLIZ/Library/CloudStorage/GoogleDrive-yahli.zamero@mail.huji.ac.il/My Drive/Intro to CS/text_analyzer/examples/Q1_examples/example_2/people_small_2.csv"
    stopwords_file = "/Users/YAHLIZ/Library/CloudStorage/GoogleDrive-yahli.zamero@mail.huji.ac.il/My Drive/Intro to CS/text_analyzer/data/REMOVEWORDS.csv"
    output_file = "/Users/YAHLIZ/Library/CloudStorage/GoogleDrive-yahli.zamero@mail.huji.ac.il/My Drive/Intro to CS/text_analyzer/examples/Q1_examples/example_2/generated_Q2_result.json"

    # Check if required files exist
    for file_path in [sentences_file, people_file, stopwords_file]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Required file not found: {file_path}")

    preprocessor = Preprocessing(
        question_num=1,
        sentences_path=sentences_file,
        people_path=people_file,
        stopwords_path=stopwords_file
    )
    preprocessor.save_to_json(output_file)
    print(f"JSON results saved to {output_file}")
