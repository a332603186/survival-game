def check_weapon(_data):
    if _data.player.item_in_hand == 'WeaponKnife1':
        return 1
    elif _data.player.item_in_hand == 'WeaponKnife2':
        return 1
    elif _data.player.item_in_hand == 'WeaponSpear1':
        return 2
    elif _data.player.item_in_hand == 'WeaponSpear2':
        return 2

def check_distance(_boss):
    if _boss.distance_from_player > 300:
        return 1
    else:
        return 0

def check_hp(_boss):
    if _boss.data['hp'] > 20:
        return 1
    else:
        return 0

def script_cal(self, _data): # 运行时会很卡顿，甚至闪退
    i = 0
    while i < 400000:
        i += 1

def script_cal_a(self, _data): # 拆成4段 效果一样 但不会卡
    if _data.frames % 30 == 1:
        i = 0
        while i < 100000:
            i += 1
def script_cal_b(self, _data):
    if _data.frames % 30 == 2:
        i = 0
        while i < 100000:
            i += 1
def script_cal_c(self, _data):
    if _data.frames % 30 == 3:
        i = 0
        while i < 100000:
            i += 1
def script_cal_d(self, _data):
    if _data.frames % 30 == 4:
        i = 0
        while i < 100000:
            i += 1
