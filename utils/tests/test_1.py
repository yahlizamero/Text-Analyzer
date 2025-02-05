import unittest
from unittest.mock import patch, mock_open
from task_implementation.Task_1_Preprocessing import Preprocessing, clean_text


class TestPreprocessing(unittest.TestCase):

    def setUp(self):
        self.sample_sentences = "sentence\nHarry Potter was here.\nJohn the Potter left the city."
        self.sample_people = "Name,Other Names\nHarry Potter,The Boy Who Lived\nJohn Potter,Johnny"
        self.stopwords = {"was", "the", "left"}

    @patch("builtins.open", new_callable=mock_open, read_data="was\nthe\nleft")
    def test_load_stopwords_file(self, mock_file):
        stopwords = Preprocessing.load_stopwords_file("fake_path")
        self.assertEqual(stopwords, {"was", "the", "left"})

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_stopwords_file_missing(self, mock_file):
        with self.assertRaises(SystemExit):
            Preprocessing.load_stopwords_file("missing_stopwords.txt")

    def test_clean_text(self):
        text = "Ha!rry Po-tter was here!"
        cleaned = clean_text(text, self.stopwords)
        self.assertEqual(cleaned, "ha rry po tter here")

    @patch("builtins.open", new_callable=mock_open,
           read_data="sentence\nHarry Potter was here.\nJohn the Potter left the city.")
    @patch("os.path.exists", return_value=True)
    @patch("os.path.getsize", return_value=100)
    def test_preprocess_sentences(self, mock_size, mock_exists, mock_file):
        preprocessor = Preprocessing(question_num=1, sentences_path="fake_sentences.csv",
                                     stopwords_path="fake_stopwords.txt")
        preprocessor.stopwords = self.stopwords
        result = preprocessor.preprocess_sentences()
        self.assertEqual(result, [["harry", "potter", "here"], ["john", "potter", "city"]])

    @patch("builtins.open", new_callable=mock_open, read_data="sentence\n")
    @patch("os.path.exists", return_value=True)
    @patch("os.path.getsize", return_value=100)
    def test_preprocess_sentences_empty(self, mock_size, mock_exists, mock_file):
        preprocessor = Preprocessing(question_num=1, sentences_path="fake_sentences2.csv",
                                     stopwords_path="fake_stopwords2.txt")
        preprocessor.stopwords = self.stopwords
        result = preprocessor.preprocess_sentences()
        self.assertEqual(result, [])

    @patch("builtins.open", new_callable=mock_open,
           read_data="Name,Other Names\nHarry Potter,The Boy Who Lived\nJohn Potter,Johnny two shoes")
    @patch("os.path.exists", return_value=True)
    @patch("os.path.getsize", return_value=100)
    def test_preprocess_people(self, mock_size, mock_exists, mock_file):
        preprocessor = Preprocessing(question_num=1, people_path="fake_people.csv", stopwords_path="fake_stopwords.txt")
        preprocessor.stopwords = self.stopwords
        result = preprocessor.preprocess_people()
        expected_result = [[["harry", "potter"], [["boy", "who", "lived"]]],
                           [["john", "potter"], [["johnny", "two", "shoes"]]]]
        self.assertEqual(result, expected_result)

    @patch("builtins.open", new_callable=mock_open, read_data="Name,Other Names\n")
    @patch("os.path.exists", return_value=True)
    @patch("os.path.getsize", return_value=100)
    def test_preprocess_people_empty(self, mock_size, mock_exists, mock_file):
        preprocessor = Preprocessing(question_num=1, people_path="fake_people.csv",
                                     stopwords_path="fake_stopwords.txt")
        preprocessor.stopwords = self.stopwords
        result = preprocessor.preprocess_people()
        self.assertEqual(result, [])

    @patch("builtins.open")
    @patch("os.path.exists", return_value=True)
    @patch("os.path.getsize", return_value=100)
    def test_generate_results(self, mock_size, mock_exists, mock_open_function):
        mock_files = {
            "fake_stopwords.txt": "was\nthe\nleft",
            "fake_sentences.csv": "sentence\nHarry Potter was here.\nJohn the Potter left the city.",
            "fake_people.csv": "Name,Other Names\nHarry Potter,The Boy Who Lived\nJohn Potter,Johnny two shoes"
        }

        def mock_file_open(file, *args, **kwargs):
            return mock_open(read_data=mock_files[file]).return_value

        mock_open_function.side_effect = mock_file_open

        preprocessor = Preprocessing(
            question_num=1,
            sentences_path="fake_sentences.csv",
            people_path="fake_people.csv",
            stopwords_path="fake_stopwords.txt"
        )

        result = preprocessor.generate_results()

        expected_result = {
            'Question 1': {
                'Processed Sentences': [['harry', 'potter', 'here'], ['john', 'potter', 'city']],
                'Processed Names': [
                    [['harry', 'potter'], [['boy', 'who', 'lived']]],
                    [['john', 'potter'], [['johnny', 'two', 'shoes']]]
                ]
            }
        }

        self.assertEqual(result, expected_result)

    @patch("builtins.open")
    @patch("os.path.exists", return_value=True)
    @patch("os.path.getsize", side_effect=lambda path: 0 if "empty" in path else 100)
    def test_generate_results_with_empty_files(self, mock_size, mock_exists, mock_open_function):
        mock_files = {
            "fake_stopwords.txt": "",
            "fake_sentences_empty.csv": "sentence\n",
            "fake_people_empty.csv": "Name,Other Names\n"
        }

        def mock_file_open(file, *args, **kwargs):
            return mock_open(read_data=mock_files[file]).return_value

        mock_open_function.side_effect = mock_file_open

        with self.assertRaises(SystemExit):
            Preprocessing(
                question_num=1,
                sentences_path="fake_sentences_empty.csv",
                people_path="fake_people_empty.csv",
                stopwords_path="fake_stopwords.txt"
            )

    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_empty_stopwords_file(self, mock_file):
        stopwords = Preprocessing.load_stopwords_file("empty_stopwords.txt")
        self.assertEqual(stopwords, set())

    @patch("builtins.open", new_callable=mock_open,
           read_data="Name,Other Names\nHarry Potter,The Boy Who Lived\nharry potter,Johnny")
    @patch("os.path.exists", return_value=True)
    @patch("os.path.getsize", return_value=100)
    def test_preprocess_people_with_case_insensitive_duplicates(self, mock_size, mock_exists, mock_file):
        preprocessor = Preprocessing(question_num=1, people_path="fake_people.csv", stopwords_path="fake_stopwords.txt")
        preprocessor.stopwords = self.stopwords
        result = preprocessor.preprocess_people()
        expected_result = [
            [["harry", "potter"], [["boy", "who", "lived"]]]]  # Should ignore the duplicate 'harry potter'
        self.assertEqual(result, expected_result)

    @patch("builtins.open", new_callable=mock_open, read_data="wrong_header\nHarry Potter was here.")
    @patch("os.path.exists", return_value=True)
    @patch("os.path.getsize", return_value=100)
    def test_preprocess_sentences_with_wrong_header(self, mock_size, mock_exists, mock_file):
        with self.assertRaises(SystemExit):
            Preprocessing(question_num=1, sentences_path="fake_sentences.csv", stopwords_path="fake_stopwords.txt")


if __name__ == "__main__":
    unittest.main()
