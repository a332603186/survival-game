import pygame
import os
import common_methods
class Dictionary:
    block_dict = dict()
    item_dict = dict()
    craft_dict = dict()
    unit_dict = dict()
    image_dict = dict()
    sound_dict = dict()

    def __init__(self):
        ASSETS_DIR = 'Assets\\'
        # 载入图片库
        file_list = os.listdir(ASSETS_DIR + 'Ground\\')
        # 载入block字典
        file_list = os.listdir(ASSETS_DIR + 'Block\\')
        for file_path in file_list:
            if file_path[-4:] == '.txt':
                f = open(ASSETS_DIR + 'Block\\' + file_path, 'r')
                f_str = f.readlines()
                _offset = (0, 0)
                if int(f_str[1]) == 1:
                    _offset = common_methods.CommonMethods.calculate_image_offset(self.image_dict['Block\\' + file_path[:-4] + '.png'])
                self.block_dict[file_path[:-4]] = (_offset,        # 图片偏移量(int32)
                                                   int(f_str[0]),  # 是否实心(0否/1是)
                                                   int(f_str[1]),  # 是否有图片(0否/1是)
                                                   int(f_str[2]),  # 是否可交互(0否/1是)
                                                   f_str[3])       # 效果/条件字符串(str)
        # 载入item字典
        file_list = os.listdir(ASSETS_DIR + 'Item\\')
        for file_path in file_list:
            if file_path[-4:] == '.txt':
                f = open(ASSETS_DIR + 'Item\\' + file_path, 'r')
                f_str = f.readlines()
                self.item_dict[file_path[:-4]] = (int(f_str[0]),  # 堆叠上限(int32)
                                                  int(f_str[1]),  # 是否有图片(0否/1是)
                                                  int(f_str[2]),  # 是否可使用(0否/1是)
                                                  f_str[3])       # 使用函数及参数(str)
        # 载入合成表
        file_list = os.listdir(ASSETS_DIR + 'Craft Guide\\')
        for file_path in file_list:
            if file_path[-4:] == '.txt':
                f = open(ASSETS_DIR + 'Craft Guide\\' + file_path, 'r')
                f_str = f.readlines()
                _strs = [f_str[0][:-1], f_str[1][:-1], f_str[2][:-1], f_str[3][:-1]]
                _strs.sort()
                self.craft_dict[_strs[0] + _strs[1] + _strs[2] + _strs[3]] = (f_str[4][:-1],  # 合成结果(str(item))
                                                                              f_str[5])  # 条件函数及参数(str)
        # 载入unit字典
        file_list = os.listdir(ASSETS_DIR + 'Unit\\')
        for file_path in file_list:
            if file_path[-4:] == '.txt':
                f = open(ASSETS_DIR + 'Unit\\' + file_path, 'r')
                f_str = f.readlines()
                self.unit_dict[file_path[:-4]] = (int(f_str[0]),  # 是否实心(0否/1是)
                                                  int(f_str[1]),  # 是否有图片(0否/1是)
                                                  f_str[2][:-1],  # 脚本名(str)
                                                  int(f_str[3]),  # 碰撞判定矩阵长(int32)
                                                  int(f_str[4]),  # 碰撞判定矩阵高(int32)
                                                  int(f_str[5]),  # 是否有碰撞事件(0否/1是)
                                                  f_str[6])       # 效果/条件字符串(str)
        # 载入音效库
        file_list = os.listdir(ASSETS_DIR + 'Sound\\')
        for file_path in file_list:
            self.sound_dict[file_path[:-4]] = \
                pygame.mixer.Sound(ASSETS_DIR + 'Sound\\' + file_path)



