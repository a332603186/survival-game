import pygame
from pygame.locals import *
import sys
import os
import math


# 设置窗口的大小，单位为像素
screen = pygame.display.set_mode((800, 600))

# 设置窗口标题
pygame.display.set_caption('My Python Game')

# 定义常数
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 图加载
background_img = pygame.image.load('地块.png')

# 初始化
pygame.init()

# 主循环
while True:
    # 背景图
    screen.fill(WHITE)
    i = -80
    j = -80
    transform = 40
    while i < 1000:
        j = -80
        while j < 1000:
            screen.blit(background_img, (j + transform, i))
            j += 160
        i += 40
        transform = -transform

    # 代码更新区
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
