import pygame
from pygame.draw import *

pygame.init()

FPS = 30
WIDTH, HEIGHT = 400, 600

# environment
blue = (54, 247, 244)
green = (57, 250, 27)
yellow = (240, 255, 33)

# tree
dark_green = (33, 148, 52)
white_grey = (237, 230, 230)
orange = (247, 228, 183)

# unicorn
white = (250, 250, 250)
pink = (252, 177, 231)
purple = (231, 139, 247)
yellowish = (254, 255, 173)
greenish = (219, 255, 173)
blueish = (202, 237, 252)
brownish = (240, 225, 168)
purplish = (240, 197, 250)
black = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(blue)
grass = rect(screen, green, (0, int(HEIGHT * 0.45), WIDTH, int(HEIGHT * 0.55)))
sun = circle(screen, yellow, (WIDTH - 20, 40), 80)


class Tree():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.layer = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # self.border = rect(self.layer, black, (0, 0, self.width, self.height), 1)
        self.stem = rect(self.layer, white_grey, (int(self.width / 2 - 15), int(self.height - 100), 30, 80))
        self.bottom_leaves = ellipse(self.layer, dark_green,
                                     (int(self.width / 2 - 55), int(self.height - 150), 110, 90))
        ellipse(self.layer, orange, (int(self.width / 2 + 20), int(self.height - 95), 28, 28))
        self.middle_leaves = ellipse(self.layer, dark_green,
                                     (int(self.width / 2 - 90), int(self.height - 225), 180, 110))
        ellipse(self.layer, orange, (int(self.width / 2 - 70), int(self.height - 180), 28, 28))
        ellipse(self.layer, orange, (int(self.width / 2 + 55), int(self.height - 180), 30, 28))
        self.top_leaves = ellipse(self.layer, dark_green, (int(self.width / 2 - 55), int(self.height - 300), 110, 150))
        ellipse(self.layer, orange, (int(self.width / 2 + 15), int(self.height - 270), 28, 28))


class Hair():
    def __init__(self):
        self.layer = pygame.Surface((90, 90), pygame.SRCALPHA)
        # rect(self.layer, black, (0, 0, 90, 90), 1)
        ellipse(self.layer, pink, (40, 19, 35, 12))
        ellipse(self.layer, brownish, (30, 25, 32, 22))
        ellipse(self.layer, greenish, (50, 57, 30, 14))
        ellipse(self.layer, brownish, (42, 47, 30, 15))
        ellipse(self.layer, yellowish, (20, 35, 47, 18))
        ellipse(self.layer, yellowish, (20, 53, 32, 12))
        ellipse(self.layer, greenish, (13, 45, 35, 12))
        ellipse(self.layer, blueish, (12, 57, 22, 10))
        ellipse(self.layer, purplish, (33, 61, 35, 14))
        ellipse(self.layer, blueish, (12, 65, 32, 12))
        ellipse(self.layer, purplish, (33, 68, 35, 12))
        ellipse(self.layer, blueish, (45, 66, 30, 12))
        ellipse(self.layer, purple, (6, 71, 40, 12))


class Unicorn():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.layer = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # self.border = rect(self.layer, black, (0, 0, self.width, self.height), 1)
        tail_top = Hair()
        tail_bottom = Hair()
        rotated_hair = pygame.transform.flip(tail_bottom.layer, True, False)
        self.layer.blit(rotated_hair, (0, 152))
        self.layer.blit(tail_top.layer, (5, 130))
        self.body = ellipse(self.layer, white, (60, int(self.height - 150), 160, 70))
        # legs
        rect(self.layer, white, (75, int(self.height - 110), 15, 80))
        rect(self.layer, white, (105, int(self.height - 110), 15, 70))
        rect(self.layer, white, (165, int(self.height - 110), 15, 85))
        rect(self.layer, white, (195, int(self.height - 110), 12, 70))
        # neck
        polygon(self.layer, white, [(130, int(self.height - 110)),
                                    (210, int(self.height - 110)),
                                    (210, int(self.height - 190)),
                                    (175, int(self.height - 190))
                                    ])
        # head
        ellipse(self.layer, white, (175, int(self.height - 210), 48, 38))
        # mouth
        ellipse(self.layer, white, (195, int(self.height - 200), 50, 25))
        # corn
        polygon(self.layer, pink, [(190, int(self.height - 208)),
                                   (203, int(self.height - 208)),
                                   (203, int(self.height - 270)),
                                   ])
        # eye
        ellipse(self.layer, purple, (198, int(self.height - 200), 15, 13))
        ellipse(self.layer, black, (205, int(self.height - 197), 6, 6))
        eye_blink = pygame.Surface((8, 8), pygame.SRCALPHA)
        ellipse(eye_blink, white, (0, 4, 7, 4))
        rotated_blink = pygame.transform.rotate(eye_blink, -30)
        self.layer.blit(rotated_blink, (202, int(self.height - 203)))
        # hair
        ellipse(self.layer, pink, (170, 68, 25, 15))
        ellipse(self.layer, brownish, (160, 85, 30, 15))
        hair = Hair()
        self.layer.blit(hair.layer, (110, int(self.height - 220)))


tree = Tree(200, 340)
unicorn = Unicorn(300, 280)

screen.blit(tree.layer, (-25, 70))
screen.blit(unicorn.layer, (120, 250))

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
