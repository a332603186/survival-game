import pygame
from pygame.locals import *
from common_methods import *
import math

class Player:
    def __init__(self):
        self.player_name = 'user'
        self.stay_img = [[0 for _ in range(0, 8)] for _ in range(0, 8)]
        self.run_img = [[0 for _ in range(0, 8)] for _ in range(0, 8)]
        self.stay_img_index = 0
        self.run_img_index = 0
        for i in range(0, 8):
            for j in range(1, 9):
                self.stay_img[i][j - 1] = pygame.image.load('Assets\\Player\\PlayerStay'+ str(i) + ' (' + str(j) + ').png').convert_alpha()
                self.run_img[i][j - 1] = pygame.image.load('Assets\\Player\\PlayerRun' + str(i) + ' (' + str(j) + ').png').convert_alpha()
        self.pos_pixel_x = 0
        self.pos_pixel_y = 0
        self.pos_matrix_x = 0
        self.pos_matrix_y = 0
        self.next_pos_pixel_x = 0
        self.next_pos_pixel_y = 0
        self.next_pos_matrix_x = 0
        self.next_pos_matrix_y = 0
        self.pixel_speed = 50
        self.movement = [0, 0]
        self.WALK_SPEED = 10
        self.RUN_SPEED = 50
        self.state = 'S'

        self.item_list = []
        self.item_count_dict = dict()
        self.item_in_hand = 'Nothing'
        self.item_in_hand_index = -1

        self.hp = 100
        self.sp = 100

        self.FACE_TO = [(1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1)]
        self.face_to_index = 0


    def update(self, press_keys, _data):
        # key W A S D 控制移动 lshift跑步
        self.movement = [0, 0]
        self.state = 'S'
        if press_keys[K_a]:
            self.movement[0] -= 2
            self.state = 'W'
        if press_keys[K_d]:
            self.movement[0] += 2
            self.state = 'W'
        if press_keys[K_w]:
            self.movement[1] -= 1
            self.state = 'W'
        if press_keys[K_s]:
            self.movement[1] += 1
            self.state = 'W'
        if press_keys[K_LSHIFT]:
            self.pixel_speed = self.RUN_SPEED
            self.state = 'R'
        else:
            self.pixel_speed = self.WALK_SPEED

        if self.movement != [0, 0]:

            side_length = math.hypot(self.movement[0], self.movement[1])
            self.next_pos_pixel_x = self.pos_pixel_x + int(self.movement[0] * self.pixel_speed / side_length)
            self.next_pos_pixel_y = self.pos_pixel_y + int(self.movement[1] * self.pixel_speed / side_length)
            self.next_pos_matrix_x, self.next_pos_matrix_y = \
                CommonMethods.pos_pixel_to_pos_matrix(self.next_pos_pixel_x, self.next_pos_pixel_y)
            can_move = True
            if _data.environment.block[self.next_pos_matrix_x][self.next_pos_matrix_y].solid != 0:
                can_move = False
            for _unit in _data.awake_units:
                if _unit.solid and \
                 math.fabs(_unit.pos_pixel_x - self.next_pos_pixel_x) < _unit.collision_half_width - 9 and \
                        math.fabs(_unit.pos_pixel_y - self.next_pos_pixel_y) < _unit.collision_half_height - 9:
                    can_move = False
            if can_move:
                self.pos_pixel_x = self.next_pos_pixel_x
                self.pos_pixel_y = self.next_pos_pixel_y

        # 更新player矩阵位置
        self.pos_matrix_x, self.pos_matrix_y = \
            CommonMethods.pos_pixel_to_pos_matrix(self.pos_pixel_x, self.pos_pixel_y)

        # 更新面向
        if self.movement[0] > 0:
            if self.movement[1] > 0:
                self.face_to_index = 2
            elif self.movement[1] == 0:
                self.face_to_index = 1
            elif self.movement[1] < 0:
                self.face_to_index = 0
        elif self.movement[0] == 0:
            if self.movement[1] > 0:
                self.face_to_index = 3
            elif self.movement[1] < 0:
                self.face_to_index = 7
        elif self.movement[0] < 0:
            if self.movement[1] > 0:
                self.face_to_index = 4
            elif self.movement[1] == 0:
                self.face_to_index = 5
            elif self.movement[1] < 0:
                self.face_to_index = 6

    def change_item_in_hand(self, _index):
        self.item_in_hand_index = _index
        if _index < len(self.item_list):
            self.item_in_hand = self.item_list[_index]
        else:
            self.item_in_hand = 'Nothing'
            
    def add_item(self, _item_name):
        if _item_name in self.item_count_dict:
            self.item_count_dict[_item_name] += 1
        else:
            self.item_list.append(_item_name)
            self.item_count_dict[_item_name] = 1

    def sub_item(self, _item_name):
        if _item_name in self.item_count_dict:
            self.item_count_dict[_item_name] -= 1
        else:
            print("Error:player doesn't have item:" + _item_name)

    def update_item_list(self):
        for _item_name in self.item_list:
            if self.item_count_dict[_item_name] <= 0:
                del self.item_count_dict[_item_name]
                self.item_list.remove(_item_name)
                if self.item_in_hand == _item_name:
                    self.item_in_hand = 'Nothing'
                    self.item_in_hand_index = -1

    def get_img(self):
        if self.movement == [0, 0]:
            return self.stay_img[self.face_to_index][self.stay_img_index]
        else:
            return self.run_img[self.face_to_index][self.run_img_index]

    def add_hp(self, value):
        self.hp += value
        if self.hp > 100:
            self.hp = 100

    def add_sp(self, value):
        self.sp += value
        if self.sp > 100:
            self.sp = 100

    def sub_hp(self, value):
        self.hp -= value
        if self.hp < 0:
            self.hp = 0

    def sub_sp(self, value):
        self.sp -= value
        if self.sp < 0:
            self.sp = 0
            self.sub_hp(10)



