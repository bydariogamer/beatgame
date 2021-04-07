import pygame
from level import Level


class Player:

    def __init__(self, level: Level):

        self.level = level

        # set images
        self.images = {
            'run': [
                pygame.image.load('assets/images/run1.png').convert(),
                pygame.image.load('assets/images/run2.png').convert()
            ],
            'stand': [pygame.image.load('assets/images/stand.png').convert()],
            'jump': [pygame.image.load('assets/images/jump.png').convert()],
            'hurt': [pygame.image.load('assets/images/hurt.png').convert()],
            'dead': [pygame.image.load('assets/images/dead.png').convert()]
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
        self.jump = 0

        self.anim = 0

        self.item_chance = 0.04

        self.state = 'stand'
        self.former = 'stand'
        self.ended = False

    def update(self):
        if self.state == 'jump':
            self.rect.y -= self.vel_y
            self.vel_y -= self.grav
            if self.vel_y < 0 and self.rect.y >= 336:
                self.vel_y = 0
                self.rect.y = 336
                self.state = 'run'

        for obstacle in self.level.obstacles:
            if self.rect.colliderect(obstacle):
                self.vel_y += self.grav
                self.rect.y += self.vel_y
                self.vel_y = 0
                self.state = 'run'

        for obstacle in self.level.obstacles:
            obstacle.x -= self.vel_x
            if self.rect.colliderect(obstacle):
                self.life -= self.damage

    def draw(self, game):
        color = pygame.color.Color(256,256,256) - self.level.color
        game.fill(color)
        pygame.draw.rect(game, color + pygame.color.Color(30, 30, 35), (0, 400, 800, 100))
        for index in range(len(self.level.obstacles)):
            if self.level.obstacles[index].x < 800:
                pygame.draw.rect(game, self.level.obstacles[index], self.level.colors[index])
        if len(self.images[self.state]):
            self.anim += 1
            if self.anim >= len(self.images[self.state]):
                self.anim = 0
        game.blit(self.images[self.state][self.anim], (self.rect.x, self.rect.y))

    def spacebar(self):
        if self.state == 'stand':
            self.state = 'run'
            self.vel_x = 7

        elif self.state == 'run' and self.jump < 2:
            self.jump += 1
            self.vel_y -= 20

        elif self.state == 'dead':
            self.ended = True
