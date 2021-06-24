import math
import random
import sys
import time

import pygame

nb_flowers = 20
nb_bees = 70


class Flower:
    id = 0
    list = []

    def __init__(self):
        self.id = self.__class__.id
        self.__class__.id += 1
        self.__class__.list.append(self)
        self.x = random.randint(0, 999)
        self.y = random.randint(0, 999)
        self.qty = random.randint(2, 5)
        self.expiration = time.time() + random.random() * 10 + 20

    def use(self):
        self.qty -= 1
        if self.qty <= 0:
            _index = Flower.list.index(self)
            del Flower.list[_index]


class Bee:
    id = 0
    list = []

    def __init__(self):
        self.id = self.__class__.id
        self.__class__.id += 1
        self.__class__.list.append(self)
        self.velocity = 1
        self.strength = 1
        self.energy = 100
        self.x = 500
        self.y = 500
        self.state = "travel"
        self.color = (0, 127, 255)
        self.detect_radius = random.randint(20, 40)
        self.dest_x, self.dest_y = random.randint(0, 999), random.randint(0, 999)
        self.last = [0, 0]

    def move(self, _flowers):
        target, x, y = None, 500, 500
        if self.state == "empty":
            target = self.near_flower(_flowers)
            if target is None:
                x, y = None, None
            else:
                x, y, = target.x, target.y
        elif self.state == "full":
            x, y = 500, 500
        elif self.state == "travel":
            x, y = self.dest_x, self.dest_y
        if x is not None:
            if self.x - self.velocity <= x <= self.x + self.velocity:
                self.x = x
            elif x < self.x - self.velocity:
                self.x -= self.velocity
            elif x > self.x + self.velocity:
                self.x += self.velocity
        else:
            a = random.random()
            if self.last[0] == 0:
                self.last[0] = random.randint(-1, 1)
            if a < 0.85:
                self.x += self.last[0] * self.velocity
            elif a < 0.9:
                self.x -= self.last[0] * self.velocity
                self.last[0] = -self.last[0]
            else:
                self.last[0] = 0
        if y is not None:
            if self.y - self.velocity <= y <= self.y + self.velocity:
                self.y = y
            elif y < self.y - self.velocity:
                self.y -= self.velocity
            elif y > self.y + self.velocity:
                self.y += self.velocity
        else:
            a = random.random()
            if self.last[1] == 0:
                self.last[1] = random.randint(-1, 1)
            if a < 0.85:
                self.y += self.last[1] * self.velocity
            elif a < 0.9:
                self.y -= self.last[1] * self.velocity
                self.last[1] = -self.last[1]
            else:
                self.last[1] = 0
        if x == self.x and y == self.y:
            if self.state == "empty":
                self.state = "full"
                self.color = (0, 255, 0)
                target.use()
            elif self.state == "full":
                self.state = "travel"
                self.color = (0, 127, 255)
                self.dest_x, self.dest_y = random.randint(0, 999), random.randint(0, 999)
            elif self.state == "travel":
                self.state = "empty"
                self.color = (255, 255, 0)
        self.x = sorted([0, self.x, 999])[1]
        self.y = sorted([0, self.y, 999])[1]

    def near_flower(self, _flowers):
        d_min, nearest = self.detect_radius, None
        for _flower in _flowers:
            d = math.dist((self.x, self.y), (_flower.x, _flower.y))
            if d < d_min:
                d_min = d
                nearest = _flower
        return nearest


for i in range(nb_flowers):
    Flower()

for i in range(nb_bees):
    Bee()

pygame.init()
screen = pygame.display.set_mode((1000, 1000))
running = True
t = time.time()
regen_flower = t
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                break

    for flower in Flower.list:
        pygame.draw.rect(screen, (255, 0, 0), [flower.x - 2, flower.y - 2, 4, 4])
    for bee in Bee.list:
        pygame.draw.rect(screen, bee.color, [bee.x - 1, bee.y - 1, 2, 2])
        bee.move(Flower.list)
    for flower in Flower.list:
        if t > flower.expiration:
            index = Flower.list.index(flower)
            del Flower.list[index]
    while time.time() < t + 1 / 60:
        pass
    t = time.time()
    if t >= regen_flower + 25 / nb_flowers:
        Flower()
        regen_flower = t
    pygame.display.flip()
pygame.quit()
sys.exit()
