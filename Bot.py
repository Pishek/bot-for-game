import MakeWindowActive
import time
import win32api
import win32con
import keyboard
import cv2
import function
from threading import Thread
from random import randint
import socket
from math import cos, sin, pi, exp
import json  # подключили библиотеку для работы с json
#Этот бот написан с помощью другого скрина, не IMagegrab и работает быстрее
#name_pc - проверка имя компьютера
with open('key.json', 'r', encoding='utf-8') as f:
    name_user = json.load(f)
# кнопка стоп
o = 'v'
#для здоровья переменная
hp_z = 0
hp_z_2 = 0
count_mob = 0
total = 0
total_2 = 0
first_skill = 0
second_skill = 0
third_skill = 0
skorka = 0
perevoplot = 0
#секундомер для свитка
def secundomer():
    sec = 0
    global skorka
    global first_skill
    global second_skill
    global perevoplot
    global third_skill
    while True:
        time.sleep(1)
        skorka += 1
        first_skill += 1
        second_skill += 1
        perevoplot += 1
        third_skill += 1
#Функция для движения мышкой
def mouse(widht,hight,drop,number_of_drop,number_skorka,number_f1,number_f2,number_2, krit,number_perevoplot,shag_x,shag_y, prodazha, ymin, ymax):
    global hp_z
    global hp_z_2
    global count_mob
    global total
    global total_2
    global first_skill
    global second_skill
    global third_skill
    global skorka
    global perevoplot
    while True:
        theta = 0.0
        step = 0.2
        loops = 6
        a = 10
        b = 5
        while theta < 2 * loops * pi:
            theta += step
            r = a + b * theta
            x = int(widht / 2 + (r * cos(theta))*1.5)
            y = int(hight / 2 + (r * sin(theta))*0.7)
            #time.sleep(0.1)
            #Счетчик для поворотов камерой на 90(поэтому два цикла бесконечных,  больше не знаю как)
            total = 0
            #индикатор крита
            indikator_krit = 1
            # Если тепнулся в город то выйти из цикла
            if hp_z == 1 or hp_z_2 == 1:  # Для выхода из цикла
                break
            #Проверка здоровья
            intens_zdorovia_hp, intens_zdorovia_hilka, intens_zdorovie_fight = function.zdorovie(widht, hight)
            #Тут переменную можно удалить, она не используется
            del intens_zdorovia_hilka
            #ТП в город
            if intens_zdorovia_hp < 55 and hp_z == 0:
                function.press(0x31)
                hp_z =1
            # Если начали бить, жать свиток(для данжей типо тп 3)
            if intens_zdorovie_fight < 55:
                function.press(0x37)
                # Чтоб экран загрузки прошел
                time.sleep(1.7)
                #Если есть хилки, то пьет 3 шт, если нет то дальше тепается просто
                intens_slota_hilki = function.screen_hilka(widht, hight)
                if intens_slota_hilki  > 35:
                    #после свитка выпить 4 хилки
                    for i in range(0, 4):
                        function.press(0x51)
                        time.sleep(0.35)
            #Делаем скрин области вокруг мыши, и берем оттуда результат совпадения(*)
            base_screen_convert_gray, loc = function.screen(x, y)
            #найти все объекты белого цвета
            ret, threshold1 = cv2.threshold(base_screen_convert_gray, 252, 255, cv2.THRESH_BINARY)
            #размываем и растягиваем с применением фильтра
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 5))
            closed = cv2.morphologyEx(threshold1, cv2.MORPH_CLOSE, kernel)
            #тут проверка, если совпадение то устанавливаем курсор на моба, len из (*)
            if len(loc[0]) != 0:
                x_2 = 0
                y_2 = 0
                # Находим координаты первого квадратика, который выше моба
                for pt in zip(*loc[::-1]):
                    x_2 = int(pt[0])
                    y_2 = int(pt[1])
                #Задаем интенсивность пикселя, координаты которого выше(n/m местами менять тут над)
                intensivnost_first_cub = base_screen_convert_gray[y_2 + 1, x_2 + 1]
                #зададим интенсивность пикселя, на нике моба, (процесс наводки через стену)
                #Обычно тут вылезала ошибка с IndexErrror попробуем сделать исключение для этой ошибки
                try:
                    intensivnost_name_of_mob = closed[int(y_2 + 1 + ((hight - 768)*0.0555)) + 18, x_2 + 1 + 10]
                except IndexError:
                    #типо если эта ошибка(то будем считать что ника моба нет)
                    intensivnost_name_of_mob = 200
                #Условие яркости квадрата( у зеленого 154, взял 145 на всякий)
                if intensivnost_first_cub > 145 and intensivnost_name_of_mob >= 240:
                    time.sleep(0.01)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
                    time.sleep(0.08)
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
                    time.sleep(0.1)
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
                    time.sleep(0.1)
                    #Далее делаем скрин нижней таблички хп моба, если она есть, то цикл продолжает делать скрины
                    res_of_screen_2, int_niz_hp = function.screen_2(widht, hight)
                    total_2 = 0
                    while res_of_screen_2 != 0:
                        # Проверка здоровья
                        intens_zdorovia_hp_2, intens_zdorovia_hilka, intens_zdorovie_fight = function.zdorovie(widht, hight)
                        #Тп в город
                        if intens_zdorovia_hp_2 < 55 and hp_z_2 == 0:
                            function.press(0x31)
                            hp_z_2 = 1
                        # тп свитком, если бьют ( для данжей)
                        if intens_zdorovie_fight < 55:
                            function.press(0x37)
                            # Чтоб экран загрузки прошел
                            time.sleep(1.7)
                            intens_slota_hilki = function.screen_hilka(widht, hight)
                            if intens_slota_hilki > 35:
                                # после свитка выпить 4 хилки
                                for i in range(0, 4):
                                    function.press(0x51)
                                    time.sleep(0.3)
                            # после свитка выпить 4 хилки
                            for i in range(0, 4):
                                function.press(0x51)
                                time.sleep(0.3)
                        #Для хилки условие
                        if intens_zdorovia_hilka < 55:
                            function.press(0x51)
                        # типо крит на 2
                        if krit == 1 and indikator_krit == 1 and int_niz_hp < 140:
                            random_krit = 1
                            if random_krit == randint(0, 1):
                                function.press(0x32)
                                time.sleep(1)
                            indikator_krit = 0
                        # увеличваем total на 1 за каждый цикл
                        total_2 += 1
                        # Если таргет больше 400(это количество циклов выполненых), то выходим из цикла
                        if total_2 >= 400:
                            # Поворот на 90 примерно
                            win32api.keybd_event(0x44, 0, 0, 0)
                            time.sleep(1)
                            win32api.keybd_event(0x44, 0, win32con.KEYEVENTF_KEYUP, 0)
                            time.sleep(0.3)
                            total_2 = 0
                            #Если таргет долго держиться, то проверка, мб из-за перевеса
                            if prodazha == 1:
                                function.podbor_dropa(widht, hight)
                            break
                        another_res_of_screen_2, int_niz_hp = function.screen_2(widht, hight)
                        if another_res_of_screen_2 == 0:
                            if drop == 1:
                                function.drop(number_of_drop) #подбор дропа
                                if prodazha == 1:
                                    function.podbor_dropa(widht, hight)
                            # Поворот на 90 примерн
                            win32api.keybd_event(0x44, 0, 0, 0)
                            time.sleep(1)
                            win32api.keybd_event(0x44, 0, win32con.KEYEVENTF_KEYUP, 0)
                            count_mob += 1
                            #Индикатор крита снова 1
                            indikator_krit = 1
                            #Тайминг для скорки
                            if skorka >= number_skorka:
                                function.press(0x77)
                                time.sleep(2)
                                skorka = 0
                            #Тайминг  для первого скила
                            #типо если мобов n убивает, то жмет скил на F1
                            if first_skill >= number_f1:
                                function.press(0x70)
                                time.sleep(2)
                                first_skill = 0
                            # Тайминг  для второго скила
                            # типо если мобов n убивает, то жмет скил на F2
                            if second_skill >= number_f2:
                                function.press(0x71)
                                time.sleep(3)
                                second_skill = 0
                            # Тайминг  для третьего скила
                            # типо если мобов n убивает, то жмет скил на F3
                            if third_skill >= number_2:
                                function.press(0x72)
                                time.sleep(3)
                                third_skill = 0
                            #Перевоплот на F7(каждые 40 мобов перевоплот)
                            if perevoplot >= number_perevoplot:
                                function.press(0x76)
                                time.sleep(2)
                                perevoplot = 0
                                #Юзать хлеб на кнопку F6
                                for i in range(0, 3):
                                    function.press(0x75)
                                    time.sleep(0.15)
                            print('Убито:', count_mob , 'мобов')
                            #Если моб убит, то обнуляем счетчик поворотов(вдргу там еще мобы есть)
                            total = 0
                            break
            #Установка курсора
            win32api.SetCursorPos((x, y))
            if keyboard.is_pressed(o):
                break
            #Если тепнулся в город то выйти из цикла
            if keyboard.is_pressed(o) or  hp_z == 1 or hp_z_2 == 1:  # Для выхода из цикла
                break
                # Счетчик бесполезных поворотов, если просто крутим камерой и никого нет, то есть 2 раза, т.е на 180, то свиток тп
        total += 1
        if total == 2:
            function.press(0x37)
            # Чтоб экрна загрузки прошел
            time.sleep(2.5)
            total = 0
            break
        # Поворот на 90 примерн
        win32api.keybd_event(0x44, 0, 0, 0)
        time.sleep(1)
        win32api.keybd_event(0x44, 0, win32con.KEYEVENTF_KEYUP, 0)
        return (hp_z, hp_z_2)
def start():
    #Проверка id_pk
    name_pc = socket.gethostname()
    if name_user == name_pc:
        print('Проверка пк пройдена:\nЗапускаю бота')
        # Делаем активным окно R2(СЛОЖНА Н1АХУЙ)
        MakeWindowActive.get_window_info()
        time.sleep(1)
        inputfile = "log.txt"
        with open(inputfile) as file:
            my_list = [row.strip().split()[1] for row in file]
        # создаем второй поток для таймера(чтоб одновременно работал для свитков тп) (Daemon = True, чтобы поток убивался с выходом в мейен)
        th_1 = Thread(target=secundomer, daemon=True)
        th_1.start()
        while True:
            hpp1, hpp2 = mouse(int(my_list[0]),int(my_list[1]),int(my_list[2]),int(my_list[3]),int(my_list[4]),int(my_list[5]),int(my_list[6]),int(my_list[7]),int(my_list[8]), int(my_list[9]), int(my_list[10]), int(my_list[11]), int(my_list[12]), int(my_list[13]), int(my_list[14]))
            if keyboard.is_pressed(o) or hpp1 == 1 or hpp2 == 1:
                break
    else:
        print('Нет лецензии')
#Запускаем цикл
start()
input()