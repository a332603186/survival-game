import environment
import unit
import pygame


class CommonMethods:

    # 像素坐标转矩阵坐标
    @staticmethod
    def pos_pixel_to_pos_matrix(pos_pixel_x, pos_pixel_y):
        _tmp_x = pos_pixel_x
        _tmp_y = pos_pixel_y * 2
        _x = _tmp_x % 80
        _y = _tmp_y % 80
        _res_x = int(_tmp_x / 80)
        _res_y = int(_tmp_y / 80)
        if (_res_x + _res_y) % 2 == 0:
            if (_x + _y) > 80:
                _res_x += 1
                _res_y += 1
        else:
            if _x > _y:
                _res_x += 1
            else:
                _res_y += 1

        if _res_y % 2 == 1:
            _res_x -= 1

        return int(_res_x / 2), _res_y

    @staticmethod
    def pos_matrix_to_pos_pixel(pos_matrix_x, pos_matrix_y):
        if pos_matrix_y % 2 == 0:
            return pos_matrix_x * 160, pos_matrix_y * 40
        else:
            return pos_matrix_x * 160 + 40, pos_matrix_y * 40


    # 计算图片偏移
    @staticmethod
    def calculate_image_offset(_image):
        w, h = _image.get_size()
        w = w // 2
        return 80 - w, 80 - h

    # 计算UNIT图片偏移
    @staticmethod
    def calculate_unit_image_offset(_image):
        w, h = _image.get_size()
        w = w // 2
        return  - w,  - h


    # 玩家使用物品
    @staticmethod
    def use_item(_data, _item_index=-65536):
        if _item_index == -65536:
            _item_index = _data.player.item_in_hand_index
        if _item_index >= len(_data.player.item_list):
            return
        using_item = environment.Item(_data.player.item_list[_item_index], _data.dictionary.item_dict)
        if using_item.can_use == 1:
            CommonMethods.handle_interact(using_item.method_str, _data)

    # 处理条件
    @staticmethod
    def handle_condition(_condition_str, _data):
        if _condition_str[0:3] == 'nul': # 无条件
            return True
        elif _condition_str[0:3] == 'phi': # 玩家有xxx(item)
            if _condition_str[4:] in _data.player.item_list:
                return True
            else:
                return False
        elif _condition_str[0:3] == 'pbs': # 玩家所处block为
            if _condition_str[4:] == _data.environment.block[_data.player.pos_matrix_x][_data.player.pos_matrix_y].name:
                return True
            else:
                return False
        elif _condition_str[0:3] == 'pbf': # 玩家面对block为
            if _condition_str[4:] == _data.environment.block[_data.player.next_pos_matrix_x][_data.player.next_pos_matrix_y].name:
                return True
            else:
                return False
        elif _condition_str[0:3] == 'bsc': # 玩家所处block名称含有
            if _condition_str[4:] in _data.environment.block[_data.player.pos_matrix_x][_data.player.pos_matrix_y].name:
                return True
            else:
                return False
        elif _condition_str[0:3] == 'bsf': # 玩家面对block名称含有
            if _condition_str[4:] in _data.environment.block[_data.player.next_pos_matrix_x][_data.player.next_pos_matrix_y].name:
                return True
            else:
                return False
        print("Error:condition string not exist")
        return False

    # 处理立即触发效果
    @staticmethod
    def handle_effect(_effect_str, _data):
        if _effect_str[0:3] == 'nul':  # 无效果
            return
        elif _effect_str[0:3] == 'bct':  # 将本Block替换为xxx
            _data.environment.block[_data.player.pos_matrix_x][_data.player.pos_matrix_y] = \
                environment.Block(_effect_str[4:], _data.dictionary.block_dict)
            return
        elif _effect_str[0:3] == 'bcf':  # 将玩家面对的Block替换为xxx
            _data.environment.block[_data.player.next_pos_matrix_x][_data.player.next_pos_matrix_y] = \
                environment.Block(_effect_str[4:], _data.dictionary.block_dict)
            return
        elif _effect_str[0:3] == 'pgi':  # 玩家得到xxx(item)
            _data.player.add_item(_effect_str[4:])
            return
        elif _effect_str[0:3] == 'psi':  # 玩家的xxx(item)数量-1
            _data.player.sub_item(_effect_str[4:])
            return
        elif _effect_str[0:3] == 'php':  # 玩家的hp = hp + xxx
            _data.player.add_hp(int(_effect_str[4:]))
            return
        elif _effect_str[0:3] == 'psp':  # 玩家的sp = hp + xxx
            _data.player.add_sp(int(_effect_str[4:]))
            return
        elif _effect_str[0:3] == 'pmb':  # 玩家move by
            _strs = _effect_str[4:].split(',')
            _data.player.pos_pixel_x += int(_strs[0])
            _data.player.pos_pixel_y += int(_strs[1])
            return
        elif _effect_str[0:3] == 'pmt':  # 玩家move to
            _strs = _effect_str[4:].split(',')
            _data.player.pos_pixel_x = int(_strs[0])
            _data.player.pos_pixel_y = int(_strs[1])
            return
        elif _effect_str[0:3] == 'pca':  # 玩家近身攻击xxx,yyy
            _strs = _effect_str[4:].split(',')
            _data.player_close_attack(int(_strs[0]), int(_strs[1]))
            return
        elif _effect_str[0:3] == 'ptt':  # 将玩家转移至xxx
            if _effect_str[4:] != 'home':
                _data.next_environment = _effect_str[4:] + '_environment'
                mx, my = _data.hell_environment.units[0].pos_pixel_x - 600, _data.hell_environment.units[0].pos_pixel_y - 600
                _data.player_next_pos_pixel_x ,_data.player_next_pos_pixel_y = mx, my
            else:
                key = str(_data.player.pos_matrix_x) + ',' + str(_data.player.pos_matrix_y)
                _data.player_next_pos_pixel_x = 320
                _data.player_next_pos_pixel_y = 160
                if key in _data.home_index_dict:
                    _data.next_environment = 'homes[' + str(_data.home_index_dict[key]) + ']'
                else:
                    _data.create_home(_data.player.pos_matrix_x, _data.player.pos_matrix_y, _data.environment.block[_data.player.pos_matrix_x][_data.player.pos_matrix_y].name)
                    _data.next_environment = 'homes[' + str(_data.home_index_dict[key]) + ']'
            _data.transforming = True
            return
        elif _effect_str[0:3] == 'uio':  # 开关显示ui
            if _effect_str[4:] == 'box':
                _data.show_box_ui = ~_data.show_box_ui
            return
        elif _effect_str[0:3] == 'ugt':  # 在玩家位置创建unit
            _data.environment.units.append(environment.Unit(_effect_str[4:], _data.dictionary))
            _data.environment.units[-1].pos_pixel_x = _data.player.pos_pixel_x
            _data.environment.units[-1].pos_pixel_y = _data.player.pos_pixel_y
            return
        elif _effect_str[0:3] == 'ugf':  # 在玩家面对位置创建unit
            _data.environment.units.append(environment.Unit(_effect_str[4:], _data.dictionary))
            _data.environment.units[-1].pos_pixel_x = _data.player.pos_pixel_x + _data.player.FACE_TO[_data.player.face_to_index][0] * 40
            _data.environment.units[-1].pos_pixel_y = _data.player.pos_pixel_y + _data.player.FACE_TO[_data.player.face_to_index][1] * 40
            return
        elif _effect_str[0:3] == 'uga':  # 在指定位置创建unit
            _strs = _effect_str[4:].split(',')
            _data.environment.units.append(environment.Unit(_strs[0], _data.dictionary))
            _data.environment.units[-1].pos_pixel_x = int(_strs[1])
            _data.environment.units[-1].pos_pixel_y = int(_strs[2])
            return

        print("Error:effect string not exist")


    # 处理音乐和音效
    @staticmethod
    def handle_mixer(_mixer_str, _data):
        if _mixer_str[0:3] == 'mpl':  # 无参数播放music
            pygame.mixer.music.load('Assets\\Music\\' + _mixer_str[4:])
            pygame.mixer.music.play()
            return
        elif _mixer_str[0:3] == 'spl':  # 无参数播放sound
            _data.dictionary.sound_dict[_mixer_str[4:]].play()
            return
        print("Error:mixer string not exist")

    # 处理交互
    @staticmethod
    def handle_interact(_interact_str, _data):
        _interact_strs = _interact_str.split(';')
        _condition_meet = True
        for _str in _interact_strs:
            if _str[0] == 'c':  # 处理条件字符串
                _condition_meet = CommonMethods.handle_condition(_str[1:], _data)
                continue
            elif _condition_meet and _str[0] == 'e':  # 如果条件满足 处理立即效果
                CommonMethods.handle_effect(_str[1:], _data)
                continue
            elif _condition_meet and _str[0] == 'm':  # 如果条件满足 处理音效和音乐
                CommonMethods.handle_mixer(_str[1:], _data)
                continue
            elif _condition_meet and _str[0] == 'f':  # 如果条件满足 处理按帧持续效果
                _strs = _str.split('.')
                _data.f_event_list.append([_strs[0][1:], int(_strs[1])])
                continue
            elif _condition_meet and _str[0] == 's':  # 如果条件满足 处理按秒持续效果
                _strs = _str.split('.')
                _data.s_event_list.append([_strs[0][1:], int(_strs[1])])
                continue
            elif _condition_meet and _str[0] == 'd':  # 如果条件满足 处理按帧延时效果
                _strs = _str.split('.')
                _data.d_event_list.append([_strs[0][1:], int(_strs[1])])
                continue

            print("Error:symbol not exist or condition not meet")

    # 物品合成 return crafting_result
    @staticmethod
    def craft_items(_crafting_items, _data):
        _sorted_crafting_items = sorted(_crafting_items)
        _str = _sorted_crafting_items[0] + _sorted_crafting_items[1] + \
            _sorted_crafting_items[2] + _sorted_crafting_items[3]
        if _str in _data.dictionary.craft_dict:
            if not CommonMethods.handle_condition(_data.dictionary.craft_dict[_str][1][1:], _data):
                return 'Nothing'
            else:
                return _data.dictionary.craft_dict[_str][0]
        else:
            return 'Nothing'

