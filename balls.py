import pygame
from pygame.draw import *
from random import randint, choice, random
import math
import csv

pygame.init()
pygame.font.init()

FPS = 60
WIDTH = 1200
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN, WHITE]


class Target:
    '''
    Создание класса мишеней
    '''
    def __init__(self, v):
        self.new_target(v)

    def new_target(self, v):
        '''
        Задает параметры мишени
        '''
        self.color = choice(COLORS)
        self.r = randint(10, 30)
        self.x = randint(self.r, WIDTH-self.r)
        self.y = randint(self.r, HEIGHT-self.r)
        self.v = v
        self.angle = random() * 2 * math.pi
        self.v_x = self.v * math.cos(self.angle)
        self.v_y = self.v * math.sin(self.angle)


class Ball(Target):
    '''
    Создание класса мишеней - мяча
    '''
    def clicked(self, event):
        '''
        Начисление одного очка за попадание в шарик.
        '''
        # Проверка условия попадания в мяч.
        if math.dist(event.pos, (self.x, self.y)) <= self.r:
            score.increase(1)
            self.new_target(100)

    def move(self):
        '''
        Отрисовка и движение мяча. Проверка условия невылета мяча за пределы поля.
        '''
        # Изменение угла при достижении правой границы.
        if self.x > WIDTH-self.r:
            self.angle = (random() + 1) * math.pi
        # Изменение угла при достижении левой границы.
        elif self.x < self.r:
            self.angle = random() * math.pi
        # Изменение угла при достижении нижней границы.
        if self.y > HEIGHT-self.r:
            self.angle = (random() + 1.5) * math.pi
        # Изменение угла при достижении верхней границы.
        elif self.y < self.r:
            self.angle = (random() + 0.5) * math.pi
        # Новые параметры для скорости и координат мяча.
        self.v_x = self.v * math.sin(self.angle)
        self.v_y = self.v * math.cos(self.angle) * (-1)
        self.x += self.v_x / FPS
        self.y += self.v_y / FPS
        # Отрисовка  мяча.
        circle(screen, self.color, (int(self.x), int(self.y)), self.r)


class Square(Target):
    '''
    Создание класса мишеней - квадрата
    '''
    def clicked(self, event):
        '''
        Начисление 10 очков за попадание в квадрат
        '''
        # Проверка условия попадания в квадрат.
        if abs(event.pos[0] - self.x) <= self.r and abs(event.pos[1] - self.y) <= self.r:
            score.increase(10)
            self.new_target(300)

    def move(self):
        '''
        Отрисовка и движение квадрата. Проверка условия невылета квадрата за пределы поля.
        '''
        # Изменение угла при достижении правой границы.
        if self.x > WIDTH-self.r:
            self.angle = (random() + 0.5) * math.pi
        # Изменение угла при достижении левой границы.
        elif self.x < self.r:
            self.angle = (random() - 0.5) * math.pi
        # Изменение угла при достижении нижней границы.
        if self.y > HEIGHT-self.r:
            self.angle = (random() + 1) * math.pi
        # Изменение угла при достижении верхней границы.    
        elif self.y < self.r:
            self.angle = random() * math.pi
        # Изменение угла при попадании курсора по цели. 
        if abs(pygame.mouse.get_pos()[0] - self.x) <= self.r and abs(pygame.mouse.get_pos()[1] - self.y) <= self.r:
            self.angle = math.atan2(self.y - pygame.mouse.get_pos()[1], self.x - pygame.mouse.get_pos()[0])
        # Новые параметры для скорости и координат квадрата.
        self.v_x = self.v * math.cos(self.angle)
        self.v_y = self.v * math.sin(self.angle)
        self.x += self.v_x / FPS
        self.y += self.v_y / FPS
        # Отрисовка  квадрата.
        rect(screen, self.color, [int(self.x - self.r), int(self.y - self.r), int(2*self.r), int(2*self.r)])

class Counter:
    '''
    Подсчет количества очков
    '''
    def __init__(self):
        self.count = 0

    def increase(self, prize):
        self.count += prize

    def draw(self):
        # Вывод количества очков на дисплей.
        surface_counter = labelFont.render(str(self.count), False, WHITE)
        screen.blit(surface_counter, (0, 0))

Name = input("Type your name: ")        
# Создаем первую партию из 10 двигающихся мячей из класса Ball.
balls = [Ball(100) for i in range(10)]
# Создаём двигающийся квадрат из класса Square.
square = Square(300)
# Выводим количество очков.
score = Counter()
labelFont = pygame.font.SysFont('Monaco', 100)
pygame.display.update()
clock = pygame.time.Clock()
finished = False


# Основной цикл программы
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        # Проверяем выход из программы.
        if event.type == pygame.QUIT:
            finished = True
        # Проверяем попадание по мишени.   
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for ball in balls:
                ball.clicked(event)
            square.clicked(event)
    # Дальнейшее движение новых мишеней.
    for ball in balls:
        ball.move()
    square.move()
    score.draw()
    pygame.display.update()
    screen.fill(BLACK)



data = [{Name: score.count}]
with open('records.csv', 'a') as f:
    writer = csv.DictWriter(
        f, fieldnames = list(data[0].keys()), quoting=csv.QUOTE_NONNUMERIC)
    writer.writeheader()
    for d in data:
        writer.writerow(d)
pygame.quit()
