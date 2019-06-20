import pygame
import common_methods
import math
import random
import environment

class Unit:
    FACE_TO = [(1, -1), (1.4, 0), (1, 1), (0, 1.4), (-1, 1), (-1.4, 0), (-1, -1), (0, -1.4), (0, 0)]
    def __init__(self, name, _dict):
        # 位置
        self.pos_pixel_x = 0
        self.pos_pixel_y = 0
        self.pos_matrix_x = 0
        self.pos_matrix_y = 0
        self.pixel_speed = 10
        self.movement = [0, 0]

        # 加载字典内容
        self.name = name
        self.solid = _dict.unit_dict[name][0]
        self.have_img = _dict.unit_dict[name][1]
        if self.have_img == 1:
            self.image = _dict.image_dict['Unit\\' + name + '.png']
        elif self.have_img > 1:
            self.images = []
            for i in range(1, self.have_img + 1):
                self.images.append(_dict.image_dict['Unit\\' + name + ' (' + str(i) + ').png'])
            self.image_index = 0
            self.image = self.images[0]
        self.script = _dict.unit_dict[name][2]
        self.scripts = self.script.split(';')
        self.collision_half_width = _dict.unit_dict[name][3]
        self.collision_half_height = _dict.unit_dict[name][4]
        self.can_collide = _dict.unit_dict[name][5]
        self.method_str = _dict.unit_dict[name][6]
        self.offset = common_methods.CommonMethods.calculate_unit_image_offset(self.image)

        # 其他
        self.awake = False
        self.colliding = False
        self.pause_move = False
        self.distance_from_player_x = 0
        self.distance_from_player_y = 0
        self.distance_from_player = 0
        self.data = dict()

    def __lt__(self, other):
        return self.pos_pixel_y < other.pos_pixel_y

    def update(self, _data):
        # 计算是否触发
        if self.pos_pixel_x - self.collision_half_width <= _data.player.pos_pixel_x <= self.pos_pixel_x + self.collision_half_width and \
                self.pos_pixel_y - 2* self.collision_half_width <= _data.player.pos_pixel_y <= self.pos_pixel_y :
            self.colliding = True
        else:
            self.colliding = False

        # 计算距离
        self.distance_from_player_x = math.fabs(self.pos_pixel_x - _data.player.pos_pixel_x)
        self.distance_from_player_y = math.fabs(self.pos_pixel_y - _data.player.pos_pixel_y)
        self.distance_from_player = math.hypot(self.distance_from_player_x, self.distance_from_player_y)
        for _script in self.scripts:
            eval('self.script_' + _script)(_data)

    def script_stay(self, _data):
        return

    def script_one_time_maya(self, _data):
        if _data.frames % 5 == 0:
            self.image_index += 1
            if self.image_index >= self.have_img:
                _data.del_unit(self)
                return
            self.image = self.images[self.image_index]

    def script_one_time_maya_fast(self, _data):
        if _data.frames % 2 == 0:
            self.image_index += 1
            if self.image_index >= self.have_img:
                _data.del_unit(self)
                return
            self.image = self.images[self.image_index]

    def script_play_loop(self, _data):
        if _data.frames % 10 == 0:
            self.image_index += 1
            if self.image_index >= self.have_img:
                self.image_index = 0
                return
            self.image = self.images[self.image_index]

    def script_play_loop_fast(self, _data):
        if _data.frames % 5 == 0:
            self.image_index += 1
            if self.image_index >= self.have_img:
                self.image_index = 0
                return
            self.image = self.images[self.image_index]

    def script_play_loop_by_face(self, _data):
        if _data.frames % 10 == 0:
            self.image_index += 2
            if self.image_index >= self.have_img:
                self.image_index = 0
            if self.data['face'] == 1 and self.image_index % 2 == 0:  # 0 左 1 右
                self.image_index += 1
            self.image = self.images[self.image_index]


    def script_del_by_hp(self, _data):
        if self.data['hp'] <= 0:
            if 'drop_thing' in self.data:
                _x, _y = common_methods.CommonMethods.pos_pixel_to_pos_matrix(self.pos_pixel_x, self.pos_pixel_y)
                if _data.environment.block[_x][_y].name == 'Air':
                    _data.environment.block[_x][_y] = environment.Block(self.data['drop_thing'], _data.dictionary.block_dict)
                if self.name == 'PigMan':
                    _data.victory = True
            _data.del_unit(self)

    def script_del_by_frames(self, _data):
        if _data.frames >= self.data['del_frame']:
            _data.del_unit(self)


    def script_knock_off_player(self, _data):
        if self.colliding:
            _vector_x = self.pos_pixel_x - _data.player.pos_pixel_x
            _vector_y = self.pos_pixel_y - _data.player.pos_pixel_y
            side_length = math.hypot(_vector_x, _vector_y) + 0.1
            _vector_x = int(_vector_x * 30/ side_length)
            _vector_y = int(_vector_y * 30/ side_length)
            common_methods.CommonMethods.handle_interact('fepmb %d,%d.3' % (-_vector_x, -_vector_y), _data)

    def script_knock_off_player_from_point(self, _data):
        if self.colliding:
            _vector_x = self.data['knock_point_x'] - _data.player.pos_pixel_x
            _vector_y = self.data['knock_point_y'] - _data.player.pos_pixel_y
            side_length = math.hypot(_vector_x, _vector_y) + 0.1
            _vector_x = int(_vector_x * 30 / side_length)
            _vector_y = int(_vector_y * 30 / side_length)
            common_methods.CommonMethods.handle_interact('fepmb %d,%d.3' % (-_vector_x, -_vector_y), _data)

    def script_attack_by_knock(self, _data):
        if self.colliding and not self.data['attack_cd']:
            common_methods.CommonMethods.handle_mixer('spl Injured', _data)
            _data.player.sub_hp(self.data['attack'])
            self.data['attack_cd'] = True
        if _data.frames % 30 == 15:
            self.data['attack_cd'] = False

    def script_attack_by_knock_and_del(self, _data):
        if self.colliding and not self.data['attack_cd']:
            common_methods.CommonMethods.handle_mixer('spl Injured', _data)
            _data.player.sub_hp(self.data['attack'])
            _data.del_unit(self)

    def script_attack_q_table(self, _data):
        if self.colliding and not self.data['attack_cd']:
            if self.name == 'SkillSmallFire2':
                index = 0
            elif self.name == 'SkillFireSurroundBlast2':
                index = 1
            elif self.name == 'SkillFireBall2':
                index = 2
            elif self.name == 'SkillFireStorm2':
                index = 3
            elif self.name == 'SkillMapFire2':
                index = 4
            if self.distance_from_player < 200:
                _data.q_table_close_hit_time[index] += 1
            else:
                _data.q_table_far_hit_time[index] += 1


    def script_random_move(self, _data):
        if self.distance_from_player >= self.data['alert_distance']:
            if _data.frames % 60 == 2:
                self.data['movement'] = (random.random() - 0.5, random.random() - 0.5)
            self.pos_pixel_x += self.data['movement'][0] * self.data['speed']
            self.pos_pixel_y += self.data['movement'][1] * self.data['speed']
            if 'face' in self.data:
                self.data['face'] = 1 if self.data['movement'][0] > 0 else 0

    def script_move_to_player(self, _data):
        if self.distance_from_player < self.data['alert_distance'] and not self.pause_move:
            _vector_x = self.pos_pixel_x - _data.player.pos_pixel_x
            _vector_y = self.pos_pixel_y - _data.player.pos_pixel_y
            side_length = math.hypot(_vector_x, _vector_y) + 0.1
            _vector_x = int(_vector_x * self.data['speed'] / side_length)
            _vector_y = int(_vector_y * self.data['speed'] / side_length)
            self.pos_pixel_x -= _vector_x
            self.pos_pixel_y -= _vector_y
            if 'face' in self.data:
                self.data['face'] = 1 if _vector_x < 0 else 0
    def script_move_boss(self, _data):
        if self.pause_move:
            return
        elif self.data['action'] == 0 and self.distance_from_player < self.data['alert_distance']:
            _vector_x = self.pos_pixel_x - _data.player.pos_pixel_x
            _vector_y = self.pos_pixel_y - _data.player.pos_pixel_y
            side_length = math.hypot(_vector_x, _vector_y) + 0.1
            _vector_x = int(_vector_x * self.data['speed'] / side_length)
            _vector_y = int(_vector_y * self.data['speed'] / side_length)
            self.pos_pixel_x += _vector_x
            self.pos_pixel_y += _vector_y
            if 'face' in self.data:
                self.data['face'] = 0 if _vector_x < 0 else 1
        elif self.data['action'] == 1 and self.distance_from_player < self.data['alert_distance']:
            _vector_x = self.pos_pixel_x - _data.player.pos_pixel_x
            _vector_y = self.pos_pixel_y - _data.player.pos_pixel_y
            side_length = math.hypot(_vector_x, _vector_y) + 0.1
            _vector_x = int(_vector_x * self.data['speed'] / side_length)
            _vector_y = int(_vector_y * self.data['speed'] / side_length)
            self.pos_pixel_x -= _vector_x
            self.pos_pixel_y -= _vector_y
            if 'face' in self.data:
                self.data['face'] = 1 if _vector_x < 0 else 0


    def script_set_at_player(self, _data):
        self.pos_pixel_x = _data.player.pos_pixel_x - 5
        self.pos_pixel_y = _data.player.pos_pixel_y + 40

    def script_move_by(self, _data):
        self.pos_pixel_x += self.data['speed_x']
        self.pos_pixel_y += self.data['speed_y']

    def script_home_door(self, _data):
        if self.colliding:
            common_methods.CommonMethods.handle_interact('eptt main', _data)
            px, py = common_methods.CommonMethods.pos_matrix_to_pos_pixel(self.data['pos'][0], self.data['pos'][1])
            _data.player_next_pos_pixel_x = px
            _data.player_next_pos_pixel_y = py

    def script_skill_use(self, _data):
        if self.data['hp'] > 0:
            self.data['action'] = _data.use_decision_tree()
        if _data.frames % 90 == 89 and not self.pause_move and self.data['action'] == 1:
            now_max_reward = 0.0
            now_skill = 'null'
            now_skill_index = -1
            # 距离判断
            if self.distance_from_player < 200:
                # 假设下个状态是远状态 先计算下个状态的最大预期收益
                for i in range(0, len(_data.Q_TABLE_SKILL_NAME)):
                    if not self.data[_data.Q_TABLE_SKILL_NAME[i]+'CD']:
                        next_reward = _data.Q_TABLE_SKILL_DAMAGE[i] * _data.q_table_far_hit_time[i] / _data.q_table_far_shoot_time[i]
                        temp = _data.Q_TABLE_SKILL_DAMAGE[i] * _data.q_table_close_hit_time[i] / _data.q_table_close_shoot_time[i]
                        if temp > now_max_reward and temp > next_reward * _data.NEXT_RATIO:
                            now_max_reward = temp
                            now_skill = _data.Q_TABLE_SKILL_NAME[i]
                            now_skill_index = i
                if now_skill == 'null':
                    return
                else:
                    self.data[now_skill] = True
                    self.data[now_skill + 'SF'] = _data.frames
                    _data.q_table_close_shoot_time[now_skill_index] += 1
            else:
                # 假设下个状态是近状态 先计算下个状态的最大预期收益
                for i in range(0, len(_data.Q_TABLE_SKILL_NAME)):
                    if not self.data[_data.Q_TABLE_SKILL_NAME[i] + 'CD']:
                        next_reward = _data.Q_TABLE_SKILL_DAMAGE[i] * _data.q_table_close_hit_time[i] / \
                               _data.q_table_close_shoot_time[i]
                        temp = _data.Q_TABLE_SKILL_DAMAGE[i] * _data.q_table_far_hit_time[i] / \
                               _data.q_table_far_shoot_time[i]
                        if temp > now_max_reward and temp > next_reward * _data.NEXT_RATIO:
                            now_max_reward = temp
                            now_skill = _data.Q_TABLE_SKILL_NAME[i]
                            now_skill_index = i
                if now_skill == 'null':
                    return
                else:
                    self.data[now_skill] = True
                    self.data[now_skill + 'SF'] = _data.frames
                    _data.q_table_far_shoot_time[now_skill_index] += 1

        for i in _data.Q_TABLE_SKILL_NAME:
            eval("self.skill_" + i)(_data)

    def skill_SmallFire(self, _data):
        if not self.data['SmallFire'] :
            return
        _res = _data.frames - self.data['SmallFireSF']
        if _res == 0:
            _data.environment.units.append(environment.Unit('SkillSmallFire', _data.dictionary))
            _data.environment.units[-1].pos_pixel_x = int((5 * _data.player.pos_pixel_x + self.pos_pixel_x) / 6)
            _data.environment.units[-1].pos_pixel_y = int((5 * _data.player.pos_pixel_y + self.pos_pixel_y) / 6 + 40)
            _data.environment.units[-1].data['knock_point_x'] = self.pos_pixel_x
            _data.environment.units[-1].data['knock_point_y'] = self.pos_pixel_y
            self.data['SmallFireCD'] = True
            self.pause_move = True
            common_methods.CommonMethods.handle_interact('dmspl Boom.1', _data)
        elif _res == 30:
            self.pause_move = False
        elif _res == 80:
            self.data['SmallFire'] = False
            self.data['SmallFireCD'] = False
    def script_small_fire(self, _data):
        if _data.frames % 1 == 0:
            self.image_index += 1
            if self.image_index >= self.have_img:
                _data.environment.units.append(environment.Unit('SkillSmallFire2', _data.dictionary))
                _data.environment.units[-1].pos_pixel_x = self.pos_pixel_x
                _data.environment.units[-1].pos_pixel_y = self.pos_pixel_y
                _data.environment.units[-1].data['attack'] = 20
                _data.environment.units[-1].data['attack_cd'] = False
                _data.environment.units[-1].data['knock_point_x'] = self.data['knock_point_x']
                _data.environment.units[-1].data['knock_point_y'] = self.data['knock_point_y']
                _data.del_unit(self)
                return
            self.image = self.images[self.image_index]

    def skill_FireSurroundBlast(self, _data):
        if not self.data['FireSurroundBlast'] :
            return
        _res = _data.frames - self.data['FireSurroundBlastSF']
        if _res == 0:
            self.skill_FireSurroundBlast1(_data, 80)
            self.pause_move = True
            self.data['FireSurroundBlastCD'] = True
            common_methods.CommonMethods.handle_mixer('spl Ready1', _data)
        elif _res == 18:
            common_methods.CommonMethods.handle_mixer('spl Boom', _data)
        elif _res == 10:
            self.skill_FireSurroundBlast1(_data, 120)
            common_methods.CommonMethods.handle_mixer('spl Ready1', _data)
        elif _res == 28:
            common_methods.CommonMethods.handle_mixer('spl Boom', _data)
        elif _res == 20:
            self.skill_FireSurroundBlast1(_data, 160)
            common_methods.CommonMethods.handle_mixer('spl Ready1', _data)
        elif _res == 38:
            common_methods.CommonMethods.handle_mixer('spl Boom', _data)
        elif _res == 68:
            self.pause_move = False
        elif _res == 360:
            self.data['FireSurroundBlastCD'] = False
            self.data['FireSurroundBlast'] = False

    def skill_FireSurroundBlast1(self, _data, _range):
        for i in range(0, 8):
            _x = int(self.FACE_TO[i][0] * _range + self.pos_pixel_x)
            _y = int(self.FACE_TO[i][1] * _range + self.pos_pixel_y)
            _data.environment.units.append(environment.Unit('SkillFireSurroundBlast1', _data.dictionary))
            _data.environment.units[-1].pos_pixel_x = _x
            _data.environment.units[-1].pos_pixel_y = _y
            _data.environment.units[-1].data['knock_point_x'] = self.pos_pixel_x
            _data.environment.units[-1].data['knock_point_y'] = self.pos_pixel_y
        self.skill_FireBall(_data)

    def script_fire_surround_blast(self, _data):
        if _data.frames % 2 == 0:
            self.image_index += 1
            if self.image_index >= self.have_img:
                _data.environment.units.append(environment.Unit('SkillFireSurroundBlast2', _data.dictionary))
                _data.environment.units[-1].pos_pixel_x = self.pos_pixel_x
                _data.environment.units[-1].pos_pixel_y = self.pos_pixel_y
                _data.environment.units[-1].data['attack'] = 20
                _data.environment.units[-1].data['attack_cd'] = False
                _data.environment.units[-1].data['knock_point_x'] = self.data['knock_point_x']
                _data.environment.units[-1].data['knock_point_y'] = self.data['knock_point_y']
                _data.del_unit(self)
                return
            self.image = self.images[self.image_index]

    def skill_FireBall(self, _data):
        if not self.data['FireBall'] :
            return
        _res = _data.frames - self.data['FireBallSF']
        if _res == 0:
            _data.environment.units.append(environment.Unit('SkillFireBall1', _data.dictionary))
            _data.environment.units[-1].pos_pixel_x = _data.player.pos_pixel_x
            _data.environment.units[-1].pos_pixel_y = _data.player.pos_pixel_y + 40
            _data.environment.units[-1].data['knock_point_x'] = self.pos_pixel_x
            _data.environment.units[-1].data['knock_point_y'] = self.pos_pixel_y
            common_methods.CommonMethods.handle_mixer('spl Ready2', _data)
            self.data['FireBallCD'] = True
        elif _res == 20:
            common_methods.CommonMethods.handle_mixer('spl Fire Ball', _data)
        elif _res == 80:
            self.data['FireBall'] = False
            self.data['FireBallCD'] = False

    def script_fire_ball(self, _data):
        if _data.frames % 2 == 0:
            self.image_index += 1
            if self.image_index >= self.have_img:
                _data.environment.units.append(environment.Unit('SkillFireBall2', _data.dictionary))
                _data.environment.units[-1].pos_pixel_x = self.pos_pixel_x
                _data.environment.units[-1].pos_pixel_y = self.pos_pixel_y
                _data.environment.units[-1].data['alert_distance'] = 2000
                _data.environment.units[-1].data['speed'] = 10
                _data.environment.units[-1].data['attack'] = 20
                _data.environment.units[-1].data['attack_cd'] = False
                _data.environment.units[-1].data['del_frame'] = _data.frames + 30
                _data.environment.units[-1].data['knock_point_x'] = self.pos_pixel_x
                _data.environment.units[-1].data['knock_point_y'] = self.pos_pixel_y
                _data.del_unit(self)
                return
            self.image = self.images[self.image_index]

    def skill_FireStorm(self, _data):
        if not self.data['FireStorm'] :
            return
        _res = _data.frames - self.data['FireStormSF']
        if _res == 0:
            self.pause_move = True
            common_methods.CommonMethods.handle_mixer('spl Fire Storm', _data)
            for i in range(0, 4):
                _data.environment.units.append(environment.Unit('SkillFireStorm1', _data.dictionary))
                _data.environment.units[-1].pos_pixel_x = self.pos_pixel_x + random.choice([-1, 1]) * random.randint(200, 400)
                _data.environment.units[-1].pos_pixel_y = self.pos_pixel_y + random.choice([-1, 1]) * random.randint(150, 300)
            self.data['FireStormCD'] = True
        elif _res == 50:
            common_methods.CommonMethods.handle_mixer('spl Fire Storm', _data)
            for i in range(0, 4):
                _data.environment.units.append(environment.Unit('SkillFireStorm1', _data.dictionary))
                _data.environment.units[-1].pos_pixel_x = self.pos_pixel_x + random.choice([-1, 1]) * random.randint(200, 400)
                _data.environment.units[-1].pos_pixel_y = self.pos_pixel_y + random.choice([-1, 1]) * random.randint(150, 300)
        elif _res == 91:
            self.pause_move = False
        elif _res == 360:
            self.data['FireStorm'] = False
            self.data['FireStormCD'] = False

    def script_fire_storm(self, _data):
        if _data.frames % 4 == 0:
            self.image_index += 1
            if self.image_index >= self.have_img:
                _data.environment.units.append(environment.Unit('SkillFireStorm2', _data.dictionary))
                _data.environment.units[-1].pos_pixel_x = self.pos_pixel_x
                _data.environment.units[-1].pos_pixel_y = self.pos_pixel_y
                _data.environment.units[-1].data['alert_distance'] = 2000
                _data.environment.units[-1].data['speed'] = 6
                _data.environment.units[-1].data['attack'] = 20
                _data.environment.units[-1].data['attack_cd'] = False
                _data.del_unit(self)
                return
            self.image = self.images[self.image_index]

    def skill_MapFire(self, _data):
        if not self.data['MapFire'] :
            return
        _res = _data.frames - self.data['MapFireSF']
        if _res == 0:
            common_methods.CommonMethods.handle_mixer('spl Map Fire', _data)
            for i in range(0, 4):
                _data.environment.units.append(environment.Unit('SkillMapFire', _data.dictionary))
                _data.environment.units[-1].pos_pixel_x = _data.player.pos_pixel_x + random.randint(-400, 400)
                _data.environment.units[-1].pos_pixel_y = _data.player.pos_pixel_y + random.randint(-300, 300)
            self.data['MapFireCD'] = True
            self.pause_move = True
        elif _res == 50:
            common_methods.CommonMethods.handle_mixer('spl Map Fire', _data)
        elif _res == 90:
            self.pause_move = False
        elif _res == 1080:
            self.data['MapFire'] = False
            self.data['MapFireCD'] = False

    def script_map_fire(self, _data):
        if _data.frames % 2 == 0:
            self.image_index += 1
            if self.image_index == 7:
                _data.environment.units.append(environment.Unit('SkillMapFire1', _data.dictionary))
                _data.environment.units[-1].pos_pixel_x = self.pos_pixel_x
                _data.environment.units[-1].pos_pixel_y = self.pos_pixel_y
                _data.environment.units[-1].data['del_frame'] = _data.frames + 90
            if self.image_index >= self.have_img:
                _data.del_unit(self)
                return
            self.image = self.images[self.image_index]

    def script_map_fire_1(self, _data):
        if _data.frames % 30 == 6:
            for i in range(0, 6):
                _data.environment.units.append(environment.Unit('SkillMapFire2', _data.dictionary))
                _data.environment.units[-1].pos_pixel_x = self.pos_pixel_x
                _data.environment.units[-1].pos_pixel_y = self.pos_pixel_y
                _data.environment.units[-1].data['del_frame'] = _data.frames + 60
                _x = random.randint(-3, 3)
                _y = random.randint(-3, 3)
                _side_length =  math.hypot(_x, _y) + 0.1
                _data.environment.units[-1].data['speed_x'] = int(_x / _side_length * 10)
                _data.environment.units[-1].data['speed_y'] = int(_y / _side_length * 10)
                _data.environment.units[-1].data['alert_distance'] = 2000
                _data.environment.units[-1].data['attack'] = 20
                _data.environment.units[-1].data['attack_cd'] = False

    def script_map_fire_2(self, _data):
        if _data.frames % 2 == 0:
            self.image_index += 1
            if self.image_index >= self.have_img:
                self.image_index = 4
            self.image = self.images[self.image_index]





