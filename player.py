import pygame


class Player:
    def __init__(self):
        self.image = pygame.image.load("assets/images/player.png")
        self.rect = self.image.get_rect()
        self.vel_x = 20
        self.vel_y = 0
        self.grav = 10
