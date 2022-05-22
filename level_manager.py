# FILE DEFINES CLASSES & FUNCTIONS USED TO CONTROL AND GO THROUGH GAME LEVELS AND FUNCTIONALITIES
import pygame as pg
from pygame import Vector2
import time
import random
import math

# custom libraries
from game_lib import SCREEN, GROUP_ENEMY, FPS, play_sound, SPAWN_TOP, SPAWN_BOTTOM, SPAWN_RIGHT, SPAWN_LEFT, SCREEN_SIZE
from enemies_lib import Astroid

# import assets
from assets import level_1_music, level_1_background, level_2_background, level_2_music, \
    level_3_background, level_3_music, sound_level_up


# class controls the flow between levels, connects them
class LEVEL_MANAGER:
    def __init__(self, start_level=0):
        # initiate pygame sound / music functionality
        pg.mixer.init()

        # avl. levels
        self.level_list = [Level_1, Level_2, Level_3]

        # used for current level
        self.level_numb = start_level

        # initiate level
        self.level = self.level_list[self.level_numb]()
        self.level_music()

        # control variables
        self.leveling_up = False
        self.level_up_screen_start = None

        # level complete msg variables
        self.win_font = pg.font.SysFont('broadway', 120)
        self.win_color = (255, 255, 255)
        self.win_msg = self.win_font.render(f'LEVEL {self.level_numb} COMPLETED!!!', True, self.win_color)
        self.win_msg_opacity = 0
        self.win_msg_pos = (450, 400)

        self.win_sound_played = False

        self.win_fade_time = 2
        self.win_show_time = 4
        self.win_total_time = self.win_show_time + 2 * self.win_fade_time
        self.win_msg_opacity_term = 255 / (FPS * self.win_fade_time)

    # called every frame / display update
    def update(self):

        # draw background
        SCREEN.blit(self.level.background.image, self.level.background.location)

        # update level / next wave
        self.level.update()

        # check if next level, start new level
        if ((self.level.done and len(GROUP_ENEMY) == 0) or \
                (self.level.done == True and self.level.level_stop <= time.time() - self.level.start_time)) \
                and not self.leveling_up:

            # update level number
            self.level_numb += 1
            self.win_msg = self.win_font.render(f'LEVEL {self.level_numb} COMPLETED!!!', True, self.win_color)

            # leveling up true, start displaying text
            if not self.level_numb >= len(self.level_list):
                self.level.music.stop()
                self.leveling_up = True
                self.level_up_screen_start = time.time()

            else:
                # all levels complete, go to win-screen -> menu
                return True

        # execute on level up, display win text
        if self.leveling_up:

            time_passed = time.time() - self.level_up_screen_start

            # fade msg
            self.win_msg.set_alpha(self.win_msg_opacity)

            # show message on screen
            SCREEN.blit(self.win_msg, self.win_msg_pos)

            # play sound once
            if not self.win_sound_played:
                play_sound(sound=sound_level_up, channel=5)
                self.win_sound_played = True

            # fade effect on level up text
            if time_passed <= self.win_fade_time:
                self.win_msg_opacity += self.win_msg_opacity_term
            # start next level when message is seen
            elif time_passed >= self.win_total_time:
                self.leveling_up = False
                self.win_sound_played = False
                self.win_msg_opacity = 0

                # start next level
                self.level = self.level_list[self.level_numb]()
                self.level_music()

            # fade away msg
            elif time_passed >= (self.win_show_time + self.win_fade_time):
                self.win_msg_opacity -= self.win_msg_opacity_term

            else:   # continue to show message
                pass

    # controls level music, used to change music
    def level_music(self):
        pg.mixer.Channel(0).stop()
        play_sound(sound=self.level.music, channel=0, loops=-1, fade_ms=2000)


# function returns appropriate direction within interval for asteroid spawns depening on which area it
# spawned in
def get_direction(spawn: str) -> Vector2:

    # parse variables
    spawn = spawn.lower()

    # +- of direction asteroid can go
    angle_marg = math.pi/4
    angle_range = (0, 0)

    # calc angle range depending on area
    if spawn == 'spawn_top':
        angle_range = (0+angle_marg, math.pi-angle_marg)
    elif spawn == 'spawn_bottom':
        angle_range = (math.pi+angle_marg, 2 * math.pi-angle_marg)
    elif spawn == 'spawn_left':
        angle_range = ((3*math.pi)/2+angle_marg, (5*math.pi)/2-angle_marg)
    elif spawn == 'spawn_right':
        angle_range = ((3*math.pi)/2-angle_marg, math.pi/2+angle_marg)

    # chose random angle within intervall
    angle = random.uniform(angle_range[0], angle_range[1])

    # return direction
    return Vector2((math.cos(angle), math.sin(angle)))


# function used to easily and effectively spawn asteroid within selected areas
def spawn_asteroid(spawn=None, position=None, direction=None, speed=None, alter=None):

    # areas where asteroid can spawn
    spawn_reg = {
        SPAWN_TOP: 'SPAWN_TOP',
        SPAWN_BOTTOM: 'SPAWN_BOTTOM',
        SPAWN_LEFT: 'SPAWN_LEFT',
        SPAWN_RIGHT: 'SPAWN_RIGHT'
    }

    # chose random alternative asset, not the giant one
    if alter == None:
        alter = random.randint(0, 2)

    # chose random speed
    if speed == None:
        speed = random.uniform(0.5, 4)

    # chose random spawn position
    if not spawn and not position:
        spawns = [SPAWN_TOP, SPAWN_BOTTOM, SPAWN_LEFT, SPAWN_RIGHT]

        spawn = spawns[random.randint(0, 3)]

        position = Vector2(random.randrange(spawn[0][0], spawn[0][1]),
                           random.randrange(spawn[1][0], spawn[1][1]))

    # chose random position within selected spawn area
    if spawn and not position:
        position = Vector2(random.randrange(spawn[0][0], spawn[0][1]),
                           random.randrange(spawn[1][0], spawn[1][1]))

    # get logical direction depending on spawn area
    if direction is None:

        direction = get_direction(spawn=spawn_reg[spawn])

    # ultimately spawn asteroid
    Astroid(position=position, alter=alter, speed=speed, direction=direction)


# ONLY THIS LEVEL CLASS WILL BE PROPERLY COMMENTED, AS THEY ALL WORK EXACTLY THE SAME
# class that defines a level in the game
class Level_1:
    def __init__(self):

        # level scene specific variables used by level_manager
        self.background = level_1_background
        self.music = level_1_music

        # control variables
        self.start_time = time.time()
        self.time_passed = time.time() - self.start_time
        self.done = False

        # how long until last wave and max level time, proceeds to next level when level_stop is reached
        self.level_time = 110
        self.level_stop = 200

        # register of all waves, key: wave number; (seconds after start wave spawns, which wave function is run)
        self.wave_reg = {
            0: (0, self._wave_0),
            1: (15, self._wave_1),
            2: (40, self._wave_2),
            3: (65, self._wave_3),
            4: (110, self._wave_4)
        }

        # current wave, wave number and register length
        self.wave = self.wave_reg[0]
        self.wave_nmb = 0
        self.wave_reg_len = len(self.wave_reg)

    # update, start next wave of enemies, next wave always pending in self.wave variable
    def update(self):

        self.time_passed = time.time() - self.start_time

        # proceed to start current wave when start time is achieved and level isn't done
        if ((self.time_passed >= self.wave[0]) or (len(GROUP_ENEMY) == 0)) and not self.done:

            # start current wave
            self.wave[1]()
            self.wave_nmb += 1

            # all waves done, wait out until level_stop is achieved or all enemies are killed
            if self.wave_nmb >= self.wave_reg_len:

                self.done = True
                return

            # otherwise proceed to next wave
            self.wave = self.wave_reg[self.wave_nmb]

        else:
            pass

    # ONLY ONE WAVE IS COMMENTED, AS THEY ALL ARE SIMPLE AND WORK ABOUT EXACTLY THE SAME
    # function defines a single wave of enemies spawned in one single frame of time
    def _wave_0(self):

        # spawn in 40 asteroids in left area, asset 0
        for i in range(40):
            spawn_asteroid(spawn=SPAWN_LEFT, alter=0)

        # spawn in 10 asteroids in left area, asset 1
        for i in range(10):
            spawn_asteroid(spawn=SPAWN_LEFT, alter=1)

    def _wave_1(self):
        for i in range(40):
            spawn_asteroid(spawn=SPAWN_RIGHT, alter=0)

        for i in range(10):
            spawn_asteroid(spawn=SPAWN_RIGHT, alter=1)

    def _wave_2(self):
        for i in range(80):
            spawn_asteroid(spawn=SPAWN_TOP, alter=0)

        for i in range(10):
            spawn_asteroid(spawn=SPAWN_TOP, alter=2)

    def _wave_3(self):
        for i in range(80):
            spawn_asteroid(spawn=SPAWN_BOTTOM, alter=0)

        for i in range(10):
            spawn_asteroid(spawn=SPAWN_BOTTOM, alter=1)

    # boss-battle (same as other waves)
    def _wave_4(self):

        spawn_asteroid(spawn=SPAWN_TOP, alter=3, speed=0.75, position=Vector2((SCREEN_SIZE.x - 400) / 3, -99),
                       direction=Vector2([0, 1]))

        spawn_asteroid(spawn=SPAWN_TOP, alter=3, speed=0.75, position=Vector2((SCREEN_SIZE.x - 400) / 3 * 2, -99),
                       direction=Vector2([0, 1]))

        spawn_asteroid(spawn=SPAWN_TOP, alter=3, speed=0.75, position=Vector2((SCREEN_SIZE.x - 400), -99),
                       direction=Vector2([0, 1]))


class Level_2:
    def __init__(self):
        self.background = level_2_background
        self.music = level_2_music
        self.start_time = time.time()
        self.time_passed = time.time() - self.start_time
        self.done = False

        self.level_time = 110
        self.level_stop = 200

        # register of all waves
        self.wave_reg = {
            # top wave
            0: (0, self._wave_0),
            1: (2, self._wave_0),
            2: (4, self._wave_0),

            # bottom wave
            3: (10, self._wave_1),
            4: (12, self._wave_1),
            5: (14, self._wave_1),

            # left/right wave
            6: (20, self._wave_2),
            7: (22, self._wave_2),
            8: (24, self._wave_2),

            # top wave
            9: (30, self._wave_3),
            10: (31, self._wave_3),
            11: (32, self._wave_3),

            # bottom wave
            12: (34, self._wave_4),
            13: (35, self._wave_4),
            14: (36, self._wave_4),

            # left/right wave
            15: (38, self._wave_5),
            16: (39, self._wave_5),
            17: (40, self._wave_5),

            # top wave
            18: (50, self._wave_0),
            19: (52, self._wave_0),
            20: (54, self._wave_0),

            # bottom wave
            21: (60, self._wave_1),
            22: (62, self._wave_1),
            23: (64, self._wave_1),

            # left/right wave
            24: (70, self._wave_2),
            25: (72, self._wave_2),
            26: (74, self._wave_2),

            # top wave
            27: (80, self._wave_3),
            28: (81, self._wave_3),
            29: (82, self._wave_3),

            # bottom wave
            30: (85, self._wave_4),
            31: (86, self._wave_4),
            32: (87, self._wave_4),

            # left/right wave
            33: (90, self._wave_5),
            34: (91, self._wave_5),
            35: (92, self._wave_5),

            # boss fight
            36: (95, self._wave_6),
            37: (95, self._wave_7)
        }

        self.wave = self.wave_reg[0]
        self.wave_nmb = 0
        self.wave_reg_len = len(self.wave_reg)

    # update, start next wave of enemies
    def update(self):

        self.time_passed = time.time() - self.start_time

        if ((self.time_passed >= self.wave[0]) or (len(GROUP_ENEMY) == 0)) and not self.done:

            self.wave[1]()
            self.wave_nmb += 1

            if self.wave_nmb >= self.wave_reg_len:

                self.done = True
                return

            self.wave = self.wave_reg[self.wave_nmb]

        else:
            pass

    def _wave_0(self):
        for i in range(10):
            spawn_asteroid(spawn=SPAWN_TOP, alter=2, speed=5)

    def _wave_1(self):
        for i in range(10):
            spawn_asteroid(spawn=SPAWN_BOTTOM, alter=2, speed=5)

    def _wave_2(self):
        for i in range(10):
            spawn_asteroid(spawn=SPAWN_LEFT, alter=2, speed=5)
            spawn_asteroid(spawn=SPAWN_RIGHT, alter=2, speed=5)

    def _wave_3(self):
        for i in range(3):
            spawn_asteroid(spawn=SPAWN_TOP, alter=2, speed=8)

    def _wave_4(self):
        for i in range(3):
            spawn_asteroid(spawn=SPAWN_BOTTOM, alter=2, speed=8)

    def _wave_5(self):
        for i in range(3):
            spawn_asteroid(spawn=SPAWN_TOP, alter=2, speed=8)
            spawn_asteroid(spawn=SPAWN_LEFT, alter=2, speed=8)

    # boss-battle
    def _wave_6(self):
        for i in range(100):
            spawn_asteroid(alter=0, speed=2)

        for i in range(20):
            spawn_asteroid(alter=1, speed=1.5)

    def _wave_7(self):
        spawn_asteroid(position=Vector2(-75, 400), speed=1, alter=3, direction=Vector2([1,0]))
        spawn_asteroid(position=Vector2(SCREEN_SIZE.x + 150, 400), speed=1, alter=3, direction=Vector2([-1,0]))


class Level_3:
    def __init__(self):
        self.background = level_3_background
        self.music = level_3_music
        self.start_time = time.time()
        self.time_passed = time.time() - self.start_time
        self.done = False

        self.level_time = 80
        self.level_stop = 160

        # register of all waves
        self.wave_reg = {
            # left wave
            0: (0, self._wave_0),
            1: (1, self._wave_0),
            2: (2, self._wave_0),
            3: (3, self._wave_0),
            4: (4, self._wave_0),
            5: (5, self._wave_0),
            6: (6, self._wave_0),
            7: (7, self._wave_0),
            8: (8, self._wave_0),

            # top wave
            9: (15, self._wave_1),
            10: (16, self._wave_1),
            11: (17, self._wave_1),
            12: (18, self._wave_1),
            13: (19, self._wave_1),
            14: (20, self._wave_1),
            15: (21, self._wave_1),
            16: (22, self._wave_1),
            17: (23, self._wave_1),

            # bottom wave
            18: (33, self._wave_2),
            19: (34, self._wave_2),
            20: (35, self._wave_2),
            21: (36, self._wave_2),
            22: (37, self._wave_2),
            23: (38, self._wave_2),
            24: (39, self._wave_2),
            25: (40, self._wave_2),
            26: (41, self._wave_2),

            # right wave
            27: (50, self._wave_3),
            28: (51, self._wave_3),
            29: (52, self._wave_3),
            30: (53, self._wave_3),
            31: (54, self._wave_3),
            32: (55, self._wave_3),
            33: (56, self._wave_3),
            34: (57, self._wave_3),
            35: (58, self._wave_3),

            # boss fight
            36: (70, self._wave_5),
            37: (71, self._wave_4),
            38: (74, self._wave_4),
            39: (77, self._wave_4),

        }

        self.wave = self.wave_reg[0]
        self.wave_nmb = 0
        self.wave_reg_len = len(self.wave_reg)

    # update, start next wave of enemies
    def update(self):

        self.time_passed = time.time() - self.start_time

        if ((self.time_passed >= self.wave[0]) or (len(GROUP_ENEMY) == 0)) and not self.done:

            self.wave[1]()
            self.wave_nmb += 1

            if self.wave_nmb >= self.wave_reg_len:

                self.done = True
                return

            self.wave = self.wave_reg[self.wave_nmb]

        else:
            pass

    def _wave_0(self):
        for i in range(4):
            spawn_asteroid(spawn=SPAWN_LEFT, alter=1, speed=3)
            spawn_asteroid(spawn=SPAWN_LEFT, alter=1, speed=6)

        for i in range(4):
            spawn_asteroid(spawn=SPAWN_LEFT, alter=1, speed=2)
            spawn_asteroid(spawn=SPAWN_LEFT, alter=0, speed=2.5)

    def _wave_1(self):
        for i in range(4):
            spawn_asteroid(spawn=SPAWN_TOP, alter=1, speed=3)
            spawn_asteroid(spawn=SPAWN_TOP, alter=1, speed=6)

        for i in range(4):
            spawn_asteroid(spawn=SPAWN_TOP, alter=1, speed=2)
            spawn_asteroid(spawn=SPAWN_TOP, alter=0, speed=2.5)

    def _wave_2(self):
        for i in range(4):
            spawn_asteroid(spawn=SPAWN_BOTTOM, alter=1, speed=3)
            spawn_asteroid(spawn=SPAWN_BOTTOM, alter=1, speed=6)

        for i in range(4):
            spawn_asteroid(spawn=SPAWN_BOTTOM, alter=1, speed=2)
            spawn_asteroid(spawn=SPAWN_BOTTOM, alter=0, speed=2.5)

    def _wave_3(self):
        for i in range(4):
            spawn_asteroid(spawn=SPAWN_RIGHT, alter=1, speed=3)
            spawn_asteroid(spawn=SPAWN_RIGHT, alter=1, speed=6)

        for i in range(4):
            spawn_asteroid(spawn=SPAWN_RIGHT, alter=1, speed=2)
            spawn_asteroid(spawn=SPAWN_RIGHT, alter=0, speed=2.5)

    # BOSS FIGHT
    def _wave_4(self):
        for i in range(7):
            spawn_asteroid(alter=2, speed=1)
            spawn_asteroid(alter=2, speed=2)

    def _wave_5(self):
        spawn_asteroid(spawn=SPAWN_RIGHT, alter=3, speed=2)
        spawn_asteroid(spawn=SPAWN_LEFT, alter=3, speed=2)
        spawn_asteroid(spawn=SPAWN_TOP, alter=3, speed=2)
        spawn_asteroid(spawn=SPAWN_BOTTOM, alter=3, speed=2)






