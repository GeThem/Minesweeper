import Minesweeper
import pygame
from sys import exit

clock = pygame.time.Clock()

from pygame.locals import *

pygame.init()

pygame.display.set_caption('Minesweeper')
# tiles configuration
tile_size = 25
tile_color = (112, 146, 190)
active_tile_color = (142, 176, 220)
flag_img = pygame.image.load('flag.png')
flag_img = pygame.transform.scale(flag_img, (tile_size, tile_size))
# window size
boarder = 30
top_info_size = 60
WINDOW_SIZE = (1 + 2 * boarder + Minesweeper.columns * (tile_size + 1),
               1 + boarder + top_info_size + Minesweeper.rows * (tile_size + 1))
# screen design
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
background_color = (210, 210, 210)
play_background_color = (235, 235, 235)
screen.fill(background_color)
pygame.draw.rect(screen, play_background_color,
                 (boarder - 3, top_info_size - 3, WINDOW_SIZE[0] - 2 * boarder + 6, WINDOW_SIZE[1] - top_info_size - boarder + 6))
# covered tiles
tiles = tuple(tuple([x, True] for x in range(Minesweeper.columns)) for _ in range(Minesweeper.rows))

numbers_colors = {
    -1: (180, 0, 0),
    0: background_color,
    1: (0, 0, 0),
    2: (0, 0, 0),
    3: (0, 0, 0),
    4: (0, 0, 0),
    5: (0, 0, 0),
    6: (0, 0, 0),
    7: (0, 0, 0),
    8: (0, 0, 0),
}

is_pressed = False
was_pressed = False
tile_exists = False
was_pressed_counter = 0


def clear(x, y, cur_tile):
    if cur_tile > -1:
        number = pygame.font.SysFont('arial', 23, 1).render(str(cur_tile), 0,
                                                            numbers_colors[cur_tile])
        pygame.draw.rect(screen, background_color,
                         (1 + boarder + x * (tile_size + 1),
                          1 + top_info_size + y * (tile_size + 1),
                          tile_size, tile_size))
        screen.blit(number,
                    (8 + boarder + x * (tile_size + 1), top_info_size + y * (tile_size + 1)))
        tiles[y][x][1] = 2
        return True
    else:
        return False

while 1:
    sum_of_closed_tiles = 0
    # draw tiles
    for y, row in enumerate(tiles):
        for x, status in row:
            if status == 1:
                pygame.draw.rect(screen, tile_color,
                                 (1 + boarder + x * (tile_size + 1), 1 + top_info_size + y * (tile_size + 1),
                                  tile_size, tile_size))
                sum_of_closed_tiles += 1
            elif status == 3:
                pygame.draw.rect(screen, tile_color,
                                (1 + boarder + x * (tile_size + 1), 1 + top_info_size + y * (tile_size + 1),
                                tile_size, tile_size))
                screen.blit(flag_img, (1 + boarder + x * (tile_size + 1), 1 + top_info_size + y * (tile_size + 1)))
                sum_of_closed_tiles += 1
            else:
                cur_tile = Minesweeper.matrix[y][x]
                if cur_tile == 0 and status == 0:
                    for choice_y in (y, Minesweeper.rows, 1), (y - 1, -1, -1):
                        for y_2 in range(*choice_y):
                            row_was_cleaned = 0
                            for choice_x in (x, Minesweeper.columns), (x - 1, -1, -1):
                                for x_2 in range(*choice_x):
                                    if not clear(x_2, y_2, Minesweeper.matrix[y_2][x_2]) and \
                                            Minesweeper.matrix[y_2 - choice_y[2]][x_2] != 0:
                                        break
                                    row_was_cleaned += 1
                            if not row_was_cleaned:
                                break
                elif cur_tile == -1:
                    pygame.quit()
                    exit()


    # draw mine counter
    pygame.draw.rect(screen, tile_color,
                     (WINDOW_SIZE[0] / 2 - 30, top_info_size / 2 - 15, 60, 30))
    mine_count = pygame.font.SysFont('arial', 27, 1).render(str(Minesweeper.minecount), 0, (180, 50, 50))
    mine_count_size = mine_count.get_size()
    screen.blit(mine_count, (WINDOW_SIZE[0] / 2 - mine_count_size[0] / 2, top_info_size / 2 - mine_count_size[1] / 2))

    # mouse position processing
    mouse_pos = list(pygame.mouse.get_pos())
    mouse_pos_ind = [0, 0]
    if boarder+1 < mouse_pos[0] < WINDOW_SIZE[0]-1-boarder and 1+top_info_size < mouse_pos[1] < WINDOW_SIZE[1]-1-boarder:
        mouse_pos_ind[0] = (mouse_pos[0] - boarder - 1) // (tile_size + 1)
        mouse_pos_ind[1] = (mouse_pos[1] - top_info_size - 1) // (tile_size + 1)

        tile_exists = tiles[mouse_pos_ind[1]][mouse_pos_ind[0]][1]

        mouse_pos[0] = boarder + 1 + mouse_pos_ind[0] * (tile_size + 1)
        mouse_pos[1] = top_info_size + 1 + mouse_pos_ind[1] * (tile_size + 1)
    else:
        tile_exists = False

    if tile_exists:
        if is_pressed:
            if tile_exists == 1:
                pygame.draw.rect(screen, play_background_color, (mouse_pos[0], mouse_pos[1], tile_size, tile_size))
        elif was_pressed:
            if tile_exists == 1:
                cur_tile = Minesweeper.matrix[mouse_pos_ind[1]][mouse_pos_ind[0]]
                tiles[mouse_pos_ind[1]][mouse_pos_ind[0]][1] = 0
                was_pressed_counter += 1
                if was_pressed_counter == 1:
                    Minesweeper.no_mine = mouse_pos_ind[0], mouse_pos_ind[1]
                    Minesweeper.generate()
                number = pygame.font.SysFont('arial', 23, 1).render(str(cur_tile), 0, numbers_colors[cur_tile])
                pygame.draw.rect(screen, background_color,
                                 (1 + boarder + mouse_pos_ind[0] * (tile_size + 1),
                                  1 + top_info_size + mouse_pos_ind[1] * (tile_size + 1),
                                  tile_size, tile_size))
                screen.blit(number, (8 + boarder + mouse_pos_ind[0] * (tile_size + 1),
                                     top_info_size + mouse_pos_ind[1] * (tile_size + 1)))
            was_pressed = False
        else:
            if tile_exists == 1:
                pygame.draw.rect(screen, active_tile_color, (mouse_pos[0], mouse_pos[1], tile_size, tile_size))
            elif tile_exists == 3:
                pygame.draw.rect(screen, active_tile_color, (mouse_pos[0], mouse_pos[1], tile_size, tile_size))
                screen.blit(flag_img, (mouse_pos[0], mouse_pos[1]))
    # win condition
    if Minesweeper.minecount_const == sum_of_closed_tiles:
        pygame.quit()
        exit()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 3:
                if tile_exists:
                    if tiles[mouse_pos_ind[1]][mouse_pos_ind[0]][1] == 3:
                        tiles[mouse_pos_ind[1]][mouse_pos_ind[0]][1] = 1
                        Minesweeper.minecount += 1
                    elif tiles[mouse_pos_ind[1]][mouse_pos_ind[0]][1] == 1:
                        tiles[mouse_pos_ind[1]][mouse_pos_ind[0]][1] = 3
                        Minesweeper.minecount -= 1
            else:
                is_pressed = True
                was_pressed = True
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            is_pressed = False
            was_pressed = tile_exists
    pygame.display.update()
    clock.tick(30)