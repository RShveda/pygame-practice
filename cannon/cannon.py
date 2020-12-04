import pygame
import random
from pygame.draw import *


class App:

    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 1280, 800
        self._mouse_button = False
        self.clock = None
        self.FPS = 30

    def on_init(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._mouse_button = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self._mouse_button = False

    def on_loop(self, game_round):
        if random.random() < 0.01:
            game_round.add_new_target()
        if pygame.mouse.get_focused():
            game_round.cannon.set_aim(pygame.mouse.get_pos())
        if self._mouse_button:
            game_round.cannon.load()
        elif not self._mouse_button and game_round.cannon.is_loaded():
            bullet_params = game_round.cannon.fire()
            game_round.add_new_bullet(bullet_params)
            game_round.cannon.load_reset()
        game_round.move_objects()
        game_round.collision_check()

    def on_render(self, game_round):
        surface = self._display_surf
        game_round.draw_objects(surface)
        pygame.display.update()
        self._display_surf.fill((255, 255, 255))

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        self.on_init()
        game_round = GameRound(self)
        game_round.set_cannon()
        game_round.set_scoreboard()
        while self._running:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop(game_round)
            self.on_render(game_round)
        self.on_cleanup()


class ScoreBoardView:

    def __init__(self, size):
        self.width = size[0] // 8
        self.height = size[1] // 16
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.font_color = (0, 0, 0)

    def draw(self, score, surface):
        text = "Your score is {}".format(score)
        textsurface = self.font.render(text, False, self.font_color)
        surface.blit(textsurface, (0, 0))


class GameRound:

    def __init__(self, app):
        self.targets = []
        self.bullets = []
        self.app = app
        self.cannon = None
        self.scoreboard = None
        self.score = 0

    def add_new_target(self):
        new_target = Target(self.app)
        new_target.on_init()
        self.targets.append(new_target)

    def add_new_bullet(self, bullet_params):
        new_bullet = Bullet(self.app, *bullet_params)
        new_bullet.on_init()
        self.bullets.append(new_bullet)

    def set_cannon(self):
        cannon = Cannon(self.app)
        cannon.on_init()
        self.cannon = cannon

    def set_scoreboard(self):
        scoreboard = ScoreBoardView(self.app.size)
        self.scoreboard = scoreboard

    def draw_objects(self, surface):
        self.cannon.draw(surface)
        self.scoreboard.draw(self.score, surface)
        for target in self.targets:
            target.draw(surface)
        for bullet in self.bullets:
            bullet.draw(surface)

    def move_objects(self):
        for bullet in self.bullets:
            bullet.move()
        for target in self.targets:
            target.move()

    def collision_check(self):
        for bullet in self.bullets:
            for target in self.targets:
                distance = ((target.get_position()[0] - bullet.get_position()[0])**2 +
                            (target.get_position()[1] - bullet.get_position()[1])**2)**0.5
                if int(distance) < target.get_radius()+bullet.get_radius():
                    target.on_destroy()
                    self.score += 1
                    self.targets.remove(target)


class GameObject:
    def __init__(self, app):
        self.app = app
        self._position = ()
        self._size = ()
        self._direction = ()
        self._aim = ()
        self._color = ()
        self._speed = 0
        self._radius = 0
        self._is_active = False

    def on_init(self):
        self._color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self._is_active = True

    def on_destroy(self):
        pass

    def move(self):
        coords_x = self._position[0] + self._direction[0] * self._speed
        coords_y = self._position[1] + self._direction[1] * self._speed
        self._position = (coords_x, coords_y)

    def draw(self, surface):
        pass

    def get_position(self):
        return self._position

    def get_radius(self):
        return self._radius


class Target(GameObject):

    # def __init__(self, app):
    #     super().__init__(app)
    #     self._radius = 0

    def on_init(self):
        self._position = (random.randint(100, self.app.width), random.randint(0, self.app.height))
        self._radius = (random.randint(10, self.app.width/16))
        self._direction = (random.randint(-2, 2), random.randint(-2, 2))
        self._speed = random.randint(1, 2)
        super().on_init()

    def draw(self, surface):
        circle(surface, self._color, self._position, self._radius)


class Cannon(GameObject):

    def __init__(self, app):
        super().__init__(app)
        self._radius = 5
        self._load = 0

    def on_init(self):
        self._position = (20, random.randint(50, self.app.height))
        self._direction = (self._position[0], self._position[1]+1)
        super().on_init()
        self._color = (255, 0, 0)
        self._aim = (self.app.width/2, self.app.height/2)

    def load(self):
        self._load += 0.3

    def is_loaded(self):
        return self._load

    def load_reset(self):
        self._load = 0

    def fire(self):
        """ returns bullet start position, direction, and loaded force """
        return self._position, self._aim, self._load

    def set_aim(self, mouse_coords):
        distance = [mouse_coords[0] - self._position[0], mouse_coords[1] - self._position[1]]
        norm = (distance[0] ** 2 + distance[1] ** 2) ** 0.5
        self._aim = (distance[0] / norm, distance[1] / norm)

    def draw(self, surface):
        for i in range(int(self._load+10)*2):
            position = self._position[0] + self._aim[0]*i, self._position[1] + self._aim[1]*i
            circle(surface, self._color, position, self._radius)


class Bullet(GameObject):

    def __init__(self, app, position, direction, speed):
        super().__init__(app)
        self._position = position
        self._direction = direction
        self._speed = speed

    def on_init(self):
        self._radius = random.randint(5, self.app.width//32)
        super().on_init()

    def draw(self, surface):
        # print(self._color, self._position, self._radius)
        circle(surface, self._color, self._position, self._radius)


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()