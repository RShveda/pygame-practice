import json


def save_scores(scores_data):
    with open('scores.json', 'w') as f:
        json.dump(scores_data, f)


def load_scores():
    try:
        with open('scores.json', 'r') as f:
            data = json.load(f)
    except OSError:
        data = [
            {"name": "empty", "score": 0},
            {"name": "empty", "score": 0},
            {"name": "empty", "score": 0},
        ]
    return data