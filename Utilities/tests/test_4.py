import unittest
from unittest.mock import patch, mock_open
from collections import defaultdict
from task_implementation.Task_4_Search_Engine import SearchEngine
import json


class TestSearchEngine(unittest.TestCase):
    def setUp(self):
        self.mock_k_seq_data = json.dumps({
            "keys": [["harry", "potter"], ["hogwarts"]]
        })

        self.mock_preprocessed_data = {
            "Processed Sentences": [
                ["harry", "potter", "was", "here"],
                ["welcome", "to", "hogwarts"],
                ["harry", "visited", "hogwarts"]
            ]
        }

        self.mock_sentence_index = defaultdict(set, {
            "harry potter": {("harry", "potter", "was", "here")},
            "hogwarts": {("welcome", "to", "hogwarts"), ("harry", "visited", "hogwarts")}
        })

    @patch("os.path.exists", return_value=True)
    @patch("os.path.getsize", return_value=100)
    @patch("task_implementation.Task_4_Search_Engine.open", new_callable=mock_open,
           read_data='{"keys": [["harry", "potter"], ["hogwarts"]]}')
    @patch("task_implementation.Task_4_Search_Engine.preprocess_init", return_value={
        "Processed Sentences": [
            ["harry", "potter", "was", "here"],
            ["welcome", "to", "hogwarts"],
            ["harry", "visited", "hogwarts"]
        ]
    })
    @patch("task_implementation.Task_4_Search_Engine.map_n_grams", return_value=defaultdict(list, {
        "harry potter": [["harry", "potter", "was", "here"]],
        "hogwarts": [["welcome", "to", "hogwarts"], ["harry", "visited", "hogwarts"]]
    }))
    def test_build_search_index(self, mock_map_n_grams, mock_preprocess_init, mock_file, mock_getsize, mock_exists):
        engine = SearchEngine(
            question_num=4,
            sentences_path="fake_sentences.csv",
            stopwords_path="fake_stopwords.txt",
            preprocess_path="fake_preprocessed.json",
            k_seq_path="fake_k_seq.json"
        )

        result = engine.build_search_index()

        expected = {
            "harry potter": [["harry", "potter", "was", "here"]],
            "hogwarts": [["harry", "visited", "hogwarts"], ["welcome", "to", "hogwarts"]]
        }

        self.assertEqual(dict(result), expected)

    @patch("os.path.exists", return_value=True)
    @patch("os.path.getsize", return_value=100)
    @patch("task_implementation.Task_4_Search_Engine.open", new_callable=mock_open,
           read_data='{"keys": [["dumbledore"]]}')
    @patch("task_implementation.Task_4_Search_Engine.preprocess_init", return_value={
        "Processed Sentences": [
            ["harry", "potter", "was", "here"],
            ["welcome", "to", "hogwarts"],
            ["harry", "visited", "hogwarts"]
        ]
    })
    @patch("task_implementation.Task_4_Search_Engine.map_n_grams", return_value=defaultdict(list, {
        "harry potter": [["harry", "potter", "was", "here"]],
        "hogwarts": [["harry", "visited", "hogwarts"], ["welcome", "to", "hogwarts"]]
    }))
    def test_no_matches(self, mock_map_n_grams, mock_preprocess_init, mock_file, mock_getsize, mock_exists):
        engine = SearchEngine(
            question_num=4,
            sentences_path="fake_sentences.csv",
            stopwords_path="fake_stopwords.txt",
            preprocess_path="fake_preprocessed.json",
            k_seq_path="fake_k_seq.json"
        )
        result = engine.build_search_index()
        expected = {}  # Since 'dumbledore' isn't in any sentence
        self.assertEqual(dict(result), expected)

    @patch("os.path.exists", return_value=True)
    @patch("os.path.getsize", return_value=100)
    @patch("builtins.open", new_callable=mock_open, read_data='{"keys": []}')
    @patch("task_implementation.Task_4_Search_Engine.preprocess_init", return_value={
        "Processed Sentences": [
            ["harry", "potter", "was", "here"],
            ["welcome", "to", "hogwarts"],
            ["harry", "visited", "hogwarts"]
        ]
    })
    @patch("task_implementation.Task_4_Search_Engine.map_n_grams", return_value=defaultdict(set, {
        "harry potter": {("harry", "potter", "was", "here")},
        "hogwarts": {("harry", "visited", "hogwarts"), ("welcome", "to", "hogwarts")}
    }))
    def test_empty_k_seq(self, mock_map_n_grams, mock_preprocess_init, mock_file, mock_getsize, mock_exists):
        engine = SearchEngine(
            question_num=4,
            sentences_path="fake_sentences.csv",
            stopwords_path="fake_stopwords.txt",
            preprocess_path="fake_preprocessed.json",
            k_seq_path="fake_k_seq.json"
        )
        result = engine.generate_results()
        expected = {
            "Question 4": {
                "K-Seq Matches": []
            }
        }
        self.assertEqual(result, expected)

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='["harry", "potter"]')
    @patch("utils.helper.preprocess_init", return_value={
        "Processed Sentences": [
            ["harry", "potter", "was", "here"],
            ["welcome", "to", "hogwarts"],
            ["harry", "visited", "hogwarts"]
        ]
    })
    def test_invalid_k_seq_format(self, mock_preprocess_init, mock_file, mock_exists):
        with self.assertRaises(SystemExit) as cm:
            SearchEngine(
                question_num=4,
                sentences_path="fake_sentences.csv",
                stopwords_path="fake_stopwords.txt",
                preprocess_path="fake_preprocessed.json",
                k_seq_path="fake_k_seq.json"
            )
        self.assertEqual(cm.exception.code, 1)

    @patch("os.path.exists", return_value=True)
    @patch("utils.helper.preprocess_init", return_value={
        "Processed Sentences": [
            ["harry", "potter", "was", "here"],
            ["welcome", "to", "hogwarts"],
            ["harry", "visited", "hogwarts"]
        ]
    })
    def test_no_k_seq_path_provided(self, mock_preprocess_init, mock_exists):
        with self.assertRaises(SystemExit) as cm:
            SearchEngine(
                question_num=4,
                sentences_path="fake_sentences.csv",
                stopwords_path="fake_stopwords.txt",
                preprocess_path="fake_preprocessed.json",
                k_seq_path=None
            )
        self.assertEqual(cm.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
