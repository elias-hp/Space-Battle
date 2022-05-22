# FILE DEFINES BASIC CLASSES, VARIABLES AND FUNCTIONS GLOBALLY USED BETWEEN LIBRARIES AND main.py
import pygame as pg
from pygame import Vector2
from PIL import Image
import os

# general game variables
CLOCK = pg.time.Clock()
FPS = 60

# game-screen configuration
SCREEN_SIZE = Vector2((1800, 1000))
SCREEN = pg.display.set_mode((SCREEN_SIZE.x, SCREEN_SIZE.y))
pg.display.set_caption('Space-Battle')

# sprite groups, used for collisions and updates
GROUP_ENEMY = pg.sprite.Group()
GROUP_PLAYER = pg.sprite.Group()
GROUP_ITEM = pg.sprite.Group()
GROUP_GAME_SPRITES = pg.sprite.Group()

ALL_GROUP = [GROUP_ITEM, GROUP_PLAYER, GROUP_ENEMY, GROUP_GAME_SPRITES]

# borders, used for sprite movement limitation and deletion
#                X - VALS                    Y - VALS
SPAWN_BORDER = ((-50, SCREEN_SIZE.x + 250), (-50, SCREEN_SIZE.y + 250))
BORDER = ((-100, SCREEN_SIZE.x + 350), (-100, SCREEN_SIZE.y + 350))
BORDER_PLAYER = ((-70, SCREEN_SIZE.x + 70), (-70, SCREEN_SIZE.y + 70))

# spawn areas, used for spawning in asteroid enemies
SPAWN_TOP = ((-100, SCREEN_SIZE.x + 350), (-100, -50))
SPAWN_BOTTOM = ((-100, SCREEN_SIZE.x + 350), (SCREEN_SIZE.y + 50, SCREEN_SIZE.y + 100))
SPAWN_LEFT = ((-100, -50), (-100, SCREEN_SIZE.y + 350))
SPAWN_RIGHT = ((SCREEN_SIZE.x + 100, SCREEN_SIZE.x + 350), (-100, SCREEN_SIZE.y + 350))


# used to remove all sprites upon game restart
def reset_game():
    for i in GROUP_GAME_SPRITES:
        i.delete()


# used to properly close game-program
def end_game():
    pg.quit()
    exit()


# func plays sound in specific sound/music-channel, sound plays in separate process
# channels: 0=music/background, 1=Explosions, 2=Bullets, 3=Items, 4=warp, 5=other
def play_sound(sound: pg.mixer.Sound, channel: int=5, loops=0, fade_ms=0):
    pg.mixer.Channel(channel).play(sound, loops=loops, fade_ms=fade_ms)


# used to load images the correct way according to pygame, significantly lowers processing / lag
def image_load(image_dir):
    return pg.image.load(image_dir).convert_alpha()


# asset class, represents backgrounds, works like pygame sprite (although not in a group)
class Background(pg.sprite.Sprite):
    def __init__(self, image_dir: str, location=[0, 0]):
        super().__init__()

        # load and fit image file to screen
        self.image = image_load(image_dir)
        self.image = pg.transform.scale(self.image, (SCREEN_SIZE.x, SCREEN_SIZE.y))

        # center / move correctly
        self.location = location
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


# asset class, represents all still image assets
class Asset:
    def __init__(self, img_dir, size_factor=1):
        self.img_dir = img_dir

        # gets image size
        with Image.open(img_dir) as img:
            self.img_dim = Vector2([img.width, img.height])

        # loads image and uniformly transforms image to new size
        image = pg.transform.scale(image_load(img_dir), size=(self.img_dim * size_factor))

        # adds to dictionary of alternative sizes of relevant asset
        self.alter = {0: image}

    # func adds new size of asset
    def add_alter(self, size_factor, nmb: int):
        # loads image and uniformly transforms image to new size
        alt_image = pg.transform.scale(image_load(self.img_dir), size=(self.img_dim * size_factor))
        # adds to list of alternative sizes of relevant asset
        self.alter[nmb] = alt_image

    # get asset for use in sprite
    def get(self, alter: int = 0):
        # get alternative version from register
        asset = self.alter[alter]

        return asset


# asset class, represents all animated assets
class AnimatedAsset:
    def __init__(self, img_fold, size_factor=1):
        self.img_fold = img_fold
        self.frame_list = []

        # gets image size (all frames should be same size)
        with Image.open(rf'{self.img_fold}/0.png') as img:
            self.img_dim = Vector2([img.width, img.height])

        # append / order all image frames to frame_list
        for i, file in enumerate(os.listdir(self.img_fold)):

            frame = rf'{self.img_fold}/{i}.png'

            # gets image size
            with Image.open(frame) as img:
                frame_size = Vector2([img.width, img.height])

            # loads image and uniformly transforms image to new size
            frame = pg.transform.scale(image_load(frame), size=(frame_size * size_factor))

            self.frame_list.append(frame)

        # adds to dictionary of alternative sizes of relevant asset
        self.alter = {0: self.frame_list}

    # func adds new size of asset
    def add_alter(self, size_factor, nmb: int):
        alt_frames = []

        # append / order all image frames to frame_list, also loads and transforms them accordingly
        for i, j in enumerate(self.frame_list):
            mod_frame = pg.transform.scale(image_load(rf'{self.img_fold}/{i}.png'), size=(self.img_dim * size_factor))
            alt_frames.append(mod_frame)

        # adds to dictionary of alternative sizes of relevant asset
        self.alter[nmb] = alt_frames

    # get asset for use in sprite
    def get(self, alter: int = 0):
        asset = self.alter[alter]

        return asset


# class used by most sprite in game, adds additional / basic features
class GameSprite(pg.sprite.Sprite):
    def __init__(self):
        # update parent-class pygame sprite
        super().__init__()

        # basic characteristics all interactable sprites need to function
        self.health = 1
        self.attack = 0

        # add to group used for updates & drawing
        GROUP_GAME_SPRITES.add(self)

    # "kills" sprite, removes it from the game
    def kill(self) -> None:
        for i in ALL_GROUP:
            i.remove(self)

    # alternative to kill if child class repurposes kill function
    def delete(self) -> None:
        for i in ALL_GROUP:
            i.remove(self)

def update(self):

        # logic deletes sprite if it's outside game borders
        if not BORDER[0][0] <= self.position.x <= BORDER[0][1]:
            self.delete()
        elif not BORDER[1][0] <= self.position.y <= BORDER[1][1]:
            self.delete()
        # logic kills sprite if health drops to or below zero
        elif self.health <= 0:
            self.kill()
