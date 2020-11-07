import json


def save_scores(scores_data: list):
    """
    Function is responsible for writing a list of top score records into json file.
    :param scores_data: list of objects that hold top 3 scores.
    """
    if (len(scores_data) == 3 and
            type(scores_data) == list):
        with open('scores.json', 'w') as f:
            json.dump(scores_data, f)


def load_scores():
    """
    Function extract data (top3 scores) from json file.
    :return: list of objects holding top 3 scores or zero records if json file does not exist.
    """

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


