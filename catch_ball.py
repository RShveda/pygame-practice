import pygame
from pygame.draw import *
from random import randint, uniform, random, choice
import numpy as np
import json

pygame.init()

WIDTH = 800
HEIGHT = 600

FPS = 10
MAX_BALLS = 10
screen = pygame.display.set_mode((WIDTH, HEIGHT))
score = 0

CREEP_FILENAMES = [
        'bluecreep.png',
        'pinkcreep.png',
        'graycreep.png']

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def draw_scoreboard(score):
    text = "Your score is {}".format(score)
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    textsurface = myfont.render(text, False, (255, 255, 255))
    screen.blit(textsurface, (0, 0))
    # for position, record in enumerate(scores_data):
    #     text = str(position + 1) + ". {} - {}".format(record["name"], record["score"])
    #     textsurface = myfont.render(text, False, (255, 255, 255))
    #     screen.blit(textsurface, (WIDTH*0.75, position * HEIGHT/20))



def bounce_off_walls(coords, radius, direction, is_ball):
    direction_x, direction_y = direction
    coords_x, coords_y = coords
    if coords_x < 0 + radius:
        coords_x = radius
        direction_x *= -1
    elif coords_x > WIDTH - radius:
        coords_x = WIDTH - radius
        direction_x *= -1
    elif coords_y < 0 + radius:
        coords_y = radius
        direction_y *= -1
    elif coords_y > HEIGHT - radius:
        coords_y = HEIGHT - radius
        direction_y *= -1
    else:  # creeps unique ability to rotate randomly
        if not is_ball:
            if random() < 0.1:
                direction_x *= -1
            if random() < 0.1:
                direction_y *= -1
    return (direction_x, direction_y), (coords_x, coords_y)


def rotate_image(image, coords, direction):
    v = np.array(direction)
    direction_angle = np.arctan2(v[1], v[0]) / np.pi * 180
    image = pygame.transform.rotate(image, -direction_angle)
    return image


def blit_creep(image, coords):
    image_w, image_h = image.get_size()
    draw_pos = image.get_rect().move(
        coords[0] - image_w / 2,
        coords[1] - image_h / 2)
    screen.blit(image, draw_pos)


def show_balls(balls):
    speed = 5
    for key, ball in enumerate(balls):
        is_ball, coords, direction, radius, fill = ball
        coords = (int(coords[0] + direction[0] * speed), int(coords[1] + direction[1] * speed))
        new_direction, new_coords = bounce_off_walls(coords, radius, direction, is_ball)
        if ball[0]:
            color = fill
            circle(screen, color, new_coords, radius)
            balls[key] = (is_ball, new_coords, new_direction, radius, color)
        else:
            img_name = fill
            image = pygame.image.load(img_name).convert_alpha()
            rotated_image = rotate_image(image, new_coords, new_direction)
            blit_creep(rotated_image, new_coords)
            balls[key] = (is_ball, new_coords, new_direction, radius, fill)


def new_ball():
    """draw a new ball"""
    x_direction = uniform(-1, 1)
    y_direction = uniform(-1, 1)
    x = randint(100, WIDTH - 100)
    y = randint(100, HEIGHT - 100)
    if random() < 0.1:
        img_filename = choice(CREEP_FILENAMES)
        is_ball = False
        image = pygame.image.load(img_filename).convert_alpha()
        image_width, image_height = image.get_size()
        radius = int((image_height + image_width)/4)
        balls.append((is_ball, (x, y), (x_direction, y_direction), radius, img_filename))
        blit_creep(image, (x, y))
    else:
        r = randint(10, 100)
        color = COLORS[randint(0, 5)]
        is_ball = True
        balls.append((is_ball, (x, y), (x_direction, y_direction), r, color))
        circle(screen, color, (x, y), r)


def click(event, balls, score):
    for ball in balls:
        is_creep, coords, radius = ball[0], ball[1], ball[3]
        distance = ((coords[0] - event.pos[0])**2 + (coords[1] - event.pos[1])**2)**0.5
        if int(distance) < radius:
            print("Gotcha ball")
            if ball[0]:
                score += 1
            else:
                score += 2
            balls.remove(ball)
    return score


def game_over(score, player_name, scores_data):
    gameover_surface = pygame.Surface((WIDTH/1.5, HEIGHT/2), pygame.SRCALPHA)
    gameover_surface_size = gameover_surface.get_size()
    text_area("GAME OVER", gameover_surface, 0)
    rank = is_winer(score, scores_data)
    if rank is not False:
        text_area("You got into TOP 3!", gameover_surface, 0.5)
        text_area("Type your name:", gameover_surface, 1)
        text_area("{}_".format(player_name), gameover_surface, 2)
    else:
        if not show_ranking:
            text_area("Press Enter to continue", gameover_surface, 0.5)
        else:
            text_area("Best results:", gameover_surface, 0.5)
            for position, record in enumerate(scores_data):
                text_area(str(position+1) + ". {} - {}".format(record["name"], record["score"]), gameover_surface, position*0.5+1)
    coords = ((WIDTH - gameover_surface_size[0])/2, (HEIGHT - gameover_surface_size[1])/2)
    screen.blit(gameover_surface, coords)


def text_area(text, surface, position):
    width, height = surface.get_size()
    color = (255, 255, 255)
    font = pygame.font.SysFont('Comic Sans MS', 40)
    text_surface = font.render(text, False, color)
    text_width = max(300, text_surface.get_width() + 10)
    coords = ((width - text_width)/2, position * height/3)
    surface.blit(text_surface, coords)


def add_to_ranking(score, player_name, scores_data):
    for position, record in enumerate(scores_data):
        if score > record["score"]:
            new_record = {"name": player_name, "score": score}
            scores_data.insert(position, new_record)
            return scores_data[:3]
    return scores_data[:3]


def is_winer(score, scores_data):
    for position, record in enumerate(scores_data):
        if score > record["score"]:
            return position
    return False


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


pygame.display.update()
clock = pygame.time.Clock()
finished = False
balls = []
is_game_over = False
show_ranking = False
player_name = ''
scores_data = load_scores()


while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not is_game_over:
                score = click(event, balls, score)
        elif event.type == pygame.KEYDOWN:
            print(is_game_over, show_ranking)
            if is_game_over:
                if show_ranking:
                    if event.key == pygame.K_RETURN:
                        # scores_data = add_to_ranking(score, player_name, scores_data)
                        print(scores_data)
                        finished = True
                else:
                    if event.key == pygame.K_RETURN:
                        scores_data = add_to_ranking(score, player_name, scores_data)
                        score = 0
                        save_scores(scores_data)
                        show_ranking = True
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode

    show_balls(balls)
    draw_scoreboard(score)
    if len(balls) < MAX_BALLS:
        if random() < 0.2:
            new_ball()
    else:
        game_over(score, player_name, scores_data)
        is_game_over = True
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()