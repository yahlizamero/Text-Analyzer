from task_implementation.Task_6_Direct_Connections import DirectConnections, PersonGraph
import json
from typing import Dict, Any


# def build_graph_from_scratch(sentences_path: str, people_path: str, stopwords_path: str, window_size: int,
#                              threshold: int) -> PersonGraph:
#     """ Builds a new graph in task 6's format using Task 6's DirectConnections. """
#
#     new_graph = DirectConnections(
#         question_num=6,
#         sentences_path=sentences_path,
#         people_path=people_path,
#         stopwords_path=stopwords_path,
#         window_size=window_size,
#         threshold=threshold  # Use the same threshold as Task 6
#     )
#     return new_graph.graph  # Return the built graph


def load_graph_from_json(threshold: int, people_connections_path: str) -> PersonGraph:
    """ Loads a precomputed graph from Task 6's JSON output. """

    with open(people_connections_path, "r") as file:
        data = json.load(file)

    graph = PersonGraph(threshold)

    return graph


def build_graph_from_task6(task6_output: Any) -> PersonGraph:
    """ Builds a graph from Task 6's precomputed results. """

    graph = PersonGraph(threshold=0)  # No threshold needed for indirect connections

    # Ensure task6_output is a dictionary
    if isinstance(task6_output, DirectConnections):
        task6_output = task6_output.generate_results()

    # Extract pair matches safely
    pair_matches = task6_output.get("Question 6", {}).get("Pair Matches", [])

    # Add people and connections to the graph
    for pair in pair_matches:
        person1 = " ".join(pair[0])
        person2 = " ".join(pair[1])

        graph.add_person(person1, [])
        graph.add_person(person2, [])
        graph.add_connection(person1, person2, 1)  # Fake count of 1 since edges exist

    return graph