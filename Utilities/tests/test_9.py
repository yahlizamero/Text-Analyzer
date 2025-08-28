import unittest
from unittest.mock import patch
from task_implementation.Task_9_Grouping_Sentences import SentenceClustering


class TestSentenceClustering(unittest.TestCase):

    @patch('task_implementation.Task_9_Grouping_Sentences.preprocess_init', return_value={
        "Processed Sentences": [
            ['harry', 'potter', 'was', 'here'],
            ['ron', 'weasley', 'was', 'here'],
            ['hermione', 'granger', 'was', 'there'],
            ['harry', 'and', 'hermione', 'visited', 'hogwarts']
        ]
    })
    def test_basic_grouping(self, mock_preprocess):
        clustering = SentenceClustering(question_num=9, threshold=2)
        result = clustering.generate_results()
        expected = {'Question 9': {'group Matches': [['Group 1', [['harry', 'and', 'hermione', 'visited', 'hogwarts']]],
                                                     ['Group 2', [['hermione', 'granger', 'was', 'there']]],
                                                     ['Group 3', [['harry', 'potter', 'was', 'here'],
                                                                  ['ron', 'weasley', 'was', 'here']]]]}}
        self.assertEqual(result, expected)

    @patch('task_implementation.Task_9_Grouping_Sentences.preprocess_init', return_value={
        "Processed Sentences": [
            ['harry', 'potter', 'was', 'here'],
            ['ron', 'weasley', 'was', 'here']
        ]
    })
    def test_no_groups_due_to_high_threshold(self, mock_preprocess):
        clustering = SentenceClustering(question_num=9, threshold=5)
        result = clustering.generate_results()
        expected = {
            "Question 9": {
                "group Matches": [
                    ["Group 1", [["harry", "potter", "was", "here"]]],
                    ["Group 2", [["ron", "weasley", "was", "here"]]]
                ]
            }
        }
        self.assertEqual(result, expected)

    @patch('task_implementation.Task_9_Grouping_Sentences.preprocess_init', return_value={
        "Processed Sentences": []
    })
    def test_empty_sentences(self, mock_preprocess):
        clustering = SentenceClustering(question_num=9, threshold=1)
        result = clustering.generate_results()
        expected = {"Question 9": {"group Matches": []}}
        self.assertEqual(result, expected)

    @patch('task_implementation.Task_9_Grouping_Sentences.preprocess_init', return_value={
        "Processed Sentences": [
            ['harry', 'potter', 'was', 'here'],
            ['ron', 'weasley', 'was', 'here']
        ]
    })
    def test_threshold_zero(self, mock_preprocess):
        clustering = SentenceClustering(question_num=9, threshold=0)
        result = clustering.generate_results()
        expected = {'Question 9': {'group Matches': [['Group 1',
                                   [['harry', 'potter', 'was', 'here']]],
                                  ['Group 2',
                                   [['ron', 'weasley', 'was', 'here']]]]}}
        self.assertEqual(result, expected)

    @patch('task_implementation.Task_9_Grouping_Sentences.preprocess_init', return_value={
        "Processed Sentences": [
            ['harry', 'potter', 'visited', 'hogwarts'],
            ['hermione', 'granger', 'visited', 'hogwarts'],
            ['ron', 'weasley', 'visited', 'hogwarts']
        ]
    })
    def test_all_sentences_in_one_group(self, mock_preprocess):
        clustering = SentenceClustering(question_num=9, threshold=1)
        result = clustering.generate_results()
        expected = {
            "Question 9": {
                "group Matches": [
                    ["Group 1", [
                        ["harry", "potter", "visited", "hogwarts"],
                        ["hermione", "granger", "visited", "hogwarts"],
                        ["ron", "weasley", "visited", "hogwarts"]
                    ]]
                ]
            }
        }
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
