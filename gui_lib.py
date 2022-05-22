# FILE DEFINES CLASSES ADN VARIABLES USED TO FROM GUI
import pygame as pg
from pygame import Vector2
import pygame_widgets
from pygame_widgets.slider import Slider

# custom libraries
from game_lib import SCREEN, SCREEN_SIZE, play_sound, end_game, FPS

# import assets
from assets import sound_click, background_menu, sound_menu, sound_death_screen, sound_win_screen

# colors in RGB
WHITE = (255, 255, 255)
RED = (250, 36, 36)
RED_DARK = (159, 0, 0)
BLUE = (36, 36, 250)
BLUE_DARK = (0, 0, 159)
BLUE_LIGHT = (95, 219, 255)
BLACK = (0, 0, 0)
GREEN = (0, 204, 0)
GREEN_DARK = (0, 85, 0)
YELLOW = (253, 238, 0)
YELLOW_DARK = (245, 199, 26)
YELLOW_LIGHT = (255, 255, 102)

# gui bar configuration
BARS_LENGTH = 700
BARS_WIDTH = 17
BARS_OUTLINE = 3
BARS_OUTLINE_LENGTH = BARS_LENGTH + BARS_OUTLINE * 2
BARS_OUTLINE_WIDTH = BARS_WIDTH + BARS_OUTLINE * 2
BARS_SPACING = Vector2(0, BARS_OUTLINE_WIDTH + BARS_WIDTH + 10)

BARS_POS = Vector2([20, 850])
BAR_HEALTH_POS = BARS_POS + 2 * BARS_SPACING
BAR_WARP_POS = BARS_POS + BARS_SPACING
BAR_SHIELD_POS = BARS_POS

BAR_MAX_X = BARS_POS + Vector2(BARS_LENGTH, 0)
BAR_WARP_INTERVALL = 5

LEVEL_BAR_LENGTH = 1000
LEVEL_BAR_WIDTH = 17
LEVEL_BAR_OUTLINE = 3
LEVEL_BAR_OUTLINE_LENGTH = LEVEL_BAR_LENGTH + LEVEL_BAR_OUTLINE * 2
LEVEL_BAR_OUTLINE_WIDTH = LEVEL_BAR_WIDTH + LEVEL_BAR_OUTLINE * 2

LEVEL_BAR_POS = Vector2([400, 10])

# score configuration
SCORE_FONT = pg.font.SysFont('Impact', 60)
SCORE_LOCATION = SCREEN_SIZE - (250, 975)


# gui management class, controls and computes most of gui
class GUI:

    def __init__(self):

        # score-counter 
        self.score_text = SCORE_FONT.render('SCORE: 0', True, WHITE)

    # called every frame / display update, updates all in-game gui w. relevant game variables
    def update(self, score, health, health_max, warp_max, warp_avl, current_warp_intervall_fps, warp_intervall_fps,
               shield_time, shield_time_current, level_time, current_level_time, level_stop_time):

        # draw score
        self.score_text = SCORE_FONT.render(f'SCORE: {score}', True, WHITE)
        SCREEN.blit(self.score_text, SCORE_LOCATION)

        # draw level bar
        level_percent = 1 - current_level_time / level_stop_time
        level_stop_percent = (level_stop_time - level_time) / level_stop_time
        if level_percent <= level_stop_percent:
            level_stop_percent = level_percent
        pg.draw.rect(SCREEN, BLACK, pg.Rect(LEVEL_BAR_POS.x - LEVEL_BAR_OUTLINE, LEVEL_BAR_POS.y - LEVEL_BAR_OUTLINE,
                                            LEVEL_BAR_OUTLINE_LENGTH, LEVEL_BAR_OUTLINE_WIDTH))
        pg.draw.rect(SCREEN, YELLOW_DARK, pg.Rect(LEVEL_BAR_POS.x, LEVEL_BAR_POS.y, LEVEL_BAR_LENGTH, LEVEL_BAR_WIDTH))
        pg.draw.rect(SCREEN, YELLOW,
                     pg.Rect(LEVEL_BAR_POS.x, LEVEL_BAR_POS.y, LEVEL_BAR_LENGTH * level_percent, LEVEL_BAR_WIDTH))
        pg.draw.rect(SCREEN, YELLOW_LIGHT,
                     pg.Rect(LEVEL_BAR_POS.x, LEVEL_BAR_POS.y, LEVEL_BAR_LENGTH * level_stop_percent, LEVEL_BAR_WIDTH))

        # draw health bar
        health_percent = health / health_max
        pg.draw.rect(SCREEN, BLACK,
                     pg.Rect(BAR_HEALTH_POS.x - BARS_OUTLINE, BAR_HEALTH_POS.y - BARS_OUTLINE, BARS_OUTLINE_LENGTH,
                             BARS_OUTLINE_WIDTH))
        pg.draw.rect(SCREEN, RED_DARK, pg.Rect(BAR_HEALTH_POS.x, BAR_HEALTH_POS.y, BARS_LENGTH, BARS_WIDTH))
        pg.draw.rect(SCREEN, RED, pg.Rect(BAR_HEALTH_POS.x, BAR_HEALTH_POS.y, BARS_LENGTH * health_percent, BARS_WIDTH))

        # draw shield bar
        if shield_time_current > 0:
            shield_percent = shield_time_current / shield_time
        else:
            shield_percent = 0
        pg.draw.rect(SCREEN, BLACK,
                     pg.Rect(BAR_SHIELD_POS.x - BARS_OUTLINE, BAR_SHIELD_POS.y - BARS_OUTLINE, BARS_OUTLINE_LENGTH,
                             BARS_OUTLINE_WIDTH))
        pg.draw.rect(SCREEN, GREEN_DARK, pg.Rect(BAR_SHIELD_POS.x, BAR_SHIELD_POS.y, BARS_LENGTH, BARS_WIDTH))
        pg.draw.rect(SCREEN, GREEN,
                     pg.Rect(BAR_SHIELD_POS.x, BAR_SHIELD_POS.y, BARS_LENGTH * shield_percent, BARS_WIDTH))

        # Warp bar
        pg.draw.rect(SCREEN, BLACK,
                     pg.Rect(BAR_WARP_POS.x - BARS_OUTLINE, BAR_WARP_POS.y - BARS_OUTLINE, BARS_OUTLINE_LENGTH,
                             BARS_OUTLINE_WIDTH))
        pg.draw.rect(SCREEN, BLUE, pg.Rect(BAR_WARP_POS.x, BAR_WARP_POS.y, BARS_LENGTH, BARS_WIDTH))
        # draw background cells
        cell_length = (BARS_LENGTH - (warp_max * BAR_WARP_INTERVALL) - BAR_WARP_INTERVALL) / warp_max
        cell_x = BAR_WARP_POS.x + BAR_WARP_INTERVALL
        for rect in range(warp_max):
            pg.draw.rect(SCREEN, BLUE_DARK, pg.Rect(cell_x, BAR_WARP_POS.y, cell_length, BARS_WIDTH))
            cell_x += BAR_WARP_INTERVALL + cell_length
        # draw active cells
        cell_x = BAR_WARP_POS.x + BAR_WARP_INTERVALL
        for rect in range(warp_avl):
            pg.draw.rect(SCREEN, BLUE_LIGHT, pg.Rect(cell_x, BAR_WARP_POS.y, cell_length, BARS_WIDTH))
            cell_x += BAR_WARP_INTERVALL + cell_length
        # draw regenerating cell
        if warp_avl < warp_max:
            cell_percent = (warp_intervall_fps - current_warp_intervall_fps) / warp_intervall_fps
            pg.draw.rect(SCREEN, BLUE_LIGHT, pg.Rect(cell_x, BAR_WARP_POS.y, cell_length * cell_percent, BARS_WIDTH))


# menu gui configuration
BUTTON_COLOR_0 = (125, 125, 125)
BUTTON_COLOR_1 = (175, 175, 175)

BUTTON_MARGINAL_COLOR_0 = (200, 200, 200)
BUTTON_MARGINAL_COLOR_1 = (255, 255, 255)

BUTTON_SIZE = (550, 130)
MARGINAL_SIZE = 10

MENU_FONT = pg.font.SysFont('Impact', 80)
MENU_BACKGROUND = background_menu
MENU_MUSIC = sound_menu

BUTTON_START_POS = ((SCREEN_SIZE.x - BUTTON_SIZE[0]) / 2, 200)
BUTTON_START_TEXT = MENU_FONT.render('- START -', True, BUTTON_MARGINAL_COLOR_0)

BUTTON_START_TEXT_SIZE = BUTTON_START_TEXT.get_size()
BUTTON_START_TEXT_POSITION =  (BUTTON_START_POS[0] + (BUTTON_SIZE[0] - BUTTON_START_TEXT_SIZE[0]) / 2,
             BUTTON_START_POS[1] + (BUTTON_SIZE[1] - BUTTON_START_TEXT_SIZE[1]) / 2)

BUTTON_EXIT_POS = ((SCREEN_SIZE.x - BUTTON_SIZE[0]) / 2, 750)
BUTTON_EXIT_TEXT = MENU_FONT.render('- EXIT -', True, BUTTON_MARGINAL_COLOR_0)

BUTTON_EXIT_TEXT_SIZE = BUTTON_EXIT_TEXT.get_size()
BUTTON_EXIT_TEXT_POSITION = (BUTTON_EXIT_POS[0] + (BUTTON_SIZE[0] - BUTTON_EXIT_TEXT_SIZE[0]) / 2,
             BUTTON_EXIT_POS[1] + (BUTTON_SIZE[1] - BUTTON_EXIT_TEXT_SIZE[1]) / 2)


SLIDER_FONT = pg.font.SysFont('Times New Roman', 40)
SLIDER_LENGTH = 600
SLIDER_WIDTH = 30
SLIDER_POS_X = (SCREEN_SIZE.x - SLIDER_LENGTH) / 2

SLIDER_MUSIC_TEXT = SLIDER_FONT.render('MUSIC VOLUME', True, BUTTON_MARGINAL_COLOR_0)

SLIDER_MUSIC_TEXT_SIZE = SLIDER_MUSIC_TEXT.get_size()
SLIDER_MUSIC_TEXT_POSITION = ((SCREEN_SIZE.x - SLIDER_MUSIC_TEXT_SIZE[0]) / 2, 400)

SLIDER_VFX_TEXT = SLIDER_FONT.render('VFX VOLUME', True, BUTTON_MARGINAL_COLOR_0)

SLIDER_VFX_TEXT_SIZE = SLIDER_VFX_TEXT.get_size()
SLIDER_VFX_TEXT_POSITION = ((SCREEN_SIZE.x - SLIDER_VFX_TEXT_SIZE[0]) / 2, 570)


# menu management class, controls and computes gui related to menu
class MENU:

    def __init__(self): 

        # music control variable
        self.music_played = False
            
        # button list
        self.buttons = [((BUTTON_EXIT_POS[0], BUTTON_EXIT_POS[1], BUTTON_SIZE[0],
                          BUTTON_SIZE[1]), BUTTON_EXIT_TEXT, BUTTON_EXIT_TEXT_POSITION),
                        ((BUTTON_START_POS[0], BUTTON_START_POS[1], BUTTON_SIZE[0],
                          BUTTON_SIZE[1]), BUTTON_START_TEXT, BUTTON_START_TEXT_POSITION)]

        # volume sliders
        self.slider_music = Slider(SCREEN, SLIDER_POS_X, 450, SLIDER_LENGTH, SLIDER_WIDTH, min=0, max=100, step=1)
        self.slider_vfx = Slider(SCREEN, SLIDER_POS_X, 620, SLIDER_LENGTH, SLIDER_WIDTH, min=0, max=100, step=1)

    # called every frame / display update
    def update(self):

        # play music only once, in loop
        if not self.music_played:
            play_sound(sound=sound_menu, channel=0, loops=-1)
            self.music_played = True

        # display background
        SCREEN.blit(MENU_BACKGROUND.image, MENU_BACKGROUND.location)

        # update sliders
        self.update_sliders()

        # update buttons
        if self.update_buttons():
            self.stop_music()
            # returns True to main.py, "game signal", if start button is pressed
            return True

    # func updates menu sliders, controls channel audio
    def update_sliders(self) -> None:

        # update sliders / get events
        events = pg.event.get()
        pygame_widgets.update(events)

        # set music channel
        pg.mixer.Channel(0).set_volume(0.01 * self.slider_music.getValue())

        # set vfx & other channels
        for i in range(5):
            pg.mixer.Channel(i+1).set_volume(0.01 * self.slider_vfx.getValue())

        # display explanation text
        SCREEN.blit(SLIDER_MUSIC_TEXT, SLIDER_MUSIC_TEXT_POSITION)
        SCREEN.blit(SLIDER_VFX_TEXT, SLIDER_VFX_TEXT_POSITION)

    # func updates menu buttons, controls game start / end
    def update_buttons(self) -> bool:

        # get mouse action
        mouse_presses = pg.mouse.get_pressed()
        mouse_pressed = mouse_presses[0]

        # look for player action on each button
        for button in self.buttons:

            # button / outline sizes for rectangle drawing and mouse press
            outline_rect = (l, t, w, h) = button[0]
            button_rect = (
            l + MARGINAL_SIZE, t + MARGINAL_SIZE, w - MARGINAL_SIZE * 2, h - MARGINAL_SIZE * 2)

            # colors for drawing
            color_outline = BUTTON_MARGINAL_COLOR_0
            color_button = BUTTON_COLOR_0

            # check if mouse is above button
            if pg.Rect(outline_rect).collidepoint(pg.mouse.get_pos()):

                # change color
                color_outline = BUTTON_MARGINAL_COLOR_1
                color_button = BUTTON_COLOR_1

                # commit to action if mouse pressed
                if mouse_pressed:
                    play_sound(sound=sound_click, channel=5)

                    # stop game program
                    if button == self.buttons[0]:
                        end_game()

                    # start game
                    elif button == self.buttons[1]:
                        return True
            else:
                pass

            # draw button outline
            pg.draw.rect(surface=SCREEN, color=color_outline, rect=pg.Rect(outline_rect))

            # draw button
            pg.draw.rect(surface=SCREEN, color=color_button, rect=pg.Rect(button_rect))

            # display button text
            SCREEN.blit(button[1], button[2])

    # function stops menu music, so game music can play uninterrupted
    def stop_music(self) -> None:
        self.music_played = False
        pg.mixer.Channel(0).stop()


# class used to fade in messages / screens at win or death
class SCREEN_FADE:
    def __init__(self, screen_time: int, fade_time: int, fade_color: tuple, screen_sound: pg.mixer.Sound,
                 msg: str, msg_font: pg.font, msg_color: tuple, msg_pos: Vector2,
                 msg_fade_time: int, msg_start_time: int):

        self.screen_time = screen_time
        self.screen_time_active = 0

        self.screen_opacity = 0
        self.screen_opacity_term = 7 / (fade_time * FPS)

        self.screen = pg.Surface(SCREEN_SIZE)
        self.screen.fill(color=fade_color)
        self.screen.set_alpha(self.screen_opacity)

        self.msg_font = msg_font
        self.msg = msg_font.render(msg, True, msg_color)
        self.msg_pos = msg_pos

        self.msg_opacity = 0
        self.msg_opacity_term = 7 / (msg_fade_time * FPS)
        self.msg_start_time = msg_start_time

        self.screen_sound = screen_sound
        self.screen_sound_played = False

    # called every frame / display update
    def update(self) -> bool:

        # make less see through
        self.screen_opacity += self.screen_opacity_term
        self.screen.set_alpha(self.screen_opacity)

        SCREEN.blit(self.screen, (0, 0))

        self.screen_time_active += 1 / FPS

        # start to fade in message at time
        if self.screen_time_active >= self.msg_start_time:
            self.msg.set_alpha(self.msg_opacity)

            SCREEN.blit(self.msg, self.msg_pos)

            self.msg_opacity += self.msg_opacity_term

        # play sound in music channel, clear music channel first
        if not self.screen_sound_played:
            pg.mixer.Channel(0).stop()
            play_sound(sound=self.screen_sound, channel=0)
            self.screen_sound_played = True

        # reset screen if done showing, return True to main to continue to menu
        if self.screen_time_active >= self.screen_time:
            self._reset()
            return True

    # resets variables for screen_fade object re-use + make invisible
    def _reset(self) -> None:

        self.screen_time_active = 0
        self.screen_sound_played = False

        self.screen_opacity = 0
        self.msg_opacity = 0
        self.screen.set_alpha(self.screen_opacity)


# death screen configuration
DEATH_SCREEN_TIME = 8
DEATH_SCREEN_FADE_TIME = 4
DEATH_SCREEN_COLOR = (0, 0, 0)

DEATH_MSG_TIME = 2
DEATH_MSG_COLOR = (255, 0, 0)
DEATH_MSG_POS = Vector2([650, 400])
DEATH_MSG_FADE_TIME = 3
DEATH_MSG_FONT = pg.font.SysFont('Times New Roman', 120)
DEATH_MSG = 'YOU DIED'


# death screen
class DEATH_SCREEN(SCREEN_FADE):
    def __init__(self):
        super().__init__(screen_time=DEATH_SCREEN_TIME,
                         fade_time=DEATH_MSG_FADE_TIME,
                         fade_color=DEATH_SCREEN_COLOR,
                         screen_sound=sound_death_screen,
                         msg=DEATH_MSG,
                         msg_font=DEATH_MSG_FONT,
                         msg_color=DEATH_MSG_COLOR,
                         msg_pos=DEATH_MSG_POS,
                         msg_fade_time=DEATH_MSG_FADE_TIME,
                         msg_start_time=DEATH_MSG_TIME)


# win screen configuration
WIN_SCREEN_TIME = 8
WIN_SCREEN_FADE_TIME = 4
WIN_SCREEN_COLOR = (255, 255, 255)

WIN_MSG_TIME = 2
WIN_MSG_COLOR = (255,239,0)
WIN_MSG_POS = Vector2([550, 400])
WIN_MSG_FADE_TIME = 3
WIN_MSG_FONT = pg.font.SysFont('Times New Roman', 120)
WIN_MSG = 'YOU WIN!!!'


# win screen
class WIN_SCREEN(SCREEN_FADE):
    def __init__(self):
        super().__init__(screen_time=WIN_SCREEN_TIME,
                         fade_time=WIN_MSG_FADE_TIME,
                         fade_color=WIN_SCREEN_COLOR,
                         screen_sound=sound_win_screen,
                         msg=WIN_MSG,
                         msg_font=WIN_MSG_FONT,
                         msg_color=WIN_MSG_COLOR,
                         msg_pos=WIN_MSG_POS,
                         msg_fade_time=WIN_MSG_FADE_TIME,
                         msg_start_time=WIN_MSG_TIME)
