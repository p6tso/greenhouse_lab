from random import randint


class Time:
    def __init__(self, h=0, m=0):
        self.h = h
        self.m = m
    def __add__(self, other):
        ans = Time()
        if other.m + self.m >= 60:
            ans.h +=1
        ans.m = (other.m + self.m)%60
        ans.h += other.h + self.h
        return ans
    def __sub__(self, other):
        ans = Time()
        if other.m > self.m:
            ans.h -= 1
        ans.m = (self.m - other.m) % 60
        ans.h += self.h - other.h
        return ans
    def __gt__(self, other):
        return (self.h > other.h) or (self.h == other.h and self.m > other.m)
    def __eq__(self, other):
        return (self.h == other.h) and (self.m == other.m)
    def __ge__(self, other):
        return self > other or self == other
    def __str__(self):
        return str(self.h)+':'+str(self.m)

class Plant:
    def __init__(self, name, w, b, t : Time):
        self.name = name
        self.w = w
        self.b = b
        self.birth_time = t
        self.height = 0
        self.health = 0
        self.lost_time = Time()
        self.health_time = 0
        self.f = 0
        self.time_old = Time()
        self.days = Time()
    water_high = 0
    light_high = 0
    percent_high = 0
    time_high = Time()
    min_w, max_w = 0, 0
    min_b, max_b = 0, 0
    eal_time = 0
    min_high = 0
    last_child = Time()
    max_age = Time()
    def check_high(self):
        if self.f == 0:
            self.f = self.height>=self.min_high
            if self.f == 1:
                self.time_old = Time()

        return self.f
    def child(self):
        pass
    def add_water(self, w):
        self.w += w
    def add_light(self, b):
        self.b += b
    def eal_check(self):
        if self.health >= 3: return self.health
        f =  max(self.max_w < self.w, self.w > self.min_w,
                 self.max_b < self.b, self.min_b > self.b)
        self.health += f
        self.eal_time += (self.health and not f)
        if self.eal_time == 3:
            self.health -= 1
            self.eal_time = 0
        return self.health
    def get_high(self):
        self.w -= self.water_high
        self.b -= self.light_high
        self.height += self.percent_high
    def time_skip(self, t : Time):
        t += self.lost_time
        while t >= self.time_high:
            t-=self.time_high
            self.get_high()
            if self.f == 0:
                self.check_high()
            if self.f == 1:
                self.last_child+=self.time_high
                self.child()
        self.lost_time = t
        if self.f == 1:
            self.last_child += t





class AppleTree(Plant):
    def __init__(self, name, w, b, t : Time):
        super().__init__(name, w, b, t)
        self.count_apples = 0

    water_high = 10
    light_high = 8
    percent_high = 2
    time_high = Time(0, 40)
    min_w, max_w = 10, 90
    min_b, max_b = 10, 60
    min_high = 80
    max_age = Time(240, 0)

    def child(self):
        if self.last_child >= Time(24, 0):
            self.last_child = Time()
            a = randint(10, 20)
            self.count_apples += a
            self.days += Time(24,0)
            if self.days >= self.max_age:
                self.health = 4
            return a

class Orchid(Plant):
    def __init__(self, name, w, b, t: Time):
        super().__init__(name, w, b, t)
        self.color = randint(1, 5)

    water_high = 5
    light_high = 10
    percent_high = 5
    time_high = Time(0, 20)
    min_w, max_w = 15, 55
    min_b, max_b = 30, 80
    min_high = 90
    max_age = Time(48, 0)
    def child(self):
        if self.days >= self.max_age:
            self.health = 4
        return self.color

class Greenhouse:
    def __init__(self):
        self.holder = {}
        self.time_exist = Time()
    def tend_to_plants(self):
        for i in self.holder.keys():
            tree = self.holder[i]
            if tree.w <= tree.min_w:
                tree.w = tree.max_w - 1
            if tree.b <= tree.min_b:
                tree.b = tree.max_b -1
    def add(self, tree_type, name, w, b):
        tree = tree_type(name, w, b, self.time_exist)
        self.holder[name] = tree
        return tree
    def find(self, name):
        if name in self.holder.keys():
            return self.holder[name]
        else:
            return 0
    def add_w(self, name, w):
        tree = self.find(name)
        if tree!=0:
            tree.add_water(w)
        return tree
    def add_b(self, name, b):
        tree = self.find(name)
        if tree!=0:
            tree.add_ligth(b)
        return tree
    def remove(self, name):
        tree = self.find(name)
        if tree!=0:
            self.holder.pop(name)
        return tree
    def time_skip(self, t:Time):
        t += Time(0, self.time_exist.m)
        self.time_exist -= Time(0, self.time_exist.m)
        while t.h>0:
            t -= Time(1, 0)
            self.time_exist += Time(1, 0)
            for i in self.holder.keys():
                self.holder[i].time_skip(Time(0, 30))
                self.holder[i].eal_check()
                self.holder[i].time_skip(Time(0, 30))
            self.tend_to_plants()
            for i in self.holder.keys(): self.holder[i].eal_check()
        self.time_exist += t


f = 1
g = Greenhouse()
tp = {
    'Орхидея' : Orchid,
    'Яблоня' : AppleTree
    }
tp_rev = {
    Orchid : 'Орхидея',
    AppleTree : 'Яблоня'
    }
health = [
    'Здоровое',
    'Легкая болезнь',
    'Тяжелая болезнь',
    'Мертво',
    'Естественная смерть'
]
colors = [
    'красные',
    'синие',
    'желтые'
]
while f:
    i = input().split()
    a = int(i[0])
    if a == 0:
        f = 0
    elif a == 1:
        t = g.time_exist
        h,m = map(int, i[1].split(':'))
        g.time_skip(Time(h,m))
        print(f'Время изменилось с {t} на {g.time_exist}. Прошло {h} часов {m} минут')
    elif a == 2:
        g.add(tp[i[1]], i[2], int(i[3]), int(i[4]))
        print(f'Посажена {i[1]} с наименованием \"{i[2]}\"!')
    elif a==3:
        g.add_w(i[1], int(i[2]))
    elif a==4:
        g.add_b(i[1], int(i[2]))
    elif a==5:
        g.remove(i[1])
        print(f'Растение \"{i[1]}\" было вынесено из оранжереи')
    elif a==6:
        tree = g.find(i[1])
        if tree!=0:
            print(f'Статистика по \"{i[1]}\":')
            print(f'Тип: {tp_rev[type(tree)]}')
            print(f'Вода: {tree.min_w}<{tree.w}<{tree.max_w}')
            print(f'Свет: {tree.min_b}<{tree.b}<{tree.max_b}')
            print(f'Рост: {tree.height}%')
            print(f'Состояние: {health[tree.health]}')
            print(f'Посажено в {tree.birth_time}')
            s = ''
            if tree.f == 0:
                if type(tree) == Orchid:
                    s = 'Лепестки отсутствуют'
                else:
                    s = 'Не плодоносит'
            else:
                if type(tree) == Orchid:
                    s = f'Имеет {colors[tree.color]} лепестки'
                else:
                    s = 'Плодоносит'
            print(s)
        else: print(f'Растение с именем \"{i[1]}\" отсутствует в оранжерее!')


