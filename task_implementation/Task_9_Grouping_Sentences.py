# Description: Implementation of Task 9: Grouping Sentences.
# This script is used to group sentences based on shared words.
# The SentenceGraph class builds a graph where nodes are sentences and edges exist based on shared words.
# The groups of connected sentences are then found using BFS.
# The SentenceClustering class initializes the SentenceGraph and generates the final results for Task 9.

import json
import collections
from typing import List, Dict, Any
from itertools import combinations
from task_implementation.Task_1_Preprocessing import Preprocessing


class SentenceGraph:
    """Graph representation where nodes are sentences and edges exist based on shared words."""

    def __init__(self, threshold: int):
        """ Initialize the SentenceGraph class.
        :param threshold: A minimum number of shared words required for sentence connection.
        """

        self.sentences = []  # List of sentences
        self.graph = collections.defaultdict(set)  # Adjacency list representation
        self.threshold = threshold  # Minimum shared word count for an edge

    def add_sentence(self, sentence: str):
        """Adds a sentence to the graph."""

        self.sentences.append(sentence)

    def build_graph(self):
        """Creates edges between sentences that share at least `threshold` words."""
        for i, j in combinations(range(len(self.sentences)), 2):  # Generate all pairs of sentences
            common_words = set(self.sentences[i]) & set(self.sentences[j])  # Set intersection
            if len(common_words) >= self.threshold:
                self.graph[i].add(j)
                self.graph[j].add(i)

    def find_groups(self) -> List[List[str]]:
        """Finds groups of connected sentences using BFS."""

        visited = set()
        groups = []

        for i in range(len(self.sentences)):
            if i not in visited:
                queue = collections.deque([i])
                group = []
                while queue:
                    node = queue.popleft()
                    if node not in visited:
                        visited.add(node)
                        group.append(" ".join(self.sentences[node]))  # Convert back to full sentence
                        queue.extend(self.graph[node])
                groups.append(sorted(group))  # Sort sentences within each group

        return sorted(groups, key=lambda g: (len(g), g))  # Sort groups by size, then alphabetically


class SentenceClustering:
    def __init__(self, question_num: int, sentences_path: str = None, stopwords_path: str = None,
                 threshold: int = None, preprocess: str = None, data_file: str = None):
        """
        Initialize the SentenceClustering class.

        :param question_num: Task reference number.
        :param sentences_path: Path to the sentences file.
        :param stopwords_path: Path to the stopwords file.
        :param threshold: Minimum number of shared words required for sentence connection.
        :param preprocess: Preprocessing flag.
        :param data_file: Path to preprocessed JSON file (if available).
        """
        self.question_num = question_num
        self.threshold = threshold

        if preprocess == "--p":
            if not data_file:
                raise ValueError("A data file must be provided when preprocess=True.")
            with open(data_file, "r") as file:
                self.sentences = json.load(file).get("Processed Sentences", [])
        else:
            if not sentences_path or not stopwords_path:
                raise ValueError("Sentences and stopwords paths must be provided when preprocess=False.")
            self.sentences = Preprocessing.preprocess_other_tasks(sentences_path, stopwords_path)
            self.sentences = self.sentences.get("Processed Sentences", [])

    def generate_results(self) -> Dict[str, Any]:
        """Generates the final results for Task 9."""
        graph = SentenceGraph(self.threshold)

        # Add sentences as lists of words (preprocessed sentences)
        for sentence in self.sentences:
            graph.add_sentence(sentence)

        graph.build_graph()
        groups = graph.find_groups()

        formatted_groups = [
            [f"Group {i + 1}", [sentence.split() for sentence in group]]
            for i, group in enumerate(groups)
        ]

        return {f"Question {self.question_num}": {"group Matches": formatted_groups}}

