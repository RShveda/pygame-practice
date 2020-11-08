import pygame
from random import randint, uniform, random, choice
from views import blit_creep, blit_circle
import constants as cons
import json


def new_ball(balls: list):
    """
    Function which creates a new ball (or creep type of ball) and adds it to list of existing
    balls. Each ball holds following params:
    is_ball - bool, if false then ball is of "creep" type
    (x, y) - tuple that holds current coordinates for ball (left top corner)
    (x_direction, y_direction) - tuple that holds 2d vector params
    radius - integer, distance from center to edges (for creeps this value is not precise)
    fill - for regular ball it will be a color (RGB), for creeps it will be a name of file
    that holds an image
    :param balls: list that holds existing balls parameters
    """
    x_direction = uniform(-1, 1)
    y_direction = uniform(-1, 1)
    x = randint(100, cons.WIDTH - 100)
    y = randint(100, cons.HEIGHT - 100)
    if random() < 0.1:
        is_ball = False
        img_filename = choice(cons.CREEP_FILENAMES)
        image = pygame.image.load(img_filename).convert_alpha()
        image_width, image_height = image.get_size()
        radius = int((image_height + image_width)/4)
        balls.append((is_ball, (x, y), (x_direction, y_direction), radius, img_filename))
    else:
        is_ball = True
        color = cons.COLORS[randint(0, 5)]
        radius = randint(10, 100)
        balls.append((is_ball, (x, y), (x_direction, y_direction), radius, color))


def move_balls(balls: list):
    """
    Function that move balls on a game surface. It calculates ball new position and direction
    according to a speed modifier and possible collisions with walls. Then it draw balls in those
    positions.
    :param balls: list that holds existing balls parameters
    """
    speed = 5
    for key, ball in enumerate(balls):
        is_ball, coords, direction, radius, fill = ball
        shifted_ball = shift_ball(ball, speed)
        new_direction, new_coords = bounce_off_walls(shifted_ball)
        balls[key] = (is_ball, new_coords, new_direction, radius, fill)
        if ball[0]:
            color = fill
            blit_circle(color, new_coords, radius)
        else:
            blit_creep(balls[key])


def shift_ball(ball: tuple, speed: int):
    """
    Function to update ball position according to a speed.
    :param ball: tuple that holds ball params
    :param speed: integer that represent shift modifier
    :return: new ball with shifted position
    """
    is_ball, coords, direction, radius, fill = ball
    new_coords = (int(coords[0] + direction[0] * speed), int(coords[1] + direction[1] * speed))
    shifted_ball = (is_ball, new_coords, direction, radius, fill)
    return shifted_ball


def bounce_off_walls(ball: tuple):
    """
    Helper function to check for ball collision with walls and calculate new coordinates
    and directions for a ball.
    :param ball: tuple that holds ball params
    :return: two tuples that holds new direction params (x,y) and new coordinates params (x,y)
    """
    is_ball, coords, direction, radius, fill = ball
    direction_x, direction_y = direction
    coords_x, coords_y = coords
    if coords_x < 0 + radius:
        coords_x = radius
        direction_x *= -1
    elif coords_x > cons.WIDTH - radius:
        coords_x = cons.WIDTH - radius
        direction_x *= -1
    elif coords_y < 0 + radius:
        coords_y = radius
        direction_y *= -1
    elif coords_y > cons.HEIGHT - radius:
        coords_y = cons.HEIGHT - radius
        direction_y *= -1
    else:  # creeps unique ability to bounce from imaginary walls
        if not is_ball:
            if random() < 0:
                direction_x *= -1
            if random() < 0:
                direction_y *= -1
    return (direction_x, direction_y), (coords_x, coords_y)


def add_to_ranking(score: int, player_name: str, scores_data: list):
    """
    Helper function to insert player result into top 3 list.
    position.
    :param score: player final score
    :param player_name: player name
    :param scores_data: current list of top 3 results
    :return: updated list of top 3 results
    """
    for position, record in enumerate(scores_data):
        if score > record["score"]:
            new_record = {"name": player_name, "score": score}
            scores_data.insert(position, new_record)
            return scores_data[:3]
    return scores_data[:3]


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