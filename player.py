import pygame
import os
from level import Level
import random
import config


pygame.init()
pygame.mixer.init()


class Player:

    def __init__(self, level: Level):

        self.level = level

        # set images

        self.images = {}
        for key in config.PLAYER_ICONS:
            self.images[key] = pygame.image.load(config.PLAYER_ICONS[key]).convert()
        self.particle = pygame.image.load(config.PARTICLE_ICON).convert()
        self.wrong = pygame.mixer.Sound(config.WRONG_SOUND)
        self.wrong.set_volume(config.WRONG_VOLUME)

        self.particle_counter = 0

        self.rect = self.images['stand'].get_rect()
        self.rect.x = config.PLAYER_POS_X
        self.floor = config.DISP_HEI - config.FLOOR_HEIGHT - self.rect.height
        self.rect.y = self.floor

        self.vel_x = 0
        self.vel_y = 0.
        self.jump = 0

        self.score = 0.
        self.combo = 0

        self.life = self.level.duration//3 + 5
        self.shield = 2

        self.collide = False
        self.run = False
        self.ended = False

        self.stars = []
        for _ in range(config.STARS_COUNT):
            self.stars.append([int(random.uniform(0, config.DISP_WID)), int(random.uniform(0, config.DISP_HEI - config.FLOOR_HEIGHT))])
            self.stars.append([int(random.uniform(0, config.DISP_WID)) + config.DISP_WID, int(random.uniform(0, config.DISP_HEI - config.FLOOR_HEIGHT))])

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
                    if self.vel_y < config.VELOCITY_Y_DURING_DAMAGE:
                        self.vel_y = float(config.VELOCITY_Y_DURING_DAMAGE)
            if not self.collide:
                self.vel_y -= self.level.gravity/config.BASE_FPS
            self.rect.y -= self.vel_y/config.BASE_FPS   
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

            #show particles when the player is in the air
            if self.level.obstacles:
                self.score += self.combo *(config.SCORE_POINTS_PER_SECOND/config.BASE_FPS)
            self.particle_counter += 1
            if self.particle_counter>=config.BASE_FPS/config.PARTICLES_PER_SECOND:
                self.particles.append(self.rect.y)
                self.particle_counter = 0
            if not self.vel_y:
                self.particles = []
            if self.combo < len(self.particles):
                del self.particles[0:-int(self.combo)]

        if self.life < 0:
            self.life = 0
        if self.life == 0:
            self.level.song.stop()

        for index, obstacle in enumerate(self.level.obstacles):
            if obstacle.x < -100:
                del self.level.obstacles[index]
                del self.level.colors[index]

        # stars code
        # move stars and delete the ones out of screen
        if self.run and self.level.obstacles:
            for index, star in enumerate(self.stars):
                star[0] -= 1
                if star[0] < -5:
                    del self.stars[index]
            # every time half of the stars are deleted, new ones are added
            if len(self.stars) <= config.STARS_COUNT:
                for _ in range(config.STARS_COUNT):
                    self.stars.append([int(random.uniform(0, config.DISP_WID)) +  config.DISP_WID, int(random.uniform(0, config.DISP_HEI - config.FLOOR_HEIGHT))])

    def damage(self):
        self.shield -= 1
        if self.shield < 0:
            self.life += self.shield
            self.shield = 0
        self.wrong.play()
        
    def draw(self, game):
        # draw background
        game.fill((0, 0, 20))

        # draw stars
        for star in self.stars:
            pygame.draw.circle(game, (250, 250, 250), star, config.STAR_SIZE)

        # draw ground
        pygame.draw.rect(game, (255, 240, 240), (0, config.DISP_HEI - config.FLOOR_HEIGHT, config.DISP_WID, config.FLOOR_HEIGHT))

        # draw particles
        if self.vel_y:
            for index, pos_y in enumerate(self.particles):
                game.blit(self.particle, (self.rect.x - 8 * ((len(self.particles) - index)), pos_y))

        # draw obstacles
        for index in range(len(self.level.obstacles)):
            if self.level.obstacles[index].x < config.DISP_WID + 1:
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
        self.vel_x = config.VELOCITY_X
        self.level.song.play()

    def spacebar(self):
        if self.jump < 2:
            self.jump += 1
            if self.level.obstacles:
                if self.jump == 1:
                    self.combo += 1
                self.shield += self.combo
                if self.shield > config.SHIELD_MAXIMUM:
                    self.shield = config.SHIELD_MAXIMUM
            if self.vel_y < 0:
                self.vel_y = self.level.jump_speed
            else:
                self.vel_y += self.level.jump_speed
        if not self.life:
            self.ended = True

    def save(self):
        song = str(hash(self.level.song_name))
        separator = ' '
        highs = []
        first_time = True
        if os.path.exists(config.HIGHSCORE_FILENAME):
            with open(config.HIGHSCORE_FILENAME, 'r') as highscores:
                highs = highscores.readlines()
            for index, line in enumerate(highs):
                if line.startswith(song):
                    value = int(line.split(separator)[1])
                    highs[index] = song + separator + str(int(max(self.score, value))) + '\n'
                    first_time = False
        if first_time:
            highs.append(song + separator + str(int(self.score)) + '\n')
        with open(config.HIGHSCORE_FILENAME, 'w') as highscores:
            highscores.writelines(highs)
