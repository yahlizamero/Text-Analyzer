from task_implementation.Task_1_Preprocessing import *
import json
import os
from typing import List, Dict, Any
from utils.helper_functions import load_file, save_to_json

class Contexts:
    def __init__(
            self,
            sentences_path: str,
            remove_path: str = None,
            preprocess: bool = False,
            preprocessed_data: Dict[str, Any] = None
    ):
        """
        Initialize the WordPrediction class.

        :param sentences_path: Path to the sentences CSV file.
        :param remove_path: Path to the stopwords CSV file.
        :param preprocess: Flag to indicate whether preprocessing is required.
        :param preprocessed_data: Preprocessed data as a dictionary (optional).
        """
        if preprocess and not sentences_path:
            raise ValueError("Sentences path must be provided if preprocessing is enabled.")

        self.sentences = (
            load_preprocessed_sentences(preprocessed_data)
            if preprocessed_data
            else self.preprocess_sentences(sentences_path, remove_path)
        )

    def preprocess_sentences(self, sentences_path: str, remove_path: str) -> dict[str, Any]:
        """Preprocess the sentences from the CSV file."""
        return preprocess_data(self, sentences_path, remove_path)

    def generate_word_predictions(self) -> Dict[str, Dict[str, int]]:
        """
        Generate word predictions based on sentence context.

        :return: A dictionary where keys are words and values are dictionaries of possible next words with their counts.
        """
        word_predictions = {}

        for sentence in self.sentences:
            for i in range(len(sentence) - 1):
                current_word = sentence[i]
                next_word = sentence[i + 1]

                if current_word not in word_predictions:
                    word_predictions[current_word] = {}

                if next_word not in word_predictions[current_word]:
                    word_predictions[current_word][next_word] = 0

                word_predictions[current_word][next_word] += 1

        return word_predictions

    def generate_results(self) -> Dict[str, Any]:
        """Generate the final results for word predictions."""
        predictions = self.generate_word_predictions()

        # Sort predictions for each word
        sorted_predictions = {
            word: {
                next_word: count
                for next_word, count in sorted(predictions[word].items(), key=lambda x: (-x[1], x[0]))
            }
            for word in predictions
        }

        return {
            "Question 5": {
                "Word Predictions": sorted_predictions
            }
        }

    def print_results(self) -> None:
        """Print the results in JSON format."""
        results = self.generate_results()
        print(json.dumps(results, indent=4))


# Example usage
if __name__ == "__main__":
    sentences_file = "examples_new/Q5_examples/example_1/sentences_small_1.csv"
    stopwords_file = "data/REMOVEWORDS.csv"
    output_file = "examples_new/Q5_examples/example_1/generated_Q5_result.json"

    # Check if required files exist
    for file_path in [sentences_file, stopwords_file, output_file]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Required file not found: {file_path}")

    word_predictor = Contexts(
        sentences_path=sentences_file,
        remove_path=stopwords_file,
        preprocess=True
    )

    # Use the helper function to save the processed data
    save_to_json(output_path=output_file, process_function=word_predictor.generate_results)
    print(f"JSON results saved to {output_file}")
