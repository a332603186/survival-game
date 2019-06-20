from dictionary import *
from unit import *
import random
import math

class Environment:
    def __init__(self, name, matrix_width, matrix_height, _dictionary):
        # 常数
        self.ODD_ROW_EIGHT_GRID = [(1, 0), (-1, 0), (1, -1), (0, 1), (1, 1), (0, -1), (0, -2), (0, 2)]
        self.EVEN_ROW_EIGHT_GRID = [(1, 0), (-1, 0), (-1, 1), (0, 1), (-1, -1), (0, -1), (0, -2), (0, 2)]
        self.SURROUND_GROUND = ''
        self.MAIN_GROUND = ''
        self.GROUND_NAME_LIST = []
        self.BLOCK_NAME_LIST = []
        self.BLOCK_CHANCE_LIST = []

        self.name = name
        self.matrix_width = matrix_width
        self.matrix_height = matrix_height
        self.game_dictionary = _dictionary

        # 按长宽初始化 ground block二维数组
        self.ground = [[Ground('Air 1') for _ in range(matrix_height)] for _ in range(matrix_width)]
        self.block = \
            [[Block('Air', self.game_dictionary.block_dict) for _ in range(matrix_height)]
             for _ in range(matrix_width)]

        # 初始化Unit列表
        self.units = []

        print("Environment initialize completed")

    def randomize_array(self, width, height, update_time):
        _array = [[0 for _ in range(height)] for _ in range(width)]
        tmp = min(width, height) * 10
        for col in range(0, width):
            for row in range(0, height):
                min_distance = min(col * 2, row, (width - col - 1) * 2, height - row - 1)
                probability = max((100 - min_distance * tmp, 50))
                if random.randint(1, 100) < probability:
                    _array[col][row] = 1
        for time in range(0, update_time):
            for col in range(2, width - 2):
                for row in range(2, height - 2):
                    _count = 0
                    for i, j in self.EVEN_ROW_EIGHT_GRID if row % 2 == 0 else self.ODD_ROW_EIGHT_GRID:
                        if _array[i + col][j + row] == 1:
                            _count += 1
                    if _count > 4:
                        _array[col][row] = 1
                    else:
                        _array[col][row] = 0
        return _array

    def randomize_ground(self):
        # Step 1 随机大海
        for col in range(0, self.matrix_width):
            for row in range(0, self.matrix_height):
                min_distance = min(col * 2, row, (self.matrix_width - col - 1) * 2, self.matrix_height - row - 1)
                probability = max((100 - min_distance * 2, 50))
                if random.randint(1, 100) < probability:
                    self.ground[col][row] = Ground(self.SURROUND_GROUND + " " + str(random.randint(1, 4)))
        for time in range(0, 3):
            for col in range(2, self.matrix_width - 2):
                for row in range(2, self.matrix_height - 2):
                    _count = 0
                    for i, j in self.EVEN_ROW_EIGHT_GRID if row % 2 == 0 else self.ODD_ROW_EIGHT_GRID:
                        if self.ground[i + col][j + row].name[0:-2] == self.SURROUND_GROUND:
                            _count += 1
                    if _count > 4:
                        self.ground[col][row] = Ground(self.SURROUND_GROUND + ' ' + str(random.randint(1, 4)))
                    else:
                        self.ground[col][row] = Ground(self.MAIN_GROUND + ' ' + str(random.randint(1, 4)))

        # Step 2 随机添加各种地形
        for time in range(0, 40):  # 随机添加的地形数量
            _x1 = random.randint(0, self.matrix_width - 21)  # 随机地形左上角x值
            _y1 = random.randint(0, self.matrix_height - 21)  # 随机地形左上角y值
            _width = min(random.randint(8, 30), self.matrix_width - _x1 - 1)  # 随机地形宽度
            _height = min(random.randint(24, 90), self.matrix_height - _y1 - 1)  # 随机地形高度
            _array = self.randomize_array(_width, _height, 3)
            _ground_name = self.GROUND_NAME_LIST[random.randint(0, len(self.GROUND_NAME_LIST) - 1)]  # 随机的地形种类
            for col in range(0, _width):
                for row in range(0, _height):
                    if _array[col][row] == 0 and self.ground[col + _x1][row + _y1].name[0:-2] == self.MAIN_GROUND:
                        self.ground[col + _x1][row + _y1] = Ground(_ground_name + ' ' + str(random.randint(1, 4)))

    def randomize_hell_ground(self):
        # Step 1 随机大海
        for col in range(0, self.matrix_width):
            for row in range(0, self.matrix_height):
                min_distance = min(col * 2, row, (self.matrix_width - col - 1) * 2, self.matrix_height - row - 1)
                if min_distance < 5:
                    probability = 100
                else:
                    probability = 0
                if random.randint(1, 100) < probability:
                    self.ground[col][row] = Ground(self.SURROUND_GROUND + " " + str(random.randint(1, 4)))
        for time in range(0, 1):
            for col in range(2, self.matrix_width - 2):
                for row in range(2, self.matrix_height - 2):
                    _count = 0
                    for i, j in self.EVEN_ROW_EIGHT_GRID if row % 2 == 0 else self.ODD_ROW_EIGHT_GRID:
                        if self.ground[i + col][j + row].name[0:-2] == self.SURROUND_GROUND:
                            _count += 1
                    if _count > 4:
                        self.ground[col][row] = Ground(self.SURROUND_GROUND + ' ' + str(random.randint(1, 4)))
                    else:
                        self.ground[col][row] = Ground(self.MAIN_GROUND + ' ' + str(random.randint(1, 4)))

        # Step 2 随机添加各种地形
        for time in range(0, 40):  # 随机添加的地形数量
            _x1 = random.randint(0, self.matrix_width - 21)  # 随机地形左上角x值
            _y1 = random.randint(0, self.matrix_height - 21)  # 随机地形左上角y值
            _width = min(random.randint(8, 30), self.matrix_width - _x1 - 1)  # 随机地形宽度
            _height = min(random.randint(24, 90), self.matrix_height - _y1 - 1)  # 随机地形高度
            _array = self.randomize_array(_width, _height, 3)
            _ground_name = self.GROUND_NAME_LIST[random.randint(0, len(self.GROUND_NAME_LIST) - 1)]  # 随机的地形种类
            for col in range(0, _width):
                for row in range(0, _height):
                    if _array[col][row] == 0 and self.ground[col + _x1][row + _y1].name[0:-2] == self.MAIN_GROUND:
                        self.ground[col + _x1][row + _y1] = Ground(_ground_name + ' ' + str(random.randint(1, 4)))

    def add_sand(self):
        # Step 3 添加沙子
        for col in range(2, self.matrix_width - 2):
            for row in range(2, self.matrix_height - 2):
                if self.ground[col][row].name[0:-2] == 'Blue':
                    for i, j in self.EVEN_ROW_EIGHT_GRID if row % 2 == 0 else self.ODD_ROW_EIGHT_GRID:
                        if self.ground[i + col][j + row].name[0:4] != 'Blue':
                            self.ground[i + col][j + row] = Ground("Sand " + str(random.randint(1, 4)))
                        if random.randint(1, 100) < 30:
                            for k, l in self.EVEN_ROW_EIGHT_GRID if (row + i) % 2 == 0 else self.ODD_ROW_EIGHT_GRID:
                                if self.ground[k + i + col][j + row].name[0:4] != 'Blue':
                                    self.ground[k + i + col][j + row] = Ground("Sand " + str(random.randint(1, 4)))


    def randomize_block(self):
        # Step 1 给大海添加空气墙
        for col in range(0, self.matrix_width):
            for row in range(0, self.matrix_height):
                if self.ground[col][row].name[0:-2] == self.SURROUND_GROUND:
                    self.block[col][row] = Block('Air Wall', self.game_dictionary.block_dict)

        # Step 2 给不同地形添加Block
        for col in range(0, self.matrix_width):
            for row in range(0, self.matrix_height):
                self.randomize_single_block(col, row)

    def randomize_single_block(self, col, row):
        for _ground in range(0, len(self.GROUND_NAME_LIST)):
            if self.GROUND_NAME_LIST[_ground] == self.ground[col][row].name[0:-2]:
                tmp = random.randint(1, 2000)
                for _block in range(0, len(self.BLOCK_NAME_LIST)):
                    if tmp < self.BLOCK_CHANCE_LIST[_ground][_block]:
                        _str = self.BLOCK_NAME_LIST[_block]  # 普通block

                        # 带随机的block
                        if self.BLOCK_NAME_LIST[_block] == 'Decorate':
                            _str = self.BLOCK_NAME_LIST[_block] + self.GROUND_NAME_LIST[_ground] + ' (' + str(
                                random.randint(1, 4)) + ')'
                        if self.BLOCK_NAME_LIST[_block] == 'Tree':
                            _str = self.BLOCK_NAME_LIST[_block] + self.GROUND_NAME_LIST[_ground] + ' (' + str(
                                random.randint(1, 4)) + ')'
                        if self.BLOCK_NAME_LIST[_block] == 'GoldStone':
                            _str = self.BLOCK_NAME_LIST[_block] + ' (' + str(random.randint(1, 4)) + ')'
                        if self.BLOCK_NAME_LIST[_block] == 'BoneHeap':
                            _str = self.BLOCK_NAME_LIST[_block] + ' (' + str(random.randint(1, 4)) + ')'
                        if self.BLOCK_NAME_LIST[_block] == 'ClayStone':
                            _str = self.BLOCK_NAME_LIST[_block] + ' (' + str(random.randint(1, 4)) + ')'
                        self.block[col][row] = Block(_str, self.game_dictionary.block_dict)
                        break
                    tmp -= self.BLOCK_CHANCE_LIST[_ground][_block]
                break

    def init_home(self, _type):
        for col in range(0, self.matrix_width):
            for row in range(0, self.matrix_height):
                self.ground[col][row] = Ground('Air 1')
                self.block[col][row] = Block('Air Wall', self.game_dictionary.block_dict)

        LISTS = [(1, 3), (2, 4), (2, 3), (1, 5), (3, 4), (2, 5), (2, 6), (3, 5), (3, 6), (2, 7)]
        LISTM = [(1, 3), (2, 4), (2, 3), (1, 5), (3, 4), (2, 5), (2, 6), (3, 5), (3, 6), (2, 7), (1, 6), (1, 7), (2, 8), (2, 9), (3, 8), (3, 7), (4, 6)]
        LISTL = [(1, 3), (2, 4), (2, 3), (1, 5), (3, 4), (2, 5), (2, 6), (3, 5), (3, 6), (2, 7), (1, 6), (1, 7), (2, 8), (2, 9), (3, 8), (3, 7), (4, 6), (3, 2), (3, 3), (4, 4), (4, 5), (5, 6), (4, 7), (4, 8), (3, 9), (3, 10)]

        for _point in eval('LIST' + _type):
            self.ground[_point[0]][_point[1]] = Ground('Brown Brick 1')
            self.block[_point[0]][_point[1]] = Block('Air', self.game_dictionary.block_dict)

    def get_random_xy(self):
        _x = random.randint(1, self.matrix_width - 1)
        _y = random.randint(1, self.matrix_height - 1)
        while self.block[_x][_y].name == 'Air Wall':
            _x = random.randint(1, self.matrix_width - 1)
            _y = random.randint(1, self.matrix_height - 1)
        return _x, _y

    def get_random_xy_2(self):
        _x = random.randint(int(self.matrix_width / 2), self.matrix_width - 6)
        _y = random.randint(int(self.matrix_height / 2), self.matrix_height - 10)
        while self.block[_x][_y].name == 'Air Wall':
            _x = random.randint(int(self.matrix_width / 2), self.matrix_width - 6)
            _y = random.randint(int(self.matrix_height / 2), self.matrix_height - 10)
        return _x, _y

class Ground:
    def __init__(self, name):
        self.name = name
        self.img_path = name + '.png'
        # self.img = pygame.image.load('Assets\\Images\\Ground\\' + name)


class Block:
    def __init__(self, name, block_dict):
        self.name = name
        self.offset = block_dict[name][0]
        self.solid = block_dict[name][1]
        self.have_img = block_dict[name][2]
        if self.have_img == 1:
            self.img_path = name + '.png'
        self.can_interact = block_dict[name][3]
        self.method_str = block_dict[name][4]

class Item:

    def __init__(self, name, item_dict):
        self.name = name
        self.stack_limit = item_dict[name][0]
        self.have_img = item_dict[name][1]
        if self.have_img == 1:
            self.img_path = name + '.png'
        self.can_use = item_dict[name][2]
        self.method_str = item_dict[name][3]



