import pygame
from pygame.draw import *
import numpy as np
import catch_ball

print("views.py imported")


def draw_scoreboard(score, screen):
    text = "Your score is {}".format(score)
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    textsurface = myfont.render(text, False, (255, 255, 255))
    screen.blit(textsurface, (0, 0))


def rotate_image(image, direction):
    v = np.array(direction)
    direction_angle = np.arctan2(v[1], v[0]) / np.pi * 180
    image = pygame.transform.rotate(image, -direction_angle)
    return image


def blit_creep(screen, image, coords):
    image_w, image_h = image.get_size()
    draw_pos = image.get_rect().move(
        coords[0] - image_w / 2,
        coords[1] - image_h / 2)
    screen.blit(image, draw_pos)


def show_balls(screen, balls):
    speed = 5
    for key, ball in enumerate(balls):
        is_ball, coords, direction, radius, fill = ball
        coords = (int(coords[0] + direction[0] * speed), int(coords[1] + direction[1] * speed))
        new_direction, new_coords = catch_ball.bounce_off_walls(coords, radius, direction, is_ball)
        if ball[0]:
            color = fill
            circle(screen, color, new_coords, radius)
            balls[key] = (is_ball, new_coords, new_direction, radius, color)
        else:
            img_name = fill
            image = pygame.image.load(img_name).convert_alpha()
            rotated_image = rotate_image(image, new_direction)
            blit_creep(screen, rotated_image, new_coords)
            balls[key] = (is_ball, new_coords, new_direction, radius, fill)


def text_area(text, surface, position):
    width, height = surface.get_size()
    color = (255, 255, 255)
    font = pygame.font.SysFont('Comic Sans MS', 40)
    text_surface = font.render(text, False, color)
    text_width = max(300, text_surface.get_width() + 10)
    coords = ((width - text_width)/2, position * height/3)
    surface.blit(text_surface, coords)