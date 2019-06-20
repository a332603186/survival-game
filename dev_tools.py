import pygame
import common_methods

'''
开发人员指令:游戏中按F12启动             0123456789ABCDEFGHIJKLM
更改game_environment.ground[x][y]为zzz:  "cg xxx,yyy zzz"
更改game_environment.block[x][y]为zzz:   "cb xxx,yyy zzz"
绘制地图像素坐标:                        "ex show pixel coordinate"
绘制玩家坐标(F1):                        "ex show player position"
绘制鼠标坐标(F2):                        "ex show mouse position"
绘制fps(F11):                            "ex show fps"
执行特效指令xxx                          "de xxx"
给玩家添加xxx物品                        "pi xxx"
'''


class DevTools:
    def __init__(self, data, screen, clock):
        self.__enable = False
        self.screen = screen
        self.clock = clock
        self.data = data
        self.DEV_FONT = pygame.font.SysFont('arial', 22)

        self.__show_player_pos = False
        self.__show_mouse_pos = False
        self.__show_fps = False

    def dev_tool(self, command_string, data):
        self.__enable = True
        if command_string[0:2] == 'cg':
            x = int(command_string[3:6])
            y = int(command_string[7:10])
            aim = command_string[11:]
            data.environment.ground[x][y] = data.environment.Ground(aim)
        elif command_string[0:2] == 'cb':
            x = int(command_string[3:6])
            y = int(command_string[7:10])
            aim = command_string[11:]
            data.environment.block[x][y] = data.environment.Block(aim, data.environment.game_dictionary.block_dict)
        elif command_string[0:2] == 'ex':
            if command_string[3:] == 'show player position':
                self.__show_player_pos = True
            if command_string[3:] == 'show mouse position':
                self.__show_mouse_pos = True
            if command_string[3:] == 'show fps':
                self.__show_fps = True
        elif command_string[0:2] == 'de':
            data.environment.block[data.player.pos_matrix_x][data.player.pos_matrix_y].interact_method_str = command_string[3:]
            common_methods.CommonMethods.handle_interact(command_string[3:], data)
        elif command_string[0:2] == 'pi':
            data.player.add_item(command_string[3:])

    def dev_update(self,):
        if self.__enable:
            if self.__show_fps:
                text_screen = self.DEV_FONT.render('FPS: ' + str(int(self.clock.get_fps())), False, (0, 0, 0))
                self.screen.blit(text_screen, (0, 550))
            if self.__show_player_pos:
                text_screen = self.DEV_FONT.render('player_pixel_x: ' + str(self.data.player.pos_pixel_x), False, (0, 0, 0))
                self.screen.blit(text_screen, (0, 450))
                text_screen = self.DEV_FONT.render('player_pixel_y: ' + str(self.data.player.pos_pixel_y), False, (0, 0, 0))
                self.screen.blit(text_screen, (0, 475))
                text_screen = self.DEV_FONT.render('player_matrix_x: ' + str(self.data.player.pos_matrix_x), False, (0, 0, 0))
                self.screen.blit(text_screen, (0, 500))
                text_screen = self.DEV_FONT.render('player_matrix_y: ' + str(self.data.player.pos_matrix_y), False, (0, 0, 0))
                self.screen.blit(text_screen, (0, 525))
                text_screen = self.DEV_FONT.render('player_face_to_x: ' + str(self.data.player.next_pos_pixel_x), False, (0, 0, 0))
                self.screen.blit(text_screen, (0, 550))
                text_screen = self.DEV_FONT.render('player_face_to_y: ' + str(self.data.player.next_pos_pixel_y), False, (0, 0, 0))
                self.screen.blit(text_screen, (0, 575))
            if self.__show_mouse_pos:
                _x, _y = pygame.mouse.get_pos()
                _m_x, _m_y = common_methods.CommonMethods.pos_pixel_to_pos_matrix(_x, _y)
                text_screen = self.DEV_FONT.render('mouse_pixel_x: ' + str(_x), False, (0, 0, 0))
                self.screen.blit(text_screen, (620, 450))
                text_screen = self.DEV_FONT.render('mouse_pixel_y: ' + str(_y), False, (0, 0, 0))
                self.screen.blit(text_screen, (620, 475))
                text_screen = self.DEV_FONT.render('mouse_matrix_x: ' + str(_m_x), False, (0, 0, 0))
                self.screen.blit(text_screen, (620, 500))
                text_screen = self.DEV_FONT.render('mouse_matrix_y: ' + str(_m_y), False, (0, 0, 0))
                self.screen.blit(text_screen, (620, 525))
