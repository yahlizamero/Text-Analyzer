
# Description: Implementation of Task 6 - Direct Connections.
# This script finds direct connections between people based on shared contexts.
# The DirectConnections class preprocesses the input data if necessary and generates the final results for Task 6.
# It uses a PersonGraph to represent people as nodes and shared contexts as edges.

import json
import re
from collections import defaultdict
from typing import Dict, Any, List, Tuple
from task_implementation.Task_1_Preprocessing import Preprocessing


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
            data_file: str = None,
            sentences_path: str = None,
            people_path: str = None,
            stopwords_path: str = None,
            preprocess: str = None,
            window_size: int = None,
            threshold: int = None
    ):
        """
        Initialize the DirectConnections class.

        :param question_num: The task reference number.
        :param data_file: Path to the preprocessed JSON file (optional).
        :param sentences_path: Path to the sentences CSV file.
        :param people_path: Path to the people CSV file.
        :param stopwords_path: Path to the stopwords file.
        :param preprocess: Flag indicating if preprocessing is required.
        :param window_size: The size of the window to consider.
        :param threshold: The threshold to use for the direct connections.
        """

        self.question_num = question_num
        self.window_size = window_size
        self.threshold = threshold
        self.graph = PersonGraph(self.threshold)

        # Load preprocessed data or preprocess raw input files
        if preprocess == "--p" and self.questions_num == 6:
            if not data_file:
                raise ValueError("A data file must be provided when preprocess=True.")
            with open(data_file, "r") as file:
                self.data = json.load(file)
        elif preprocess is None:
            if not sentences_path or not stopwords_path or not people_path and self.questions_num == 6:
                raise ValueError("Sentences, people, and stopwords paths must be provided when preprocess=False.")
            self.data = Preprocessing.preprocess_other_tasks(
                sentences_path=sentences_path, stopwords_path=stopwords_path, people_path=people_path
            )
        else:
            raise ValueError("Invalid arguments provided for preprocessing.")

        # Extract relevant processed data
        self.processed_sentences = (
            self.data.get("Question 1", {}).get("Processed Sentences", [])
            if "Question 1" in self.data
            else self.data.get("Processed Sentences", [])
        )

        self.processed_people = (
            self.data.get("Question 1", {}).get("Processed Names", [])
            if "Question 1" in self.data
            else self.data.get("Processed Names", [])
        )

        if not self.processed_sentences or not self.processed_people:
            raise ValueError("The provided data does not contain valid 'Processed Sentences' or 'Processed Names'.")

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
        name_to_sentences = defaultdict(set)

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

