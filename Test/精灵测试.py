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
class s(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('地块.png').convert_alpha()
        self.rect = self.image.get_rect()

# 初始化
pygame.init()
g = pygame.sprite.Group()
g.add(s())
# 主循环
while True:
    # 背景图
    screen.fill(WHITE)
    g.draw(screen)

    # 代码更新区
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
