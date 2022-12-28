import os
import random
import hashlib

import pygame

from level import Level
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

        self.health_dmg_sound = pygame.mixer.Sound(config.HEALTH_DAMAGE_SOUND)
        self.health_dmg_sound.set_volume(config.HEALTH_DAMAGE_VOLUME)
        self.shield_dmg_sound = pygame.mixer.Sound(config.SHIELD_DAMAGE_SOUND)
        self.shield_dmg_sound.set_volume(config.SHIELD_DAMAGE_VOLUME)
        self.shield_regen_sound = pygame.mixer.Sound(config.SHIELD_REGENERATION_SOUND)
        self.shield_regen_sound.set_volume(config.SHIELD_REGENERATION_VOLUME)

        self.particle_counter = 0

        self.rect = self.images["stand"].get_rect()
        self.rect.x = config.PLAYER_POS_X
        self.floor = config.DISP_HEI - config.FLOOR_HEIGHT - self.rect.height
        self.rect.y = self.floor

        self.vel_x = 0
        self.vel_y = 0.0
        self.jump = 0

        self.score = 0.0
        self.combo = 0

        self.life = config.HEALTH_POINTS_PER_OBSTACLE * len(self.level.obstacles)
        self.shield = 2

        self.collide = False
        self.run = False
        self.ended = False

        self.stars = []
        for _ in range(config.STARS_COUNT):
            self.stars.append(
                [
                    int(random.uniform(0, config.DISP_WID)),
                    int(random.uniform(0, config.DISP_HEI - config.FLOOR_HEIGHT)),
                ]
            )
            self.stars.append(
                [
                    int(random.uniform(0, config.DISP_WID)) + config.DISP_WID,
                    int(random.uniform(0, config.DISP_HEI - config.FLOOR_HEIGHT)),
                ]
            )

        self.particles = []

    def update(self, dt):
        if self.life:
            self.collide = False
            offset = round(-pygame.mixer.music.get_pos() / 1000 * self.vel_x)
            for obstacle in self.level.obstacles:
                obstacle.update_offset(offset)
                if self.rect.colliderect(obstacle):
                    self.damage()
                    self.collide = True
                    self.combo = 0
                    self.jump = 0
                    if self.vel_y < config.VELOCITY_Y_DURING_DAMAGE:
                        self.vel_y = float(config.VELOCITY_Y_DURING_DAMAGE)
            if not self.collide:
                self.vel_y -= self.level.gravity * dt / 1000
            self.rect.y -= self.vel_y * dt / 1000
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

            # increase score
            if self.level.obstacles:
                self.score += self.combo * (
                    config.SCORE_POINTS_PER_SECOND / config.BASE_FPS
                )

            self.particle_counter += 1
            if self.particle_counter >= config.BASE_FPS / config.PARTICLES_PER_SECOND:
                self.particles.append(self.rect.y)
                self.particle_counter = 0
            if not self.vel_y:
                self.particles = []
            if self.combo < len(self.particles):
                del self.particles[0 : -int(self.combo)]

        if self.life < 0:
            self.life = 0
        if self.life == 0:
            pygame.mixer.music.unload()

        for index, obstacle in enumerate(self.level.obstacles):
            if obstacle.x < -100:
                del self.level.obstacles[index]
                del self.level.colors[index]

        # stars code
        # move stars and delete the ones out of screen
        if self.run and self.level.obstacles:
            for index, star in enumerate(self.stars):
                star[0] -= dt / 10
                if star[0] < -5:
                    del self.stars[index]
            # every time half of the stars are deleted, new ones are added
            if len(self.stars) <= config.STARS_COUNT:
                for _ in range(config.STARS_COUNT):
                    self.stars.append(
                        [
                            int(random.uniform(0, config.DISP_WID)) + config.DISP_WID,
                            int(
                                random.uniform(0, config.DISP_HEI - config.FLOOR_HEIGHT)
                            ),
                        ]
                    )

    def damage(self):
        if self.shield > 0:
            self.shield -= 1
            self.shield_dmg_sound.play()
        else:
            self.life -= 1
            self.health_dmg_sound.play()

    def draw(self, game):
        # draw background
        game.fill((0, 0, 20))

        # draw stars
        for star in self.stars:
            pygame.draw.circle(game, (250, 250, 250), star, config.STAR_SIZE)

        # draw ground
        pygame.draw.rect(
            game,
            (255, 240, 240),
            (
                0,
                config.DISP_HEI - config.FLOOR_HEIGHT,
                config.DISP_WID,
                config.FLOOR_HEIGHT,
            ),
        )

        # draw particles
        if self.vel_y:
            for index, pos_y in enumerate(self.particles):
                game.blit(
                    self.particle,
                    (self.rect.x - 8 * (len(self.particles) - index), pos_y),
                )

        # draw obstacles
        for index in range(len(self.level.obstacles)):
            if self.level.obstacles[index].x < config.DISP_WID + 1:
                pygame.draw.rect(
                    game, self.level.colors[index], self.level.obstacles[index]
                )

        # draw character
        if not self.life:
            game.blit(self.images["dead"], (self.rect.x, self.rect.y))
        elif not self.run:
            game.blit(self.images["stand"], (self.rect.x, self.rect.y))
        elif self.collide:
            game.blit(self.images["collide"], (self.rect.x, self.rect.y))
        elif self.vel_y > 0:
            game.blit(self.images["up"], (self.rect.x, self.rect.y))
        elif self.vel_y < 0:
            game.blit(self.images["down"], (self.rect.x, self.rect.y))
        else:
            game.blit(self.images["run"], (self.rect.x, self.rect.y))

    def start(self):
        self.run = True
        self.vel_x = config.VELOCITY_X
        pygame.mixer.music.play()

    def spacebar(self):
        if self.jump < 2:
            self.jump += 1
            if self.level.obstacles:
                if self.jump == 1:
                    self.combo += 1
                if self.shield < config.SHIELD_MAXIMUM:
                    self.shield += 1
                    self.shield_regen_sound.play()
            if self.vel_y < 0:
                self.vel_y = self.level.jump_speed
            else:
                self.vel_y += self.level.jump_speed
        if not self.life:
            self.ended = True

    def save(self):
        song = str(hashlib.md5(self.level.song.get_raw()).hexdigest())
        separator = " "
        highs = []
        first_time = True
        if os.path.exists(config.HIGHSCORE_FILENAME):
            with open(config.HIGHSCORE_FILENAME, "r") as highscores:
                highs = highscores.readlines()
            for index, line in enumerate(highs):
                if line.startswith(song):
                    value = int(line.split(separator)[1])
                    highs[index] = (
                        song + separator + str(int(max(self.score, value))) + "\n"
                    )
                    first_time = False
        if first_time:
            highs.append(song + separator + str(int(self.score)) + "\n")
        with open(config.HIGHSCORE_FILENAME, "w") as highscores:
            highscores.writelines(highs)
