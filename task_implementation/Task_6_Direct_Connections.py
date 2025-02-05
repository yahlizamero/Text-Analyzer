# Description: Implementation of Task 6 - Direct Connections.
# This script finds direct connections between people based on shared contexts.
# The DirectConnections class preprocesses the input data if necessary and generates the final results for Task 6.
# It uses a PersonGraph to represent people as nodes and shared contexts as edges.

import json
import re
import sys
from collections import defaultdict
from typing import Dict, Any, List, Tuple
from utils.helper import preprocess_init


class PersonNode:
    """ Represents a person in the graph with their main name, aliases, and connections. """

    def __init__(self, main_name: str, aliases: List[str]):
        self.main_name = main_name
        self.aliases = set(aliases)  # Store aliases including partial names
        self.neighbors = set()  # Store PersonNode references

    def add_neighbor(self, other: "PersonNode"):
        """ Connect this node to another person (undirected graph). """
        if other != self:  # Prevent self-loops
            self.neighbors.add(other)


class PersonGraph:
    """ Represents an undirected graph of people with edges based on co-occurrence in k-seqs. """

    def __init__(self, threshold: int):
        self.nodes: Dict[str, PersonNode] = {}  # Dictionary {person_name -> PersonNode}
        self.threshold = threshold  # Minimum co-occurrence count required for an edge

    def add_person(self, main_name: str, aliases: List[str]):
        """ Adds a new person node if not already in the graph. """
        if main_name not in self.nodes:
            self.nodes[main_name] = PersonNode(main_name, aliases)

    def add_connection(self, person1: str, person2: str, count: int):
        """ Adds an edge between two people if they meet the threshold. """
        if count >= self.threshold:
            node1 = self.nodes.get(person1)
            node2 = self.nodes.get(person2)
            if node1 and node2:
                node1.add_neighbor(node2)
                node2.add_neighbor(node1)

    def get_edges(self) -> List[List[List[str]]]:
        """ Returns a sorted list of unique edges in nested list format. """
        edges = set()
        for node in self.nodes.values():
            for neighbor in node.neighbors:
                edge = tuple(sorted([node.main_name, neighbor.main_name]))
                edges.add(edge)

        return sorted([[name.split() for name in edge] for edge in edges])  # Nested list format


class DirectConnections:
    """ Handles processing and graph construction for Task 6. """

    def __init__(
            self,
            question_num: int,
            sentences_path: str = None,
            people_path: str = None,
            stopwords_path: str = None,
            preprocess_path: str = None,
            window_size: int = None,
            threshold: int = None
    ):
        """
        Initialize the DirectConnections class.

        :param question_num: The task reference number.
        :param sentences_path: Path to the sentences CSV file.
        :param people_path: Path to the people CSV file.
        :param stopwords_path: Path to the stopwords file.
        :param preprocess_path: Path to the preprocessed JSON file (optional).
        :param window_size: The size of the window to consider.
        :param threshold: The threshold to use for the direct connections.
        """

        self.question_num = question_num
        self.window_size = window_size
        self.threshold = threshold
        self.graph = PersonGraph(self.threshold)

        # Load the preprocessed data or preprocess it from raw data
        self.data = preprocess_init(preprocess_path, sentences_path, people_path, stopwords_path)

        # Extract processed data
        self.processed_sentences = self.data.get("Processed Sentences", [])
        self.processed_people = self.data.get("Processed Names", [])

        self.validate_inputs()

    def validate_inputs(self):
        """ Validate window size and threshold inputs. """
        if self.window_size is None or self.window_size < 0:
            print("Error: Window size (K) must be provided and non-negative.")
            sys.exit(1)
        if self.threshold is None or self.threshold < 0:
            print("Error: Threshold (T) must be provided and non-negative.")
            sys.exit(1)
        if self.window_size > len(self.processed_sentences):
            print("Error: Window size (K) cannot exceed the number of sentences.")
            sys.exit(1)

    def create_nodes_with_aliases(self):
        """ Creates nodes with aliases and assigns them to the graph. """
        for person in self.processed_people:
            main_name = " ".join(person[0])
            aliases = {" ".join(alias) for alias in person[1]}
            partial_names = {word for full_name in [main_name] + list(aliases) for word in full_name.split()}
            all_names = {main_name} | aliases | partial_names

            self.graph.add_person(main_name, list(all_names))

    def add_edges_from_co_occurrences(self):
        """ Adds edges to the graph based on co-occurrences in shared windows of sentences. """

        # No edges if window size is 0 or threshold is greater than the number of sentences
        if self.window_size == 0 or (self.threshold > len(self.processed_sentences) and self.window_size > 1):
            return []

        name_to_sentences = defaultdict(set)

        # Map names to the sentences they appear in
        for main_name, node in self.graph.nodes.items():
            for sentence in self.processed_sentences:
                sentence_text = " ".join(sentence)

                # Ensure alias matches as a standalone word
                if any(re.search(rf'\b{name}\b', sentence_text) for name in node.aliases):
                    name_to_sentences[main_name].add(tuple(sentence))

        # Co-occurrence dictionary for counting shared windows
        co_occurrence_counts = defaultdict(int)

        # Identify valid co-occurrences in windows
        for i in range(len(self.processed_sentences) - self.window_size + 1):
            window_sentences = self.processed_sentences[i:i + self.window_size]

            people_in_window = set()
            for sentence in window_sentences:
                sentence_text = " ".join(sentence)
                for main_name, node in self.graph.nodes.items():
                    if any(re.search(rf'\b{name}\b', sentence_text) for name in node.aliases):
                        people_in_window.add(main_name)

            # Count co-occurrences
            people_list = sorted(people_in_window)
            for j in range(len(people_list)):
                for k in range(j + 1, len(people_list)):
                    co_occurrence_counts[(people_list[j], people_list[k])] += 1

        # Add valid edges based on threshold
        for (person1, person2), count in co_occurrence_counts.items():
            self.graph.add_connection(person1, person2, count)

    def generate_results(self) -> Dict[str, Any]:
        """ Generates the final results for Task 6. """
        self.create_nodes_with_aliases()
        self.add_edges_from_co_occurrences()

        return {
            f"Question {self.question_num}": {
                "Pair Matches": self.graph.get_edges()
            }
        }
