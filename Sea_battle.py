from random import randint
field_size = 6
ship_rang = [3, 2, 2, 1, 1, 1, 1]
ship_in = 0
myfield = []; aifield = []
#Визуализация для обоих досок
#        0    1    2    3    4    5    6
vis_my=["~", ".", "#", "O", "W", "~", "X"]
vis_ai=["~", "~", "~", "O", "W", "x", "X"]
#0 - пустое поле
#1 - контур (непоказывается, не занято)
#2 - простой корабль (у меня показывает, у компа нет, считается пустой
#3 - промах (для обоих как занято)
#4 - подбит (для обоих как занято)
#5 - контур подбитого (для обоих как занято, но на моей доске не отображается)
#6 - корабль потоплен


class BoardException(Exception):
    pass

class BoardDoubleException(BoardException):
    def __str__(self):
        return "Вы стреляли в эту точку!"
    pass

class Board:
    def __init__(self, field):
        self.field = field
        return

    def shot(selfd):
        pass

    def new_board(self):
        ship_list = []; ship_par_list = []; ship_lives = ship_rang
        while True:
            self.field = []
            for i in range(field_size):
                self.field.append([0, 0, 0, 0, 0, 0])
            ship_counter = 0
            ship_max = len(ship_rang)
            for i in range(ship_max):
                ship_num = i
                l = ship_rang[i]
                rep_cou = 0
                while rep_cou < 10000:
                    dir = randint(0, 1)
                    max_x = field_size - 1; max_y = field_size - 1
                    if dir == 1:
                        max_x = field_size - l
                    else:
                        max_y = field_size - l
                    x = randint(0, max_x); y = randint(0, max_y)
                    smin_x = x - 1; smax_x = x + 1 + dir*(l - 1)
                    smin_y = y - 1; smax_y = y + 1 + (1 - dir)*(l - 1)
                    check = True
                    for i in range(smin_x, smax_x + 1):
                        for j in range(smin_y, smax_y + 1):
                            if i > -1 and i < 6 and j > -1 and j < 6:
                                if self.field[i][j] > 1:
                                    check = False
                    if not check:
                        rep_cou += 1
                        continue
                    ship=[]
                    for i in range(smin_x, smax_x + 1):
                        for j in range(smin_y, smax_y + 1):
                            if i > -1 and i < 6 and j > -1 and j < 6:
                                if i > smin_x and i < smax_x and j > smin_y and j < smax_y:
                                    self.field[i][j]=2
                                    ship.append([i, j])
                                else:
                                    self.field[i][j]=1
                    ship_list.append(ship)
                    ship_par =[x, y, dir, l]
                    ship_par_list.append([x, y, dir, l])
                    ship_counter += 1
                    break
                if rep_cou>10000:
                    continue
            if ship_counter >= len(ship_rang)-1:
                break
        return self.field, ship_list, ship_par_list

    def contour(self, field, ship_par, x, y, l):#Оконтуривание потопленных (field, x, y, dir, l,  field->)
        smin_x = x - 1; smax_x = x + 1 + dir*(l - 1)
        smin_y = y - 1; smax_y = y + 1 + (1 - dir)*(l - 1)
        for i in range(smin_x, smax_x + 1):
            for j in range(smin_y,smax_y + 1):
                if i > -1 and i < 6 and j > -1 and j < 6:
                    if i > smin_x and i < smax_x and j > smin_y and j < smax_y:
                        #координаты корабля
                        myfield[i][j] = 6
                    else:
                        #контур
                        if myfield[i][j] < 3:
                            myfield[i][j] = 5
        return field


class AiBoard(Board):
    def shot(self, field, t_point): #Принимает "выстрел", проверяет на доске и если попадание, то запрос к ??Ship.shot(coords), если потопл
        ship_in = 0 #Промах
        x, y = t_point
        if field[x][y] == 2:
            ship_in = 1
            field[x][y] = 4
        elif field[x][y] > 2:
            ship_in = 2 #Ошибка
            raise BoardDoubleException
        else:
            field[x][y] = 3
        return field, ship_in

class MyBoard(Board):
    def shot(self, field, t_point):
       pass


class Player:
    def __init__(self, Board, pl):#Параметры: собственная доска (объект класса Board), доска врага
        self.board = Board
        self.pl = pl
    def ask(self):
        pass

class AI(Player):
    def ask(self, field):
        ship_in = 0 #Промах
        while True:
            x = randint(0, field_size - 1); y = randint(0, field_size - 1)
            if field[x][y] < 2:
                field[x][y] = 3
                break
            if field[x][y] == 2:
                ship_in = 1
                field[x][y] = 4
                break
            continue
        return field, x, y, ship_in

class Human(Player):
    def ask(self):
        while True:
            in_str = input("Введите координаты точки (xy): ")
            if len(in_str) != 2:
                print("Должно быть два числа!")
                continue
            elif not in_str.isdigit():
                print("Вводите только числа!")
                continue
            else:
                x = int(in_str[0]) - 1
                y = int(in_str[1]) - 1
            if x in range(0, 6) and y in range(0, 6):
                t_point = [x, y]
                break
            else:
                print("Числа от 1 до 6 !")
                continue
        return t_point


class Game:
    def __init__(self):#Параметры: Игрок (объект класса Human, пользователь + Доска пользователя)/(объект класса Computer + Доска компьютера)
        return
    def greet(self):
        print("-"*55, "Игра \"Морской бой\"", "-"*55)
        print("Правила игры: 1. Для вас и компьютера поле генерируется случайным образом")
        print("              2. Ходы делаются по очереди, если не было попадания в корабль противника, иначе еще один ход")
        print("              3. Нельзя указывать клетку за пределами поля и ту, в которую уже был произведен выстрел")
        print("              4. Нельзя стрелять рядом с уничтоженным кораблем (очевидно, что там пусто)")
        print("              5. Ввод координат выстрела - два числа (от 1 до 6), первое по горизонтали, второе по вертикали, без пробела")
        t=input("Для начала игры нажмите Enter")
    def show(self, myfield, aifield):
        print("   ------Вы-----"+" "*12+"--Компьютер--"+"\n"+"    1 2 3 4 5 6"+" "*14+"1 2 3 4 5 6")
        for i in range(field_size):
            prt_str=" "+str(i+1)+" "; hum_str="|";com_str="|"
            for j in range(field_size):
                hum_str +=vis_my[myfield[j][i]]+"|"; com_str +=vis_ai[aifield[j][i]]+"|"
            prt_str=prt_str + hum_str + " "*10 + str(i+1) + " " + com_str; print(prt_str)
    def loop(self):
        #while True:
            pl_num=randint(0,1)
            ai_lives = 11; my_lives = 11
            myfield, my_slist, my_ship_plist = MyBoard.new_board(self)
            aifield, ai_slist, ai_ship_plist = AiBoard.new_board(self)
            self.show(myfield, aifield)
            t_point = [0, 0]
            while True:
                if pl_num == 0:
                    ship_in = 2
                    while ship_in > 1:
                        try:
                            x, y = Human.ask(self)
                            aifield, ship_in = AiBoard.shot(self, aifield, [x, y])
                        except BoardDoubleException as e:
                            print(e)
                            continue
                        if ship_in == 1:
                            ai_lives -= 1
                            print("Попадание!", ai_lives)
                        elif ship_in == 0:
                            print("Мимо!")
                else:
                    myfield, x, y, ship_in = AI.ask(self, myfield)
                    print("Ход компьютера: ", x, y)
                    if ship_in == 1:
                        my_lives -= 1
                        print("Попадание!", my_lives)
                if ship_in != 1: #Если промах
                    if pl_num == 0:
                        pl_num = 1
                    else:
                        pl_num = 0
                #print("\n"*1)
                self.show(myfield, aifield)
                if my_lives <1:
                    print("Ты победил!")
                    break
                if ai_lives <1:
                    print("Победил компьютер!")
                    break
            return

    def start(self):
        self.greet()
        self.loop()

MyGame=Game()
MyGame.start()


