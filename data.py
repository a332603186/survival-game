import settings
import environment
import player
import dictionary
import math
import random
import unit
import Decision_Tree
from common_methods import CommonMethods

class Data:
    def __init__(self):
        # 初始化设置 settings
        self.settings = settings.Settings(800, 600)
        # 初始化字典 dictionary
        self.dictionary = dictionary.Dictionary()
        # 强化学习q-table
        self.q_table_close_hit_time = [80, 80, 20, 30, 100]
        self.q_table_close_shoot_time = [100, 100, 100, 100, 100]
        self.q_table_far_hit_time = [0, 0, 50, 50, 100]
        self.q_table_far_shoot_time = [100, 100, 100, 100, 100]
        self.Q_TABLE_SKILL_NAME = ['SmallFire', 'FireSurroundBlast', 'FireBall', 'FireStorm', 'MapFire']
        self.Q_TABLE_SKILL_DAMAGE = [20, 100, 20, 50, 1000]
        self.NEXT_RATIO = 0.1
        # 初始化玩家 player
        self.player = player.Player()
        # 初始化主环境 main_environment
        self.main_environment = environment.Environment(name='main', matrix_width=256, matrix_height=256,
                                                        _dictionary=self.dictionary)
        self.main_environment.SURROUND_GROUND = 'Blue'
        self.main_environment.MAIN_GROUND = 'Grass'
        self.main_environment.GROUND_NAME_LIST = ['Grass', 'Forest','Clay','YellowGrass','Snow', 'Swamp', 'Autumn',  'Blue']
        self.main_environment.BLOCK_NAME_LIST = [ 'Rock', 'Flint', 'Twig', 'CutGrass', 'Apple', 'Carrot', 'RedMushroom', 'BlueMushroom', 'Pepper', 'Decorate', 'Tree', 'GoldStone', 'BoneHeap', 'ClayStone']
        self.main_environment.BLOCK_CHANCE_LIST =[[25,    25,      25,      25,         25,      25,       25,            5,            5,          100,         25,    5,           5,          5], # Grass
                                 [5,     5,       50,      25,         50,      0,        25,            5,            5,          100,         100,   0,           0,          0], # Forest
                                 [75,    75,      5,       5,          0,       0,        10,            0,            5,          100,         0,     20,          20,         20],  # Clay
                                 [25,    25,      25,      25,         25,      25,       25,            5,            5,          100,         50,    5,           5,          5],  # YellowGrass
                                 [25,    25,      25,      25,         25,      25,       10,            0,            5,          100,         50,    5,           0,          0], # Snow
                                 [25,    25,      25,      25,         25,      25,       25,            10,           5,          100,         50,    5,           50,         0], # Swamp
                                 [25,    25,      25,      25,         25,      25,       25,            5,            5,          100,         50,    5,           5,          5],   # Autumn
                                 [0,     0,       0,       0,          0,       0,        0,             0,            0,          0,           0,     0,           0,          0] # Blue
                                 ]
        self.main_environment.randomize_ground()
        self.main_environment.add_sand()
        self.main_environment.randomize_block()
        for i in range(0, 100):
            self.main_environment.units.append(unit.Unit('Deer', self.dictionary))
            mx, my = self.main_environment.get_random_xy()
            self.main_environment.units[-1].pos_pixel_x, self.main_environment.units[-1].pos_pixel_y = CommonMethods.pos_matrix_to_pos_pixel(mx, my)
            self.main_environment.units[-1].data['speed'] = 5
            self.main_environment.units[-1].data['hp'] = 20
            self.main_environment.units[-1].data['movement'] = (0, 0)
            self.main_environment.units[-1].data['alert_distance'] = 0
            self.main_environment.units[-1].data['drop_thing'] = 'Meat'
            self.main_environment.units[-1].data['face'] = 0
        for i in range(0, 4):
            mx, my = self.main_environment.get_random_xy()
            self.main_environment.block[mx][my] = environment.Block('HellDoor', self.dictionary.block_dict)

        mx, my = self.main_environment.get_random_xy()
        self.player.pos_pixel_x, self.player.pos_pixel_y = CommonMethods.pos_matrix_to_pos_pixel(mx, my)
        self.player.pos_matrix_x, self.player.pos_matrix_y = mx, my

        # 初始化地狱环境 hell_environment
        self.hell_environment = environment.Environment(name='hell', matrix_width=64, matrix_height=96,
                                                        _dictionary=self.dictionary)
        self.hell_environment.SURROUND_GROUND = 'Red'
        self.hell_environment.MAIN_GROUND = 'Stone'
        self.hell_environment.GROUND_NAME_LIST = ['Stone', 'Deep Stone', 'Hell', 'Obsidian']
        self.hell_environment.randomize_hell_ground()
        self.hell_environment.randomize_block()

        self.hell_environment.units.append(unit.Unit('PigMan', self.dictionary))
        mx, my = self.hell_environment.get_random_xy_2()
        self.hell_environment.units[-1].pos_pixel_x, self.hell_environment.units[
            -1].pos_pixel_y = CommonMethods.pos_matrix_to_pos_pixel(mx, my)
        self.hell_environment.units[-1].data['attack_cd'] = False
        self.hell_environment.units[-1].data['attack'] = 5
        self.hell_environment.units[-1].data['speed'] = 5
        self.hell_environment.units[-1].data['hp'] = 600
        self.hell_environment.units[-1].data['movement'] = (0, 0)
        self.hell_environment.units[-1].data['alert_distance'] = 5000
        self.hell_environment.units[-1].data['drop_thing'] = 'RedMushroom'
        self.hell_environment.units[-1].data['face'] = 0
        self.hell_environment.units[-1].data['action'] = 1
        for str in self.Q_TABLE_SKILL_NAME:
            self.hell_environment.units[-1].data[str] = False
            self.hell_environment.units[-1].data[str + 'CD'] = False
        # 家
        self.home_index_dict = dict()
        self.homes = []

        # 当前绘制场景为main_environment
        self.environment = self.main_environment
        self.transforming = False
        self.fighting_boss = False
        self.victory = False
        self.next_environment = ''
        self.player_next_pos_pixel_x = 0
        self.player_next_pos_pixel_y = 0


        # 初始化awake_units
        self.awake_units = []
        self.colliding_unit = ''

        # 初始化储物箱box
        self.box_items = dict()
        self.box_items_count = dict()

        # 初始化ui控制变量
        self.show_box_ui = False
        self.show_ex_items_ui = False

        # 初始化常量
        self.PLAYER_SCREEN_OFFSET = (int(self.settings.get_screen_width() / 2) - 20,  # 玩家屏幕偏移
                                    int(self.settings.get_screen_height() / 2) - 40)
        self.UNIT_SCREEN_OFFSET = (int(self.settings.get_screen_width() / 2),
                                   int(self.settings.get_screen_height() / 2))
        self.ONE_DAY_FRAMES = 2000
        self.CHECK_AWAKE_UNITS_X = 500
        self.CHECK_AWAKE_UNITS_Y = 400

        # 初始化计时器
        self.frames = 0
        self.frame_time_sec = 0
        self.frame_time_min = 0
        self.frame_time_hour = 0
        self.night = False

        # 初始化滤镜
        self.filter_name = 'Day'

        # 初始化延时事件集合
        self.f_event_list = []
        self.s_event_list = []
        self.d_event_list = []



    def update(self):
        self.update_units()
        self.update_clock()
        self.update_continuous_events()

        # 更新img index
        if self.frames % 8 == 0:
            self.player.stay_img_index = (self.player.stay_img_index + 1) % 8
        if self.frames % 4 == 0 and self.player.state == 'W':
            self.player.run_img_index = (self.player.run_img_index + 1) % 8
        if self.frames % 2 == 0 and self.player.state == 'R':
            self.player.run_img_index = (self.player.run_img_index + 1) % 8
        # 玩家饥饿
        if self.frames % 90 == 29:
            self.player.sub_sp(1)
        # 昼夜交替
        if self.frames % 2000 == 1999:
            self.night = ~self.night
        # 夜晚刷新怪物
        if self.night and self.frames % 300 == 299:
            self.environment.units.append(unit.Unit('MushroomMonster', self.dictionary))
            self.environment.units[-1].pos_pixel_x = self.player.pos_pixel_x + random.choice([-1, 1]) * random.randint(400, 1200)
            self.environment.units[-1].pos_pixel_y = self.player.pos_pixel_y + random.choice([-1, 1]) * random.randint(300, 900)
            self.environment.units[-1].data['attack_cd'] = False
            self.environment.units[-1].data['attack'] = 5
            self.environment.units[-1].data['speed'] = 5
            self.environment.units[-1].data['hp'] = 20
            self.environment.units[-1].data['movement'] = (0, 0)
            self.environment.units[-1].data['alert_distance'] = 1000
            self.environment.units[-1].data['drop_thing'] = 'RedMushroom'
            self.environment.units[-1].data['face'] = 0
            self.environment.units[-1].data['action'] = 1


    def update_units(self):
        for _unit in self.environment.units:
            if math.fabs(_unit.pos_pixel_x - self.player.pos_pixel_x) < self.CHECK_AWAKE_UNITS_X and \
             math.fabs(_unit.pos_pixel_y - self.player.pos_pixel_y) < self.CHECK_AWAKE_UNITS_Y:
                if not _unit.awake:
                    _unit.awake = True
                    self.awake_units.append(_unit)
                    if _unit.name == 'PigMan':
                        self.fighting_boss = True
                        self.CHECK_AWAKE_UNITS_X = 200000
                        self.CHECK_AWAKE_UNITS_Y = 200000
                    self.awake_units.sort()
                else:
                    _unit.update(self)
            else:
                if _unit.awake:
                    _unit.awake = False
                    self.awake_units.remove(_unit)

    def update_clock(self):
        self.frames += 1
        if self.frames % 30 == 0:
            self.frame_time_sec += 1
            if self.frame_time_sec % 60 == 0:
                self.frame_time_sec = 0
                self.frame_time_min += 1
                if self.frame_time_min % 60 == 0:
                    self.frame_time_min = 0
                    self.frame_time_hour += 1

    def update_block(self):
        _x = random.randint(0, self.environment.matrix_width - 1)
        _y = random.randint(0, self.environment.matrix_height - 1)
        if self.environment.block[_x][_y] == 'Air':
            self.environment.randomize_single_block(_x, _y)

    def update_continuous_events(self):
        # 处理帧模式持续事件
        for event in self.f_event_list:
            _method_str = event[0]
            CommonMethods.handle_interact(_interact_str=_method_str, _data=self)
            event[1] -= 1
            if event[1] <= 0:
                self.f_event_list.remove(event)
        # 处理秒模式持续事件
        if self.frames % 30 == 0:
            for event in self.s_event_list:
                _method_str = event[0]
                CommonMethods.handle_interact(_interact_str=_method_str, _data=self)
                event[1] -= 1
                if event[1] <= 0:
                    self.s_event_list.remove(event)
        # 处理10帧模式延时事件
        if self.frames % 10 == 0:
            for event in self.d_event_list:
                if event[1] <= 0:
                    _method_str = event[0]
                    CommonMethods.handle_interact(_interact_str=_method_str, _data=self)
                    self.d_event_list.remove(event)
                else:
                    event[1] -= 1

    def del_unit(self, _unit):
        if _unit in self.awake_units:
            self.awake_units.remove(_unit)
        if _unit in self.environment.units:
            self.environment.units.remove(_unit)

    def player_close_attack(self, _damage, _range):
        # 获取6位判定点
        _index = [self.player.face_to_index, self.player.face_to_index - 1, self.player.face_to_index + 1]
        if _index[2] > 7:
            _index[2] = 0
        _points = []
        for i in range(0, 3):
            _points.append((self.player.pos_pixel_x + self.player.FACE_TO[_index[i]][0] * _range, self.player.pos_pixel_y + self.player.FACE_TO[_index[i]][1] * _range))
            _points.append((self.player.pos_pixel_x + self.player.FACE_TO[_index[i]][0] * _range * 2, self.player.pos_pixel_y + self.player.FACE_TO[_index[i]][1] * _range * 2))
        _points.append((self.player.pos_pixel_x, self.player.pos_pixel_y))

        # 检查被命中unit
        for _unit in self.awake_units:
            _x_range = (_unit.pos_pixel_x - _unit.collision_half_width, _unit.pos_pixel_x + _unit.collision_half_width)
            _y_range = (_unit.pos_pixel_y - 2 *  _unit.collision_half_height, _unit.pos_pixel_y)
            for i in range(0, 6):
                if _x_range[0] < _points[i][0] < _x_range[1] and _y_range[0] < _points[i][1] < _y_range[1]:
                    CommonMethods.handle_mixer('spl Hit 1', self)
                    if 'hp' in _unit.data:
                        _unit.data['hp'] -= _damage
                    break

    def create_home(self, pos_m_x, pos_m_y, home_name):
        home_environment = environment.Environment(name='home', matrix_width=16, matrix_height=16,
                                                   _dictionary=self.dictionary)
        home_environment.units.append(unit.Unit('HomeDoor', self.dictionary))
        home_environment.units[-1].pos_pixel_x = 220
        home_environment.units[-1].pos_pixel_y = 140
        home_environment.units[-1].data['pos'] = (pos_m_x, pos_m_y)
        key = str(pos_m_x) + ',' + str(pos_m_y)
        self.home_index_dict[key] = len(self.homes)
        self.homes.append(home_environment)
        if home_name == 'HomeS':
            home_environment.init_home('S')
        elif home_name == 'HomeM':
            home_environment.init_home('M')
        elif home_name == 'HomeL':
            home_environment.init_home('L')

    #boss数据
    def check_weapon(self):
        if self.player.item_in_hand == 'WeaponKnife1':
            return 1
        elif self.player.item_in_hand == 'WeaponKnife2':
            return 1
        elif self.player.item_in_hand == 'WeaponSpear1':
            return 2
        elif self.player.item_in_hand == 'WeaponSpear2':
            return 2
        return 0

    def check_distance(self):
        if self.hell_environment.units[0].distance_from_player > 500:
            return 1
        else:
            return 0

    def check_hp(self):
        if self.hell_environment.units[0].data['hp'] > 100:
            return 1
        else:
            return 0

    def check_all(self):
        testVec = [self.check_hp(), self.check_weapon(), self.check_distance()]  # 输入测试数据血量，距离,武器装甲情况
        return testVec  # 测试数据


    def use_decision_tree(self):
        testVec = self.check_all()
        featLabels =Decision_Tree.readfeatLabels()
        inputTree = Decision_Tree.readTree()
        classLabel = Decision_Tree.classify(inputTree,featLabels, testVec)
        print(classLabel+ str(testVec))
        if classLabel == 'yes':
            return 1
        else:
            return 0








