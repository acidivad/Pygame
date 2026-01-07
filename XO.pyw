import pygame as pg
import sys


SIZE = 100
WINDOWSIZE = (SIZE * 3, SIZE * 3)

class colors:
    white = (255, 255, 255)
    black = (0, 0, 0)
    O = (255, 0, 0)
    X = (0, 0, 255)

FPS = 60
clock = pg.time.Clock()

pg.display.set_caption("XO")
window = pg.display.set_mode(WINDOWSIZE)

pg.init()


board = [[" " for _ in range(3)] for _ in range(3)]

def draw_board():
    window.fill(colors.white)
    for i in range(1, 3):
        pg.draw.line(window, colors.black, (i * SIZE, 0), (i * SIZE, WINDOWSIZE[1]), 2)
        pg.draw.line(window, colors.black, (0, i * SIZE), (WINDOWSIZE[0], i * SIZE), 2)

    for y, row in enumerate(board):
        for x, v in enumerate(row):
            if v == "X":
                pg.draw.line(window, colors.X, (x * SIZE + 10, y * SIZE + 10), ((x + 1) * SIZE - 10, (y + 1) * SIZE - 10), 5)
                pg.draw.line(window, colors.X, ((x + 1) * SIZE - 10, y * SIZE + 10), (x * SIZE + 10, (y + 1) * SIZE - 10), 5)
            elif board[y][x] == "O":
                pg.draw.circle(window, colors.O, (x * SIZE + SIZE // 2, y * SIZE + SIZE // 2), SIZE // 2 - 10, 5)


player = "X"
def switch_player():
    if player == "X":
        return "O"
    return "X"


winner = None
def check_for_winner():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != " ":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != " ":
            return board[0][i]

    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]
    return None


def events():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()


while True:
    mouse_pos = pg.mouse.get_pos()
    mouse_pressed = pg.mouse.get_pressed()

    events()

    draw_board()

    if mouse_pressed[0] and winner is None:
        x, y = mouse_pos[0] // SIZE, mouse_pos[1] // SIZE
        if board[y][x] == " ":
            board[y][x] = player
            player = switch_player()

    winner = check_for_winner()
    if winner:
        pg.display.set_caption("Nyertes: " + winner)


    pg.display.update()
    clock.tick(FPS)