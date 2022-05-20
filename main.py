import math
import pygame as pg
from analysis import number

MAP_W = 5632
MAP_H = 2048
WHITE = 255, 255, 255, 255
SCREEN_W = 1440
SCREEN_H = 900
PROVINCES = []

scale = 1
corner = 0, 0
c_prov = []
t_prov = []
n_prov = []
conn = []
completed = open('completed.txt', 'r')
for line in completed.readlines():
    c_prov.append(int(line))
completed.close()
connections = open('graph.txt', 'r')
for line in connections.readlines():
    a = line.split()
    conn.append([int(a[0]), int(a[1])])
connections.close()

pg.init()
screen = pg.display.set_mode((1440, 900))
prov = pg.image.load('provinces.png').convert_alpha()
clock = pg.time.Clock()

for x in range(MAP_W - 2):
    for y in range(MAP_H - 4):
        if prov.get_at((x + 2, y + 4)) == WHITE and prov.get_at(
                (x - 2, y + 4)) != WHITE:
            num = number(
                [int(prov.get_at((i, j)) == WHITE) for j in range(y, y + 5) for
                 i in
                 range(x, x + 15)])
            if num:
                digits = int(math.log10(num)) + 1
                PROVINCES.append([num, x, y, digits])

finished = False
while not finished:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True
            completed = open('completed.txt', 'w')
            for province in c_prov:
                completed.write(str(province))
                completed.write('\n')
            completed.close()
            connections = open('graph.txt', 'w')
            for province in conn:
                connections.write(str(province[0]))
                connections.write(' ')
                connections.write(str(province[1]))
                connections.write('\n')
            connections.close()
        elif event.type == pg.MOUSEBUTTONDOWN:
            match event.button:
                case 1:
                    x, y = event.pos
                    cx, cy = corner
                    x, y = int(x / scale) - cx, int(y / scale) - cy
                    for province in PROVINCES:
                        if x in range(province[1], province[1] + province[
                            3] * 4) and y in range(province[2],
                                                   province[2] + 4):
                            if t_prov:
                                n_prov.append(province[0])
                            else:
                                t_prov.append(province[0])
                            break
                case 4:
                    if scale < 5:
                        scale += 1
                case 5:
                    if scale > 1:
                        scale -= 1
        elif event.type == pg.MOUSEMOTION and event.buttons == (0, 1, 0):
            x, y = corner
            dx, dy = event.rel
            corner = x + int(dx / scale), y + int(dy / scale)
        elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
            for n_province in n_prov:
                conn.append([t_prov[0], n_province])
            n_prov = []
            c_prov.append(t_prov[0])
            t_prov = []

    rect = pg.Surface((int(SCREEN_W / scale), int(SCREEN_H / scale)))
    rect.blit(prov, corner)
    screen.blit(pg.transform.scale(rect, (SCREEN_W, SCREEN_H)), (0, 0))
    for province in PROVINCES:
        for c_province in c_prov:
            if province[0] == c_province:
                filling = pg.Surface(
                    ((province[3] * 4 - 1) * scale, 5 * scale))
                filling.fill((0, 0, 255))
                x, y = corner
                screen.blit(filling, (
                (province[1] + x) * scale, (province[2] + y) * scale))
        for c_province in t_prov:
            if province[0] == c_province:
                filling = pg.Surface(
                    ((province[3] * 4 - 1) * scale, 5 * scale))
                filling.fill((0, 255, 0))
                x, y = corner
                screen.blit(filling, (
                (province[1] + x) * scale, (province[2] + y) * scale))
        for c_province in n_prov:
            if province[0] == c_province:
                filling = pg.Surface(
                    ((province[3] * 4 - 1) * scale, 5 * scale))
                filling.fill((255, 0, 0))
                x, y = corner
                screen.blit(filling, (
                (province[1] + x) * scale, (province[2] + y) * scale))
    pg.display.update()
    clock.tick(60)
pg.quit()
