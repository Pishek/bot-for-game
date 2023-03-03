import numpy as np
import cv2
import mss.tools
import time
import win32api
import win32con
import derevo
import MakeWindowActive

# кнопка стоп
o = 'v'
temnie = cv2.imread('img_navigation/temnie.png', 0)
temnie_slovo = cv2.imread('img_navigation/temnie_slovo.png', 0)
#функция для скриншота карты
with mss.mss()  as sct:
    def screen_map():
        global x
        global y
        # Координаты захвата, top верх лев координата, x - левая координата, остальные ширина и высота
        monitor = {"top": 0, "left": 0, "width": 776, "height": 601}
        # Захват экрана, по координатам
        base_screen = sct.grab(monitor)
        # output = "map.png".format(**monitor)
        # mss.tools.to_png(base_screen.rgb, base_screen.size, output = output)
        base_screen = cv2.cvtColor(np.array(base_screen), cv2.COLOR_BGR2HSV)
        cv2.circle(base_screen, (750, 30), 35, (0, 255), -1)
        karta_color_low = (165, 120, 160)  # Данный цвет это темный ненасыщенный красный, близкий к бордовому
        karta_color_high = (166, 175, 255)
        only_strelka_hsv = cv2.inRange(base_screen, karta_color_low, karta_color_high)
        # cv2.imshow('contours2', only_strelka_hsv)
        # cv2.waitKey(0)
        # вычисляем моменты изображения
        moments = cv2.moments(only_strelka_hsv, 1)
        dM01 = moments['m01']
        dM10 = moments['m10']
        dArea = moments['m00']
        # будем реагировать только на те моменты,
        # которые содержать больше 100 пикселей
        if dArea > 0:
            x = dM10 / dArea
            y = dM01 / dArea
        return (x, y)

def dist(x1, y1, x2, y2):
    return (((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)

def move(x, y):
    win32api.keybd_event(0x0D, 0, 0, 0)

def define_corner_triangle(xp, yp):
    x1, y1 = screen_map()
    distance1 = dist(x1,y1,xp,yp)
    win32api.keybd_event(0x44, 0, 0, 0)
    time.sleep(0.08)
    win32api.keybd_event(0x44, 0, win32con.KEYEVENTF_KEYUP, 0)
    x1, y1 = screen_map()
    distance2 = dist(x1,y1,xp,yp)
    if distance2>distance1:
        win32api.keybd_event(0x41, 0, 0, 0)
        time.sleep(0.08)
        win32api.keybd_event(0x41, 0, win32con.KEYEVENTF_KEYUP, 0)
    else:
        while distance2<distance1:
            distance1 = distance2
            win32api.keybd_event(0x44, 0, 0, 0)
            time.sleep(0.078)
            win32api.keybd_event(0x44, 0, win32con.KEYEVENTF_KEYUP, 0)
            x1, y1 = screen_map()
            distance2 = dist(x1,y1,xp,yp)
        win32api.keybd_event(0x41, 0, 0, 0)
        time.sleep(0.078)
        win32api.keybd_event(0x41, 0, win32con.KEYEVENTF_KEYUP, 0)

    time.sleep(0.08)

    x1, y1 = screen_map()
    distance1 = dist(x1, y1, xp, yp)
    win32api.keybd_event(0x41, 0, 0, 0)
    time.sleep(0.08)
    win32api.keybd_event(0x41, 0, win32con.KEYEVENTF_KEYUP, 0)
    x1, y1 = screen_map()
    distance2 = dist(x1, y1, xp, yp)
    if distance2>distance1:
        win32api.keybd_event(0x44, 0, 0, 0)
        time.sleep(0.08)
        win32api.keybd_event(0x44, 0, win32con.KEYEVENTF_KEYUP, 0)
    else:
        while distance2 < distance1:
            distance1 = distance2
            win32api.keybd_event(0x41, 0, 0, 0)
            time.sleep(0.078)
            win32api.keybd_event(0x41, 0, win32con.KEYEVENTF_KEYUP, 0)
            x1, y1 = screen_map()
            distance2 = dist(x1, y1, xp, yp)
        win32api.keybd_event(0x44, 0, 0, 0)
        time.sleep(0.078)
        win32api.keybd_event(0x44, 0, win32con.KEYEVENTF_KEYUP, 0)

def min_dist_for_point():
    global p
    p = []
    x1, y1 = screen_map()
    # Сюда дистанцию до точки записываем
    for g in points:
        distance2 = dist(x1, y1, points[g][0], points[g][1])
        p.append(int(distance2))
    return min(p)

def image_white_teleport(widht,hight):
# Координаты захвата, top верх лев координата, x - левая координата, остальные ширина и высота
    monitor = {"top": 0, "left": 0, "width": widht, "height": hight}
    # Захват экрана, по координатам
    base_screen = sct.grab(monitor)
    base_screen = cv2.cvtColor(np.array(base_screen), cv2.COLOR_BGR2HSV)
    cv2.rectangle(base_screen, (0, 0), (1360, 150), (0, 255, 0), -1)
    cv2.rectangle(base_screen, (0, 768), (1360, 600), (0, 255, 0), -1)
    karta_color_low = (0, 0, 255)  # Данный цвет это темный ненасыщенный красный, близкий к бордовому
    karta_color_high = (0, 0, 255)
    only_strelka_hsv = cv2.inRange(base_screen, karta_color_low, karta_color_high)
    moments = cv2.moments(only_strelka_hsv, 1)
    dM01 = moments['m01']
    dM10 = moments['m10']
    dArea = moments['m00']
    # будем реагировать только на те моменты,
    # которые содержать больше 100 пикселей
    x=0
    y=0
    if dArea > 0:
        x = int(dM10 / dArea)
        y = int(dM01 / dArea)
    return x, y
def image_teleport(widht,hight,subject):
    # Координаты захвата, top верх лев координата, x - левая координата, остальные ширина и высота
    monitor = {"top": 0, "left": 0, "width": widht, "height": hight}
    # Захват экрана, по координатам
    base_screen = sct.grab(monitor)
    base_screen_convert_gray = cv2.cvtColor(np.array(base_screen), cv2.COLOR_BGR2GRAY)
    # Поиск предмета
    loc_1 = np.where(cv2.matchTemplate(base_screen_convert_gray, subject, cv2.TM_CCOEFF_NORMED) >= 0.5)
    return (len(loc_1[0]))

#Все точки с именами и координатами(Тут они по порядку идут)
points = {
          'p0':[219,194],
          'p1':[223, 190],
          'p2':[236, 177],
          'p3':[255, 174],
          'p4':[270, 186],
          'p5':[279, 205],
          'p6':[285, 223],
          'p7':[282, 243],
          'p8':[309, 222],
          'p9':[320, 218],
          'p10': [337, 233],
          'p11': [363, 237],
          'p12': [387, 239],
          'p13': [382, 217],
          'p14': [408, 215],
          'p15': [400, 200],
          'p16': [401, 181],
          'p17': [421, 185],
          'p18': [358, 190],
          'p19': [321, 182],
          'p20': [310, 281],
          'p21': [286, 288],
          'p22': [250, 294],
          'p23': [233, 267],
          'p24': [219, 294],
          'p25': [212, 316],
          'p26': [208, 344],
          'p27': [202, 371],
          'p28': [224, 384],
          'p29': [303, 260]}
#Все имена точек по порядку, как выше в словаре
name_points = ['p0','p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9',
               'p10','p11','p12','p13','p14','p15','p16','p17','p18','p19','p20','p21','p22' ,'p23','p24','p25','p26', 'p27', 'p28','p29']

def run_points():
    win32api.keybd_event(0x4D, 0, 0, 0)
    time.sleep(.05)
    win32api.keybd_event(0x4D, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(1)
    min_dist = min_dist_for_point()
    while min_dist > 30:
        time.sleep(1)
        win32api.keybd_event(0x37, 0, 0, 0)
        time.sleep(.05)
        win32api.keybd_event(0x37, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(3)
        min_dist = min_dist_for_point()

    # Получаем короткий путь от графа и идем по нему( Далее он берет точки из словаря какие ему надо)
    example = derevo.short_way(name_points[p.index(min(p))])
    for i in example:
        x1, y1 = screen_map()
        distance2 = dist(x1, y1, points[i][0], points[i][1])
        define_corner_triangle(points[i][0], points[i][1])
        if i == 'p0':
            while distance2 > 1:
                win32api.keybd_event(0x57, 0, 0, 0)
                time.sleep(0.1)
                win32api.keybd_event(0x57, 0, win32con.KEYEVENTF_KEYUP, 0)
                define_corner_triangle(points[i][0], points[i][1])
                x1, y1 = screen_map()
                distance2 = dist(x1, y1, points[i][0], points[i][1])
        else:
            while distance2 > 10:
                win32api.keybd_event(0x57, 0, 0, 0)
                time.sleep(1)
                win32api.keybd_event(0x57, 0, win32con.KEYEVENTF_KEYUP, 0)
                define_corner_triangle(points[i][0], points[i][1])
                x1, y1 = screen_map()
                distance2 = dist(x1, y1, points[i][0], points[i][1])
            while distance2 > 3:
                win32api.keybd_event(0x57, 0, 0, 0)
                time.sleep(0.2)
                win32api.keybd_event(0x57, 0, win32con.KEYEVENTF_KEYUP, 0)
                define_corner_triangle(points[i][0], points[i][1])
                x1, y1 = screen_map()
                distance2 = dist(x1, y1, points[i][0], points[i][1])
    win32api.keybd_event(0x4D, 0, 0, 0)
    time.sleep(.05)
    win32api.keybd_event(0x4D, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(1)