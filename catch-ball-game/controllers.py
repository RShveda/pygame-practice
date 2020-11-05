import pygame
from pygame.draw import *
from random import randint, uniform, random, choice
from views import blit_creep
import constants as cons


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
        img_filename = choice(cons.CREEP_FILENAMES)
        is_ball = False
        image = pygame.image.load(img_filename).convert_alpha()
        image_width, image_height = image.get_size()
        radius = int((image_height + image_width)/4)
        balls.append((is_ball, (x, y), (x_direction, y_direction), radius, img_filename))
    else:
        radius = randint(10, 100)
        color = cons.COLORS[randint(0, 5)]
        is_ball = True
        balls.append((is_ball, (x, y), (x_direction, y_direction), radius, color))


def move_balls(screen: pygame.Surface, balls: list):
    """
    Function that move balls on a game surface. It calculates ball new position and direction
    according to a speed modifier and possible collisions with walls. Then it draw balls in those
    positions.
    :param screen: pygame surface on which the balls are drawn
    :param balls: list that holds existing balls parameters
    """
    speed = 5
    for key, ball in enumerate(balls):
        is_ball, coords, direction, radius, fill = ball
        ball = shift_ball(ball, speed)
        new_direction, new_coords = bounce_off_walls(ball)
        balls[key] = (is_ball, new_coords, new_direction, radius, fill)
        if ball[0]:
            color = fill
            circle(screen, color, new_coords, radius)
        else:
            blit_creep(screen, balls[key])


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


def click(event: pygame.MOUSEBUTTONDOWN, balls: list, score: int):
    """
    Function which check if player clicked on a ball. If yes it will increment score and remove
    the ball from list of existing balls.
    :param event: pygame MOUSEBUTTONDOWN event
    :param balls: list of existing balls
    :param score: player current score
    :return: score
    """
    for ball in balls:
        is_creep, coords, radius = ball[0], ball[1], ball[3]
        distance = ((coords[0] - event.pos[0])**2 + (coords[1] - event.pos[1])**2)**0.5
        if int(distance) < radius:
            if ball[0]:
                score += 1
            else:
                score += 2
            balls.remove(ball)
    return score


def add_to_ranking(score: int, player_name: str, scores_data:list):
    """
    Helper function to check if final score is qualified for Top3 and insert it in appropriate
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