import pygame
from pygame.draw import *

pygame.init()

FPS = 30
WIDTH, HEIGHT = 400, 600

# environment colors
blue = (54, 247, 244)
green = (57, 250, 27)
yellow = (240, 255, 33)

# tree colors
dark_green = (33, 148, 52)
white_grey = (237, 230, 230)
orange = (247, 228, 183)

# unicorn colors
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


class Sun():
    width = 200
    height = 200

    def __init__(self):
        self.layer = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        for i in range(int(self.width/2), 0, -2):
            circle(self.layer, (240, 255, 33, int(256-(256/100*i))), (int(self.width/2), int(self.height/2)), i)


class Tree():
    width = 200
    height = 340

    def __init__(self):
        self.layer = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.stem = rect(self.layer, white_grey, (85, 240, 30, 80))
        # top leaves
        ellipse(self.layer, dark_green, (45, 40, 110, 150))
        ellipse(self.layer, green, (45, 40, 110, 150), 1)
        ellipse(self.layer, orange, (115, 70, 28, 28))
        ellipse(self.layer, green, (115, 70, 28, 28), 1)
        # middle leaves
        ellipse(self.layer, dark_green, (10, 115, 180, 110))
        ellipse(self.layer, green, (10, 115, 180, 110), 2)
        ellipse(self.layer, orange, (30, 160, 28, 28))
        ellipse(self.layer, green, (30, 160, 28, 28), 1)
        ellipse(self.layer, orange, (155, 160, 30, 28))
        ellipse(self.layer, green, (155, 160, 30, 28), 1)
        # bottom leaves
        ellipse(self.layer, dark_green, (45, 190, 110, 90))
        ellipse(self.layer, green, (45, 190, 110, 90), 1)
        ellipse(self.layer, orange, (120, 245, 28, 28))
        ellipse(self.layer, green, (120, 245, 28, 28), 1)


class Hair():
    def __init__(self):
        self.layer = pygame.Surface((90, 90), pygame.SRCALPHA)
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
    width = 300
    height = 280

    def __init__(self):
        self.layer = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # tail
        tail_top = Hair()
        tail_bottom = Hair()
        rotated_hair = pygame.transform.flip(tail_bottom.layer, True, False)
        self.layer.blit(rotated_hair, (0, 152))
        self.layer.blit(tail_top.layer, (5, 130))
        # body
        self.body = ellipse(self.layer, white, (60, 130, 160, 70))
        # legs
        rect(self.layer, white, (75, 170, 15, 80))
        rect(self.layer, white, (105, 170, 15, 70))
        rect(self.layer, white, (165, 170, 15, 85))
        rect(self.layer, white, (195, 170, 12, 70))
        # neck
        polygon(self.layer, white, [(130, 170), (210, 170), (210, 90), (175, 90), ])
        # head
        ellipse(self.layer, white, (175, int(self.height - 210), 48, 38))
        # mouth
        ellipse(self.layer, white, (195, int(self.height - 200), 50, 25))
        # corn
        polygon(self.layer, pink, [(190, 72), (203, 72), (203, 10), ])
        # eye
        ellipse(self.layer, purple, (198, 80, 15, 13))
        ellipse(self.layer, black, (205, 83, 6, 6))
        eye_blink = pygame.Surface((8, 8), pygame.SRCALPHA)
        ellipse(eye_blink, white, (0, 4, 7, 4))
        rotated_blink = pygame.transform.rotate(eye_blink, -30)
        self.layer.blit(rotated_blink, (202, 77))
        # hair
        ellipse(self.layer, pink, (170, 68, 25, 15))
        ellipse(self.layer, brownish, (160, 85, 30, 15))
        hair = Hair()
        self.layer.blit(hair.layer, (110, 60))


# initializing objects
sun = Sun()

tree_one = pygame.transform.scale(Tree().layer, (230, 320))
tree_two = pygame.transform.scale(Tree().layer, (180, 180))
tree_three = pygame.transform.scale(Tree().layer, (150, 340))
tree_four = pygame.transform.scale(Tree().layer, (150, 255))
tree_five = pygame.transform.scale(Tree().layer, (150, 255))

x = Unicorn.width
y = Unicorn.height
unicorn_one = pygame.transform.scale(Unicorn().layer, (int(x/1.1), int(y/1.1)))
unicorn_two = pygame.transform.scale(Unicorn().layer, (int(x/2.3), int(y/2.3)))
unicorn_rotated = pygame.transform.flip(Unicorn().layer, True, False)
unicorn_three = pygame.transform.scale(unicorn_rotated, (int(x/1.8), int(y/1.8)))
unicorn_four = pygame.transform.scale(unicorn_rotated, (int(x/5), int(y/5)))

# placing objects on main screen
screen.blit(sun.layer, (200, 0))

screen.blit(tree_one, (10, -35))
screen.blit(tree_two, (50, 170))
screen.blit(tree_three, (-60, 40))
screen.blit(tree_five, (20, 210))
screen.blit(tree_four, (-25, 310))

screen.blit(unicorn_one, (95, 340))
screen.blit(unicorn_two, (190, 225))
screen.blit(unicorn_three, (275, 300))
screen.blit(unicorn_four, (320, 230))


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
