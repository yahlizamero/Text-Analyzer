import unittest
from unittest.mock import patch
from task_implementation.Task_3_Counting_Person import PersonMentionCounter


class TestPersonMentionCounter(unittest.TestCase):

    def setUp(self):
        self.processed_data = {
            "Processed Sentences": [
                ["harry", "potter", "tall"],
                ["lived", "saved"],
                ["john", "potter", "left", "city"],
                ["harry", "potter","johnny","sea"]
            ],
            "Processed Names": [
                [["harry", "potter"], [["lived"]]],
                [["john", "potter"], [["johnny"]]]
            ]
        }

    @patch("task_implementation.Task_3_Counting_Person.preprocess_init", return_value={
        "Processed Sentences": [
            ["harry", "potter", "tall"],
            ["lived", "saved"]
                                ],
        "Processed Names": [
            [["harry", "potter"], [["lived"]]]
                            ]
    })
    def test_count_mentions(self, mock_preprocess):
        counter = PersonMentionCounter(sentences_path="fake_sentences.csv", people_path="fake_people.csv", stopwords_path="fake_stopwords.txt")
        result = counter.count_mentions
        expected = {"harry potter": 3}  # 2 mentions as "harry potter" and 1 as "boy who lived" (lived after removing stopwords)
        self.assertEqual(result, expected)

    @patch("task_implementation.Task_3_Counting_Person.preprocess_init", return_value={
        "Processed Sentences": [
            ["harry", "potter", "tall"],
            ["lived", "saved"],
            ["john", "potter", "left", "city"],
            ["harry", "potter", "johnny", "sea"]
        ],
        "Processed Names": [
            [["harry", "potter"], [["lived"]]],
            [["john", "potter"], [["johnny"]]]
        ]
    })
    def test_generate_results(self, mock_preprocess):
        counter = PersonMentionCounter(sentences_path="fake_sentences.csv", people_path="fake_people.csv", stopwords_path="fake_stopwords.txt")
        result = counter.generate_results()
        expected = {
            "Question 3": {
                "Name Mentions": [["harry potter", 6], ["john potter", 5]]
            }
        }
        self.assertEqual(result, expected)

    @patch("task_implementation.Task_3_Counting_Person.preprocess_init", return_value={
        "Processed Sentences": [],
        "Processed Names": []
    })
    def test_no_data(self, mock_preprocess):
        counter = PersonMentionCounter(sentences_path="fake_sentences.csv", people_path="fake_people.csv", stopwords_path="fake_stopwords.txt")
        result = counter.generate_results()
        expected = {
            "Question 3": {
                "Name Mentions": []
            }
        }
        self.assertEqual(result, expected)

    @patch("task_implementation.Task_3_Counting_Person.preprocess_init", return_value={
        "Processed Sentences": [
            ["harry", "potter", "elephant"],
            ["harry", "potter", "harry", "potter"]
        ],
        "Processed Names": [
            [["harry", "potter"], []]
        ]
    })
    def test_multiple_mentions(self, mock_preprocess):
        counter = PersonMentionCounter(sentences_path="fake_sentences.csv", people_path="fake_people.csv", stopwords_path="fake_stopwords.txt")
        result = counter.generate_results()
        expected = {
            "Question 3": {
                "Name Mentions": [["harry potter", 6]]  # 1 mention in first sentence, 4 in second
            }
        }
        self.assertEqual(result, expected)

    @patch("task_implementation.Task_3_Counting_Person.preprocess_init", return_value={
        "Processed Sentences": [
            ["johnny", "castle", "parry"],
        ],
        "Processed Names": [
            [["harry", "potter"], [["parry", "otter"]]],
            [["john", "potter"], [["johnny"]]]
        ]
    })
    def test_nickname_mentions_only(self, mock_preprocess):
        counter = PersonMentionCounter(sentences_path="fake_sentences.csv", people_path="fake_people.csv", stopwords_path="fake_stopwords.txt")
        result = counter.generate_results()
        expected = {
            "Question 3": {
                "Name Mentions": [["harry potter", 1], ["john potter", 1]]
            }
        }
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
