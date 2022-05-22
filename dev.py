# ONLY USED FOR DEVELOPMENT, NOT THE ACTUAL GAME, IGNORE THIS FILE

import multiprocessing
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import pygame as pg

from game_lib import GROUP_ENEMY, GROUP_PLAYER, GROUP_ITEM, SCREEN

TIME_LIST_Y = []
TIME_LIST_X = []
TIME_LIST_LEN = 0
TIME_LIST_LEN_MAX = 500
FPS_LIST_X = []
FPS_LIST_Y = []

FPS_QUEUE = multiprocessing.Queue()
TIME_QUEUE = multiprocessing.Queue()


class DeveloperManager:

    def __init__(self):

        # start graphical data user interface
        self.graphs_prcs = multiprocessing.Process(target=self._graphs)
        self.graphs_prcs.start()
        self.previous_update = False
        self.current_update = time.time()

    def _graphs(self):

        # subplot configuration
        fig, axes = plt.subplots(2, 1)
        ax1 = axes[0]
        ax2 = axes[1]

        # conf
        ax1.legend()
        ax1.set_title(f"Current frames per second")
        ax1.set_xlabel('Time')
        ax1.set_ylabel('FPS')
        ax1.grid(True, linestyle='-.')

        ax2.legend()
        ax2.set_title(f"Time between game-loops")
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Time between updates')
        ax2.grid(True, linestyle='-.')

        def animate(i):

            # update data values
            x_time, y_time = TIME_QUEUE.get(block=-1)
            x_fps, y_fps = FPS_QUEUE.get(block=-1)

            # remove old data
            ax1.cla()
            ax2.cla()

            # plot new data
            ax1.plot(x_fps, y_fps, c='blue', label='Frames per Second')
            ax2.plot(x_time, y_time, c='red', label='Time between updates')

        ani = FuncAnimation(plt.gcf(), animate, interval=0.000001)
        plt.show()

    def _draw_boarders(self):

        # draw all hitboxes
        for sprite in GROUP_PLAYER:
            pg.draw.lines(SCREEN, (0, 255, 0), width=2, points=sprite.mask.outline(), closed=True)
            pg.draw.rect(SCREEN, (0, 255, 0), rect=sprite.rect, width=2)

        for sprite in GROUP_ENEMY:
            pg.draw.lines(SCREEN, (255, 0, 0), width=2, points=sprite.mask.outline(), closed=True)
            pg.draw.rect(SCREEN, (255, 0, 0), rect=sprite.rect, width=2)

        for sprite in GROUP_ITEM:
            pg.draw.lines(SCREEN, (0, 0, 255), width=2, points=sprite.mask.outline(), closed=True)
            pg.draw.rect(SCREEN, (0, 0, 255), rect=sprite.rect, width=2)

    def update(self, FPS):
        global TIME_LIST_LEN, TIME_LIST_Y, TIME_LIST_X, TIME_LIST_LEN_MAX, TIME_QUEUE, FPS_QUEUE, FPS_LIST_X, FPS_LIST_Y

        self._draw_boarders()

        # check for previous frame
        if not self.previous_update:
            self.previous_update = time.time()
        else:
            self.current_update = time.time()

            # resize queue and list to not get to big
            TIME_LIST_LEN += 1
            if TIME_LIST_LEN > TIME_LIST_LEN_MAX:
                TIME_LIST_Y.pop(0)
                TIME_LIST_X.pop(0)
                FPS_LIST_X.pop(0)
                FPS_LIST_Y.pop(0)

            TIME_LIST_X.append(time.time())
            TIME_LIST_Y.append(self.current_update - self.previous_update)
            TIME_QUEUE.put((TIME_LIST_X, TIME_LIST_Y))

            FPS_LIST_Y.append(int(FPS))
            FPS_LIST_X.append(time.time())
            FPS_QUEUE.put((FPS_LIST_X, FPS_LIST_Y))

            self.previous_update = self.current_update
