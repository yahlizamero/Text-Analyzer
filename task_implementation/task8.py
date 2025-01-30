import collections
import json
import time
from collections import defaultdict, deque
from typing import Dict, Any, List, Tuple
from task_implementation.Task_6_Direct_Connections import DirectConnections, PersonGraph
from utils.helper_graphs import build_graph_from_task6

class IndirectPaths:
    def __init__(
        self,
        question_num: int,
        people_connections_path: str,
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
        self.task6_data = None
        self.people_pairs = []

        with open(people_connections_path, "r") as file:
            self.people_pairs = json.load(file).get("keys", [])

        if preprocess == "--p":
            with open(data_file, "r") as file:
                self.task6_data = json.load(file)
                self.graph = build_graph_from_task6(self.task6_data)
        else:
            self.task6_data = DirectConnections(
                question_num=6,
                sentences_path=sentences_path,
                people_path=people_path,
                stopwords_path=stopwords_path,
                window_size=window_size,
                threshold=threshold)
            self.graph = build_graph_from_task6(self.task6_data.generate_results())

    def build_graph(self) -> Dict[str, List[str]]:
        graph = defaultdict(list)
        for node in self.graph.nodes.values():
            for neighbor in node.neighbors:
                graph[node.main_name].append(neighbor.main_name)
        return graph

    def bfs_exact_paths(self, graph: Dict[str, List[str]], start: str, end: str) -> bool:
        if start not in graph or end not in graph:
            return False
        queue = deque([(start, 0)])
        visited = {start}
        while queue:
            node, depth = queue.popleft()
            if depth == self.K and node == end:
                return True
            if depth < self.K:
                for neighbor in graph.get(node, []):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, depth + 1))
        return False

    def find_fixed_length_paths(self) -> List[List[Any]]:
        graph = self.build_graph()
        result = []
        for person1, person2 in self.people_pairs:
            person1, person2 = sorted([person1, person2])
            connection_exists = self.bfs_exact_paths(graph, person1, person2)
            result.append([person1, person2, connection_exists])
        return sorted(result)

    def generate_results_task_8(self) -> Dict[str, Any]:
        start_time = time.time()
        fixed_length_matches = self.find_fixed_length_paths()
        end_time = time.time()
        runtime = end_time - start_time
        print(f"DEBUG: Task 8 execution time for K={self.K}: {runtime:.4f} seconds")
        return {f"Question {self.question_num}": {"Pair Matches": fixed_length_matches}}

if __name__ == "__main__":
    indirect_connections = IndirectPaths(
        question_num=8,
        sentences_path="examples 27.1/Q8_examples/example_2/sentences_small_2.csv",
        people_path="examples 27.1/Q7_examples/example_2/people_small_2.csv",
        stopwords_path="Data 27.1/REMOVEWORDS.csv",
        people_connections_path="examples 27.1/Q8_examples/example_2/people_connections_2.json",
        # data_file="examples 27.1/Q6_examples/example_1/Gen_result_Q6_1.json",
        # preprocess="--p",
        window_size=3,
        threshold=2,
        K=3,
    )
    results = indirect_connections.generate_results_task_8()
    print(json.dumps(results, indent=4))
    with open("examples 27.1/Q8_examples/example_2/Gen_result_Q8_2.json", "w") as file:
        json.dump(results, file, indent=4)
    print("JSON results saved.")
