import pygame


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


