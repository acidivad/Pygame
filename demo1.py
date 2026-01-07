import pygame as pg
import sys
import math


WINDOWSIZE = (800, 800)

window = pg.display.set_mode(WINDOWSIZE)

pg.init()


MID = (WINDOWSIZE[0] // 2, WINDOWSIZE[1] // 2)
R = 100
V = 0.1

def events():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()


def calculate_position():
    dt = pg.time.get_ticks()    
    position = (
        MID[0] + math.cos(math.radians(dt * V)) * R,
        MID[1] + math.sin(math.radians(dt * V)) * R
    )
    return position


while True:
    window.fill((0, 0, 0))
    events()

    pos = calculate_position()
    pg.draw.circle(window, (255, 0, 0), pos, 20)

    pg.display.update()