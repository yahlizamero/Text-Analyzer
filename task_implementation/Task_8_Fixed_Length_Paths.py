import collections
import json
from collections import defaultdict, deque
from typing import Dict, Any, List, Tuple
from task_implementation.Task_7_Indirect_Connections import IndirectConnections
from utils.helper_graphs import load_graph_from_json, build_graph_from_task6


class FixedLengthPaths:
    """ Handles processing and graph construction for Task 7. """

    def __init__(
            self,
            question_num: int,
            people_connections_path: str = None,
            data_file: str = None,
            sentences_path: str = None,
            people_path: str = None,
            stopwords_path: str = None,
            window_size: int = None,
            threshold: int = None,
            preprocess: str = None,
            K: int = None
    ):
        """
        Initialize the IndirectConnections class.

        :param question_num: The task reference number.
        :param people_connections_path: Path to JSON file with list of people pairs to check.
        :param data_file: Path to the Task 6 graph JSON file. (Optional)
        :param sentences_path: Path to the sentences CSV file.
        :param people_path: Path to the people CSV file.
        :param stopwords_path: Path to the stopwords file.
        :param window_size: The size of the window to consider.
        :param threshold: The threshold to use for the direct connections.
        :param preprocess: Flag indicating if preprocessing is required.
        :param K: The fixed length of the paths to check.

        """
        # Initialize class attributes
        self.question_num = question_num
        self.people_connections_path = people_connections_path
        self.data_file = data_file
        self.sentences_path = sentences_path
        self.people_path = people_path
        self.stopwords_path = stopwords_path
        self.window_size = window_size
        self.threshold = threshold
        self.K = K

        self.task6_data = None  # Graph instance for storing nodes & edges
        self.people_pairs = []  # Stores people pairs

        if people_connections_path:
            with open(people_connections_path, "r") as file:
                self.people_pairs = json.load(file).get("keys", [])  # Extract only the "keys" list

        # Load graph from Task 6 JSON file if provided
        if preprocess == "--p":
            if not data_file:
                raise ValueError("A people_connections file must be provided when preprocess=True.")

            with open(data_file, "r") as file:
                self.task6_data = json.load(file)
                self.graph = build_graph_from_task6(self.task6_data)


        # Otherwise, reconstruct graph using Task 6
        elif preprocess is None:
            self.task6_data = DirectConnections(
                question_num=6,
                sentences_path=sentences_path,
                people_path=people_path,
                stopwords_path=stopwords_path,
                window_size=window_size,
                threshold=threshold)

            # Getting the format of the result of task 6 (inside the JSON)
            output = DirectConnections.generate_results(self.task6_data)

            # Build a graph in order to process information
            self.graph = build_graph_from_task6(self.task6_data)

        else:
            raise ValueError("Invalid arguments provided for preprocessing.")

        if not self.task6_data:
            raise ValueError("Graph could not be initialized.")

    def build_graph(self) -> Dict[str, List[str]]:

        """ Converts Task 6 graph object into an adjacency list representation. """

        graph = defaultdict(list)

        for node in self.graph.nodes.values():
            for neighbor in node.neighbors:
                graph[node.main_name].append(neighbor.main_name)

        return graph

    def find_indirect_connections(self) -> List[List[Any]]:
        """
        Find indirect connections between nodes within the specified max distance.
        Returns a sorted list of lists where each list contains:
        [person1, person2, boolean indicating if they are connected].
        """
        graph = self.build_graph()
        indirect_matches = []

        if not graph:
            return []

        for person1, person2 in self.people_pairs:
            if person1 not in graph or person2 not in graph:
                indirect_matches.append([person1, person2, False])  # Ensure all pairs appear in the output
                continue

            # Perform BFS to find the shortest distance
            shortest_paths = self.bfs_shortest_paths(graph, person1)
            distance = shortest_paths.get(person2, float('inf'))  # Default to infinite if no path

            is_connected = 1 <= distance <= self.maximal_distance
            indirect_matches.append([person1, person2, is_connected])  # Include boolean value

        return sorted(indirect_matches)  # Ensure output is sorted

    def bfs_shortest_paths(self, graph: Dict[str, List[str]], start: str) -> Dict[str, int]:
        """
        Performs BFS to find the shortest path from a start node to all other nodes.
        :return: Dictionary mapping nodes to their shortest distance from start.
        """
        queue = collections.deque([(start, 0)])
        distances = {start: 0}

        while queue:
            node, dist = queue.popleft()
            for neighbor in graph.get(node, []):
                if neighbor not in distances:  # Not visited yet
                    distances[neighbor] = dist + 1
                    queue.append((neighbor, dist + 1))

        return distances

    def generate_results(self) -> Dict[str, Any]:
        """ Generates the final results for Task 7. """
        indirect_matches = self.find_indirect_connections()

        # Ensure each pair is alphabetically sorted and formatted correctly
        indirect_matches = sorted(
            [(sorted(pair[:2])[0], sorted(pair[:2])[1], pair[2]) for pair in indirect_matches],  # Flatten structure
            key=lambda x: x[:2]  # Sort by first and second name
        )

        return {
            f"Question {self.question_num}": {
                "Pair Matches": indirect_matches
            }
        }


if __name__ == "__main__":
    # Example usage
    indirect_connections = IndirectConnections(
        question_num=7,
        # sentences_path="examples 27.1/Q7_examples/example_4/sentences_small_4.csv",
        # people_path="examples 27.1/Q7_examples/example_4/people_small_4.csv",
        # stopwords_path="Data 27.1/REMOVEWORDS.csv",
        people_connections_path="examples 27.1/Q7_examples/example_4/people_connections_4.json",
        data_file="examples 27.1/Q6_examples/example_1/Gen_result_Q6_1.json",
        preprocess="--p",
        window_size=3,
        threshold=2,
        maximal_distance=1000,
    )

    # Generate results
    results = indirect_connections.generate_results()
    # Print results
    print(json.dumps(results, indent=4))

    # Save results to a file
    output_file = "examples 27.1/Q7_examples/example_4/Gen_result_Q7_d.json"
    with open(output_file, "w") as file:
        json.dump(results, file, indent=4)
    print(f"JSON results saved to {output_file}")
