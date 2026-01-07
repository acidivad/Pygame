import pygame as pg
import sys
import random


SIZE = 50
BOARDSIZE = (15, 15)
WINDOWSIZE = (SIZE * BOARDSIZE[0], SIZE * BOARDSIZE[1])

class colors:
    white = (255, 255, 255)
    black = (0, 0, 0)
    snake = (0, 255, 0)
    apple = (255, 0, 0)

clock = pg.time.Clock()
FPS = 60

MOVE_DELAY = 500

pg.display.set_caption("Snake")
window = pg.display.set_mode(WINDOWSIZE)

pg.init()


length = 1
snake = [(BOARDSIZE[0] // 2, BOARDSIZE[1] // 2)]

moving = None
holding_space = False
directions = {
    "left": (-1, 0),
    "right": (1, 0),
    "up": (0, -1),
    "down": (0, 1),
}

apple = (0, 0)
def create_apple():
    pos = None
    while pos == None or pos in (snake + [apple]):
        pos = (random.randint(0, BOARDSIZE[0] - 1), random.randint(0, BOARDSIZE[1] - 1))
    return pos
apple = create_apple()


def move():
    global length, apple

    if moving is None: return

    head = snake[-1]
    d = directions[moving]
    new_head = (head[0] + d[0], head[1] + d[1])

    if new_head[0] < 0:
        new_head = (BOARDSIZE[0] - 1, new_head[1])
    if new_head[0] >= BOARDSIZE[0]:
        new_head = (0, new_head[1])
    if new_head[1] < 0:
        new_head = (new_head[0], BOARDSIZE[1] - 1)
    if new_head[1] >= BOARDSIZE[1]:
        new_head = (new_head[0], 0)

    if new_head in snake:
        pg.quit()
        sys.exit()
    
    if new_head == apple:
        length += 1
        apple = create_apple()

    snake.append(new_head)
    if length < len(snake):
        snake.pop(0)


def draw():
    window.fill(colors.black)

    for part in snake:
        pg.draw.rect(window, colors.snake, ((part[0] * SIZE, part[1] * SIZE), (SIZE, SIZE)))

    pg.draw.rect(window, colors.apple, ((apple[0] * SIZE, apple[1] * SIZE), (SIZE, SIZE)))


def events():
    global moving, holding_space

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                holding_space = True
            if event.key == pg.K_a or event.key == pg.K_LEFT:
                if moving == "right": continue
                moving = "left"
            if event.key == pg.K_d or event.key == pg.K_RIGHT:
                if moving == "left": continue
                moving = "right"
            if event.key == pg.K_w or event.key == pg.K_UP:
                if moving == "down": continue
                moving = "up"
            if event.key == pg.K_s or event.key == pg.K_DOWN:
                if moving == "up": continue
                moving = "down"

        if event.type == pg.KEYUP:
            if event.key == pg.K_SPACE:
                holding_space = False


last_moved = pg.time.get_ticks()
holding_space = False
while True:
    events()

    speed = {True: 3, False: 1}[holding_space]
    if pg.time.get_ticks() >= last_moved + (MOVE_DELAY / speed):
        last_moved = pg.time.get_ticks()
        move()

    draw()

    pg.display.update()
    clock.tick(FPS)