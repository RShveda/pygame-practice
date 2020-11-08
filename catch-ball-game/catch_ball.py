import pygame
from random import random
from models import save_scores, load_scores, new_ball, move_balls, add_to_ranking
from views import draw_scoreboard, game_over_view, blank_screen
from controllers import click
import constants as cons


def main():
    """
    Main function of the module which is responsible for variables initialisation
    and game event loop.
    """
    pygame.init()
    clock = pygame.time.Clock()
    scores_data = load_scores()
    score = 0
    balls = []
    player_name = ''
    is_finished = False
    is_game_over = False
    show_ranking = False

    while not is_finished:
        clock.tick(cons.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not is_game_over:
                    score = click(event, balls, score)
            elif event.type == pygame.KEYDOWN:
                if is_game_over:
                    if show_ranking:
                        if event.key == pygame.K_RETURN:
                            is_finished = True
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
        move_balls(balls)
        if show_ranking is False:  # hides score board after user inputted name
            draw_scoreboard(score)
        if len(balls) < cons.MAX_BALLS:
            if random() < 0.2:
                new_ball(balls)
        else:
            game_over_view(score, player_name, scores_data, show_ranking)
            is_game_over = True
        pygame.display.update()
        blank_screen()
    pygame.quit()


if __name__ == '__main__':
    main()
