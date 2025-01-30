# Description: Task 7 and 8 implementation.
#


import collections
import json
import time
from collections import defaultdict, deque
from typing import Dict, Any, List, Tuple
from task_implementation.Task_6_Direct_Connections import DirectConnections, PersonGraph, PersonNode
from utils.helper_graphs import load_graph_from_json, build_graph_from_task6


class IndirectPaths:
    """ Handles processing and graph construction for Task 7. """

    def __init__(
            self,
            question_num: int = None,
            people_connections_path: str = None,
            data_file: str = None,
            maximal_distance: int = None,
            sentences_path: str = None,
            people_path: str = None,
            stopwords_path: str = None,
            window_size: int = None,
            threshold: int = None,
            preprocess: str = None,
            K: int = None
    ):
        """
        Initialize the IndirectPaths class.

        :param question_num: The task reference number.
        :param people_connections_path: Path to JSON file with list of people pairs to check.
        :param data_file: Path to the Task 6 graph JSON file. (Optional)
        :param maximal_distance: The maximal allowed distance between two people. (for Task 7)
        :param sentences_path: Path to the sentences CSV file.
        :param people_path: Path to the people CSV file.
        :param stopwords_path: Path to the stopwords file.
        :param window_size: The size of the window to consider.
        :param threshold: The threshold to use for the direct connections.
        :param preprocess: Flag indicating if preprocessing is required.
        :param K: The fixed length of the paths to check. (for Task 8)

        """
        # Initialize class attributes
        self.question_num = question_num
        self.people_connections_path = people_connections_path
        self.data_file = data_file
        self.maximal_distance = maximal_distance
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
                self.people_pairs = json.load(file).get("keys", [])  # ✅ Extract only the "keys" list

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

            if self.question_num == 7:
                is_connected = 1 <= distance <= self.maximal_distance
            if self.question_num == 8:
                is_connected = distance == self.K
            indirect_matches.append([person1, person2, is_connected])  # Include boolean value

        return sorted(indirect_matches)  # Ensure output is sorted

    # Task 7 implementation
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

    def generate_results_task_7(self) -> Dict[str, Any]:
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

    # Task 8 implementation

    def bfs_exact_paths(self, graph: Dict[str, List[str]], start: str, end: str) -> bool:
        """
        Perform BFS to check if there exists a path of exactly length K between start and end.
        :return: True if a path of exactly length K exists, otherwise False.
        """
        print(f"DEBUG: Checking exact path of length {self.K} from '{start}' to '{end}'")

        if start not in graph or end not in graph:
            return False  # If nodes do not exist, return False

        queue = collections.deque([(start, 0, {start})])  # (current node, depth, visited set)

        while queue:
            node, depth, visited = queue.popleft()

            if depth == self.K:
                if node == end:
                    return True  # Found exact-length path
                continue  # Do not explore further if we reached K steps

            if depth < self.K:
                for neighbor in graph.get(node, []):
                    if neighbor not in visited:  # Prevent revisiting nodes in the same path
                        queue.append(
                            (neighbor, depth + 1, visited | {neighbor}))  # Add neighbor with updated visited set

        return False  # No valid path found

    def find_fixed_length_paths(self) -> list[list[bool]]:
        """
        Find whether each pair of people is connected by exactly length K.
        :return: A sorted list of results.
        """
        result = []
        for person1, person2 in self.people_pairs:
            person1, person2 = sorted([person1, person2])  # Ensure sorted order
            connection_exists = self.bfs_exact_paths(graph=self.build_graph(), start=person1, end=person2)
            result.append([person1, person2, connection_exists])

        # Sort the results alphabetically
        result.sort()
        return result

    def generate_results_task_8(self) -> Dict[str, Any]:
        """ Generates the final results for Task 8. """
        start_time = time.time()  # Track execution time
        fixed_length_matches = self.find_fixed_length_paths()
        end_time = time.time()
        runtime = end_time - start_time

        print(f"DEBUG: Task 8 execution time for K={self.K}: {runtime:.4f} seconds")

        return {
            f"Question {self.question_num}": {
                "Pair Matches": fixed_length_matches
            }
        }


if __name__ == "__main__":
    # Example usage
    indirect_connections = IndirectPaths(
        question_num=7,
        sentences_path="examples 27.1/Q7_examples/example_3/sentences_small_3.csv",
        people_path="examples 27.1/Q7_examples/example_3/people_small_3.csv",
        stopwords_path="Data 27.1/REMOVEWORDS.csv",
        people_connections_path="examples 27.1/Q7_examples/example_3/people_connections_3.json",
        # data_file="examples 27.1/Q6_examples/example_1/Gen_result_Q6_1.json",
        # preprocess="--p",
        window_size=5,
        threshold=1,
        # K=2,
        maximal_distance=1000,
    )

    # Generate results
    results = indirect_connections.generate_results_task_7()
    # results = indirect_connections.generate_results_task_8()
    # Print results
    print(json.dumps(results, indent=4))

    # Save results to a file
    output_file = "examples 27.1/Q7_examples/example_3/Gen_result_Q7_3.json"
    with open(output_file, "w") as file:
        json.dump(results, file, indent=4)
    print(f"JSON results saved to {output_file}")
