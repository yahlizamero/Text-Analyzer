import unittest
import json
from task_implementation.Task_1_Preprocessing import Preprocessing


class TestPreprocessing(unittest.TestCase):
    def setUp(self):
        """Set up file paths and initialize the Preprocessing class for testing."""
        self.sentences_path = "/Users/YAHLIZ/Library/CloudStorage/GoogleDrive-yahli.zamero@mail.huji.ac.il/My Drive/Intro to CS/text_analyzer/examples/Q1_examples/example_1/sentences_small_1.csv"
        self.people_path = "/Users/YAHLIZ/Library/CloudStorage/GoogleDrive-yahli.zamero@mail.huji.ac.il/My Drive/Intro to CS/text_analyzer/examples/Q1_examples/example_1/people_small_1.csv"
        self.stopwords_path = "/Users/YAHLIZ/Library/CloudStorage/GoogleDrive-yahli.zamero@mail.huji.ac.il/My Drive/Intro to CS/text_analyzer/data/REMOVEWORDS.csv"
        self.preprocessor = Preprocessing(
            question_num=1,
            sentences_path=self.sentences_path,
            people_path=self.people_path,
            stopwords_path=self.stopwords_path,
        )
        with open("/Users/YAHLIZ/Library/CloudStorage/GoogleDrive-yahli.zamero@mail.huji.ac.il/My Drive/Intro to CS/text_analyzer/examples/Q1_examples/example_1/Q1_result1.json", "r") as result_file:
            self.expected_output = json.load(result_file)

    def test_preprocess_sentences(self):
        """Test sentence preprocessing to match the expected output."""
        processed_sentences = self.preprocessor.preprocess_sentences()
        expected_sentences = self.expected_output["Question 1"]["Processed Sentences"]
        self.assertEqual(processed_sentences, expected_sentences)

    def test_preprocess_people(self):
        """Test people preprocessing to match the expected output."""
        processed_people = self.preprocessor.preprocess_people()
        expected_people = self.expected_output["Question 1"]["Processed Names"]
        self.assertEqual(processed_people, expected_people)

    def test_preprocess(self):
        """Test the full preprocessing pipeline to match the expected output."""
        processed_data = self.preprocessor.preprocess()
        expected_data = self.expected_output["Question 1"]
        self.assertEqual(processed_data["Processed Sentences"], expected_data["Processed Sentences"])
        self.assertEqual(processed_data["Processed Names"], expected_data["Processed Names"])


if __name__ == "__main__":
    unittest.main()
