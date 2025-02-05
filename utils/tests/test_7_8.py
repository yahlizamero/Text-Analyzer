import unittest
from unittest.mock import patch, mock_open
from task_implementation.Task_7_8_Indirect_Connections import IndirectPaths


class TestIndirectPaths(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open,
           read_data='{"keys": [["harry potter", "ron weasley"], ["harry potter", "hermione granger"]]}')
    @patch('task_implementation.Task_6_Direct_Connections.preprocess_init', return_value={
        "Processed Sentences": [['harry', 'potter', 'and', 'ron', 'weasley', 'were', 'at', 'hogwarts']],
        "Processed Names": [[['harry', 'potter'], []], [['ron', 'weasley'], []], [['hermione', 'granger'], []]]
    })
    def test_task_7_basic_indirect_connection(self, mock_preprocess, mock_file):
        indirect_paths = IndirectPaths(
            question_num=7,
            sentences_path="fake_sentences.csv",
            people_path="fake_people.csv",
            stopwords_path="fake_stopwords.txt",
            window_size=1,
            threshold=0,
            people_connections_path="fake_people_connections.json",
            maximal_distance=2
        )

        result = indirect_paths.generate_results_task_7()
        expected = {'Question 7':
                        {'Pair Matches': [['harry potter', 'hermione granger', False],
                                          ['harry potter', 'ron weasley', True]]
                         }
                    }
        self.assertEqual(result, expected)

    @patch('builtins.open', new_callable=mock_open,
           read_data='{"keys": [["harry potter", "hermione granger"]]}')
    @patch('task_implementation.Task_6_Direct_Connections.preprocess_init', return_value={
        "Processed Sentences": [['harry', 'potter', 'and', 'ron', 'weasley', 'were', 'at', 'hogwarts']],
        "Processed Names": [[['harry', 'potter'], []], [['ron', 'weasley'], []], [['hermione', 'granger'], []]]
    })
    def test_task_7_no_connection(self, mock_preprocess, mock_file):
        indirect_paths = IndirectPaths(
            question_num=7,
            sentences_path="fake_sentences.csv",
            people_path="fake_people.csv",
            stopwords_path="fake_stopwords.txt",
            window_size=1,
            threshold=0,
            people_connections_path="fake_people_connections.json",
            maximal_distance=1
        )

        result = indirect_paths.generate_results_task_7()
        expected = {'Question 7': {'Pair Matches': [['harry potter', 'hermione granger', False]]}}
        self.assertEqual(result, expected)

    @patch('builtins.open', new_callable=mock_open,
           read_data='{"keys": [["harry potter", "ron weasley"]]}')
    @patch('task_implementation.Task_6_Direct_Connections.preprocess_init', return_value={
        "Processed Sentences": [['harry', 'potter', 'ron', 'weasley', 'and', 'hermione', 'granger']],
        "Processed Names": [[['harry', 'potter'], []], [['ron', 'weasley'], []], [['hermione', 'granger'], []]]
    })
    def test_task_8_exact_length_connection(self, mock_preprocess, mock_file):
        indirect_paths = IndirectPaths(
            question_num=8,
            sentences_path="fake_sentences.csv",
            people_path="fake_people.csv",
            stopwords_path="fake_stopwords.txt",
            window_size=1,
            threshold=0,
            people_connections_path="fake_people_connections.json",
            K=1
        )

        result = indirect_paths.generate_results_task_8()
        expected = {
            "Question 8": {
                "Pair Matches": [
                    ["harry potter", "ron weasley", True]
                ]
            }
        }
        self.assertEqual(result, expected)

    @patch('builtins.open', new_callable=mock_open,
           read_data='{"keys": [["harry potter", "hermione granger"]]}')
    @patch('task_implementation.Task_6_Direct_Connections.preprocess_init', return_value={
        "Processed Sentences": [['harry', 'potter', 'and', 'ron', 'weasley']],
        "Processed Names": [[['harry', 'potter'], []], [['ron', 'weasley'], []], [['hermione', 'granger'], []]]
    })
    def test_task_8_no_exact_length_connection(self, mock_preprocess, mock_file):
        indirect_paths = IndirectPaths(
            question_num=8,
            sentences_path="fake_sentences.csv",
            people_path="fake_people.csv",
            stopwords_path="fake_stopwords.txt",
            window_size=1,
            threshold=0,
            people_connections_path="fake_people_connections.json",
            K=1
        )

        result = indirect_paths.generate_results_task_8()
        expected = {
            "Question 8": {
                "Pair Matches": [
                    ["harry potter", "hermione granger", False]
                ]
            }
        }
        self.assertEqual(result, expected)

    @patch('builtins.open', new_callable=mock_open, read_data='{"keys": []}')
    @patch('task_implementation.Task_6_Direct_Connections.preprocess_init', return_value={
        "Processed Sentences": [['harry', 'potter', 'and', 'ron', 'weasley', 'were', 'at', 'hogwarts']],
        "Processed Names": [[['harry', 'potter'], []], [['ron', 'weasley'], []]]
    })
    def test_empty_people_connections(self, mock_preprocess, mock_file):
        indirect_paths = IndirectPaths(
            question_num=7,
            sentences_path="fake_sentences.csv",
            people_path="fake_people.csv",
            stopwords_path="fake_stopwords.txt",
            window_size=1,
            threshold=1,
            people_connections_path="fake_people_connections.json",
            maximal_distance=2
        )

        result = indirect_paths.generate_results_task_7()
        expected = {
            "Question 7": {
                "Pair Matches": []
            }
        }
        self.assertEqual(result, expected)

    @patch('builtins.open', new_callable=mock_open,
           read_data='{"keys": [["harry potter", "albus dumbledore"]]}')
    @patch('task_implementation.Task_6_Direct_Connections.preprocess_init', return_value={
        "Processed Sentences": [['harry', 'potter', 'and', 'ron', 'weasley', 'were', 'at', 'hogwarts']],
        "Processed Names": [[['harry', 'potter'], []], [['ron', 'weasley'], []]]  # No 'albus dumbledore'
    })
    def test_person_not_in_graph(self, mock_preprocess, mock_file):
        indirect_paths = IndirectPaths(
            question_num=7,
            sentences_path="fake_sentences.csv",
            people_path="fake_people.csv",
            stopwords_path="fake_stopwords.txt",
            window_size=1,
            threshold=1,
            people_connections_path="fake_people_connections.json",
            maximal_distance=2
        )

        result = indirect_paths.generate_results_task_7()
        expected = {
            "Question 7": {
                "Pair Matches": [
                    ['albus dumbledore', 'harry potter', False]  # Should return False as 'albus dumbledore' is missing
                ]
            }
        }
        self.assertEqual(result, expected)

    @patch('builtins.open', new_callable=mock_open,
           read_data='{"keys": [["harry potter", "ron weasley"]]}')
    @patch('task_implementation.Task_6_Direct_Connections.preprocess_init', return_value={
        "Processed Sentences": [],
        "Processed Names": [[['harry', 'potter'], []], [['ron', 'weasley'], []]]
    })
    def test_no_sentences(self, mock_preprocess, mock_file):
        indirect_paths = IndirectPaths(
            question_num=7,
            sentences_path="fake_sentences.csv",
            people_path="fake_people.csv",
            stopwords_path="fake_stopwords.txt",
            window_size=0,
            threshold=1,
            people_connections_path="fake_people_connections.json",
            maximal_distance=2
        )

        result = indirect_paths.generate_results_task_7()
        expected = {
            "Question 7": {
                "Pair Matches": [
                    ["harry potter", "ron weasley", False]
                ]
            }
        }
        self.assertEqual(result, expected)

    @patch('builtins.open', new_callable=mock_open, read_data='{"keys": [["harry potter", "ron weasley"]]}')
    @patch('task_implementation.Task_6_Direct_Connections.preprocess_init', return_value={
        "Processed Sentences": [],
        "Processed Names": [[['harry', 'potter'], []], [['ron', 'weasley'], []]]
    })
    def test_task_8_k_zero(self, mock_preprocess, mock_file):
        indirect_paths = IndirectPaths(
            question_num=8,
            sentences_path="fake_sentences.csv",
            people_path="fake_people.csv",
            stopwords_path="fake_stopwords.txt",
            window_size=0,
            threshold=1,
            people_connections_path="fake_people_connections.json",
            K=0
        )

        result = indirect_paths.generate_results_task_8()
        expected = {
            "Question 8": {
                "Pair Matches": [
                    ["harry potter", "ron weasley", False]
                ]
            }
        }
        self.assertEqual(result, expected)

    @patch('builtins.open', new_callable=mock_open, read_data='{"keys": [["harry potter", "ron weasley"], ["harry '
                                                              'potter", "hermione granger"]]}')
    @patch('task_implementation.Task_6_Direct_Connections.preprocess_init', return_value={
        "Processed Sentences": [],
        "Processed Names": [[['harry', 'potter'], []], [['ron', 'weasley'], []], [['hermione', 'granger'],[]]]
    })
    def test_task_8_maxd_zero(self, mock_preprocess, mock_file):
        indirect_paths = IndirectPaths(
            question_num=7,
            sentences_path="fake_sentences.csv",
            people_path="fake_people.csv",
            stopwords_path="fake_stopwords.txt",
            window_size=0,
            threshold=1,
            people_connections_path="fake_people_connections.json",
            maximal_distance=0
        )

        result = indirect_paths.generate_results_task_8()
        expected = {
            "Question 7": {
                "Pair Matches": [
                ["harry potter", "hermione granger", False], ["harry potter", "ron weasley", False]
                ]
            }
        }
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
