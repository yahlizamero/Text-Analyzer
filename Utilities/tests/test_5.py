import unittest
from collections import defaultdict
from unittest.mock import patch, mock_open
from task_implementation.Task_5_Contexts import PersonContexts


class TestContextsAndKSeqs(unittest.TestCase):

    @patch("task_implementation.Task_5_Contexts.map_n_grams", return_value=defaultdict(set, {
        'harry': {("harry", "visited", "hogwarts"), ("harry", "potter", "was", "here")},
        'potter': {("john", "potter", "left", "the", "city"), ("harry", "potter", "was", "here")},
        'was': {("harry", "potter", "was", "here")},
        'here': {("harry", "potter", "was", "here")},
        'visited': {("harry", "visited", "hogwarts")},
        'hogwarts': {("harry", "visited", "hogwarts")},
        'john': {("john", "potter", "left", "the", "city")},
        'left': {("john", "potter", "left", "the", "city")},
        'the': {("john", "potter", "left", "the", "city")},
        'city': {("john", "potter", "left", "the", "city")}
    }))
    @patch("task_implementation.Task_5_Contexts.preprocess_init", return_value={
        "Processed Sentences": [
            ["harry", "potter", "was", "here"],
            ["harry", "visited", "hogwarts"],
            ["john", "potter", "left", "the", "city"]
        ],
        "Processed Names": [
            [["harry", "potter"], [["the", "boy", "who", "lived"]]],
            [["john", "potter"], [["johnny"]]]
        ]
    })
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open,
           read_data="sentence\nHarry Potter was here.\nHarry visited Hogwarts.\nJohn Potter left the city.")
    def test_contexts_and_k_seqs(self, mock_open, mock_exists, mock_preprocess_init, mock_map_n_grams):
        context = PersonContexts(N=2)
        result = context.contexts_and_k_seqs()

        expected = [
            ['harry potter', [['city'], ['harry'], ['here'], ['hogwarts'], ['john'], ['left'], ['potter'], ['the'],
                              ['visited'], ['was']]],
            ['john potter', [['city'], ['harry'], ['here'], ['john'], ['left'], ['potter'], ['the'], ['was']]]
        ]

        self.assertEqual(result, expected)

    @patch("task_implementation.Task_5_Contexts.map_n_grams", return_value=defaultdict(set, {}))
    @patch("task_implementation.Task_5_Contexts.preprocess_init", return_value={
        "Processed Sentences": [],
        "Processed Names": []
    })
    def test_empty_data(self, mock_preprocess_init, mock_map_n_grams):
        context = PersonContexts(N=2)
        result = context.contexts_and_k_seqs()
        expected = []
        self.assertEqual(result, expected)

    @patch("task_implementation.Task_5_Contexts.map_n_grams", return_value=defaultdict(set, {
        'hermione': {("hermione", "granger", "was", "brilliant")},
        'granger': {("hermione", "granger", "was", "brilliant")},
        'was': {("hermione", "granger", "was", "brilliant")},
        'brilliant': {("hermione", "granger", "was", "brilliant")}
    }))
    @patch("task_implementation.Task_5_Contexts.preprocess_init", return_value={
        "Processed Sentences": [
            ["hermione", "granger", "was", "brilliant"]
        ],
        "Processed Names": [
            [["hermione", "granger"], [["mione"]]]
        ]
    })
    def test_single_person_with_alias(self, mock_preprocess_init, mock_map_n_grams):
        context = PersonContexts(N=2)
        result = context.contexts_and_k_seqs()

        expected = [['hermione granger', [['brilliant'], ['granger'], ['hermione'], ['was']]]]

        self.assertEqual(result, expected)

    @patch("task_implementation.Task_5_Contexts.map_n_grams", return_value=defaultdict(set, {
        'harry': {("harry", "ran", "quickly")},
        'ran': {("harry", "ran", "quickly"), ("ron", "ran", "slowly")},
        'quickly': {("harry", "ran", "quickly")},
        'ron': {("ron", "ran", "slowly")},
        'slowly': {("ron", "ran", "slowly")}
    }))
    @patch("task_implementation.Task_5_Contexts.preprocess_init", return_value={
        "Processed Sentences": [
            ["harry", "ran", "quickly"],
            ["ron", "ran", "slowly"]
        ],
        "Processed Names": [
            [["harry", "potter"], []],
            [["ron", "weasley"], []]
        ]
    })
    def test_multiple_people_no_overlap(self, mock_preprocess_init, mock_map_n_grams):
        context = PersonContexts(N=2)
        result = context.contexts_and_k_seqs()

        expected = [['harry potter', [['harry'], ['quickly'], ['ran']]],
                    ['ron weasley', [['ran'], ['ron'], ['slowly']]]]

        self.assertEqual(result, expected)

    def test_missing_N_raises_system_exit(self):
        with self.assertRaises(SystemExit) as cm:
            PersonContexts()
        self.assertEqual(cm.exception.code, 1)

if __name__ == "__main__":
    unittest.main()