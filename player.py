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

        self.rect.x = 30
        self.rect.y = 368
        self.vel_x = 0
        self.vel_y = 0
        self.grav = 4
        self.floor = 368
        self.life = 100.0
        self.damage = 0.5
        self.jump = 0
        self.collide = False
        self.anim = 0

        self.run = False
        self.ended = False

    def update(self):
        self.collide = False
        self.rect.y -= self.vel_y
        self.vel_y -= self.grav
        if self.rect.y >= self.floor:
            self.rect.y = self.floor
            self.vel_y = 0
            self.jump = 0

            for obstacle in self.level.obstacles:
                if 0 < self.rect.x < 100:
                    if self.rect.colliderect(obstacle):
                        self.vel_y += self.grav 
                        self.rect.y -= self.vel_y
                        self.vel_y = 0
                        self.jump = 0

            for obstacle in self.level.obstacles:
                obstacle.x -= self.vel_x
                if self.rect.colliderect(obstacle):
                    self.life -= self.damage
                    self.collide = True

        if self.life < 0:
            self.life = 0
        if self.life == 0:
            self.level.song.stop()

    def draw(self, game):
        color = pygame.color.Color(255, 255, 255) - self.level.color
        game.fill(color)
        pygame.draw.rect(game, color + pygame.color.Color(30, 30, 35), (0, 400, 800, 100))
        for index in range(len(self.level.obstacles)):
            if self.level.obstacles[index].x < 800:
                pygame.draw.rect(game, self.level.colors[index], self.level.obstacles[index])
        if not self.life:
            self.anim = 0
            game.blit(self.images['dead'][self.anim], (self.rect.x, self.rect.y))
        elif self.collide:
            self.anim = 0
            game.blit(self.images['hurt'][self.anim], (self.rect.x, self.rect.y))
        elif self.jump:
            game.blit(self.images['jump'][self.anim], (self.rect.x, self.rect.y))
        elif self.run:
            self.anim = not self.anim
            game.blit(self.images['run'][self.anim], (self.rect.x, self.rect.y))
        else:
            self.anim = 0
            game.blit(self.images['stand'][self.anim], (self.rect.x, self.rect.y))

    def spacebar(self):
        if not self.run:
            self.run = True
            self.vel_x = 4
            self.level.song.play()

        if self.jump < 2:
            self.jump += 1
            self.vel_y -= 20

        if not self.life:
            self.ended = True
