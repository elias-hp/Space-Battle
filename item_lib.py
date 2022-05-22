import pygame as pg
from pygame import Vector2

# custom libs
from game_lib import GameSprite, GROUP_ITEM, play_sound

# import assets
from assets import asset_coin, asset_shield, asset_medkit, sound_medkit, sound_coin, sound_shield


# class for all item sprites, e.g. coins & shields
class Item(GameSprite):
    def __init__(self, position: Vector2, direction: Vector2, image, speed=0):
        super().__init__()

        # sprite image
        self.image = image

        # movement
        self.position = position
        self.direction = direction
        self.speed = speed

        # collision
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(surface=self.image)
        self.mask_rect = self.mask.get_rect(center=self.rect.center)

        self.rect.center = self.position
        self.mask_rect.center = self.position

        # add to item group, used for collision w. player
        GROUP_ITEM.add(self)

    # called every frame / display update
    def update(self):

        # movement
        self.position += self.direction * self.speed

        # movement & collision detection
        self.rect.center = self.position
        self.mask_rect.center = self.position

        # parent class update, e.g. for border deletion feature
        super().update()


# medkit item class, represents medkit sprite
class medkit(Item):
    def __init__(self, position: Vector2, direction: Vector2, speed=0):
        image = asset_medkit.get(alter=0)
        super().__init__(position, direction, image, speed)

    # play sound when player "kills" (picks up) item
    def kill(self) -> None:
        play_sound(channel=3, sound=sound_medkit)
        self.delete()


# shield item class, represents shield sprite
class shield(Item):
    def __init__(self, position: Vector2, direction: Vector2, speed=0):
        image = asset_shield.get(alter=0)
        super().__init__(position, direction, image, speed)

    # play sound when player "kills" (picks up) item
    def kill(self) -> None:
        play_sound(channel=3, sound=sound_shield)
        self.delete()


# coin item class, represents coin sprite
class coin(Item):
    def __init__(self, position: Vector2, direction: Vector2 = Vector2((0, 1)), speed=0):

        # setup variables used for flip animation
        self.frames = asset_coin.get()
        self.image = self.frames[0]
        self.current_frame = 0
        self.previous_frame = 0

        super().__init__(position=position, speed=speed, direction=direction, image=self.frames[0])

    # play sound when player "kills" (picks up) item
    def kill(self) -> None:
        play_sound(channel=3, sound=sound_coin)
        self.delete()

    # called every frame / display update
    def update(self):

        # animation speed
        self.current_frame += 0.175

        # restart animation
        if self.current_frame >= len(self.frames):
            self.current_frame = 0

        # change animation frame
        if int(self.current_frame) != int(self.previous_frame):
            self.image = self.frames[int(self.current_frame)]
            self.mask = pg.mask.from_surface(surface=self.image)
            self.rect = self.mask.get_rect()

        # update typical item features
        super().update()

