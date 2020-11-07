"""
Tests can be run from command line: python -m unittest
"""
import unittest
from models import load_scores, save_scores


# Models tests
class LoadScores(unittest.TestCase):

    def test_output(self):
        scores = load_scores()
        self.assertTrue(len(scores) == 3)


class SaveScores(unittest.TestCase):

    def test_file_creation(self):
        import os.path
        if os.path.isfile("scores.json"):
            os.remove("scores.json")
        data = [
            {"name": "empty", "score": 0},
            {"name": "empty", "score": 0},
            {"name": "empty", "score": 0},
        ]
        save_scores(data)
        self.assertTrue(os.path.isfile("scores.json"))

    def test_with_invalid_data(self):
        import os.path
        if os.path.isfile("scores.json"):
            os.remove("scores.json")
        data = [
            {"name": "empty", "score": 0},
            {"name": "empty", "score": 0},
        ]
        save_scores(data)
        self.assertFalse(os.path.isfile("scores.json"))

