import pygame
from level import Level


class Player:

    def __init__(self, level: Level):

        self.level = level
        self._TEST = False
        # set images
        self.images = {
            'run': pygame.image.load('assets/images/run.png').convert(),
            'stand': pygame.image.load('assets/images/stand.png').convert(),
            'up': pygame.image.load('assets/images/up.png').convert(),
            'down': pygame.image.load('assets/images/down.png').convert(),
            'dead': pygame.image.load('assets/images/dead.png').convert(),
            'collide': pygame.image.load('assets/images/collide.png').convert()
        }

        self.rect = self.images['stand'].get_rect()

        self.rect.x = 30
        self.rect.y = 368
        self.vel_x = 0
        self.vel_y = 0
        self.grav = 3
        self.floor = 368
        self.life = 10
        self.damage = 1
        self.jump = 0
        self.collide = False
        self.run = False
        self.ended = False

    def update(self):
        if self.life:
            if self._TEST:
                print(1, self.rect.x, self.rect.y)
            self.collide = False
            self.rect.y -= self.vel_y
            self.vel_y -= self.grav
            if self._TEST:
                print(2, self.rect.x, self.rect.y)
            if self.rect.y >= self.floor:
                self.rect.y = self.floor
                self.vel_y = 0
                self.jump = 0
                if self._TEST:
                    print(3, self.rect.x, self.rect.y)

            for obstacle in self.level.obstacles:
                if self.rect.colliderect(obstacle):
                    if self.collide:
                        self.rect.y -= 1
                    else:
                        self.rect.bottom = obstacle.top
                    if self.vel_y < 0:
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
        print(self.vel_y)

    def draw(self, game):
        color = pygame.color.Color(255, 255, 255) - self.level.color
        game.fill(color)
        pygame.draw.rect(game, color + pygame.color.Color(30, 30, 35), (0, 400, 800, 100))
        for index in range(len(self.level.obstacles)):
            if self.level.obstacles[index].x < 800:
                pygame.draw.rect(game, self.level.colors[index], self.level.obstacles[index])
        if not self.life:
            game.blit(self.images['dead'], (self.rect.x, self.rect.y))
        elif not self.run:
            game.blit(self.images['stand'], (self.rect.x, self.rect.y))
        elif self.collide:
            game.blit(self.images['collide'], (self.rect.x, self.rect.y))
        elif self.vel_y > 0:
            game.blit(self.images['up'], (self.rect.x, self.rect.y))
        elif self.vel_y < 0:
            game.blit(self.images['down'], (self.rect.x, self.rect.y))
        else:
            game.blit(self.images['run'], (self.rect.x, self.rect.y))

    def spacebar(self):
        if not self.run:
            self.run = True
            self.vel_x = 4
            self.level.song.play()

        if self.jump < 2:
            self.jump += 1
            self.vel_y += 30
            if self._TEST:
                print('jump')
        if not self.life:
            self.ended = True
