import pygame
from models import load_scores
from views import blank_screen
from controllers import user_controller_tick, system_controller_tick
import constants as cons


def main():
    """
    Main function of the module which is responsible for variables initialisation
    and game event loop.
    """
    pygame.init()
    clock = pygame.time.Clock()
    load_scores()
    is_finished = False

    while not is_finished:
        clock.tick(cons.FPS)
        is_finished = user_controller_tick(is_finished)
        system_controller_tick()
        pygame.display.update()
        blank_screen()
    pygame.quit()


if __name__ == '__main__':
    main()
