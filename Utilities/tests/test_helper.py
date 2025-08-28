import unittest
from unittest.mock import patch, mock_open
from collections import defaultdict
from Utilities.helper import preprocess_init, map_n_grams


class TestHelperFunctions(unittest.TestCase):

    @patch("os.path.exists", return_value=True)
    @patch("os.path.getsize", return_value=100)
    @patch("builtins.open", new_callable=mock_open,
           read_data='{"Question 1": {"Processed Sentences": [["hello", "world"]], "Processed Names": [["john", "doe"]]}}')
    def test_preprocess_init_with_preprocessed_file(self, mock_file, mock_getsize, mock_exists):
        result = preprocess_init(preprocess_path="fake_preprocessed.json")

        expected = {
            "Processed Sentences": [["hello", "world"]],
            "Processed Names": [["john", "doe"]]
        }

        self.assertEqual(result, expected)

    def test_map_n_grams_no_N(self):
        sentences = [["hello", "world"], ["hello", "again"]]
        result = map_n_grams(sentences, N=None)
        expected = defaultdict(set, {
            "hello": {tuple(["hello", "world"]), tuple(["hello", "again"])},
            "hello world": {tuple(["hello", "world"])},
            "world": {tuple(["hello", "world"])},
            "hello again": {tuple(["hello", "again"])},
            "again": {tuple(["hello", "again"])}
        })
        self.assertEqual(result, expected)

    def test_map_n_grams_with_N(self):
        sentences = [["the", "quick", "brown", "fox"]]
        result = map_n_grams(sentences, N=2)
        expected = defaultdict(set, {
            "the": {tuple(["the", "quick", "brown", "fox"])},
            "the quick": {tuple(["the", "quick", "brown", "fox"])},
            "quick": {tuple(["the", "quick", "brown", "fox"])},
            "quick brown": {tuple(["the", "quick", "brown", "fox"])},
            "brown": {tuple(["the", "quick", "brown", "fox"])},
            "brown fox": {tuple(["the", "quick", "brown", "fox"])},
            "fox": {tuple(["the", "quick", "brown", "fox"])}
        })
        self.assertEqual(result, expected)

    def test_empty_sentences(self):
        sentences = []
        expected_output = defaultdict(set)
        result = map_n_grams(sentences, N=None)
        self.assertEqual(result, expected_output)

    def test_k_seqs_not_found(self):
        sentences = [
            ["this", "is", "a", "test"],
            ["this", "test", "is", "a", "test"]
        ]
        k_seqs = {
            "not found": ["not", "found"],
            "no match": ["no", "match"]
        }
        sentence_index = map_n_grams(sentences, N=None)
        search_index = defaultdict(set)
        for k_seq_key, k_seq_value in k_seqs.items():
            k_seq_str = " ".join(k_seq_value)
            if k_seq_str in sentence_index:
                search_index[k_seq_str] = sentence_index[k_seq_str]
        expected_output = {}
        self.assertEqual(search_index, expected_output)

    def test_nested_k_seqs(self):
        sentences = [
            ["this", "is", "a", "test"],
            ["this", "test", "is", "a", "test"]
        ]
        k_seqs = {
            "this is": ["this", "is"],
            "a test": ["a", "test"]
        }
        sentence_index = map_n_grams(sentences, N=None)
        search_index = defaultdict(set)
        for k_seq_key, k_seq_value in k_seqs.items():
            k_seq_str = " ".join(k_seq_value)
            if k_seq_str in sentence_index:
                search_index[k_seq_str] = sentence_index[k_seq_str]
        expected_output = {
            "this is": {('this', 'is', 'a', 'test')},
            "a test": {('this', 'is', 'a', 'test'), ('this', 'test', 'is', 'a', 'test')}
        }
        self.assertEqual(search_index, expected_output)


if __name__ == "__main__":
    unittest.main()
