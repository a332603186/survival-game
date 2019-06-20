import pygame

import dev_tools
from common_methods import *
from pygame.locals import *
import data

class UI:
    # 初始化UI常数
    ITEM_OFFSET_X = 4
    ITEM_OFFSET_Y = 2
    ITEMS_UI_X = 100
    ITEMS_UI_Y = 550
    ITEMS_UI_BLANK = 55
    ITEMS_UI_PX = [(100, 550, 150, 600),
                   (155, 550, 205, 600),
                   (210, 550, 260, 600),
                   (265, 550, 315, 600),
                   (320, 550, 370, 600),
                   (375, 550, 425, 600),
                   (430, 550, 480, 600),
                   (485, 550, 535, 600),
                   (540, 550, 590, 600),
                   (595, 550, 645, 600),
                   (100, 495, 150, 545),
                   (155, 495, 205, 545),
                   (210, 495, 260, 545),
                   (265, 495, 315, 545),
                   (320, 495, 370, 545),
                   (375, 495, 425, 545),
                   (430, 495, 480, 545),
                   (485, 495, 535, 545),
                   (540, 495, 590, 545),
                   (595, 495, 645, 545),
                   (100, 440, 150, 490),
                   (155, 440, 205, 490),
                   (210, 440, 260, 490),
                   (265, 440, 315, 490),
                   (320, 440, 370, 490),
                   (375, 440, 425, 490),
                   (430, 440, 480, 490),
                   (485, 440, 535, 490),
                   (540, 440, 590, 490),
                   (595, 440, 645, 490) ]

    CRAFTING_UI_PX = [(210, 360, 260, 410),
                      (265, 360, 315, 410),
                      (320, 360, 370, 410),
                      (375, 360, 425, 410),
                      (485, 360, 535, 410), ]
    CRAFTING_UI_ARROW_PX = (438, 370)
    CRAFTING_UI_STATE_PX = (120, 380)

    BOX_UI_PX = [(630, 210, 680, 260),
                 (685, 210, 735, 260),
                 (740, 210, 790, 260),
                 (630, 265, 680, 315),
                 (685, 265, 735, 315),
                 (740, 265, 790, 315),
                 (630, 320, 680, 370),
                 (685, 320, 735, 370),
                 (740, 320, 790, 370)
                 ]

    HP_UI_X = 5
    HP_UI_Y = 5

    SP_UI_X = 770
    SP_UI_Y = 5

    TIME_UI_X = 720
    TIME_UI_Y = 5

    def __init__(self, game_data, game_screen):
        self.game_data = game_data
        self.game_screen = game_screen

        self.UI_FONT = pygame.font.SysFont('arial', 22)
        self.UI_FONT_SMALL = pygame.font.SysFont('arial', 12)
        self.UI_CHINESE_FONT = pygame.font.Font('Assets//UI//SIMYOU.TTF', 16)

        self.dragging = False
        self.dragging_event = 'null'
        self.dragging_item_name = 'Nothing'

        self.crafting = False
        self.crafting_items = ['Nothing', 'Nothing', 'Nothing', 'Nothing']
        self.crafting_result = 'Nothing'

    def update(self):
        self.draw_items_ui()
        self.draw_player_ui()
        self.draw_crafting_ui()
        self.draw_box_ui()

    def draw_items_ui(self):
        __num = 0
        __limit = 30 if self.game_data.show_ex_items_ui else 10


        # 绘制 物品栏边框
        while __num < __limit:
            if __num != self.game_data.player.item_in_hand_index:
                self.game_screen.blit(self.game_data.dictionary.image_dict['UI\\Edge.png'], (self.ITEMS_UI_PX[__num][0], self.ITEMS_UI_PX[__num][1]))
            else:
                self.game_screen.blit(self.game_data.dictionary.image_dict['UI\\White Edge.png'], (self.ITEMS_UI_PX[__num][0], self.ITEMS_UI_PX[__num][1]))
            __num += 1
        __num = 0

        # 绘制 物品图片及个数
        for __item in self.game_data.player.item_list:
            __item_text = self.UI_FONT_SMALL.render(str(self.game_data.player.item_count_dict[__item]), True, (0, 0, 0))
            self.game_screen.blit(__item_text, (self.ITEMS_UI_PX[__num][0] + self.ITEM_OFFSET_X, self.ITEMS_UI_PX[__num][1] + self.ITEM_OFFSET_Y))
            self.game_screen.blit(self.game_data.dictionary.image_dict['Item\\' + __item + '.png'], (self.ITEMS_UI_PX[__num][0] + 5, self.ITEMS_UI_PX[__num][1] + 5))
            __num += 1
            if __num >= __limit:
                break

    def draw_player_ui(self):
        __x = self.HP_UI_X
        __y = self.HP_UI_Y
        _limit = int((self.game_data.player.hp + 19) / 20)
        for i in range(0, _limit):
            self.game_screen.blit(self.game_data.dictionary.image_dict['UI\\HP.png'], (__x + i * 30,__y))
        __x = self.SP_UI_X
        __y = self.SP_UI_Y
        _limit = int((self.game_data.player.sp + 19) / 20)
        for i in range(0, _limit):
            self.game_screen.blit(self.game_data.dictionary.image_dict['UI\\SP.png'], (__x - i * 30, __y))

    def draw_world_ui(self):
        __x = self.TIME_UI_X
        __y = self.TIME_UI_Y
        __text_screen = self.UI_FONT.render((str(self.game_data.frame_time_hour).zfill(2)
                                        + ':' + str(self.game_data.frame_time_min).zfill(2)
                                        + ':' + str(self.game_data.frame_time_sec).zfill(2)), True, (0, 0, 0))
        self.game_screen.blit(__text_screen, (__x, __y))

    def draw_mouse(self):
        if self.dragging:
            if self.dragging_event == 'drag from item ui':
                x, y = pygame.mouse.get_pos()
                self.game_screen.blit(self.game_data.dictionary.image_dict['Item\\' + self.dragging_item_name + '.png'], (x - 10, y - 10))

    def draw_crafting_ui(self):
        if not self.crafting:
            return

        self.crafting_result = CommonMethods.craft_items(_crafting_items=self.crafting_items, _data=self.game_data)

        # 绘制 合成状态文字
        if self.game_data.environment.block[self.game_data.player.pos_matrix_x][self.game_data.player.pos_matrix_y].name == 'BuildingCraftingTable':
            _text_screen = self.UI_CHINESE_FONT.render('工作台制造:', True, (0, 0, 0))
        elif self.game_data.environment.block[self.game_data.player.pos_matrix_x][self.game_data.player.pos_matrix_y].name == 'BuildingPot':
            _text_screen = self.UI_CHINESE_FONT.render('烹饪:', True, (0, 0, 0))
        elif self.game_data.environment.block[self.game_data.player.pos_matrix_x][self.game_data.player.pos_matrix_y].name == 'BuildingForgingTable':
            _text_screen = self.UI_CHINESE_FONT.render('锻造:', True, (0, 0, 0))
        elif self.game_data.environment.block[self.game_data.player.pos_matrix_x][self.game_data.player.pos_matrix_y].name == 'BuildingAlchemyFurnace':
            _text_screen = self.UI_CHINESE_FONT.render('炼金:', True, (0, 0, 0))
        else:
            _text_screen = self.UI_CHINESE_FONT.render('手工制造:', True, (0, 0, 0))
        self.game_screen.blit(_text_screen, self.CRAFTING_UI_STATE_PX)

        # 绘制 物品栏边框
        for i in range(0, 5):
            self.game_screen.blit(self.game_data.dictionary.image_dict['UI\\Edge.png'],
                        (self.CRAFTING_UI_PX[i][0], self.CRAFTING_UI_PX[i][1]))

        # 绘制 箭头
        self.game_screen.blit(self.game_data.dictionary.image_dict['UI\\Arrow.png'],
                    (self.CRAFTING_UI_ARROW_PX[0], self.CRAFTING_UI_ARROW_PX[1]))

        # 绘制 合成素材图片
        for i in range(0, 4):
            if self.game_data.dictionary.item_dict[self.crafting_items[i]][1] == 1:
                self.game_screen.blit(self.game_data.dictionary.image_dict['Item\\' + self.crafting_items[i] + '.png'],
                            (self.CRAFTING_UI_PX[i][0] + self.ITEM_OFFSET_X, self.CRAFTING_UI_PX[i][1] + self.ITEM_OFFSET_Y))

        # 绘制 合成结果图片
        if self.crafting_result != 'Nothing':
            self.game_screen.blit(self.game_data.dictionary.image_dict['Item\\' + self.crafting_result + '.png'],
                             (self.CRAFTING_UI_PX[4][0] + self.ITEM_OFFSET_X,
                              self.CRAFTING_UI_PX[4][1] + self.ITEM_OFFSET_Y))

    def draw_box_ui(self):
        if self.game_data.show_box_ui:
            _box_mx = self.game_data.player.pos_matrix_x
            _box_my = self.game_data.player.pos_matrix_y
            _key = str(_box_mx) + ',' + str(_box_my)
            for _x in range(0, 9):
                self.game_screen.blit(self.game_data.dictionary.image_dict['UI\\Edge.png'], (self.BOX_UI_PX[_x][0], self.BOX_UI_PX[_x][1]))

            if _key in self.game_data.box_items:
                for _x in range(0, len(self.game_data.box_items[_key])):
                    _item_text = self.UI_FONT_SMALL.render(str(self.game_data.box_items_count[_key][_x]), True,(0, 0, 0))
                    _item_name = self.game_data.box_items[_key][_x]
                    self.game_screen.blit(_item_text, (self.BOX_UI_PX[_x][0] + 5, self.BOX_UI_PX[_x][1] + 5))
                    self.game_screen.blit(self.game_data.dictionary.image_dict['Item\\' + _item_name + '.png'],(self.BOX_UI_PX[_x][0] + 5, self.BOX_UI_PX[_x][1] + 5))


    def handle_keydown(self, _key):

        # key 1-0 切换item_in_hand_index
        if _key == K_1:
            self.game_data.player.change_item_in_hand(0)
        if _key == K_2:
            self.game_data.player.change_item_in_hand(1)
        if _key == K_3:
            self.game_data.player.change_item_in_hand(2)
        if _key == K_4:
            self.game_data.player.change_item_in_hand(3)
        if _key == K_5:
            self.game_data.player.change_item_in_hand(4)
        if _key == K_6:
            self.game_data.player.change_item_in_hand(5)
        if _key == K_7:
            self.game_data.player.change_item_in_hand(6)
        if _key == K_8:
            self.game_data.player.change_item_in_hand(7)
        if _key == K_9:
            self.game_data.player.change_item_in_hand(8)
        if _key == K_0:
            self.game_data.player.change_item_in_hand(9)

        # key F 使用item_in_hand
        if _key == K_f:
            if self.game_data.dictionary.item_dict[self.game_data.player.item_in_hand][2] == 1:
                CommonMethods.use_item(_data=self.game_data)
                self.game_data.player.update_item_list()

        # key SPACE 与Block交互
        if _key == K_SPACE:
            if self.game_data.environment.block[self.game_data.player.pos_matrix_x][self.game_data.player.pos_matrix_y].can_interact == 1:
                CommonMethods.handle_interact(_interact_str=self.game_data.environment.block[self.game_data.player.pos_matrix_x][self.game_data.player.pos_matrix_y].method_str,
                    _data=self.game_data)

        # key E 开启/关闭 创造UI
        if _key == K_e:
            if self.crafting:
                for i in range(0, 4):
                    if self.crafting_items[i] != 'Nothing':
                        self.game_data.player.add_item(self.crafting_items[i])
                        self.crafting_items[i] = 'Nothing'
            self.crafting = ~self.crafting
            self.game_data.show_ex_items_ui = ~self.game_data.show_ex_items_ui

        # key W A S D 关闭BOX UI
        if _key == K_w or _key == K_a or _key == K_s or _key == K_d:
            self.game_data.show_box_ui = False

    def handle_mousedown(self, _event):
        _mouse_down = _event.button  # 左键1 右键3 中间2
        _mouse_down_x, _mouse_down_y = _event.pos
        _limit = 30 if self.game_data.show_ex_items_ui else 10
        if _mouse_down == 1:
            self.dragging = True

        # items ui 点击判断 左键选定 右键使用
        for _index in range(0, _limit):
            if self.ITEMS_UI_PX[_index][0] < _mouse_down_x < self.ITEMS_UI_PX[_index][2] and \
                    self.ITEMS_UI_PX[_index][1] < _mouse_down_y < self.ITEMS_UI_PX[_index][3]:
                if _mouse_down == 1:
                    self.game_data.player.change_item_in_hand(_index)
                    if _index < len(self.game_data.player.item_list):
                        self.dragging_event = 'drag from item ui'
                        self.dragging_item_name = self.game_data.player.item_in_hand
                        self.game_data.player.sub_item(self.dragging_item_name)
                elif _mouse_down == 3:
                    CommonMethods.use_item(_data=self.game_data, _item_index=_index)
                    self.game_data.player.update_item_list()

        # 处理从crafting ui开始的拖动操作
        for i in range(0, 4):
            if self.CRAFTING_UI_PX[i][0] < _mouse_down_x < self.CRAFTING_UI_PX[i][2] and \
                    self.CRAFTING_UI_PX[i][1] < _mouse_down_y < self.CRAFTING_UI_PX[i][3]:
                if _mouse_down == 1:
                    if self.crafting_items[i] != 'Nothing':
                        self.dragging_event = 'drag from item ui'
                        self.dragging_item_name = self.crafting_items[i]
                        self.crafting_items[i] = 'Nothing'
        if self.CRAFTING_UI_PX[4][0] < _mouse_down_x < self.CRAFTING_UI_PX[4][2] and \
                self.CRAFTING_UI_PX[4][1] < _mouse_down_y < self.CRAFTING_UI_PX[4][3]:
            if _mouse_down == 1:
                if self.crafting_result != 'Nothing':
                    self.dragging_event = 'drag from item ui'
                    self.dragging_item_name = self.crafting_result
                    self.crafting_result = 'Nothing'
                    for i in range(0, 4):
                        self.crafting_items[i] = 'Nothing'

        # 处理从crafting ui开始的拖动操作
        if self.game_data.show_box_ui:
            _box_mx = self.game_data.player.pos_matrix_x
            _box_my = self.game_data.player.pos_matrix_y
            _key = str(_box_mx) + ',' + str(_box_my)
            if _key in self.game_data.box_items:
                for i in range(0, len(self.game_data.box_items[_key])):
                    if self.BOX_UI_PX[i][0] < _mouse_down_x < self.BOX_UI_PX[i][2] and \
                        self.BOX_UI_PX[i][1] < _mouse_down_y < self.BOX_UI_PX[i][3]:
                        if _mouse_down == 1:
                            self.dragging_event = 'drag from item ui'
                            self.dragging_item_name = self.game_data.box_items[_key][i]
                            self.game_data.box_items_count[_key][i] -= 1
                            if self.game_data.box_items_count[_key][i] <= 0:
                                del self.game_data.box_items_count[_key][i]
                                del self.game_data.box_items[_key][i]

    def handle_mouseup(self, _event):
        _mouse_up = _event.button  # 左键1 右键3 中间2
        _mouse_up_x, _mouse_up_y = _event.pos
        if _mouse_up != 1:
            return
        self.dragging = False
        if self.dragging_event == 'drag from item ui':
            self.dragging_event = 'null'

            # 处理落在items ui的部分
            if self.game_data.show_ex_items_ui:
                if 100 < _mouse_up_x < 645 and 440 < _mouse_up_y < 600:
                    self.game_data.player.add_item(self.dragging_item_name)
            else:
                if 100 < _mouse_up_x < 645 and 550 < _mouse_up_y < 600:
                    self.game_data.player.add_item(self.dragging_item_name)

            # 处理落在crafting ui的部分
            for i in range(0, 4):
                if self.CRAFTING_UI_PX[i][0] < _mouse_up_x < self.CRAFTING_UI_PX[i][2] and \
                        self.CRAFTING_UI_PX[i][1] < _mouse_up_y < self.CRAFTING_UI_PX[i][3]:
                    if self.crafting_items[i] == 'Nothing':
                        self.crafting_items[i] = self.dragging_item_name
                    elif self.crafting_items[i] != self.dragging_item_name:
                        self.game_data.player.add_item(self.crafting_items[i])
                        self.crafting_items[i] = self.dragging_item_name
                    elif self.crafting_items[i] == self.dragging_item_name:
                        self.game_data.player.add_item(self.crafting_items[i])
                    self.game_data.player.update_item_list()

            # 处理落在box ui的部分
            if 630 < _mouse_up_x < 790 and 210 < _mouse_up_y < 370 and self.game_data.show_box_ui:
                _box_mx = self.game_data.player.pos_matrix_x
                _box_my = self.game_data.player.pos_matrix_y
                _key = str(_box_mx) + ',' + str(_box_my)
                if _key in self.game_data.box_items:
                    if self.dragging_item_name in self.game_data.box_items[_key]:
                        self.game_data.box_items_count[_key][self.game_data.box_items[_key].index(self.dragging_item_name)] += 1
                    else:
                        if len(self.game_data.box_items[_key]) < 9:
                            self.game_data.box_items[_key].append(self.dragging_item_name)
                            self.game_data.box_items_count[_key].append(1)
                        else:
                            self.game_data.player.add_item(self.dragging_item_name)
                else:
                    self.game_data.box_items[_key] = [self.dragging_item_name]
                    self.game_data.box_items_count[_key] = [1]

            # 其他落点即为丢弃
            self.game_data.player.update_item_list()





