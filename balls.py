import pygame
from pygame.draw import *
from random import randint, choice, random
import math
pygame.init()


FPS = 60
WIDTH = 1200
HEIGHT = 800
score = 0
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


class Ball:
    '''
    Создание экземпляра мяча
    '''
    def __init__(self):
        self.new_ball()
    
    def new_ball(self):
        '''
        Задает параметры мяча.
        '''
        self.color = choice(COLORS)
        self.r = randint(10, 30)
        self.x = randint(self.r, WIDTH-self.r)
        self.y = randint(self.r, HEIGHT-self.r)
        self.v = 100
        self.angle = random() * 2 * math.pi
        self.v_x = self.v * math.sin(self.angle)
        self.v_y = self.v * math.cos(self.angle)

    def Clicked(self, event):
        '''
        Начисление очков за попадание в шарик.
        '''
        global score
        # Проверка условия попадания в мяч.
        if (event.pos[0]-self.x)**2 + (event.pos[1]-self.y)**2 <= self.r**2:
            score += 1
            self.new_ball()

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
        self.v_y = self.vel * math.cos(self.angle) * (-1)
        self.x += self.v_x / FPS
        self.y += self.v_y / FPS
        # Отрисовка  мяча.
        circle(screen, self.color, (int(self.x), int(self.y)), self.r)

# Создаем первую партию из 10 двигающихся мячей из класса Ball.
balls = [Ball() for i in range(10)]
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
        # Проверяем попадание по шарику.   
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for ball in balls:
            ball.Clicked(event)
    # Дальнейшее движение новых шариков.
    for ball in balls:
        ball.move()
    pygame.display.update()
    screen.fill(BLACK)
print('ВАШ РЕЗУЛЬТАТ', score)
pygame.quit()
