import json
from deepdiff import DeepDiff


def compare_json_files(file1_path, file2_path):
    """
    Compare two JSON files and print the differences.
    :param file1_path: Path to the first JSON file.
    :param file2_path: Path to the second JSON file.
    """
    try:
        with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
            json1 = json.load(file1)
            json2 = json.load(file2)

        # Compare the two JSON objects
        diff = DeepDiff(json1, json2, view='tree')

        if not diff:
            print("The two JSON files are identical!")
        else:
            print("Differences found between the two JSON files:")
            print(diff)

    except Exception as e:
        print(f"An error occurred while comparing JSON files: {e}")


# Example usage
if __name__ == "__main__":
    file1_path = "/Users/YAHLIZ/Library/CloudStorage/GoogleDrive-yahli.zamero@mail.huji.ac.il/My Drive/Intro to CS/text_analyzer/examples/Q1_examples/example_2/Q1_result2.json"
    file2_path = "/Users/YAHLIZ/Library/CloudStorage/GoogleDrive-yahli.zamero@mail.huji.ac.il/My Drive/Intro to CS/text_analyzer/examples/Q1_examples/example_2/generated_Q2_result.json"
    compare_json_files(file1_path, file2_path)