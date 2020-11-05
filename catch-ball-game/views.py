import pygame
import numpy as np
import constants as cons


def draw_scoreboard(screen, score):
    text = "Your score is {}".format(score)
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    textsurface = myfont.render(text, False, (255, 255, 255))
    screen.blit(textsurface, (0, 0))


def rotate_image(image, direction):
    v = np.array(direction)
    direction_angle = np.arctan2(v[1], v[0]) / np.pi * 180
    image = pygame.transform.rotate(image, -direction_angle)
    return image


def blit_creep(screen, ball):
    coords = ball[1]
    direction = ball[2]
    img_name = ball[4]
    init_image = pygame.image.load(img_name).convert_alpha()
    image = rotate_image(init_image, direction)
    image_w, image_h = image.get_size()
    draw_pos = image.get_rect().move(
        coords[0] - image_w / 2,
        coords[1] - image_h / 2)
    screen.blit(image, draw_pos)


def text_area(text, surface, position):
    width, height = surface.get_size()
    color = (255, 255, 255)
    font = pygame.font.SysFont('Comic Sans MS', 40)
    text_surface = font.render(text, False, color)
    text_width = max(300, text_surface.get_width() + 10)
    coords = ((width - text_width)/2, position * height/3)
    surface.blit(text_surface, coords)


def game_over_view(screen, score, player_name, scores_data, show_ranking):
    gameover_surface = pygame.Surface((cons.WIDTH/1.5, cons.HEIGHT/2), pygame.SRCALPHA)
    gameover_surface_size = gameover_surface.get_size()
    text_area("GAME OVER", gameover_surface, 0)
    player_rank = is_winer(score, scores_data)
    if player_rank is not False:  # player_name_input
        text_area("You got into TOP 3!", gameover_surface, 0.5)
        text_area("Type your name:", gameover_surface, 1)
        text_area("{}_".format(player_name), gameover_surface, 2)
    else:
        if not show_ranking: # show_game_over
            text_area("Press Enter to continue", gameover_surface, 0.5)
        else: # show_top_rank
            text_area("Best results:", gameover_surface, 0.5)
            for position, record in enumerate(scores_data):
                text_area(str(position+1) + ". {} - {}".format(record["name"], record["score"]), gameover_surface, position*0.5+1)
    coords = ((cons.WIDTH - gameover_surface_size[0])/2, (cons.HEIGHT - gameover_surface_size[1])/2)
    screen.blit(gameover_surface, coords)


def is_winer(score, scores_data):
    for position, record in enumerate(scores_data):
        if score > record["score"]:
            return position
    return False
