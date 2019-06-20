ITEMS_UI_Y = 440
ITEMS_UI_X = 100
ITEMS_UI_BLANK = 55
__y = ITEMS_UI_Y
__x = ITEMS_UI_X
__num = 0

# 绘制 物品栏边框
while __num < 10:
    print("("+str(__x)+', '+str(__y)+', '+str(__x+50)+', '+str(__y+50)+')' +', ')
    __num += 1
    __x += ITEMS_UI_BLANK
__num = 0