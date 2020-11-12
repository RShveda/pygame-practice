import pygame
import random
from pygame.draw import *


class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 640, 400

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self, game_round):
        if random.random() < 0.1:
            new_target = Target(self)
            new_target.on_init()
            game_round.add_new_target(new_target)

    def on_render(self, game_round):
        surface = self._display_surf
        game_round.draw_objects(surface)
        pygame.display.update()
        self._display_surf.fill((255, 255, 255))

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        # if self.on_init() == False:
        #     self._running = False
        self.on_init()
        game_round = GameRound()
        cannon = Cannon(self)
        cannon.on_init()
        game_round.set_cannon(cannon)
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop(game_round)
            self.on_render(game_round)
        self.on_cleanup()


class GameRound:

    def __init__(self):
        self.targets = []
        self.bullets = []
        self.cannon = None
        self.scoreboard = None

    def add_new_target(self, target):
        self.targets.append(target)

    def set_cannon(self, cannon):
        self.cannon = cannon

    def draw_objects(self, surface):
        self.cannon.draw(surface)
        for target in self.targets:
            target.draw(surface)

    def move_objects(self):
        pass


class GameObject:
    def __init__(self, app):
        self.app = app
        self._position = ()
        self._size = ()
        self._direction = ()
        self._color = ()
        self._is_active = False

    def on_init(self):
        self._color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self._is_active = True

    def on_destroy(self):
        pass

    def move(self):
        pass

    def draw(self, surface):
        pass


class Target(GameObject):

    def __init__(self, app):
        super().__init__(app)
        self._radius = 0

    def on_init(self):
        self._position = (random.randint(100, self.app.width), random.randint(0, self.app.height))
        self._radius = (random.randint(10, self.app.width/16))
        self._direction = (random.randint(-3, 3), random.randint(-3, 3))
        super().on_init()

    def draw(self, surface):
        circle(surface, self._color, self._position, self._radius)


class Cannon(GameObject):

    def __init__(self, app):
        super().__init__(app)
        self._radius = 5
        self._direction = (0, 0)

    def on_init(self):
        self._position = (20, random.randint(50, self.app.height))
        super().on_init()
        self._color = (255, 0, 0)

    def draw(self, surface):
        circle(surface, self._color, self._position, self._radius)


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()