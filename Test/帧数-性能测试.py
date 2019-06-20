import pygame
from pygame.locals import *
import sys
import os
import string

import settings
import environment
import player
import dev_tools
from common_methods import *
from dictionary import *
import data
import ui


# 常数
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ASSETS_DIR = 'Assets\\'


# 初始化设置 settings
default_settings = settings.Settings(800, 600)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((default_settings.get_screen_width(), default_settings.get_screen_height()))
# screen = pygame.display.set_mode((1920, 1080), FULLSCREEN | DOUBLEBUF)
pygame.display.set_caption('game.py')
pygame.init()
my_font = pygame.font.SysFont('arial', 22)

# 主循环
while True:
    # 设置帧数
    # clock.tick(default_settings.get_fps())
    clock.tick(30)

    screen.fill((255, 255, 255))

    i = 0
    while i < 300000:
        i += 1

    # 30帧下 30万次为极限 20万次合适

    text_screen = my_font.render('FPS: ' + str(int(clock.get_fps())), False, (0, 0, 0))
    screen.blit(text_screen, (0, 550))

    # 事件捕获
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
                pygame.quit()
                sys.exit()

    # 更新帧
    pygame.display.flip()
