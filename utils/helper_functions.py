# Description: Helper functions for the project.
from typing import Set


def load_stopwords(file_path: str) -> Set[str]:
    """
    Load stopwords from a file into a set.
    Args:
        file_path (str): Path to the stopwords file.
    Returns:
        Set[str]: A set of stopwords.
    """
    with open(file_path, 'r') as file:
        return set(line.strip().lower() for line in file)