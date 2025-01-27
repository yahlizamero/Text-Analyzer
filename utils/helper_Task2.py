from typing import Any, Dict
import json, os
from task_implementation.Task_1_Preprocessing import Preprocessing


def load_data(self, data_file: str) -> Dict[str, Any]:
    """
    Load data from the input JSON or preprocess it from CSV if needed.

    :return: Parsed JSON data as a dictionary.
    """
    if self.preprocess:
        try:
            with open(self.data_file, 'r') as file:
                return json.load(file)
        except Exception as e:
            raise FileNotFoundError(f"Error loading JSON data file: {e}")
        finally:
            file.close()
    elif self.data_file.endswith('.csv'):
        return self.preprocess_data()
    else:
        raise ValueError("Unsupported file format. Only JSON and CSV are allowed.")


def load_preprocessed_data(self, data_file: str) -> Dict[str, Any]:
    """Load preprocessed data from a JSON file."""
    with open(data_file, "r") as file:
        return json.load(file)


def save_to_json(output_path: str, process_function: callable) -> None:
    processed_data = process_function()
    try:
        with open(output_path, "w") as file:
            json.dump(processed_data, file, indent=4)
    except Exception as e:
        raise IOError(f"Error saving output file: {e}")
