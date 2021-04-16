import pygame
from level import Level
from obstacle import Obstacle


pygame.init()
pygame.mixer.init()


class Player:

    def __init__(self, level: Level, fps):

        self.level = level
        self.fps = fps

        # set images
        self.images = {
            'run': pygame.image.load('assets/images/run.png').convert(),
            'stand': pygame.image.load('assets/images/stand.png').convert(),
            'up': pygame.image.load('assets/images/up.png').convert(),
            'down': pygame.image.load('assets/images/down.png').convert(),
            'dead': pygame.image.load('assets/images/dead.png').convert(),
            'collide': pygame.image.load('assets/images/collide.png').convert()
        }
        self.particle = pygame.image.load('assets/images/particle.png').convert()
        self.wrong = pygame.mixer.Sound('assets/sounds/wrong.wav')
        self.wrong.set_volume(0.4)

        self.count = 0.

        self.rect = self.images['stand'].get_rect()
        self.rect.x = 70
        self.rect.y = 368
        self.floor = 368

        self.vel_x = 0
        self.vel_y = 0.
        self.jump = 0
        
        self.grav = 4*900. # in pixels per second^2
        self.vel_y_on_damage = 30. # in pixels per second
        self.vel_y_on_jump = 900. # in pixels per second

        self.score = 0.
        self.combo = 0

        self.life = self.level.duration//3 + 5
        self.shield = 2

        self.collide = False
        self.run = False
        self.ended = False

        self.particles = []

    def update(self, timePassed):
        if self.life:
            self.collide = False
            offset = int(-timePassed * self.vel_x)
            for obstacle in self.level.obstacles:
                obstacle.updateOffset(offset)
                if self.rect.colliderect(obstacle):
                    self.damage()
                    self.collide = True
                    self.combo = 0
                    self.jump = 0
                    if self.vel_y < self.vel_y_on_damage:
                        self.vel_y = self.vel_y_on_damage
            if not self.collide:
                self.vel_y -= self.grav/self.fps
            self.rect.y -= self.vel_y/self.fps   
            if self.rect.y >= self.floor:
                self.rect.y = self.floor
                self.vel_y = 0
                self.jump = 0

            for obstacle in self.level.obstacles:
                if self.rect.colliderect(obstacle):
                    if not self.collide:
                        self.rect.bottom = obstacle.top
                    if self.vel_y < 0:
                        self.vel_y = 0
                    self.jump = 0

            if self.level.obstacles:
                self.score += self.combo    # TODO maybe divide by fps
                # TODO Actually I was gonna increase the combo only every 5 jumps
                #  I changed it so it is increased only every jump (doesn't matter
                #  if it is simple or double
            self.count += 1
            self.count %= 3
            if not self.count:
                self.particles.append(self.rect.y)
            if not self.vel_y:
                self.particles = []
            if self.combo > len(self.particles):
                del self.particles[0:-int(self.combo)]

        if self.life < 0:
            self.life = 0
        if self.life == 0:
            self.level.song.stop()

        new_obstacles = []
        new_colors = []
        for index, obstacle in enumerate(self.level.obstacles):
            if obstacle.x > -100:
                new_obstacles.append(self.level.obstacles[index])
                new_colors.append(self.level.colors[index])
        self.level.obstacles = new_obstacles
        self.level.colors = new_colors

        # TODO maybe this two lines are useless?
        if not len(self.level.obstacles):
            self.level.song.set_volume(self.level.song.get_volume()/1.01)

    def damage(self):
        self.shield -= 1
        if self.shield < 0:
            self.life += self.shield
            self.shield = 0
        self.wrong.play()
        
    def draw(self, game):
        # draw background
        game.fill((0, 0, 20))
        # draw ground
        pygame.draw.rect(game, (255, 240, 240), (0, 400, 800, 100))
        # draw particles
        # TODO my particles sucks... My first time with particles to be honest, but still baaad
        if self.vel_y:
            for distance, pos_y in enumerate(self.particles):
                game.blit(self.particle, (self.rect.x - 8 * distance, pos_y))
        # draw obstacles
        for index in range(len(self.level.obstacles)):
            if self.level.obstacles[index].x < 801:
                pygame.draw.rect(game, self.level.colors[index], self.level.obstacles[index])
        # draw character
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

    def start(self):
        self.run = True
        self.vel_x = self.level.pixels_per_sec
        self.level.song.play()

    def spacebar(self):
        if self.jump < 2:
            self.jump += 1
            if self.level.obstacles:
                if self.jump == 1:
                    self.combo += 60.0/self.fps
                self.shield += self.combo
                if self.shield > 10:
                    self.shield = 10
            if self.vel_y < 0:
                self.vel_y = self.vel_y_on_jump
            else:
                self.vel_y += self.vel_y_on_jump
        if not self.life:
            self.ended = True
