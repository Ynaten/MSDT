import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Main(QWidget):
    def __init__(self):
        super().__init__()
        # Инициализация игрового цикла
        self.timer = QBasicTimer()

        # Инициализация 2 танков
        self.coords2 = QLabel(self)
        self.coords = QLabel(self)

        # Инициализая пуль + переменных танка
        self.move = str()
        self.move2 = str()
        self.put = int()
        self.put2 = int()
        self.bullets = list()
        self.life = list()
        self.game_over = 0

        # Инициализация карты
        self.map = list()
        self.bricks = list()
        self.cant = list()
        self.listv = list()

        self.initui()

    def initui(self):
        self.setGeometry(800, 400, 800, 800)
        self.setWindowTitle('8 BIT TANKS')

        # Создание фона
        label = QLabel(self)
        pixmap = QPixmap('assets/background.jpg')
        label.setPixmap(pixmap)

        # Размер экрана | Не регулировать, т.к карта 10x10 для 64x64!
        self.resize(640, 640)

        # Создание танка номер 1
        self.coords2 = QLabel(self)
        self.coords2.resize(48, 48)
        frist = "assets/64.png"
        pixmap = QPixmap(frist)
        self.coords2.setPixmap(pixmap)
        self.coords2.move(296, 590)

        # Создание танка номер 2
        self.coords = QLabel(self)
        self.coords.resize(48, 48)
        frist = "assets/64_d.png"
        pixmap = QPixmap(frist)
        self.coords.setPixmap(pixmap)
        self.coords.move(296, 10)

        # Направление движения танка 1
        self.move = "W"

        # Инициализация жизни пулей
        self.bullets = []
        self.life = []
        self.game_over = 0

        # Создаем игровой цикл
        self.timer.start(12, self)

        # Создание карты
        self.map = []
        self.bricks = []
        self.cant = []
        self.listv = []
        self.create_map()

        # Активное нажатие танка 1
        self.put = 0

        # Направление движения танка 2
        self.move2 = "Down"

        # Активное нажатие танка 2
        self.put2 = 0

        self.show()

    def create_map(self):
        # Импорт карты из TXT
        with open("assets/map.txt") as D:
            a = D.read()
            a = a.split("\n")
            for i in a:
                self.map.append(i)
        # Создание карты, обработка данных
        for i in range(10):
            for j in range(10):
                if self.map[i][j] == " ":
                    pass
                elif self.map[i][j] == "T":
                    frist = "assets/brick_comp.png"
                    pixmap = QPixmap(frist)
                    self.bricks.append(QLabel(self))
                    self.bricks[-1].resize(64, 64)
                    self.bricks[-1].setPixmap(pixmap)
                    self.bricks[-1].move(j * 64, i * 64)
                elif self.map[i][j] == "X":
                    frist = "assets/cant_lomatsa.png"
                    pixmap = QPixmap(frist)
                    self.cant.append(QLabel(self))
                    self.cant[-1].resize(64, 64)
                    self.cant[-1].setPixmap(pixmap)
                    self.cant[-1].move(j * 64, i * 64)
                elif self.map[i][j] == "Z":
                    frist = "assets/listva.png"
                    pixmap = QPixmap(frist)
                    self.listv.append(QLabel(self))
                    self.listv[-1].resize(64, 64)
                    self.listv[-1].setPixmap(pixmap)
                    self.listv[-1].move(j * 64, i * 64)

    def keyPressEvent(self, event):
        # Получение информации о нажатой клавиши.
        # Выбор нужного направления

        if event.key() == Qt.Key_D:
            self.move = "D"
            self.put = 1
        elif event.key() == Qt.Key_A:
            self.move = "A"
            self.put = 1
        elif event.key() == Qt.Key_W:
            self.move = "W"
            self.put = 1
        elif event.key() == Qt.Key_S:
            self.move = "S"
            self.put = 1

        if event.key() == Qt.Key_Right:
            self.move2 = "Right"
            self.put2 = 1
        elif event.key() == Qt.Key_Left:
            self.move2 = "Left"
            self.put2 = 1
        elif event.key() == Qt.Key_Up:
            self.move2 = "Up"
            self.put2 = 1
        elif event.key() == Qt.Key_Down:
            self.move2 = "Down"
            self.put2 = 1

        # Информация о начале выпуска пуль
        if event.key() == Qt.Key_Space:
                frist = "assets/16x16bullet.png"
                pixmap = QPixmap(frist)
                self.bullets.append(QLabel(self))
                self.bullets[-1].resize(16, 16)
                self.bullets[-1].setPixmap(pixmap)
                self.bullets[-1].show()
                if self.move == "W":
                    self.life.append([self.move, 0])
                    self.bullets[-1].move(self.coords2.x() + 16,
                                          self.coords2.y() - 3)
                elif self.move == "A":
                    self.life.append([self.move, 0])
                    self.bullets[-1].move(self.coords2.x() - 3,
                                          self.coords2.y() + 16)

                elif self.move == "S":
                    self.life.append([self.move, 0])
                    self.bullets[-1].move(self.coords2.x() + 16,
                                          self.coords2.y() + 48)
                elif self.move == "D":
                    self.life.append([self.move, 0])
                    self.bullets[-1].move(self.coords2.x() + 48,
                                          self.coords2.y() + 16)

    def keyReleaseEvent(self, event):
        # Информация о отжатии клавиши, нужна,
        # Чтобы перемещать танки без всяких задержек
        key = event.key()
        if key == Qt.Key_D and not event.isAutoRepeat() and self.move == "D":
            self.put = 0
        if key == Qt.Key_A and not event.isAutoRepeat() and self.move == "A":
            self.put = 0
        if key == Qt.Key_S and not event.isAutoRepeat() and self.move == "S":
            self.put = 0
        if key == Qt.Key_W and not event.isAutoRepeat() and self.move == "W":
            self.put = 0

        if key == Qt.Key_Right and not event.isAutoRepeat() and self.move2 == "Right":
            self.put2 = 0
        if key == Qt.Key_Left and not event.isAutoRepeat() and self.move2 == "Left":
            self.put2 = 0
        if key == Qt.Key_Down and not event.isAutoRepeat() and self.move2 == "Down":
            self.put2 = 0
        if key == Qt.Key_Up and not event.isAutoRepeat() and self.move2 == "Up":
            self.put2 = 0

    def probitie(self, x, y):
        # Импорт данных о танках
        tank_x, tank_y = self.coords2.x(), self.coords2.y()
        tank2_x, tank2_y = self.coords.x(), self.coords.y()
        # Проверка на попадание пули
        if tank_x <= x <= tank_x + 48 and tank_y <= y <= tank_y + 48:
            return 1
        elif tank2_x <= x <= tank2_x + 48 and tank2_y <= y <= tank2_y + 48:
            return 2
        else:
            return False

    def move_bullet(self, a, b):
        # Функция о движении пуль.
        bullet = a
        life = b
        # Импортируется направление пули, его корды.
        # Далее пуля двигается и делается проверка на попадание
        if life[0] == "W":
            bullet.move(bullet.x(), bullet.y() - 5)
            a = self.probitie(bullet.x(), bullet.y())
        elif life[0] == "A":
            bullet.move(bullet.x() - 5, bullet.y())
            a = self.probitie(bullet.x(), bullet.y())
        elif life[0] == "S":
            bullet.move(bullet.x(), bullet.y() + 5)
            a = self.probitie(bullet.x(), bullet.y())
        elif life[0] == "D":
            bullet.move(bullet.x() + 5, bullet.y())
            a = self.probitie(bullet.x(), bullet.y())
        if life[0] == "Up":
            bullet.move(bullet.x(), bullet.y() - 5)
            a = self.probitie(bullet.x(), bullet.y())
        elif life[0] == "Left":
            bullet.move(bullet.x() - 5, bullet.y())
            a = self.probitie(bullet.x(), bullet.y())
        elif life[0] == "Down":
            bullet.move(bullet.x(), bullet.y() + 5)
            a = self.probitie(bullet.x(), bullet.y())
        elif life[0] == "Right":
            bullet.move(bullet.x() + 5, bullet.y())
            a = self.probitie(bullet.x(), bullet.y())
        if a is not False:
            self.timer.stop()
            print("Конец игры! Победил", end="")
            if life[0] in "WASD":
                print(" игрок, который использует WASD для управления")
            else:
                print(" игрок, который использует Стрелочки для управления")
            self.game_over = 1

    def mousePressEvent(self, event):
            # Создание пули, которую выпускает игрок со Стрелочек
            frist = "assets/16x16bullet.png"
            pixmap = QPixmap(frist)
            self.bullets.append(QLabel(self))
            self.bullets[-1].resize(16, 16)
            self.bullets[-1].setPixmap(pixmap)
            self.bullets[-1].show()
            if self.move2 == "Up":
                self.life.append([self.move2, 0])
                a = self.coords.x() + 16
                b = self.coords.y() - 3
                self.bullets[-1].move(a, b)
            elif self.move2 == "Left":
                self.life.append([self.move2, 0])
                a = self.coords.x() - 3
                b = self.coords.y() + 16
                self.bullets[-1].move(a, b)

            elif self.move2 == "Down":
                self.life.append([self.move2, 0])
                a = self.coords.x() + 16
                b = self.coords.y() + 48
                self.bullets[-1].move(a, b)
            elif self.move2 == "Right":
                self.life.append([self.move2, 0])
                a = self.coords.x() + 48
                b = self.coords.y() + 16
                self.bullets[-1].move(a, b)

    def check_move(self, x, y, c):
        # Проверка возможности движения для танка против блоков.
        # 4 стороны у блоков, свои функции
        tank_x = 0
        tank_y = 0
        if c == 1:
            tank_x, tank_y = self.coords2.x(), self.coords2.y()
        if c == 2:
            tank_x, tank_y = self.coords.x(), self.coords.y()
        if tank_x > x:
            return False
        if abs(tank_y - y) < 48 and abs(tank_x - x) < 52:
            return 1
        elif tank_y < y + 64 and tank_y + 64 > y + 32 and abs(tank_x - x) < 52:
            return 2
        else:
            return False

    def check_move_2(self, x, y, c):
        # Проверка возможности движения для танка против блоков.
        # 4 стороны у блоков, свои функции
        tank_x = 0
        tank_y = 0
        if c == 1:
            tank_x, tank_y = self.coords2.x(), self.coords2.y()
        if c == 2:
            tank_x, tank_y = self.coords.x(), self.coords.y()
        if tank_x < x:
            return False
        if abs(tank_y - y) < 48 and abs(tank_x - 16 - x) < 52:
            return 1
        elif tank_y < y + 64 and tank_y + 64 > y + 32 and abs(tank_x - 16 - x) < 52:
            return 2
        else:
            return False

    def check_move_3(self, x, y, c):
        # Проверка возможности движения для танка против блоков.
        # 4 стороны у блоков, свои функции
        tank_x = 0
        tank_y = 0
        if c == 1:
            tank_x, tank_y = self.coords2.x(), self.coords2.y()
        if c == 2:
            tank_x, tank_y = self.coords.x(), self.coords.y()
        if tank_y < y:
            return False
        if abs(tank_x - x) < 48 and abs(tank_y - 16 - y) < 51:
            return 1
        elif tank_x < x + 64 and tank_x + 64 > x + 32 and abs(tank_y - 16 - y) < 51:
            return 2
        elif abs(tank_x - x) < 48 and abs(tank_y - y) < 65:
            return 3
        else:
            return False

    def check_move_4(self, x, y, c):
        # Проверка возможности движения для танка против блоков.
        # 4 стороны у блоков, свои функции
        tank_x = 0
        tank_y = 0
        if c == 1:
            tank_x, tank_y = self.coords2.x(), self.coords2.y()
        if c == 2:
            tank_x, tank_y = self.coords.x(), self.coords.y()
        if tank_y > y:
            return False
        if abs(tank_x - x) < 48 and abs(tank_y - y) < 51:
            return 1
        elif tank_x < x + 64 and tank_x + 64 > x + 32 and abs(tank_y - y) < 51:
            return 2
        elif abs(tank_x - x) < 48 and abs(tank_y - y) < 50:
            return 3
        else:
            return False

    def check_brick(self, x, y):
        # Проверка пули на врезание в блок. Если кирпич - удаление кирпича и пули
        # Если Cant, то удаление пули.
        for i in self.bricks:
            if i.x() <= x <= i.x() + 64 and i.y() <= y <= i.y() + 64:
                i.move(-600, - 600)
                return True

        for i in self.cant:
            if i.x() <= x <= i.x() + 64 and i.y() <= y <= i.y() + 64:
                return True

    def check_tank(self, new_x, new_y, c):
        # Проверка, есть ли перед тобой танк.
        if c == 1:
            tank_x, tank_y = new_x, new_y
            tank_2x, tank_2y = self.coords.x(), self.coords.y()
        else:
            tank_2x, tank_2y = new_x, new_y
            tank_x, tank_y = self.coords2.x(), self.coords2.y()

        if (tank_2x <= tank_x <= tank_2x + 48 or tank_x <= tank_2x <= tank_x + 48) \
                and (tank_y <= tank_2y <= tank_y + 48 or tank_2y <= tank_y <= tank_2y + 48):
            return False
        else:
            return True

    def timerEvent(self, e):
        # Движение танка
        if self.put == 1:
            if self.move == "D":
                frist = "assets/64_r.png"
                pixmap = QPixmap(frist)
                self.coords2.setPixmap(pixmap)
                a = self.coords2.x()
                # Выравнивание танка с границей
                # + проверка на движение
                if self.check_tank(a + 1, self.coords2.y(), 1):
                    if a < 590:
                        can = 1
                        for i in self.bricks:
                            b = self.check_move(i.x() + 1, i.y(), 1)
                            if b is not False:
                                can = 0
                        for i in self.cant:
                            b = self.check_move(i.x() + 1, i.y(), 1)
                            if b is not False:
                                can = 0
                        if can == 1:
                            self.coords2.move(a + 1, self.coords2.y())
                    elif 590 == a or a == 591:
                        can = 1
                        for i in self.bricks:
                            b = self.check_move(i.x() + 1, i.y(), 1)
                            if b is not False:
                                can = 0
                        for i in self.cant:
                            b = self.check_move(i.x() + 1, i.y(), 1)
                            if b is not False:
                                can = 0
                        if can == 1:
                            self.coords2.move(590, self.coords2.y())
            elif self.move == "A":
                frist = "assets/64_l.png"
                pixmap = QPixmap(frist)
                self.coords2.setPixmap(pixmap)
                a = self.coords2.x()
                # Выравнивание танка с границей
                # + проверка на движение
                if self.check_tank(a - 1, self.coords2.y(), 1):
                    if a > 2:
                        can = 1
                        for i in self.bricks:
                            b = self.check_move_2(i.x() - 1, i.y(), 1)
                            if b is not False:
                                can = 0
                        for i in self.cant:
                            b = self.check_move_2(i.x() - 1, i.y(), 1)
                            if b is not False:
                                can = 0
                        if can == 1:
                            self.coords2.move(a - 1, self.coords2.y())
                    elif 1 == a or a == 2:
                        can = 1
                        for i in self.bricks:
                            b = self.check_move_2(i.x() - 1, i.y(), 1)
                            if b is not False:
                                can = 0
                        for i in self.cant:
                            b = self.check_move_2(i.x() - 1, i.y(), 1)
                            if b is not False:
                                can = 0
                        if can == 1:
                            self.coords2.move(0, self.coords2.y())
            elif self.move == "W":
                frist = "assets/64.png"
                pixmap = QPixmap(frist)
                self.coords2.setPixmap(pixmap)
                a = self.coords2.y()
                # Выравнивание танка с границей
                # + проверка на движение
                if self.check_tank(self.coords2.x(), a - 1, 1):
                    if a > 2:
                        can = 1
                        for i in self.bricks:
                            b = self.check_move_3(i.x(), i.y() - 1, 1)
                            if b is not False:
                                can = 0
                        for i in self.cant:
                            b = self.check_move_3(i.x(), i.y() - 1, 1)
                            if b is not False:
                                can = 0
                        if can == 1:
                            self.coords2.move(self.coords2.x(), a - 1)
                    elif 1 == a or a == 2:
                        can = 1
                        for i in self.bricks:
                            b = self.check_move_3(i.x(), i.y() - 1, 1)
                            if b is not False:
                                can = 0
                        for i in self.cant:
                            b = self.check_move_3(i.x(), i.y() - 1, 1)
                            if b is not False:
                                can = 0
                        if can == 1:
                            self.coords2.move(self.coords2.x(), a - 1)
            elif self.move == "S":
                frist = "assets/64_d.png"
                pixmap = QPixmap(frist)
                self.coords2.setPixmap(pixmap)
                a = self.coords2.y()
                # Выравнивание танка с границей
                # + проверка на движение
                if self.check_tank(self.coords2.x(), a + 1, 1):
                    if a < 590:
                        can = 1
                        for i in self.bricks:
                            b = self.check_move_4(i.x(), i.y() + 1, 1)
                            if b is not False:
                                can = 0
                        for i in self.cant:
                            b = self.check_move_4(i.x(), i.y() + 1, 1)
                            if b is not False:
                                can = 0
                        if can == 1:
                            self.coords2.move(self.coords2.x(), a + 1)
                    elif 590 == a or a == 591:
                        can = 1
                        for i in self.bricks:
                            b = self.check_move_4(i.x(), i.y() + 1, 1)
                            if b is not False:
                                can = 0
                        for i in self.cant:
                            b = self.check_move_4(i.x(), i.y() + 1, 1)
                            if b is not False:
                                can = 0
                        if can == 1:
                            self.coords2.move(self.coords2.x(), a + 1)

        # Второй танк. движение
        if self.put2 == 1:
            if self.move2 == "Right":
                frist = "assets/64_r.png"
                pixmap = QPixmap(frist)
                self.coords.setPixmap(pixmap)
                a = self.coords.x()
                # Выравнивание танка с границей
                # + проверка на движение
                if self.check_tank(self.coords.x() + 1, self.coords.y(), 2):
                    if a < 590:
                        can = 1
                        for i in self.bricks:
                            b = self.check_move(i.x() + 1, i.y(), 2)
                            if b is not False:
                                can = 0
                        for i in self.cant:
                            b = self.check_move(i.x() + 1, i.y(), 2)
                            if b is not False:
                                can = 0
                        if can == 1:
                            self.coords.move(a + 1, self.coords.y())
                    elif 590 == a or a == 591:
                        can = 1
                        for i in self.bricks:
                            b = self.check_move(i.x() + 1, i.y(), 2)
                            if b is not False:
                                can = 0
                        for i in self.cant:
                            b = self.check_move(i.x() + 1, i.y(), 2)
                            if b is not False:
                                can = 0
                        if can == 1:
                            self.coords.move(590, self.coords.y())
            elif self.move2 == "Left":
                frist = "assets/64_l.png"
                pixmap = QPixmap(frist)
                self.coords.setPixmap(pixmap)
                a = self.coords.x()
                # Выравнивание танка с границей
                # + проверка на движение
                if self.check_tank(self.coords.x() - 1, self.coords.y(), 2):
                    if a > 2:
                        can = 1
                        for i in self.bricks:
                            b = self.check_move_2(i.x() - 1, i.y(), 2)
                            if b is not False:
                                can = 0
                        for i in self.cant:
                            b = self.check_move_2(i.x() - 1, i.y(), 2)
                            if b is not False:
                                can = 0
                        if can == 1:
                            self.coords.move(a - 1, self.coords.y())
                    elif 1 == a or a == 2:
                        can = 1
                        for i in self.bricks:
                            b = self.check_move_2(i.x() - 1, i.y(), 2)
                            if b is not False:
                                can = 0
                        for i in self.cant:
                            b = self.check_move_2(i.x() - 1, i.y(), 2)
                            if b is not False:
                                can = 0
                        if can == 1:
                            self.coords.move(0, self.coords.y())
            elif self.move2 == "Up":
                frist = "assets/64.png"
                pixmap = QPixmap(frist)
                self.coords.setPixmap(pixmap)
                a = self.coords.y()
                # Выравнивание танка с границей
                # + проверка на движение
                if self.check_tank(self.coords.x(), self.coords.y() - 1, 2):
                    if a > 2:
                        can = 1
                        for i in self.bricks:
                            b = self.check_move_3(i.x(), i.y() - 1, 2)
                            if b is not False:
                                can = 0
                        for i in self.cant:
                            b = self.check_move_3(i.x(), i.y() - 1, 2)
                            if b is not False:
                                can = 0
                        if can == 1:
                            self.coords.move(self.coords.x(), a - 1)
                    elif 1 == a or a == 2:
                        can = 1
                        for i in self.bricks:
                            b = self.check_move_3(i.x(), i.y() - 1, 2)
                            if b is not False:
                                can = 0
                        for i in self.cant:
                            b = self.check_move_3(i.x(), i.y() - 1, 2)
                            if b is not False:
                                can = 0
                        if can == 1:
                            self.coords.move(self.coords.x(), a - 1)
            elif self.move2 == "Down":
                frist = "assets/64_d.png"
                pixmap = QPixmap(frist)
                self.coords.setPixmap(pixmap)
                a = self.coords.y()
                # Выравнивание танка с границей
                # + проверка на движение
                if self.check_tank(self.coords.x(), self.coords.y() + 1, 2):
                    if a < 590:
                        can = 1
                        for i in self.bricks:
                            b = self.check_move_4(i.x(), i.y() + 1, 2)
                            if b is not False:
                                can = 0
                        for i in self.cant:
                            b = self.check_move_4(i.x(), i.y() + 1, 2)
                            if b is not False:
                                can = 0
                        if can == 1:
                            self.coords.move(self.coords.x(), a + 1)
                    elif 590 == a or a == 591:
                        can = 1
                        for i in self.bricks:
                            b = self.check_move_4(i.x(), i.y() + 1, 2)
                            if b is not False:
                                can = 0
                        for i in self.cant:
                            b = self.check_move_4(i.x(), i.y() + 1, 2)
                            if b is not False:
                                can = 0
                        if can == 1:
                            self.coords.move(self.coords.x(), a + 1)

        # Обработка пуль
        new_bullet = []
        new_life = []
        if len(self.bullets) != 0:
            for i in range(len(self.bullets)):
                self.move_bullet(self.bullets[i], self.life[i])
                self.life[i][1] += 1
                # Удаление пули
                if self.life[i][1] < 150:
                    if self.bullets[i].x() < - 16 or self.bullets[i].x() > 640 \
                            or self.bullets[i].y() > 660 or self.bullets[i].y() < -16:
                        pass
                    # Проверка, врезалась ли пуля в камень.
                    elif self.check_brick(self.bullets[i].x(), self.bullets[i].y()):
                        self.bullets[i].move(-600, - 600)
                    else:
                        # Если пуля не за границей, и не врезалась в камень или танк. То пуля
                        # Продолжает жить
                        new_bullet.append(self.bullets[i])
                        new_life.append(self.life[i])

            self.bullets = new_bullet
            self.life = new_life


if __name__ == '__main__':
    # Процесс запуска функции
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())
