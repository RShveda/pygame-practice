import pygame
from pygame.draw import *
from random import randint, uniform, random, choice
from views import blit_creep
import constants as cons


def new_ball(balls):
    """create a new ball"""
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
        r = randint(10, 100)
        color = cons.COLORS[randint(0, 5)]
        is_ball = True
        balls.append((is_ball, (x, y), (x_direction, y_direction), r, color))


def move_balls(screen, balls):
    speed = 5
    for key, ball in enumerate(balls):
        is_ball, coords, direction, radius, fill = ball
        coords = (int(coords[0] + direction[0] * speed), int(coords[1] + direction[1] * speed))
        new_direction, new_coords = bounce_off_walls(coords, radius, direction, is_ball)
        balls[key] = (is_ball, new_coords, new_direction, radius, fill)
        if ball[0]:
            color = fill
            circle(screen, color, new_coords, radius)
        else:
            blit_creep(screen, balls[key])


def bounce_off_walls(coords, radius, direction, is_ball):
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


def click(event, balls, score):
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


def add_to_ranking(score, player_name, scores_data):
    for position, record in enumerate(scores_data):
        if score > record["score"]:
            new_record = {"name": player_name, "score": score}
            scores_data.insert(position, new_record)
            return scores_data[:3]
    return scores_data[:3]