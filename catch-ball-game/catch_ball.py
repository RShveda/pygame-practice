import pygame
from pygame.draw import *
from random import randint, uniform, random, choice
import json
import views
import constants as cons

print("catch_ball.py imported")


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
            views.blit_creep(screen, balls[key])


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
            print("Gotcha ball")
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


def main():
    pygame.init()
    screen = pygame.display.set_mode((cons.WIDTH, cons.HEIGHT))
    pygame.display.update()
    clock = pygame.time.Clock()
    scores_data = load_scores()
    score = 0
    balls = []
    player_name = ''
    finished = False
    is_game_over = False
    show_ranking = False


    while not finished:
        clock.tick(cons.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not is_game_over:
                    score = click(event, balls, score)
            elif event.type == pygame.KEYDOWN:
                if is_game_over:
                    if show_ranking:
                        if event.key == pygame.K_RETURN:
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
        move_balls(screen, balls)
        views.draw_scoreboard(screen, score)
        if len(balls) < cons.MAX_BALLS:
            if random() < 0.2:
                new_ball(balls)
        else:
            views.game_over_view(screen, score, player_name, scores_data, show_ranking)
            is_game_over = True
        pygame.display.update()
        screen.fill(cons.BLACK)
    pygame.quit()

if __name__ == '__main__':
    main()