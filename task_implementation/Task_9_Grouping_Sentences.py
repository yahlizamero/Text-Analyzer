# Description: Implementation of Task 9: Grouping Sentences.
# This script is used to group sentences based on shared words.
# The SentenceGraph class builds a graph where nodes are sentences and edges exist based on shared words.
# The groups of connected sentences are then found using BFS.
# The SentenceClustering class initializes the SentenceGraph and generates the final results for Task 9.

import sys
import collections
from typing import List, Dict, Any
from itertools import combinations
from utils.helper import preprocess_init


class SentenceGraph:
    """Graph representation where nodes are sentences and edges exist based on shared words."""

    def __init__(self, threshold: int):
        """ Initialize the SentenceGraph class.
        :param threshold: A minimum number of shared words required for sentence connection.
        """

        self.sentences = []  # List of sentences
        self.graph = collections.defaultdict(set)  # Adjacency list representation, i.e., {node: {connected nodes}}
        self.threshold = threshold  # Minimum shared word count for an edge

    def add_sentence(self, sentence: str):
        """Adds a sentence to the graph."""

        self.sentences.append(sentence)

    def build_graph(self):
        """Creates edges between sentences that share at least `threshold` words."""

        for i, j in combinations(range(len(self.sentences)), 2):  # Generate all pairs of sentences
            common_words = set(self.sentences[i]) & set(self.sentences[j])  # Set intersection based on shared words
            if len(common_words) >= self.threshold:  # Add an edge if the shared word count is at least the threshold
                # Add an edge between the two sentences
                self.graph[i].add(j)
                self.graph[j].add(i)

    def find_groups(self) -> List[List[str]]:
        """Finds groups of connected sentences using BFS.
            :Returns: a list of groups of sentences. Each group is a list of sentences. """

        visited = set()  # Keeps track of sentences we've already checked
        groups = []  # List of groups of connected sentences

        for i in range(len(self.sentences)):  # Iterate over all sentences
            if i not in visited:
                queue = collections.deque([i])  # Initialize queue with the current sentence
                group = []  # List of sentences in the current group
                while queue:
                    node = queue.popleft()
                    if node not in visited:
                        visited.add(node)  # Mark it as visited
                        group.append(" ".join(self.sentences[node]))  # Convert back to full sentence
                        # Add all connected sentences to the queue to be processed, because of adjacency list
                        queue.extend(self.graph[node])
                groups.append(sorted(group))  # Once a group is complete, sort its sentences alphabetically

        return sorted(groups, key=lambda g: (len(g), g))  # Sort groups by size, then alphabetically


class SentenceClustering:
    def __init__(self, question_num: int, sentences_path: str = None, stopwords_path: str = None,
                 threshold: int = None, preprocess_path: str = None):
        """
        Initialize the SentenceClustering class.

        :param question_num: Task reference number.
        :param sentences_path: Path to the sentences file.
        :param stopwords_path: Path to the stopwords file.
        :param threshold: Minimum number of shared words required for sentence connection.
        :param preprocess_path: Path to preprocessed JSON file (if available).
        """
        self.question_num = question_num
        self.threshold = threshold
        if threshold < 0:
            print("Error: The threshold should be a positive integer.")
            sys.exit(1)

        # Load the preprocessed sentences weather from a preprocessed file or preprocess it from raw data
        data = preprocess_init(preprocess_path, sentences_path, None, stopwords_path)
        self.sentences = data.get("Processed Sentences", [])  # List of preprocessed sentences

    def generate_results(self) -> Dict[str, Any]:
        """Generates the final results for Task 9."""

        graph = SentenceGraph(self.threshold)  # Initialize the SentenceGraph
        # Add sentences to the graph where each sentence is a list of words (preprocessed sentences)
        for sentence in self.sentences:
            graph.add_sentence(sentence)

        if self.threshold == 0:
            # If threshold is zero, treat each sentence as its own group
            formatted_groups = [
                [f"Group {i + 1}", [sentence]]  # Each sentence is its own group
                for i, sentence in enumerate(self.sentences)
            ]
        else:
            # If threshold > 0, proceed with building the graph and finding groups
            graph.build_graph()
            groups = graph.find_groups()  # Find groups of connected sentences
            formatted_groups = [
                [f"Group {i + 1}", [sentence.split() for sentence in group]]  # Convert back to list of words
                for i, group in enumerate(groups)  # Add numbers for each group
            ]

        return {f"Question {self.question_num}": {"group Matches": formatted_groups}}
