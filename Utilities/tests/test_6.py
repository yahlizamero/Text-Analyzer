import unittest
from unittest.mock import patch
from task_implementation.Task_6_Direct_Connections import DirectConnections, PersonNode


class TestDirectConnections(unittest.TestCase):

    @patch('task_implementation.Task_6_Direct_Connections.preprocess_init', return_value={
        "Processed Sentences": [['sentence1']],
        "Processed Names": []
    })
    def test_basic_connections(self, mock_preprocess):
        dc = DirectConnections(threshold=2, question_num=6, window_size=1)
        dc.graph.nodes = {
            'aberforth dumbledore': PersonNode('aberforth dumbledore', []),
            'aurelius dumbledore': PersonNode('aurelius dumbledore', [])
        }
        dc.graph.add_connection('aberforth dumbledore', 'aurelius dumbledore', 3)

        result = dc.graph.get_edges()
        expected = [[['aberforth', 'dumbledore'], ['aurelius', 'dumbledore']]]
        self.assertEqual(result, expected)

    @patch('task_implementation.Task_6_Direct_Connections.preprocess_init', return_value={
        "Processed Sentences": [['sentence1']],
        "Processed Names": []
    })
    def test_alias_handling(self, mock_preprocess):
        dc = DirectConnections(threshold=2, question_num=6, window_size=1)
        dc.graph.nodes = {
            'dumbledore': PersonNode('dumbledore', ['dumbledore']),
            'aurelius dumbledore': PersonNode('aurelius dumbledore', ['aurelius', 'dumbledore'])
        }
        dc.graph.add_connection('dumbledore', 'aurelius dumbledore', 3)

        result = dc.graph.get_edges()
        expected = [[['aurelius', 'dumbledore'], ['dumbledore']]]
        self.assertEqual(result, expected)

    @patch('task_implementation.Task_6_Direct_Connections.preprocess_init', return_value={
        "Processed Sentences": [['sentence1']],
        "Processed Names": []
    })
    def test_no_cooccurrence(self, mock_preprocess):
        dc = DirectConnections(threshold=2, question_num=6, window_size=1)

        result = dc.graph.get_edges()
        self.assertEqual(result, [])

    @patch('task_implementation.Task_6_Direct_Connections.preprocess_init', return_value={
        "Processed Sentences": [['sentence1'], ['sentence2'], ['sentence3'], ['sentence4']],
        "Processed Names": []
    })
    def test_multiple_connections(self, mock_preprocess):
        dc = DirectConnections(threshold=2, question_num=6, window_size=4)
        dc.graph.nodes = {
            'aberforth dumbledore': PersonNode('aberforth dumbledore', ['aberforth', 'dumbledore']),
            'aurelius dumbledore': PersonNode('aurelius dumbledore', ['aurelius', 'dumbledore']),
            'harry potter': PersonNode('harry potter', ['harry', 'potter', 'undesirable', 'number'])
        }

        dc.graph.add_connection('aberforth dumbledore', 'aurelius dumbledore', 3)
        dc.graph.add_connection('aurelius dumbledore', 'harry potter', 3)
        dc.graph.add_connection('aberforth dumbledore', 'harry potter', 3)

        result = dc.graph.get_edges()
        expected = [[['aberforth', 'dumbledore'], ['aurelius', 'dumbledore']],
                    [['aberforth', 'dumbledore'], ['harry', 'potter']],
                    [['aurelius', 'dumbledore'], ['harry', 'potter']]]
        self.assertEqual(result, expected)

    @patch('task_implementation.Task_6_Direct_Connections.preprocess_init', return_value={
        "Processed Sentences": [['sentence1']],
        "Processed Names": []
    })
    def test_self_connection(self, mock_preprocess):
        dc = DirectConnections(threshold=2, question_num=6, window_size=1)
        dc.graph.nodes = {
            'harry potter': PersonNode('harry potter', ['harry', 'potter', 'undesirable', 'number'])
        }

        dc.graph.add_connection('harry potter', 'harry potter', 3)

        result = dc.graph.get_edges()
        self.assertEqual(result, [])

    @patch('task_implementation.Task_6_Direct_Connections.preprocess_init', return_value={
        "Processed Sentences": [['sentence1']],
        "Processed Names": []
    })
    def test_create_nodes_with_aliases(self, mock_preprocess):
        dc = DirectConnections(threshold=2, question_num=6, window_size=1)
        dc.processed_people = [[['harry', 'potter'], [['undesirable', 'number'], ['the', 'boy', 'who', 'lived']]]]
        dc.create_nodes_with_aliases()

        self.assertIn('harry potter', dc.graph.nodes)
        self.assertIn('undesirable number', dc.graph.nodes['harry potter'].aliases)
        self.assertIn('boy', dc.graph.nodes['harry potter'].aliases)

    @patch('task_implementation.Task_6_Direct_Connections.preprocess_init', return_value={
        "Processed Sentences": [['harry', 'potter', 'and', 'hermione', 'granger', 'were', 'at', 'hogwarts']],
        "Processed Names": [[['harry', 'potter'], [['undesirable', 'number'], ['parry', 'otter']]],
                            [['hermione', 'granger'], []]]
    })
    def test_add_edges_from_co_occurrences(self, mock_preprocess):
        dc = DirectConnections(threshold=1, question_num=6, window_size=1)

        dc.create_nodes_with_aliases()
        dc.add_edges_from_co_occurrences()

        result = dc.graph.get_edges()
        expected = [[['harry', 'potter'], ['hermione', 'granger']]]
        self.assertEqual(expected, result)

    @patch('task_implementation.Task_6_Direct_Connections.preprocess_init', return_value={
        "Processed Sentences": [['harry', 'potter', 'ron', 'weasley']],
        "Processed Names": [[['harry', 'potter'], [['undesirable', 'number'], ['parry', 'otter']]],
                            [['ron', 'weasley'], []]]
    })
    def test_invalid_window_size(self, mock_preprocess):
        with self.assertRaises(SystemExit):
            DirectConnections(threshold=1, question_num=6, window_size=-1)

    @patch('task_implementation.Task_6_Direct_Connections.preprocess_init', return_value={
        "Processed Sentences": [['harry', 'potter', 'ron', 'weasley']],
        "Processed Names": [[['harry', 'potter'], [['undesirable', 'number'], ['parry', 'otter']]],
                            [['ron', 'weasley'], []]]
    })
    def test_threshold_zero(self, mock_preprocess):
        dc = DirectConnections(threshold=0, question_num=6, window_size=1)

        result = dc.generate_results()
        expected = {
            "Question 6": {
                "Pair Matches": [[['harry', 'potter'], ['ron', 'weasley']]]
            }
        }
        self.assertEqual(result, expected)

    @patch('task_implementation.Task_6_Direct_Connections.preprocess_init', return_value={
        "Processed Sentences": [['sentence1'], ['sentence2']],
        "Processed Names": []
    })
    def test_window_size_exceeds_sentences(self, mock_preprocess):
        with self.assertRaises(SystemExit):
            DirectConnections(threshold=1, question_num=6, window_size=5)

    @patch('task_implementation.Task_6_Direct_Connections.preprocess_init', return_value={
        "Processed Sentences": [['harry', 'potter', 'ron', 'weasley'], ['harry', 'potter', 'fought', 'ron', 'weasley']],
        "Processed Names": [[['harry', 'potter'], [['undesirable', 'number'], ['parry', 'otter']]],
                            [['ron', 'weasley'], []]]
    })
    def test_generate_results(self, mock_preprocess):
        dc = DirectConnections(threshold=1, question_num=6, window_size=1)

        result = dc.generate_results()
        expected = {
            "Question 6": {
                "Pair Matches": [[['harry', 'potter'], ['ron', 'weasley']]]
            }
        }
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
