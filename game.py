import pygame
import sys
import os
import random

import dev_tools
from common_methods import *
from pygame.locals import *
import data
import ui
import math

# 常数
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ASSETS_DIR = 'Assets\\'

STATE_MAIN_MENU = 'main_menu'
STATE_MAIN_MENU_TO_GAME = 'main_menu_to_game'
STATE_GAME = 'game'
STATE_DAY_TO_NIGHT = 'day_to_night'
STATE_NIGHT_TO_DAY = 'night_to_day'
STATE_GAME_TO_GAMEOVER = 'game_to_gameover'
STATE_GAMEOVER = 'gameover'
STATE_TRANSFORMING = 'transforming'
STATE_BOSS = 'boss'
STATE_VICTORY = 'victory'

# 程序体状态
global game_state
game_state = STATE_MAIN_MENU

# 初始化
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
pygame.display.set_caption('game.py')

game_screen = pygame.display.set_mode((800, 600), 0)
game_clock = pygame.time.Clock()
game_data = data.Data()
game_dev_tools = dev_tools.DevTools(game_data, game_screen, game_clock)
game_ui = ui.UI(game_data, game_screen)

global offset
global press_keys
global mixer_volume, mixer_music_name
offset = [0, 0]
mixer_volume = 1.0
mixer_music_name = 'MainMenu.mp3'

# MainMenu控制变量
global background_x
global background_index
global background_width
global background_height
global background_filter

background_index = random.randint(1, 8)
background_x = 0.0
background_width, background_height= -1, -1
background_filter = 12

# 测试用
pygame.mixer.music.load('Assets\\Music\\mainmenu.mp3')
pygame.mixer.music.play(-1)
game_dev_tools.dev_tool("pi Axe", game_data)


CommonMethods.handle_effect('bct HellDoor', game_data)

def draw_ground():
    global offset
    game_screen.fill(BLACK)
    __row = -4
    __transform = -40
    while __row < 16:
        __col = -2
        while __col < 6:
            __y = int(__row - int(offset[1] // 80) * 2)
            __x = int(__col - int(offset[0] // 160))
            if 0 <= __x < game_data.environment.matrix_width and 0 <= __y < game_data.environment.matrix_height \
                    and game_data.environment.ground[__x][__y].name != 'Air':
                game_screen.blit(game_data.dictionary.image_dict['Ground\\' + game_data.environment.ground[__x][__y].img_path],
                            (__col * 160 + __transform + offset[0] % 160, __row * 40 + offset[1] % 80))
            __col += 1
        __row += 1
        __transform = -__transform


def draw_player():
    img = game_data.player.get_img()
    _width, _height = img.get_size()
    game_screen.blit(img, (game_data.PLAYER_SCREEN_OFFSET[0], game_data.PLAYER_SCREEN_OFFSET[1]))


def draw_unit(_unit):
    game_screen.blit(_unit.image,
                     (_unit.pos_pixel_x + _unit.offset[0] - game_data.player.pos_pixel_x + game_data.UNIT_SCREEN_OFFSET[0],
                      _unit.pos_pixel_y + _unit.offset[1] - game_data.player.pos_pixel_y + game_data.UNIT_SCREEN_OFFSET[1]))


def draw_block_player_units():
    global offset
    __row = -4
    __transform = -40
    __have_draw_player = False
    while __row < 18:
        __col = -2
        while __col < 6:
            __y = int(__row - int(offset[1] // 80) * 2)
            __x = int(__col - int(offset[0] // 160))
            if __y > game_data.player.pos_matrix_y and not __have_draw_player:
                __have_draw_player = True
                draw_player()
            if 0 <= __x < game_data.environment.matrix_width and 0 <= __y < game_data.environment.matrix_height \
                    and game_data.environment.block[__x][__y].have_img == 1:
                game_screen.blit(game_data.dictionary.image_dict['Block\\' + game_data.environment.block[__x][__y].img_path],
                                 (__col * 160 + __transform + offset[0] % 160 + game_data.environment.block[__x][__y].offset[0],
                                  __row * 40 + offset[1] % 80 + game_data.environment.block[__x][__y].offset[1]))
            __col += 1
        __row += 1
        __transform = -__transform
    for _unit in game_data.awake_units:
        draw_unit(_unit)

def draw_filter():
    global game_filter_name
    game_screen.blit(game_data.dictionary.image_dict['Filter\\'+game_filter_name+'.png'], (0, 0))


def check_collision():
    for _unit in game_data.awake_units:
        if _unit.can_collide and \
            math.fabs(_unit.pos_pixel_x - game_data.player.pos_pixel_x) < _unit.collision_half_width and \
                math.fabs(_unit.pos_pixel_y - game_data.player.pos_pixel_y) < _unit.collision_half_height:
            game_data.colliding_unit = _unit
            CommonMethods.handle_interact(_unit.method_str, game_data)

def do_main_menu():
    global background_x
    global background_width
    global background_index
    global background_filter
    global game_state
    if background_width + background_x < 800:
        if background_filter >= 12:
            background_index = (background_index + random.randint(0, 4)) % 8 + 1
            background_width, h = game_data.dictionary.image_dict['Menu\\MainMenu (%d).png' % background_index].get_size()
            background_x = 0.0
        else:
            background_filter += 0.5
    else:
        background_x -= 0.5
        if background_filter >= 0.5:
            background_filter -= 0.5
    game_screen.blit(game_data.dictionary.image_dict['Menu\\MainMenu (%d).png' % background_index], (int(background_x), 0))
    game_screen.blit(game_data.dictionary.image_dict['Menu\\NewGame.png'], (306, 400))
    game_screen.blit(game_data.dictionary.image_dict['Filter\\B%d.png' % int(background_filter)], (0, 0))
    for _event in pygame.event.get():
        if _event.type == pygame.MOUSEBUTTONDOWN:
            _mouse_down = _event.button  # 左键1 右键3 中间2
            _mouse_down_x, _mouse_down_y = _event.pos
            if _mouse_down == 1 and 306 < _mouse_down_x < 306 + 188 and 400 < _mouse_down_y < 400 + 80 :
                game_state = STATE_MAIN_MENU_TO_GAME
        elif _event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif _event.type == pygame.KEYDOWN:
            if _event.key == pygame.K_F12:
                dev_command = input("Developer Command:")
                game_dev_tools.dev_tool(dev_command, game_data)
            if _event.key == pygame.K_F11:
                game_dev_tools.dev_tool("ex show fps", game_data)
            if _event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

def do_main_menu_to_game():
    global background_x
    global background_width
    global background_index
    global background_filter
    global game_state
    global mixer_volume
    global mixer_music_name
    if background_filter >= 24:
        game_state = STATE_GAME
    elif background_filter >= 12:
        background_x = 0.0
        background_filter += 0.15
        if mixer_volume < 1:
            mixer_volume += 0.02
        if mixer_music_name!= 'main.mp3':
            mixer_music_name = 'main.mp3'
            pygame.mixer.music.load('Assets\\Music\\main.mp3')
            pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(mixer_volume)
        do_game()
        game_screen.blit(game_data.dictionary.image_dict['Filter\\B%d.png' % (24 - int(background_filter))], (0, 0))
    else:
        background_filter += 0.2
        if mixer_volume > 0:
            mixer_volume -= 0.02
        pygame.mixer.music.set_volume(mixer_volume)
        game_screen.blit(game_data.dictionary.image_dict['Menu\\MainMenu (%d).png' % background_index], (int(background_x), 0))
        game_screen.blit(game_data.dictionary.image_dict['Filter\\B%d.png' % int(background_filter)], (0, 0))

global game_filter_name, game_filter_index
game_filter_name = 'Day'
game_filter_index = 0.0

def do_game():
    global offset
    global press_keys
    global game_state
    global game_filter_name
    global game_filter_index
    # 更新玩家
    game_data.player.update(press_keys, game_data)

    # 更新data
    game_data.update()

    # 检测碰撞
    check_collision()

    # 绘制准备
    offset = [- game_data.player.pos_pixel_x + game_data.PLAYER_SCREEN_OFFSET[0] - 20,  # 获取玩家像素坐标和屏幕偏移量计算总偏移量
              - game_data.player.pos_pixel_y + game_data.PLAYER_SCREEN_OFFSET[1] + 25]

    # 绘制 ground
    draw_ground()

    # 绘制 block和player和unit
    draw_block_player_units()

    # 绘制Filter
    draw_filter()

    # 绘制 ui
    game_ui.update()

    # 绘制鼠标
    game_ui.draw_mouse()

    # 绘制开发者工具
    game_dev_tools.dev_update()

    # 事件捕获
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # 处理键盘事件
            game_ui.handle_keydown(event.key)
            if event.key == pygame.K_F12:
                dev_command = input("Developer Command:")
                game_dev_tools.dev_tool(dev_command, game_data)
            if event.key == pygame.K_F11:
                game_dev_tools.dev_tool("ex show fps", game_data)
            if event.key == pygame.K_F1:
                game_dev_tools.dev_tool("ex show player position", game_data)
            if event.key == pygame.K_F2:
                game_dev_tools.dev_tool("ex show mouse position", game_data)

        # 处理鼠标事件
        elif event.type == pygame.MOUSEBUTTONDOWN:
            game_ui.handle_mousedown(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            game_ui.handle_mouseup(event)

    # 处理状态跳转
    if game_state == STATE_GAME:
        if game_data.fighting_boss:
            game_state = STATE_BOSS
            game_filter_index = 0
            return
        if game_data.victory:
            game_state = STATE_VICTORY
            game_filter_index = 0
            return
        if game_data.player.hp <= 0:
            game_state = STATE_GAME_TO_GAMEOVER
            game_filter_index = 0
            return
        elif game_data.transforming:
            game_state = STATE_TRANSFORMING
            game_filter_index = 0
            return
        elif game_data.frames % 4000 == 1999:
            game_state = STATE_DAY_TO_NIGHT
            game_filter_index = 0
            return
        elif game_data.frames % 4000 == 3999:
            game_state = STATE_NIGHT_TO_DAY
            game_filter_index = 0
            return

def do_day_to_night():
    global game_filter_name
    global game_filter_index
    global game_state
    game_filter_index += 0.05
    game_filter_name = 'N' + str(int(game_filter_index))
    if game_filter_index >= 5:
        game_state = STATE_GAME
    do_game()

def do_night_to_day():
    global game_filter_name
    global game_filter_index
    global game_state

    game_filter_index += 0.05
    game_filter_name = 'N' + str(5 - int(game_filter_index))
    if game_filter_index >= 5:
        game_filter_name = 'Day'
        game_state = STATE_GAME
    do_game()

def do_transforming():
    global game_filter_name
    global game_filter_index
    global game_state
    global mixer_volume
    global mixer_music_name
    game_filter_index += 0.5
    if game_filter_index >= 24:
        game_filter_index += 0.1
        game_state = STATE_GAME
        game_filter_name = 'Day' if not game_data.night else 'N5'
        game_data.transforming = False
    elif game_filter_index > 12:
        if mixer_volume < 1:
            mixer_volume += 0.05
    elif 11.999 < game_filter_index < 12.001:
        game_data.environment = eval('game_data.' + game_data.next_environment)
        game_data.player.pos_pixel_x = game_data.player_next_pos_pixel_x
        game_data.player.pos_pixel_y = game_data.player_next_pos_pixel_y
        mixer_music_name = game_data.environment.name
        pygame.mixer.music.load('Assets\\Music\\%s.mp3' % game_data.environment.name)
        pygame.mixer.music.play(-1)
    else:
        if mixer_volume > 0:
            mixer_volume -= 0.05
    game_filter_name = 'B' + str(int(12 - math.fabs(12 - game_filter_index)))
    pygame.mixer.music.set_volume(mixer_volume)
    do_game()

def do_boss():
    global game_filter_name
    global game_filter_index
    global game_state
    global mixer_volume
    global mixer_music_name
    game_filter_index += 1
    if mixer_music_name != 'boss':
        mixer_music_name = 'boss'
        pygame.mixer.music.load('Assets\\Music\\%s.mp3' % mixer_music_name)
        pygame.mixer.music.play(-1)
    if game_filter_index > 80:
        game_filter_name = 'R1'
        game_data.fighting_boss = False
        game_state = STATE_GAME
    else:
        game_filter_name = 'B' + str(int(5 - math.fabs(5 - game_filter_index % 10)))
    pygame.mixer.music.set_volume(mixer_volume)
    do_game()

def do_game_to_gameover():
    global game_filter_name
    global game_filter_index
    global game_state
    global mixer_volume
    global mixer_music_name
    game_filter_index += 0.1
    mixer_volume -= 0.01
    pygame.mixer.music.set_volume(mixer_volume)
    game_filter_name = 'B' + str(int(game_filter_index))
    if game_filter_index < 10:
        # 绘制 ground
        draw_ground()
        # 绘制 block和player和unit
        draw_block_player_units()
        # 绘制Filter
        draw_filter()
    else:
        game_screen.blit(game_data.dictionary.image_dict['Menu\\GameOver.png'], (0, 0))
        game_screen.blit(game_data.dictionary.image_dict['Filter\\'+game_filter_name+'.png'], (0, 0))
        if game_filter_index >= 12:
            game_state = STATE_GAMEOVER
            pygame.mixer.music.stop()

global firework_list
firework_list= []
global frames
frames = 0

def do_victory():
    global game_filter_name
    global game_filter_index
    global game_state
    global mixer_volume
    global mixer_music_name
    global firework_list
    global frames
    game_filter_index += 0.2
    frames += 1
    if mixer_music_name != 'victory':
        mixer_music_name = 'victory'
        pygame.mixer.music.load('Assets\\Music\\%s.mp3' % mixer_music_name)
        pygame.mixer.music.play(-1)
    if game_filter_index > 20:
        game_screen.blit(game_data.dictionary.image_dict['Menu\\Victory.png'], (0, 0))
        if frames % 30 == 0:
            firework_list.append(unit.Unit('Firework', game_data.dictionary))
            firework_list[-1].pos_pixel_x = random.randint(0, 800)
            firework_list[-1].pos_pixel_y = random.randint(0, 600)
        for i in firework_list:
            game_screen.blit(i.image, (i.pos_pixel_x, i.pos_pixel_y))
            if frames % 2 == 0:
                i.image_index += 1
            if i.image_index >= i.have_img:
                firework_list.remove(i)
            else:
                i.image = i.images[i.image_index]
    elif 20 > game_filter_index > 10:
        game_screen.blit(game_data.dictionary.image_dict['Menu\\Victory.png'], (0, 0))
        game_filter_name = 'W' + str(20 - int(game_filter_index))
        draw_filter()
    elif game_filter_index < 10:
        do_game()
        game_filter_name = 'W' + str(int(game_filter_index))
    pygame.mixer.music.set_volume(mixer_volume)

    for _event in pygame.event.get():
        if _event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif _event.type == pygame.KEYDOWN:
            if _event.key == pygame.K_F12:
                dev_command = input("Developer Command:")
                game_dev_tools.dev_tool(dev_command, game_data)
            if _event.key == pygame.K_F11:
                game_dev_tools.dev_tool("ex show fps", game_data)
            if _event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

def do_gameover():
    game_screen.blit(game_data.dictionary.image_dict['Menu\\GameOver.png'], (0, 0))
    for _event in pygame.event.get():
        if _event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif _event.type == pygame.KEYDOWN:
            if _event.key == pygame.K_F12:
                dev_command = input("Developer Command:")
                game_dev_tools.dev_tool(dev_command, game_data)
            if _event.key == pygame.K_F11:
                game_dev_tools.dev_tool("ex show fps", game_data)
            if _event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


# 主循环
while True:
    # 设置帧数
    # game_clock.tick(default_settings.get_fps())
    game_clock.tick(30)
    press_keys = pygame.key.get_pressed()
    if press_keys[K_LALT] and press_keys[K_RETURN]:
        game_data.settings.set_full_screen(True)
        game_screen = pygame.display.set_mode((800, 600), FULLSCREEN)
    eval('do_' + game_state)()

    # 更新帧
    pygame.display.update()
