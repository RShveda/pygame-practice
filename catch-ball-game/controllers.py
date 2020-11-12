import pygame
from random import random
import constants as cons
import models
from views import draw_scoreboard, game_over_view


is_game_over = False
show_ranking = False


def click(event: pygame.MOUSEBUTTONDOWN, balls: list):
    """
    Function which check if player clicked on a ball. If yes it will increment score and remove
    the ball from list of existing balls.
    :param event: pygame MOUSEBUTTONDOWN event
    :param balls: list of existing balls
    :return: score
    """
    for ball in balls:
        is_creep, coords, radius = ball[0], ball[1], ball[3]
        distance = ((coords[0] - event.pos[0])**2 + (coords[1] - event.pos[1])**2)**0.5
        if int(distance) < radius:
            if ball[0]:
                models.increment_score(1)
            else:
                models.increment_score(2)
            balls.remove(ball)


def user_controller_tick(is_finished):
    """
    This function is responsible for handling user input during active game stage (clicks) and
    during game finish stage.
    :param is_finished: flag that controls if game loop should be terminated
    :return: is_finished
    """
    global show_ranking  # flag that allow showing top 3 ranking and to finish the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return not is_finished
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not is_game_over:
                click(event, models.balls)
        elif event.type == pygame.KEYDOWN:
            if is_game_over:
                if show_ranking:
                    if event.key == pygame.K_RETURN:
                        is_finished = True
                else:
                    if event.key == pygame.K_RETURN:
                        models.add_to_ranking()
                        models.reset_score()
                        models.save_scores()
                        show_ranking = True
                    else:
                        models.edit_player_name(event)
    return is_finished


def system_controller_tick():
    """
    This function fetch system state and trigger main game events such as: create new balls, move existing
    balls, show scoreboard, initiate game finish.
    """
    global is_game_over
    models.move_balls()
    if show_ranking is False:  # hides score board after user inputted name
        draw_scoreboard()
    if len(models.balls) < cons.MAX_BALLS:
        if random() < 0.2:
            models.new_ball()
    else:
        game_over_view(show_ranking)
        is_game_over = True
