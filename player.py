import pygame
from level import Level


class Player:

    def __init__(self, level: Level):

        self.level = level

        # set images
        self.images = {
            'run': [
                pygame.image.load('assets/images/run1.png').convert(),
                pygame.image.load('assets/images/run2.png').convert(),
                pygame.image.load('assets/images/player/sticky/run3.png').convert()
            ],
            'stand': [pygame.image.load('assets/images/player/sticky/stand.png').convert()],
            'jump': [pygame.image.load('assets/images/player/sticky/jump.png').convert()],
            'hurt':[pygame.image.load('assets/images/hurt.png').convert()],
            'dead': [pygame.image.load('assets/images/player/sticky/dead.png').convert()]
        }

        for key in self.images:
            for image in self.images[key]:
                image.set_colorkey((0, 0, 0))

        self.rect = self.images['run'][0].get_rect()

        self.rect.x = 20
        self.rect.y = 464
        self.vel_x = 15.0
        self.vel_y = 0.0
        self.grav = 8

        self.score = 0
        self.runed = 0
        self.life = 100.0
        self.damage = 0.5
        self.pause = False

        self.anim = 0

        self.item_chance = 0.04

        self.state = 'stand'
        self.former = 'stand'

    def update(self):
        if self.state == 'jump':
            self.rect.y = self.rect.y - self.vel_y
            self.vel_y = self.vel_y - self.grav
            if self.vel_y < 0 and self.rect.y >= 336:
                self.vel_y = 0
                self.rect.y = 336
                self.state = 'run'

        for obstacle in self.level.obstacles:
            if self.rect.colliderect(obstacle):
                self.life -= self.damage
