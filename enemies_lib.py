# FILE DEFINES CLASSES AND VARIABLES RELATED TO ENEMIES
import pygame as pg
from pygame import Vector2
from random import randint, uniform
import math

# import custom libraries
from game_lib import GameSprite, GROUP_ENEMY, play_sound
from item_lib import coin, medkit, shield

# import assets
from assets import asset_astroid, asset_explosion, sound_explosion

# chance variables for item dropp
CHANCE_MEDKIT = 0.04
CHANCE_SHIELD = 0.01

# child spawn variables
POS_INTR = 50
ANGLE_ADJ = math.pi / 4
ASTR_SPEED_FACTOR = 0.8
ITEM_SPEED_FACTOR = 0.3


# enemy class, represents asteroid sprites
class Astroid(GameSprite):
    def __init__(self, position: Vector2, direction: Vector2 = Vector2((0, 1)), alter: int = 0,
                 speed: int or float = 0):
        super().__init__()

        # asset
        self.image = asset_astroid.get(alter=alter)

        # movement
        self.position = position
        self.speed = speed
        self.direction = direction

        # collision
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(surface=self.image)
        self.mask_rect = self.mask.get_rect(center=self.rect.center)

        self.rect.center = self.position
        self.mask_rect.center = self.position

        # calculate health / attack depending on version of asset
        self.health = 70 + 3 * (10 ** alter)
        self.attack = 50 + 3 * (12 ** alter)
        self.alter = alter

        GROUP_ENEMY.add(self)

    # called every frame / display update
    def update(self):

        # movement
        self.position += self.direction * self.speed
        self.rect.center = self.position

        super().update()

    # "kills" sprite, removes it from the game + additional features
    def kill(self) -> None:

        # spawn in children asteroids
        self._spawn_children()

        # spawn loot
        self._spawn_loot()

        # spawn explosion animation
        Explosion(position=self.position - Vector2([0, 80]), alter=self.alter)

        # remove itself from the game
        self.delete()

    # generates variables for child spawn
    def _child_var_generate(self, speed_factor: float) -> list:

        speed = self.speed * speed_factor

        alter = round(self.alter) - 1

        position = self.position + Vector2(self.alter * randint(-POS_INTR, POS_INTR),
                                           self.alter * randint(-POS_INTR, POS_INTR))

        angle = uniform(-ANGLE_ADJ, ANGLE_ADJ)
        diff_direction = Vector2([math.cos(angle), math.sin(angle)])
        direction = Vector2(self.direction + diff_direction)

        return [speed, alter, position, direction]

    # function spawn in "child asteroids"
    def _spawn_children(self) -> None:

        # amount of children
        if self.alter != 0:
            if self.alter == 1:
                children = 3
            else:
                children = self.alter

            # create children
            for i in range(children):

                # get vars
                speed, alter, position, direction = \
                    self._child_var_generate(speed_factor=ASTR_SPEED_FACTOR)

                # create
                Astroid(position=position,
                        direction=direction,
                        speed=speed,
                        alter=alter)

    # function spawn in loot depending on probability
    def _spawn_loot(self):

        # spawn coins
        for i in range(self.alter * (2 ** self.alter)):

            # get vars
            speed, _, position, direction = \
                self._child_var_generate(speed_factor=ITEM_SPEED_FACTOR)

            coin(position=position, direction=direction, speed=speed)

        # medkit
        # calculate probability
        prob = uniform(0, 1)
        if prob <= CHANCE_MEDKIT:

            # get vars
            speed, _, position, direction = \
                self._child_var_generate(speed_factor=ITEM_SPEED_FACTOR)

            medkit(position=position, direction=direction, speed=speed)

        # shield
        # calculate probability
        prob = uniform(0, 1)
        if prob <= CHANCE_SHIELD:

            # get vars
            speed, _, position, direction = \
                self._child_var_generate(speed_factor=ITEM_SPEED_FACTOR)

            shield(position=position, direction=direction, speed=speed)


# class for explosion animation sprite
class Explosion(GameSprite):
    def __init__(self, position: Vector2, alter: int=0):
        super().__init__()

        # fetch asset
        self.frames = asset_explosion.get(alter=alter)

        # animation
        self.image = self.frames[0]
        self.current_frame = 0
        self.previous_frame = 0

        # movement
        self.position = position
        self.rect = self.image.get_rect()
        self.rect.center = self.position

        # sound
        play_sound(sound=sound_explosion, channel=1)

    # called every frame / display update
    def update(self):

        # animation speed
        self.current_frame += 0.75

        # end animation & sprite life
        if self.current_frame >= len(self.frames):
            self.kill()
            return

        # change frame
        if int(self.current_frame) != int(self.previous_frame):
            self.image = self.frames[int(self.current_frame)]
