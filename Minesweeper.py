import pygame
from pygame.locals import QUIT, MOUSEBUTTONUP, MOUSEBUTTONDOWN
from random import randrange
from sys import exit

clock = pygame.time.Clock()

pygame.init()
pygame.display.set_caption('Mode selection')

WINDOW_SIZE = (500, 300)
win_half = WINDOW_SIZE[0] // 2
win_div_4 = WINDOW_SIZE[1] // 4

background_color = (191, 196, 199)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
screen.fill(background_color)

buttons_text = {
    0: pygame.font.SysFont('miriam', 22, 1).render('Newbie 10 mines (9x9)', 1, (0, 0, 0)),
    1: pygame.font.SysFont('miriam', 22, 1).render('Amateur 40 mines (16x16)', 1, (0, 0, 0)),
    2: pygame.font.SysFont('miriam', 22, 1).render('Professional 99 mines (16x30)', 1, (0, 0, 0)),
    10: pygame.font.SysFont('miriam', 22, 1).render('Newbie 10 mines (9x9)', 1, (80, 80, 80)),
    11: pygame.font.SysFont('miriam', 22, 1).render('Amateur 40 mines (16x16)', 1, (80, 80, 80)),
    12: pygame.font.SysFont('miriam', 22, 1).render('Professional 99 mines (16x30)', 1, (80, 80, 80)),
}
_, text_y = buttons_text[1].get_size()
button_x, button_y = win_div_4, win_div_4 * 2 // 3
button_size = WINDOW_SIZE[0] - 2 * win_div_4, 2 * win_div_4 // 3

buttons = (
    ((buttons_text[0], (win_half - buttons_text[0].get_size()[0] // 2, win_div_4 - text_y // 2)),
     (button_x, button_y, *button_size)),

    ((buttons_text[1], (win_half - buttons_text[1].get_size()[0] // 2, 2 * win_div_4 - text_y // 2)),
     (win_div_4, button_y + win_div_4, *button_size)),

    ((buttons_text[2], (win_half - buttons_text[2].get_size()[0] // 2, 3 * win_div_4 - text_y // 2)),
     (win_div_4, button_y + 2 * win_div_4, *button_size))
)

was_pressed = 0
start_game = 0
is_pressed = 0
while 1:
    for button in buttons:
        pygame.draw.rect(screen, (100, 100, 100), button[1])
        screen.blit(*button[0])

    mouse_pos = pygame.mouse.get_pos()

    for i, button in enumerate(buttons):
        if button[1][1] <= mouse_pos[1] <= button[1][1] + button[1][3] and \
                win_div_4 <= mouse_pos[0] <= WINDOW_SIZE[0] - win_div_4:
            mode = i
            on_button = 1
            break
    else:
        on_button = 0

    if on_button:
        if is_pressed:
            pygame.draw.rect(screen, (150, 150, 150), buttons[mode][1])
            screen.blit(buttons_text[mode + 10], buttons[mode][0][1])
        elif was_pressed:
            pygame.quit()
            break

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            is_pressed = True
            was_pressed = True
        if event.type == MOUSEBUTTONUP and event.button == 1:
            is_pressed = False
            was_pressed = on_button

    pygame.display.update()

if mode == 1:
    rows, columns, minecount = 9, 9, 10
elif mode == 2:
    rows, columns, minecount = 16, 16, 40
else:
    rows, columns, minecount = 16, 30, 99

matrix = [[0] * columns for _ in range(rows)]
minecount_const = minecount
no_mine = ()


def generate():
    mines = [(x, y) for x in range(columns) for y in range(rows)]

    for x, y in ((x, y) for x in (-1, 0, 1) for y in (-1, 0, 1)):
        y_gr, x_gr = no_mine[1] + y, no_mine[0] + x
        if 0 <= x_gr < columns and 0 <= y_gr < rows:
            mines.pop(mines.index((x_gr, y_gr)))

    for _ in range(minecount_const):
        mine_x, mine_y = mines.pop(randrange(len(mines)))
        matrix[mine_y][mine_x] = -1
        for row, column in ((x, y) for x in (-1, 0, 1) for y in (-1, 0, 1)):
            y_gr, x_gr = mine_y + row, mine_x + column
            if 0 <= x_gr < columns and 0 <= y_gr < rows and matrix[y_gr][x_gr] != -1:
                matrix[y_gr][x_gr] += 1

    print(*(" ".join(map(str, line)).replace('0', '.').replace('-1', '*') for line in matrix), sep='\n')


def restart():
    global matrix, minecount, no_mine
    matrix = [[0] * columns for _ in range(rows)]
    minecount = minecount_const