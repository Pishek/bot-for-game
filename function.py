import numpy as np
import cv2
import mss.tools
import time
import win32api
import win32con
import keyboard
import feature_detection
# кнопка стоп
o = 'v'
#Тут все функции для бота
#Загружаем фрагменты
#Переменная для руны:
inputfile = "log.txt"
with open(inputfile) as file:
    my_list_function = [row.strip().split()[1] for row in file]
# Полоска хп
hp = cv2.imread('image/hp.png', 0)
#Для продажи
peregruz = cv2.imread('image/peregruz.png', 0)
polon = cv2.imread('image/polon.png', 0)
ataka = cv2.imread('image/ataka.png', 0)
oruzh = cv2.imread('image/oruzh.png', 0)
BCHD = cv2.imread('image/BCHD.png', 0)
npc_or = cv2.imread('image/npc_or.png', 0)
sell = cv2.imread('image/sell.png', 0)
knopka_prodat = cv2.imread('image/knopka_prodat.png', 0)
danzh_BCHD2 = cv2.imread('image/danzh_BCHD2.png', 0)

#Список предметов для продажи
kolchuzh_dosp = cv2.imread('image/kolchuzh_dosp.png', 0)
plast_dosp = cv2.imread('image/plast_dosp.png', 0)
kniga_skorka = cv2.imread('image/kniga_skorka.png', 0)
kniga_isc = cv2.imread('image/kniga_isc.png', 0)
mineral = cv2.imread('image/mineral.png', 0)
BD = cv2.imread('image/BD.png', 0)
sapfir = cv2.imread('image/sapfir.png', 0)
moneti = cv2.imread('image/moneti.png', 0)
metal = cv2.imread('image/metal.png', 0)
dosp_25k = cv2.imread('image/dosp_25k.png', 0)
chast_dosp = cv2.imread('image/chast_dosp.png', 0)
ametist = cv2.imread('image/ametist.png', 0)

#Делаем скрин области вокруг мыши
with mss.mss()  as sct:
    def screen(x, y):
        # Координаты захвата, top верх лев координата, x - левая координата, остальные ширина и высота
        monitor =  {"top": y - 210 , "left":  x - 50, "width":  85, "height":  200}
        # Захват экрана, по координатам
        base_screen = sct.grab(monitor)
        # переводим в серое изображение
        base_screen_convert_gray = cv2.cvtColor(np.array(base_screen), cv2.COLOR_BGR2GRAY)
        # Поиск предмета
        res = cv2.matchTemplate(base_screen_convert_gray, hp, cv2.TM_CCOEFF_NORMED)
        return (base_screen_convert_gray, np.where(res >= 0.55))

    def screen_2(widht, hight):
        # Придется еще один скрин сделать нижней таблички, дабы моб может улететь куда нибудь
        monitor =  {"top":int(hight - 170), "left":  int((widht - 230)/2) , "width":  230, "height":  27}
        base_screen_2 = sct.grab(monitor)
        # переводим в серое изображение
        base_screen_convert_gray_2 = cv2.cvtColor(np.array(base_screen_2), cv2.COLOR_BGR2GRAY)
        # Поиск предмета
        loc_2 = np.where(cv2.matchTemplate(base_screen_convert_gray_2, hp, cv2.TM_CCOEFF_NORMED) >= 0.5)
        return (len(loc_2[0]), base_screen_convert_gray_2[15, 125])

    # Функция для телепортирования в город
    def zdorovie(widht, hight):
        monitor = {"top": int(hight - 52), "left": int((widht - 160)/2), "width": 162, "height": 20}
        base_screen_3 = sct.grab(monitor)
        # переводим в серое изображение
        base_screen_convert_gray_3 = cv2.cvtColor(np.array(base_screen_3), cv2.COLOR_BGR2GRAY)
        intensivnost_name_of_mob = base_screen_convert_gray_3[9, 45]  #эти координаты просто в пэинте искал
        #Для хилки
        intensivnost_hp_persa = base_screen_convert_gray_3[9,120]
        #Для тп на свитке( если начали бить)
        intensivnost_hp_fight = base_screen_convert_gray_3[5, 83]
        return (intensivnost_name_of_mob, intensivnost_hp_persa, intensivnost_hp_fight)

    def screen_hilka(widht, hight):
        monitor = {"top": int(hight-53), "left": int((widht - 160)/2)-75, "width": 45, "height": 40}
        base_screen_3 = sct.grab(monitor)
        # переводим в серое изображение
        base_screen_convert_gray_3 = cv2.cvtColor(np.array(base_screen_3), cv2.COLOR_BGR2GRAY)
        intensivnost_name_of_mob = base_screen_convert_gray_3[15, 40]  #эти координаты просто в пэинте искал (30  если пустой слот)
        return (intensivnost_name_of_mob)

def drop(x):
    for i in range(0, x):
        time.sleep(0.7)
        # Поднимает дроп 1
        win32api.keybd_event(0x45, 0, 0, 0)
        time.sleep(.05)
        win32api.keybd_event(0x45, 0, win32con.KEYEVENTF_KEYUP, 0)

def press(x):
    win32api.keybd_event(x, 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(x, 0, win32con.KEYEVENTF_KEYUP, 0)

#Подбор дропа
#-------------------------------------------------------------------------------------------------------------------
def screen_chat(hight):
    # Координаты захвата, top верх лев координата, x - левая координата, остальные ширина и высота
    monitor = {"top": hight - 218, "left": 0, "width": 390, "height": 110}
    # Захват экрана, по координатам
    base_screen = sct.grab(monitor)
    base_screen_convert_gray = cv2.cvtColor(np.array(base_screen), cv2.COLOR_BGR2GRAY)
    # Поиск предмета
    loc_1 = np.where(cv2.matchTemplate(base_screen_convert_gray, peregruz, cv2.TM_CCOEFF_NORMED) >= 0.8)
    loc_2 = np.where(cv2.matchTemplate(base_screen_convert_gray, polon, cv2.TM_CCOEFF_NORMED) >= 0.8)
    loc_3 = np.where(cv2.matchTemplate(base_screen_convert_gray, ataka, cv2.TM_CCOEFF_NORMED) >= 0.8)
    return (len(loc_1[0]), len(loc_2[0]), len(loc_3[0]))

def screen_menu_tp(subject):
    # Координаты захвата, top верх лев координата, x - левая координата, остальные ширина и высота
    monitor = {"top": 0, "left": 0, "width": 250, "height": 140}
    # Захват экрана, по координатам
    base_screen = sct.grab(monitor)
    base_screen_convert_gray = cv2.cvtColor(np.array(base_screen), cv2.COLOR_BGR2GRAY)
    # Поиск предмета
    loc_1 = np.where(cv2.matchTemplate(base_screen_convert_gray, subject, cv2.TM_CCOEFF_NORMED) >= 0.8)
    # Найдем координаты
    x_r = 0
    y_r = 0
    for pt in zip(*loc_1[::-1]):
        x_r = int(pt[0])
        y_r = int(pt[1])
    return (len(loc_1[0]), x_r, y_r)


def screen_full(widht, hight):
    # Координаты захвата, top верх лев координата, x - левая координата, остальные ширина и высота
    monitor = {"top": 0, "left": 0, "width": widht-5, "height": hight-5}
    # Захват экрана, по координатам
    base_screen = sct.grab(monitor)
    base_screen_convert_gray = cv2.cvtColor(np.array(base_screen), cv2.COLOR_BGR2GRAY)
    # Поиск предмета
    loc_1 = np.where(cv2.matchTemplate(base_screen_convert_gray, npc_or, cv2.TM_CCOEFF_NORMED) >= 0.6)
    # Найдем координаты
    x_r = 0
    y_r = 0
    for pt in zip(*loc_1[::-1]):
        x_r = int(pt[0])
        y_r = int(pt[1])
    return (len(loc_1[0]), x_r, y_r)


def screen_menu_or():
    # Координаты захвата, top верх лев координата, x - левая координата, остальные ширина и высота
    monitor = {"top": 0, "left": 0, "width": 250, "height": 270}
    # Захват экрана, по координатам
    base_screen = sct.grab(monitor)
    base_screen_convert_gray = cv2.cvtColor(np.array(base_screen), cv2.COLOR_BGR2GRAY)
    # Поиск предмета
    loc_1 = np.where(cv2.matchTemplate(base_screen_convert_gray, sell, cv2.TM_CCOEFF_NORMED) >= 0.8)
    # Найдем координаты
    x_r = 0
    y_r = 0
    for pt in zip(*loc_1[::-1]):
        x_r = int(pt[0])
        y_r = int(pt[1])
    return (len(loc_1[0]), x_r, y_r)


def screen_spisok_or():
    # Координаты захвата, top верх лев координата, x - левая координата, остальные ширина и высота
    monitor = {"top": 0, "left": 0, "width": 325, "height": 300}
    # Захват экрана, по координатам
    base_screen = sct.grab(monitor)
    base_screen_convert_gray = cv2.cvtColor(np.array(base_screen), cv2.COLOR_BGR2GRAY)
    return base_screen_convert_gray

def search_subject_or(base_screen, subject):
    # Поиск предмета
    loc_1 = np.where(cv2.matchTemplate(base_screen, subject, cv2.TM_CCOEFF_NORMED) >= 0.9)
    # Найдем координаты
    x_r = 0
    y_r = 0
    for pt in zip(*loc_1[::-1]):
        x_r = int(pt[0])
        y_r = int(pt[1])
    return (len(loc_1[0]), x_r, y_r)



def select_subject(screen_spisok, subject, on):
    search_subject, x_subject, y_subject = search_subject_or(screen_spisok, subject)
    print('совпадение ПРЕДМЕТА', search_subject)
    scroll = 1
    while search_subject != 0:
        if on == 1:
            win32api.SetCursorPos((0, 0))
            win32api.SetCursorPos((x_subject + 20, y_subject + 20))
            time.sleep(0.5)
            #Зажмем шифт
            win32api.keybd_event(0x10, 0, 0, 0)
            time.sleep(0.5)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
            time.sleep(0.08)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)
            time.sleep(1)
            win32api.keybd_event(0x10, 0, win32con.KEYEVENTF_KEYUP, 0)
            win32api.SetCursorPos((0, 0))
            time.sleep(0.5)
        else:
            win32api.SetCursorPos((0, 0))
            win32api.SetCursorPos((x_subject + 20, y_subject + 20))
            time.sleep(0.5)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
            time.sleep(0.08)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)
            win32api.SetCursorPos((0, 0))
            time.sleep(0.5)
        if keyboard.is_pressed(o):
            break
        # рисуем квадрат на месте проданого предмета
        cv2.rectangle(screen_spisok, (x_subject, y_subject), ((x_subject + 40), (y_subject + 40)), (0, 255, 0), -1)
        # дальше ищем
        search_subject, x_subject, y_subject = search_subject_or(screen_spisok, subject)
    print('В первом листе ничего не найдено')

def search_oruzheinik(npc, x_n, y_n, widht, hight):
    while npc == 0:
        print('не нашел оружейника')
        win32api.keybd_event(0x44, 0, 0, 0)
        time.sleep(1)
        win32api.keybd_event(0x44, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(1)
        npc, x_n, y_n = screen_full(widht, hight)
        if keyboard.is_pressed(o):
            break
    if npc != 0:
        win32api.SetCursorPos((x_n + 40, y_n + 70))
        time.sleep(1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        time.sleep(0.08)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        time.sleep(1.5)
        menu_or, x_s, y_s = screen_menu_or()
        while menu_or == 0:
            win32api.keybd_event(0x44, 0, 0, 0)
            time.sleep(1)
            win32api.keybd_event(0x44, 0, win32con.KEYEVENTF_KEYUP, 0)
            npc_2, x_n, y_n = screen_full(widht, hight)
            time.sleep(1)
            if npc_2 != 0:
                win32api.SetCursorPos((x_n + 40, y_n + 70))
                time.sleep(1)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
                time.sleep(0.08)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
                time.sleep(1.5)
            menu_or, x_s, y_s = screen_menu_or()
            if keyboard.is_pressed(o):
                break
        if menu_or != 0:
            time.sleep(1)
            win32api.SetCursorPos((x_s + 20, y_s + 5))
            time.sleep(0.5)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
            time.sleep(0.08)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
            time.sleep(1)
            win32api.SetCursorPos((0, 0))
            time.sleep(2)

def screen_knopka_prodat():
    # Координаты захвата, top верх лев координата, x - левая координата, остальные ширина и высота
    monitor = {"top": 0, "left": 0, "width": 350, "height": 520}
    # Захват экрана, по координатам
    base_screen = sct.grab(monitor)
    base_screen_convert_gray = cv2.cvtColor(np.array(base_screen), cv2.COLOR_BGR2GRAY)
    # Поиск предмета
    loc_1 = np.where(cv2.matchTemplate(base_screen_convert_gray, knopka_prodat, cv2.TM_CCOEFF_NORMED) >= 0.8)
    # Найдем координаты
    x_r = 0
    y_r = 0
    for pt in zip(*loc_1[::-1]):
        x_r = int(pt[0])
        y_r = int(pt[1])
    return (x_r, y_r)


def back_danzh(widht, hight):
    # Обратно в данж
    # Условие для кольца
    if int(my_list_function[15]) == 0:
        # Жмем 7
        win32api.keybd_event(0x37, 0, 0, 0)
        time.sleep(0.05)
        win32api.keybd_event(0x37, 0, win32con.KEYEVENTF_KEYUP, 0)
    else:
        # Нажмем F5(кц_тп/руна)
        win32api.keybd_event(0x74, 0, 0, 0)
        time.sleep(0.05)
        win32api.keybd_event(0x74, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(1)
    danzh, x_d, y_d = screen_menu_tp(BCHD)
    time.sleep(0.5)
    while danzh == 0:
        if int(my_list_function[15]) == 0:
            # Жмем 7
            win32api.keybd_event(0x37, 0, 0, 0)
            time.sleep(0.05)
            win32api.keybd_event(0x37, 0, win32con.KEYEVENTF_KEYUP, 0)
        else:
            # Нажмем F5(кц_тп/руна)
            win32api.keybd_event(0x74, 0, 0, 0)
            time.sleep(0.05)
            win32api.keybd_event(0x74, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(1)
        danzh, x_d, y_d = screen_menu_tp(BCHD)
        time.sleep(0.5)
    win32api.SetCursorPos((x_d + 40, y_d + 5))
    time.sleep(1.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.08)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.08)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    time.sleep(3)
    # ТП на второй ур
    click_centr(widht, hight)
    time.sleep(3)
    # клик левой кнопкой мышки
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.08)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.08)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    time.sleep(0.08)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.08)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    time.sleep(1.5)


def sell_all(subject, on, widht, hight):
    # Скрин всего окна и поиск оружейника, нажать на него, открыть меню и нажать кнопку продать
    npc, x_n, y_n = screen_full(widht, hight)
    search_oruzheinik(npc, x_n, y_n, widht, hight)
    # ПРОДАЕМ ПРЕДМЕТЫ
    screen_spisok = screen_spisok_or()
    select_subject(screen_spisok, subject, on) #subject то что продать скрин его
    # как все выбрал жмем кнопку продать
    x_knopka, y_knopka = screen_knopka_prodat()
    win32api.SetCursorPos((x_knopka + 30, y_knopka + 10))
    time.sleep(1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.08)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    time.sleep(1)


def click_centr(widht, hight):
    win32api.SetCursorPos((int(widht/2), int(hight/2+50)))

def screen_full_for_danzh(widht, hight, place):
    time.sleep(1)
    # Координаты захвата, top верх лев координата, x - левая координата, остальные ширина и высота
    monitor = {"top": 0, "left": 0, "width": widht-5, "height": hight-5}
    # Захват экрана, по координатам
    base_screen = sct.grab(monitor)
    base_screen_convert_gray = cv2.cvtColor(np.array(base_screen), cv2.COLOR_BGR2GRAY)
    # Поиск предмета
    loc_1 = np.where(cv2.matchTemplate(base_screen_convert_gray, place, cv2.TM_CCOEFF_NORMED) >= 0.7)
    return len(loc_1[0])

def podbor_dropa(widht, hight):
    while True:
        weight1, weight2, weight3 = screen_chat(hight)
        if weight1 != 0 or weight2 != 0 or weight3 != 0:
            time.sleep(1.5)
            # Нажмем F5(кц_тп/руна)
            win32api.keybd_event(0x74, 0, 0, 0)
            time.sleep(0.05)
            win32api.keybd_event(0x74, 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(1)
            #Условие для кольца
            if int(my_list_function[15]) == 0:
                # Жмем 7
                win32api.keybd_event(0x37, 0, 0, 0)
                time.sleep(0.05)
                win32api.keybd_event(0x37, 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(1)
            # выбрать и нажать на оружейника в меню кц тп
            oruzheinik, x_r, y_r = screen_menu_tp(oruzh)
            time.sleep(0.5)
            if oruzheinik != 0:
                win32api.SetCursorPos((x_r + 40, y_r + 5))
                time.sleep(1.5)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
                time.sleep(0.08)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
                time.sleep(0.05)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
                time.sleep(0.08)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
                time.sleep(11)

                # Продаем предмет #1
                sell_all(plast_dosp, 0, widht, hight)

                # Продаем предмет #2
                sell_all(kolchuzh_dosp, 0, widht, hight)

                # Продаем предмет #3
                sell_all(BD, 1, widht, hight)

                # Продаем предмет #4
                sell_all(mineral, 1, widht, hight)

                # Продаем предмет #5
                sell_all(moneti, 1, widht, hight)

                # Продаем предмет #4
                sell_all(kniga_skorka, 0, widht, hight)
                sell_all(kniga_skorka, 0, widht, hight)

                # Продаем предмет #5
                sell_all(kniga_isc, 0, widht, hight)
                sell_all(kniga_isc, 0, widht, hight)
                sell_all(kniga_isc, 0, widht, hight)

                # Продаем предмет #6
                sell_all(ametist, 1, widht, hight)

                # Продаем предмет #7
                sell_all(sapfir, 1, widht, hight)

                # Продаем предмет #8
                sell_all(metal, 1, widht, hight)

                # Продаем предмет #9
                sell_all(chast_dosp, 1, widht, hight)

                # Продаем предмет #10
                sell_all(dosp_25k, 0, widht, hight)
                sell_all(dosp_25k, 0, widht, hight)
                #Тп обратно в данж
                back_danzh(widht, hight)
                proverka_danzha = screen_full_for_danzh(widht, hight, danzh_BCHD2)
                while proverka_danzha == 0:
                    # Поворот на 90 примерн
                    win32api.keybd_event(0x44, 0, 0, 0)
                    time.sleep(1)
                    win32api.keybd_event(0x44, 0, win32con.KEYEVENTF_KEYUP, 0)
                    time.sleep(1)
                    back_danzh(widht, hight)
                    proverka_danzha = screen_full_for_danzh(widht, hight, danzh_BCHD2)
                # Условие для кольца
                if int(my_list_function[15]) == 0:
                    # Нажмем F4(кц)
                    win32api.keybd_event(0x73, 0, 0, 0)
                    time.sleep(0.05)
                    win32api.keybd_event(0x73, 0, win32con.KEYEVENTF_KEYUP, 0)
                time.sleep(1)
                # Жмем 7
                win32api.keybd_event(0x37, 0, 0, 0)
                time.sleep(0.05)
                win32api.keybd_event(0x37, 0, win32con.KEYEVENTF_KEYUP, 0)
                time.sleep(1)
                #После того как тп на 2 ур, идет на 3 ур)
                inputfile_2 = "setting.txt"
                with open(inputfile_2) as file:
                    my_list_2 = [row.strip().split()[1] for row in file]
                if int(my_list_2[0]) == 1:
                    feature_detection.run_points()
                    x_m, y_m = feature_detection.image_white_teleport(int(my_list_2[1]), int(my_list_2[2]))
                    win32api.SetCursorPos((x_m, y_m))
                    time.sleep(1)
                    while feature_detection.image_teleport(int(my_list_2[1]), int(my_list_2[2]), feature_detection.temnie) == 0:
                        # Поворот на 90 примерн
                        win32api.keybd_event(0x44, 0, 0, 0)
                        time.sleep(1)
                        win32api.keybd_event(0x44, 0, win32con.KEYEVENTF_KEYUP, 0)
                        x_m, y_m = feature_detection.image_white_teleport(int(my_list_2[1]), int(my_list_2[2]))
                        win32api.SetCursorPos((x_m, y_m))
                        time.sleep(1)
                        feature_detection.image_teleport(int(my_list_2[1]), int(my_list_2[2]), feature_detection.temnie)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
                    time.sleep(0.08)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
                    time.sleep(3.5)
                    while feature_detection.image_teleport(int(my_list_2[1]), int(my_list_2[2]), feature_detection.temnie_slovo) == 0:
                        # Поворот на 90 примерн
                        win32api.keybd_event(0x44, 0, 0, 0)
                        time.sleep(1)
                        win32api.keybd_event(0x44, 0, win32con.KEYEVENTF_KEYUP, 0)
                        x_m, y_m = feature_detection.image_white_teleport(int(my_list_2[1]), int(my_list_2[2]))
                        win32api.SetCursorPos((x_m, y_m))
                        time.sleep(1.5)
                        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
                        time.sleep(0.08)
                        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
                        time.sleep(3)
                        feature_detection.image_teleport(int(my_list_2[1]), int(my_list_2[2]), feature_detection.temnie_slovo)
                time.sleep(1)
                # Жмем 7
                win32api.keybd_event(0x37, 0, 0, 0)
                time.sleep(0.05)
                win32api.keybd_event(0x37, 0, win32con.KEYEVENTF_KEYUP, 0)
                print('Вернулся на место фарма')
                break
        else:
            break
        if keyboard.is_pressed(o):
            break