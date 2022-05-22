import pygame as pg
from pygame import Vector2
from copy import copy
import math

# custom libraries
from game_lib import GROUP_PLAYER, BORDER_PLAYER, FPS, GameSprite, play_sound
from enemies_lib import Explosion

# import assets
from assets import asset_space_ship, asset_laser_bullet, sound_warp, sound_laser_shot


# class represents player sprite
class space_ship(GameSprite):
    def __init__(self):
        super().__init__()

        # fetch asset
        self.image = asset_space_ship.get(alter=0)

        self.og_image = self.image

        # basics: health / attack
        self.health = 2000
        self.health_max = self.health
        self.attack = 10000

        # movement
        self.angle = 0
        self.angle_speed = 5
        self.direction = Vector2([0, 1])
        self.speed = 7
        self.current_speed = 0
        self.back_speed_factor = 0.7
        self.position = Vector2((500, 500))
        self.inertia_factor = 0.99

        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(surface=self.image)
        self.mask_rect = self.mask.get_rect(center=self.rect.center)

        self.rect.center = self.position

        # abilities
        self.warp_mode = False
        self.warp_acceleration = 2
        self.warp_distance = 250
        self.current_warp_speed = self.speed
        self.warp_start = None
        self.warp_dest = None
        self.warp_intervall_fps = 120
        self.current_warp_intervall_fps = self.warp_intervall_fps
        self.warp_max = 5
        self.warp_avl = 3
        self.warp_shield_time = 2

        self.shoot_intervall_fps = 5
        self.current_shoot_intervall_fps = self.shoot_intervall_fps

        # effects & points
        self.score = 0

        self.shield = False
        self.shield_time = 0
        self.shield_time_current = self.shield_time

        # give player shield at game start for 5 seconds
        self.activate_shield(time=5)

        # add to player group, collision management
        GROUP_PLAYER.add(self)

    # activates player warp mode, where movement & collisions work differently
    def warp(self):
        self.warp_mode = True
        # copy of position where warp started, used to end warping after certain distance
        self.warp_start = copy(self.position)
        self.activate_shield(time=self.warp_shield_time)
        play_sound(sound=sound_warp, channel=4)

    # function activates shield ability for a predetermined time
    def activate_shield(self, time):

        # shield do not add upp beyond max shield time for item / ability
        if not self.shield or time >= self.shield_time:
            self.shield = True
            self.shield_time = time
            self.shield_time_current = time

        else:
            pass

    # function allows player to shoot laser-bullets
    def shoot(self):

        # configuration for where laser-bullets are spawned relative to player
        radius = -35
        angle = 65
        speed = 25

        direction_r = Vector2(math.cos((self.angle + angle)*(math.pi/180)), math.sin((self.angle + angle)*(math.pi/180)))
        direction_l = Vector2(math.cos((self.angle - angle)*(math.pi/180)), math.sin((self.angle - angle)*(math.pi/180)))

        shooter_r = self.position + (direction_r * radius)
        shooter_l = self.position + (direction_l * radius)

        # spawn 2 bullets, one on either side
        bullet_r = laser_bullet(position=shooter_r, direction=self.direction,
                              angle=self.angle, speed=speed)
        bullet_l = laser_bullet(position=shooter_l, direction=self.direction,
                              angle=self.angle, speed=speed)

    # called every frame / display update
    def update(self):

        # fetch updated keyboard data
        key = pg.key.get_pressed()

        # normal player movement (no in warp-mode / warping)
        if not self.warp_mode:
            # translate user input into movement & abilities
            if key[pg.K_w]:
                self.position += self.direction * -self.speed
                self.current_speed = -self.speed
            if key[pg.K_s]:
                self.position += self.direction * (self.speed * self.back_speed_factor)
                self.current_speed = (self.speed * self.back_speed_factor)
            # rotation
            if key[pg.K_d]:
                self.angle += self.angle_speed
            if key[pg.K_a]:
                self.angle -= self.angle_speed
            # inertia
            if not (key[pg.K_w] or key[pg.K_s]) and abs(self.current_speed) > 0.1:
                self.position += self.direction * self.current_speed
                self.current_speed = self.current_speed * self.inertia_factor

            # shooting
            if key[pg.K_u] and self.current_shoot_intervall_fps <= 0:
                self.shoot()
                self.current_shoot_intervall_fps = self.shoot_intervall_fps
            else:
                self.current_shoot_intervall_fps -= 1

            # warping
            if key[pg.K_i] and self.warp_avl > 0:
                self.warp()
                self.warp_avl -= 1
                self.current_speed = 0
            else:   # warping timer / adder, for additional warps
                if self.current_warp_intervall_fps <= 0:
                    if self.warp_avl < self.warp_max:
                        self.warp_avl += 1
                        self.current_warp_intervall_fps = self.warp_intervall_fps
                    else:
                        pass
                if self.current_warp_intervall_fps != 0:
                    self.current_warp_intervall_fps -= 1

            # warping shield, count down / disable
            if self.shield_time_current <= 0:
                self.shield = False
                self.shield_time = 0
                self.shield_time_current = 0
            else:
                self.shield_time_current -= 1/FPS

        # movement in warp-mode (when warping)
        elif self.warp_mode:

            # movement
            self.position -= self.direction * self.current_warp_speed

            # accelerate
            self.current_warp_speed = self.current_warp_speed * self.warp_acceleration

            # disable warping depending on distance from warp start
            if self.position.distance_squared_to(self.warp_start) >= (self.warp_distance ** 2):
                self.warp_mode = False
                self.current_warp_speed = self.speed

        # make sure variables are in determined maxes
        if self.health > self.health_max:
            self.health = self.health_max

        if self.warp_avl > self.warp_max:
            self.warp_avl = self.warp_max

        # update direction & angle of sprite
        # turn sprite if it collides with player-border
        if not BORDER_PLAYER[0][0] <= self.position.x <= BORDER_PLAYER[0][1]:
            self.angle = 180 - self.angle
        elif not BORDER_PLAYER[1][0] <= self.position.y <= BORDER_PLAYER[1][1]:
            self.angle = 360 - self.angle

        self.angle %= 360
        self.direction = Vector2(math.cos(self.angle*(math.pi/180)), math.sin(self.angle*(math.pi/180)))

        # fix ev. border bug where player skips / warps through border
        if BORDER_PLAYER[0][0] >= self.position.x:
            self.position.x += BORDER_PLAYER[0][0] - self.position.x
        if BORDER_PLAYER[0][1] <= self.position.x:
            self.position.x += BORDER_PLAYER[0][1] - self.position.x
        if BORDER_PLAYER[1][0] >= self.position.y:
            self.position.y += BORDER_PLAYER[1][0] - self.position.y
        if BORDER_PLAYER[1][1] <= self.position.y:
            self.position.y += BORDER_PLAYER[1][1] - self.position.y

        # check if player still alive, else kill player
        if self.health <= 0:
            self.kill()
            return

        # move sprite to new position & rotate image
        self.rect.center = self.position

        self.image = pg.transform.rotate(self.og_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        self.mask = pg.mask.from_surface(surface=self.image)
        self.mask_rect = self.mask.get_rect(center=self.rect.center)

        self.mask_rect.center = self.position

    # spawn explosion upon player death and delete itself
    def kill(self) -> None:
        Explosion(position=self.position - (0, 100), alter=1)
        self.delete()


# class represents laser bullets shot by player
class laser_bullet(GameSprite):
    def __init__(self, position: Vector2, direction: Vector2, angle, speed=10):
        super().__init__()

        # fetch asset
        self.og_image = asset_laser_bullet.get(alter=0)

        self.angle = angle
        self.image = pg.transform.rotate(self.og_image, -self.angle)

        # movement
        self.position = position
        self.direction = direction
        self.speed = speed

        # collisions
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(surface=self.image)
        self.mask_rect = self.mask.get_rect(center=self.rect.center)

        self.rect.center = self.position
        self.mask_rect.center = self.position

        # damage to asteroids
        self.attack = 25

        # add to player group, collision management
        GROUP_PLAYER.add(self)

        play_sound(sound=sound_laser_shot, channel=2)

    # called every frame / display update
    def update(self):

        # movement
        self.position -= self.direction * self.speed
        self.rect.center = self.position
        self.mask_rect.center = self.position

        super().update()
