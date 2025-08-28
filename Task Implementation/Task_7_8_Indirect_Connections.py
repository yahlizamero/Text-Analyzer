# Description: Tasks 7 and 8 implementations.
# The IndirectPaths class is responsible for finding indirect connections between people within a specified distance.
# The class uses a graph representation of the direct connections between people to find indirect connections.
# The class can be used to find indirect connections within a specified distance (Task 7) or of a fixed length (Task 8).
# The class can also preprocess the data if necessary.


import collections
import json
import sys
from collections import defaultdict
from typing import Dict, Any, List
from task_implementation.Task_6_Direct_Connections import DirectConnections, PersonGraph


class IndirectPaths:
    """ Handles processing and graph construction for Task 7. """

    def __init__(
            self,
            question_num: int,
            sentences_path: str = None,
            people_path: str = None,
            stopwords_path: str = None,
            preprocess_path: str = None,
            window_size: int = None,
            threshold: int = None,
            people_connections_path: str = None,
            maximal_distance: int = None,
            K: int = None
    ):
        """
        Initialize the IndirectPaths class.

        :param question_num: The task reference number.
        :param sentences_path: Path to the sentences CSV file.
        :param people_path: Path to the people CSV file.
        :param stopwords_path: Path to the stopwords file.
        :param preprocess_path: Path to the Task 6 graph JSON file. (Optional)
        :param window_size: The size of the window to consider.
        :param threshold: The threshold to use for the direct connections.
        :param people_connections_path: Path to JSON file with list of people pairs to check.
        :param maximal_distance: The maximal allowed distance between two people. (for Task 7)
        :param K: The fixed length of the paths to check. (for Task 8)

        """
        # Initialize class attributes
        self.question_num = question_num
        if self.question_num not in (7, 8):  # Ensure valid question number
            print("Error: Invalid question number. Please provide either 7 or 8.")
            sys.exit(1)
        self.sentences_path = sentences_path
        self.people_path = people_path
        self.stopwords_path = stopwords_path
        self.window_size = window_size
        self.threshold = threshold
        self.people_connections_path = people_connections_path
        self.maximal_distance = maximal_distance
        if self.question_num == 7 and (
                self.maximal_distance is None or self.maximal_distance < 0):  # Ensure maximal distance is provided
            # for Task 7
            print("Error: Maximal distance must be provided for Task 7 and be a non negative integer.")
            sys.exit(1)
        self.K = K
        if self.question_num == 8 and (self.K is None or self.K < 0):  # Ensure K is provided for Task 8
            print("Error: K must be provided for Task 8 and be a non negative integer.")
            sys.exit(1)

        self.people_pairs = []  # Stores people pairs

        if people_connections_path:
            with open(people_connections_path, "r") as file:
                self.people_pairs = json.load(file).get("keys", [])  # Extract only the "keys" list
        else:
            print("No people connections file provided. Please provide a JSON file with a list of people pairs.")
            sys.exit(1)

        # Load graph from Task 6 JSON file if provided
        if preprocess_path:
            try:
                with open(preprocess_path, "r") as file:
                    self.task6_data = json.load(file)
                    # Build the graph from Task 6 using the adjacency list representation
                    self.graph = self.build_graph_from_task6()
            except Exception as e:
                print(f"Error loading preprocessed file: {e}")
                sys.exit(1)

        # Otherwise, reconstruct graph using Task 6
        elif preprocess_path is None:
            if None not in (question_num, sentences_path, people_path, stopwords_path, window_size, threshold):
                # Initialize the DirectConnections class for Task 6
                data = DirectConnections(
                    question_num=6,
                    sentences_path=sentences_path,
                    people_path=people_path,
                    stopwords_path=stopwords_path,
                    window_size=window_size,
                    threshold=threshold)
                self.task6_data = data.generate_results()
                # Build a graph like in Task 6 and use adjacency list representation
                self.graph = self.build_graph_from_task6()

            else:
                print(
                    "Invalid input parameters. Make sure you provided: question_num, sentences_path, people_path, "
                    "stopwords_path, window_size, threshold.")
                sys.exit(1)

    def build_graph_from_task6(self) -> Dict[str, List[str]]:
        """ Builds n adjacency list representation of the graph from Task 6's precomputed results.
            :param: task6_data: The precomputed results from Task 6.
            :return: A dictionary representing the graph."""

        # Initialize a temporary graph to store the connections
        temp_graph = PersonGraph(threshold=0)  # No threshold needed for indirect connections

        # Extract pair matches safely
        pair_matches = self.task6_data.get("Question 6", {}).get("Pair Matches", [])

        # Add people and connections to the graph
        for pair in pair_matches:
            person1 = " ".join(pair[0])
            person2 = " ".join(pair[1])
            temp_graph.add_person(person1, [])
            temp_graph.add_person(person2, [])
            temp_graph.add_connection(person1, person2, 1)  # Fake count of 1 since edges exist

        # Convert the graph to an adjacency list representation
        graph = defaultdict(list)

        for node in temp_graph.nodes.values():
            for neighbor in node.neighbors:
                graph[node.main_name].append(neighbor.main_name)

        return graph

    def find_indirect_connections(self) -> List[List[bool]]:
        """
        Find indirect connections between nodes within a specified distance depending on the question.
        :returns: sorted list of lists where each list contains:
        [person1, person2, boolean indicating if they are connected].
        """
        indirect_matches = []  # List to store results

        if not self.graph or (self.question_num == 8 and self.K == 0) or (
                self.question_num == 8 and self.maximal_distance == 0):  # No connections possible - edge case
            for person1, person2 in self.people_pairs:
                indirect_matches.append([person1, person2, False])  # Automatically mark as False if graph is empty
            return indirect_matches

        for person1, person2 in self.people_pairs:
            if person1 not in self.graph or person2 not in self.graph:
                indirect_matches.append([person1, person2, False])  # Ensure all pairs appear in the final output
                continue

            # Perform BFS to find the shortest distance
            shortest_paths = self.bfs_shortest_paths(person1)
            distance = shortest_paths.get(person2, float('inf'))  # Default to infinite if no path exists

            if self.question_num == 7:
                is_connected = 1 <= distance <= self.maximal_distance
            if self.question_num == 8:
                is_connected = distance == self.K
            indirect_matches.append([person1, person2, is_connected])  # Include boolean value

        return indirect_matches

    # Task 7 implementation
    def bfs_shortest_paths(self, start_node: str) -> Dict[str, int]:
        """
        Performs BFS to find the shortest path from a start node to all other nodes.
        :param start_node: The node to start the search from.
        :return: Dictionary mapping nodes to their shortest distance from start.
        """
        queue = collections.deque([(start_node, 0)])  # Initialize the queue to (start_node, distance)
        distances = {start_node: 0}  # Start node has distance 0 from itself

        while queue:  # Continue until all nodes in the queue have been processed
            node, dist = queue.popleft()  # Dequeue the next node and its distance
            for neighbor in self.graph.get(node, []):  # Iterate over each neighbor of the current node
                if neighbor not in distances:  # If the neighbor wasn't visited yet
                    distances[neighbor] = dist + 1  # Update the distance from the start_node to the neighbor
                    queue.append((neighbor, dist + 1))  # Add neighbor to queue with updated distance

        return distances  # Return the dictionary of shortest distances from the start node

    def generate_results_task_7(self) -> Dict[str, Any]:
        """ Generates the final results for Task 7. """
        indirect_matches = self.find_indirect_connections()

        # Ensure each pair is alphabetically sorted and formatted correctly
        indirect_matches = sorted(
            [[sorted(pair[:2])[0], sorted(pair[:2])[1], pair[2]] for pair in indirect_matches],  # Flatten structure
            key=lambda x: x[:2]  # Sort by first and second name
        )

        return {
            f"Question {self.question_num}": {
                "Pair Matches": indirect_matches
            }
        }

    # Task 8 implementation
    def bfs_exact_paths(self, start_node: str, end_node: str) -> bool:
        """
        Perform BFS to check if there exists a path of exactly length K between start_node and end_node.
        :return: True if a path of exactly length K exists, otherwise False.
        """

        if start_node not in self.graph or end_node not in self.graph:
            return False  # If nodes do not exist in the graph, return False

        queue = collections.deque([(start_node, 0, {start_node})])  # (current node, depth, visited set)

        while queue:  # Continue until all nodes in the queue have been processed
            # Dequeue the next node, depth, and visited set
            node, depth, visited = queue.popleft()  # Added visited to set to prevent revisiting nodes and infinite
            # loops

            if depth == self.K:
                if node == end_node:  # If we reached the end node
                    return True  # Found exact-length path
                continue  # Do not explore further if we reached K steps

            if depth < self.K:
                for neighbor in self.graph.get(node, []):  # Iterate over each neighbor of the current node
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
        # Check each pair of people for a fixed-length path using the BFS algorithm
        for person1, person2 in self.people_pairs:
            person1, person2 = sorted([person1, person2])  # Ensure sorted order
            connection_exists = self.bfs_exact_paths(start_node=person1, end_node=person2)
            result.append([person1, person2, connection_exists])  # connection_exists is a boolean

        # Sort the results alphabetically
        result.sort()
        return result

    def generate_results_task_8(self) -> Dict[str, Any]:
        """ Generates the final results for Task 8. """
        fixed_length_matches = self.find_fixed_length_paths()
        return {
            f"Question {self.question_num}": {
                "Pair Matches": fixed_length_matches
            }
        }



