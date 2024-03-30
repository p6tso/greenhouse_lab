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
    water_high = 0
    light_high = 0
    percent_high = 0
    time_high = Time()
    min_w, max_w = 0, 0
    min_b, max_b = 0, 0

    def add_water(self, w):
        self.w += w
    def add_light(self, b):
        self.b += b
    def get_high(self):
        self.w -= self.water_high
        self.b -= self.light_high
        self.height += self.percent_high
    def time_skip(self, t : Time):
        t += self.lost_time
        while t >= self.time_high:
            t-=self.time_high
            self.get_high()
        self.lost_time = t
    def eal_check(self):
        f =  max(self.max_w < self.w, self.w > self.min_w,
                 self.max_b < self.b, self.min_b > self.b)



class AppleTree(Plant):
    def __init__(self, name, w, b, t : Time):
        super().__init__(name, w, b, t)

    water_high = 10
    light_high = 8
    percent_high = 2
    time_high = Time(0, 40)
    min_w, max_w = 10, 90
    min_b, max_b = 10, 60

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

class Greenhouse:
    def __init__(self):
        self.holder = {}
        self.time_exist = Time()
