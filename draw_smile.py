import pygame
from pygame.draw import *

pygame.init()

FPS = 30
pen_color = (0, 0, 0)
main_background_color = (222, 227, 157)
body_color = (247, 247, 32)
eye_color = (224, 22, 22)
WIDTH, HEIGHT = 500, 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(main_background_color)

# face
face_radius = int(WIDTH/4)
face_position = (int(WIDTH/2), int(HEIGHT/2))
face = circle(screen, body_color, face_position, face_radius)
face_border = circle(screen, pen_color, face_position, face_radius, 1)


# eyes
class Eye():
    def __init__(self, eye_radius, is_left):
        if is_left:
            brown_position = 25
        else:
            brown_position = 100-eye_radius
        self.surface = pygame.Surface((200, 200), pygame.SRCALPHA)
        # self.border = rect(self.surface, pen_color, (0, 0, 200, 200), 1)
        self.brown = rect(self.surface, pen_color, (brown_position, (25-eye_radius)+65, 100, 10))
        self.eye_red = circle(self.surface, eye_color, (100, 100), eye_radius)
        self.eye_border = circle(self.surface, pen_color, (100, 100), eye_radius, 1)
        self.eye_ball = circle(self.surface, pen_color, (100, 100), 10)

    def make_rotated_copy(self, angle:int, coords:tuple):
        """
        :param angle: angle by which the eye.surface need to be rotated. 0 means no rotation
        :param coords: tuple of coords of left top corner for Eye surface
        :return: rotated = rotated surface, tuple = tuple of coords of left top corner for rotated surface
        """
        eye_coords_init = self.surface.get_clip()[2]
        rotated = pygame.transform.rotate(self.surface, angle)
        eye_coords = rotated.get_clip()[2]
        adjustment = int((eye_coords - eye_coords_init) / 2)
        return (rotated, (coords[0] - adjustment, coords[1] - adjustment))


#create eyes objects
left_eye = Eye(25, True)
right_eye = Eye(20, False)
rotated_left, rotated_left_position = left_eye.make_rotated_copy(-30, (95, 130))
rotated_right, rotated_right_position = right_eye.make_rotated_copy(20, (200, 130))
screen.blit(rotated_left, rotated_left_position)
screen.blit(rotated_right, rotated_right_position)

# mouth
mouth = rect(screen, pen_color, (190, 315, 120, 20))

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()