import unittest
from unittest.mock import patch, mock_open
from task_implementation.Task_2_Counting_Seq import SequenceCounter


class TestSequenceCounter(unittest.TestCase):

    def setUp(self):
        self.sample_sentences = {"Processed Sentences": [["hello", "world"], ["hello", "hello", "world"]]}
        self.empty_sentences = {"Processed Sentences": []}
        self.stopwords_content = "the\nand\nof"

    @patch("task_implementation.Task_2_Counting_Seq.preprocess_init", return_value={"Processed Sentences": [["hello", "world"], ["hello", "hello", "world"]]})
    @patch("os.path.exists", return_value=True)
    def test_count_sequences(self, mock_exists, mock_preprocess):
        counter = SequenceCounter(N=2, stopwords_path="fake_stopwords.txt")
        result = counter.count_sequences
        expected = [
            ["1_seq", [["hello", 3], ["world", 2]]],
            ["2_seq", [["hello hello", 1], ["hello world", 2]]]
        ]
        self.assertEqual(result, expected)

    @patch("task_implementation.Task_2_Counting_Seq.preprocess_init", return_value={"Processed Sentences": [["hello", "world"], ["hello", "hello", "world"]]})
    @patch("os.path.exists", return_value=True)
    def test_generate_results(self, mock_exists, mock_preprocess):
        counter = SequenceCounter(question_num=2, N=2, stopwords_path="fake_stopwords.txt")
        result = counter.generate_results()
        expected = {
            "Question 2": {
                "2-Seq Counts": [
                    ["1_seq", [["hello", 3], ["world", 2]]],
                    ["2_seq", [["hello hello", 1], ["hello world", 2]]]
                ]
            }
        }
        self.assertEqual(result, expected)

    @patch("task_implementation.Task_2_Counting_Seq.preprocess_init", return_value={"Processed Sentences": []})
    @patch("os.path.exists", return_value=True)
    def test_empty_sentences(self, mock_exists, mock_preprocess):
        counter = SequenceCounter(N=2, stopwords_path="fake_stopwords.txt")
        result = counter.count_sequences
        expected = [
            ["1_seq", []],
            ["2_seq", []]
        ]
        self.assertEqual(result, expected)

    @patch("task_implementation.Task_2_Counting_Seq.preprocess_init", return_value={"Processed Sentences": [["repeat", "repeat", "repeat"]]})
    @patch("os.path.exists", return_value=True)
    def test_repeated_words(self, mock_exists, mock_preprocess):
        counter = SequenceCounter(N=2, stopwords_path="fake_stopwords.txt")
        result = counter.count_sequences
        expected = [
            ["1_seq", [["repeat", 3]]],
            ["2_seq", [["repeat repeat", 2]]]
        ]
        self.assertEqual(result, expected)

    @patch("task_implementation.Task_2_Counting_Seq.preprocess_init", return_value={"Processed Sentences": [["unique", "words", "only"]]})
    @patch("os.path.exists", return_value=True)
    def test_no_repeated_sequences(self, mock_exists, mock_preprocess):
        counter = SequenceCounter(N=3, stopwords_path="fake_stopwords.txt")
        result = counter.count_sequences
        expected = [
            ["1_seq", [["only", 1], ["unique", 1], ["words", 1]]],
            ["2_seq", [["unique words", 1], ["words only", 1]]],
            ["3_seq", [["unique words only", 1]]]
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()