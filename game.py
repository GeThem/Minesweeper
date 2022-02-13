import Minesweeper as MS
import pygame
from sys import exit

clock = pygame.time.Clock()

from pygame.locals import *

pygame.init()

pygame.display.set_caption('MS')
# tiles configuration
tile_size = 26
tile_color = (112, 146, 190)
active_tile_color = (142, 176, 220)
flag_img = pygame.image.load('flag.png')
flag_img = pygame.transform.scale(flag_img, (tile_size, tile_size))
# window size
boarder = 30
top_info_size = 60
WINDOW_SIZE = (1 + 2 * boarder + MS.columns * (tile_size + 1),
               1 + boarder + top_info_size + MS.rows * (tile_size + 1))
# screen design
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
background_color = (210, 210, 210)
play_background_color = (235, 235, 235)
screen.fill(background_color)
pygame.draw.rect(screen, play_background_color,
                 (boarder - 3, top_info_size - 3, WINDOW_SIZE[0] - 2 * boarder + 6, WINDOW_SIZE[1] - top_info_size - boarder + 6))
# covered tiles
tiles = tuple(tuple([x, 1] for x in range(MS.columns)) for _ in range(MS.rows))

numbers_colors = {
    -1: (180, 0, 0),
    0: background_color,
    1: (65, 79, 188),
    2: (29, 105, 0),
    3: (170, 6, 8),
    4: (1, 2, 128),
    5: (123, 0, 0),
    6: (4, 122, 125),
    7: (176, 5, 7),
    8: (168, 6, 15),
}

is_pressed = False
was_pressed = False
tile_status = False
was_pressed_counter = 0


def clear(x, y, cur_tile, status):
    '''Returns False if there's a mine'''
    if cur_tile > -1 and 1 <= status <= 2:
        number = pygame.font.SysFont('miriam', tile_size, 1).render(str(cur_tile), 1, numbers_colors[cur_tile])
        n_size = number.get_size()
        pygame.draw.rect(screen, background_color,
                         (1 + boarder + x * (tile_size + 1), 1 + top_info_size + y * (tile_size + 1),
                          tile_size, tile_size))

        screen.blit(number, ((tile_size - n_size[0]) / 2 + 2 + boarder + x * (tile_size + 1), (tile_size - n_size[1]) / 2 + 2 + top_info_size + y * (tile_size + 1)))
        tiles[y][x][1] = 0
        return True
    else:
        return False


for y, row in enumerate(tiles):
    for x, status in row:
            pygame.draw.rect(screen, tile_color,
                            (1 + boarder + x * (tile_size + 1), 1 + top_info_size + y * (tile_size + 1),
                            tile_size, tile_size))

sum_of_closed_tiles = MS.rows * MS.columns
p_tile = 0
counter_prev = MS.minecount_const
while 1:
    cur_tile = ''
    # mouse position processing
    mouse_pos = list(pygame.mouse.get_pos())
    mouse_pos_ind = [0, 0]
    if boarder+1 < mouse_pos[0] < WINDOW_SIZE[0]-1-boarder and 1+top_info_size < mouse_pos[1] < WINDOW_SIZE[1]-1-boarder:
        mouse_pos_ind[0] = (mouse_pos[0] - boarder - 1) // (tile_size + 1)
        mouse_pos_ind[1] = (mouse_pos[1] - top_info_size - 1) // (tile_size + 1)

        tile_status = tiles[mouse_pos_ind[1]][mouse_pos_ind[0]][1]

        mouse_pos[0] = boarder + 1 + mouse_pos_ind[0] * (tile_size + 1)
        mouse_pos[1] = top_info_size + 1 + mouse_pos_ind[1] * (tile_size + 1)
    else:
        tile_status = 0

    if tile_status:
        if is_pressed:
            if tile_status in (1, 2):
                pygame.draw.rect(screen, play_background_color, (mouse_pos[0], mouse_pos[1], tile_size, tile_size))
        elif was_pressed:
            if tile_status in (1, 2):
                tiles[mouse_pos_ind[1]][mouse_pos_ind[0]][1] = 0
                cur_tile = (mouse_pos_ind[0], mouse_pos_ind[1], 0, MS.matrix[mouse_pos_ind[1]][mouse_pos_ind[0]])
                was_pressed_counter += 1
                if was_pressed_counter == 1:
                    MS.no_mine = mouse_pos_ind[0], mouse_pos_ind[1]
                    MS.generate()
            was_pressed = False
        else:
            if tile_status == 1:
                pygame.draw.rect(screen, active_tile_color, (mouse_pos[0], mouse_pos[1], tile_size, tile_size))
                tiles[mouse_pos_ind[1]][mouse_pos_ind[0]][1] = 2
            elif tile_status == 3:
                pygame.draw.rect(screen, active_tile_color, (mouse_pos[0], mouse_pos[1], tile_size, tile_size))
                screen.blit(flag_img, (mouse_pos[0], mouse_pos[1]))
                tiles[mouse_pos_ind[1]][mouse_pos_ind[0]][1] = 4
        tile_status = tiles[mouse_pos_ind[1]][mouse_pos_ind[0]][1]

    # draw tiles
    if p_tile and p_tile[:2] != mouse_pos_ind:
        if p_tile[2] in (1, 2):
            pygame.draw.rect(screen, tile_color,
                            (1 + boarder + p_tile[0] * (tile_size + 1), 1 + top_info_size + p_tile[1] * (tile_size + 1),
                            tile_size, tile_size))
            tiles[p_tile[1]][p_tile[0]][1] = 1
        elif p_tile[2] == 4:
            pygame.draw.rect(screen, tile_color,
                            (1 + boarder + p_tile[0] * (tile_size + 1), 1 + top_info_size + p_tile[1] * (tile_size + 1),
                            tile_size, tile_size))
            screen.blit(flag_img, (1 + boarder + p_tile[0] * (tile_size + 1), 1 + top_info_size + p_tile[1] * (tile_size + 1)))
            tiles[p_tile[1]][p_tile[0]][1] = 3
    if isinstance(cur_tile, tuple):
        if cur_tile[3] == 0:
            clear(mouse_pos_ind[0], mouse_pos_ind[1], cur_tile[3], 1)
            sum_of_closed_tiles -= 1
            for choicey in (cur_tile[1], MS.rows, 1), (MS.rows - 2, -1, -1), (1, MS.rows, 1):
                for y2 in range(*choicey):
                    row_was_cleaned = 0
                    for choicex in (cur_tile[0] + 1, MS.columns, 1), (MS.columns-2, -1, -1), (1, MS.columns, 1):
                        for x2 in range(*choicex):
                            if MS.matrix[y2][x2-choicex[2]] == 0 or MS.matrix[y2 - choicey[2]][x2] == 0:
                                if clear(x2, y2, MS.matrix[y2][x2], tiles[y2][x2][1]):
                                    sum_of_closed_tiles -= 1
                    if not row_was_cleaned:
                        break
        elif cur_tile[3] == -1:
            pygame.quit()
            exit()
        else:
            clear(mouse_pos_ind[0], mouse_pos_ind[1], cur_tile[3], 1)
            sum_of_closed_tiles -= 1

    p_tile = [mouse_pos_ind[0], mouse_pos_ind[1], tile_status]

    # draw mine counter
    if MS.minecount != counter_prev or was_pressed_counter == 0:
        counter_prev = MS.minecount
        pygame.draw.rect(screen, tile_color,
                         (WINDOW_SIZE[0] / 2 - 30, top_info_size / 2 - 15, 60, 30))
        mine_count = pygame.font.SysFont('arial', 27, 1).render(str(counter_prev), 1, (180, 50, 50))
        mine_count_size = mine_count.get_size()
        screen.blit(mine_count, (WINDOW_SIZE[0] / 2 - mine_count_size[0] / 2, top_info_size / 2 - mine_count_size[1] / 2))

    # win condition
    if MS.minecount_const == sum_of_closed_tiles:
        pygame.quit()
        exit()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 3:
                if tile_status == 4:
                    p_tile[2] = 2
                    pygame.draw.rect(screen, active_tile_color,
                                    (1 + boarder + p_tile[0] * (tile_size + 1),
                                    1 + top_info_size + p_tile[1] * (tile_size + 1),
                                    tile_size, tile_size))

                    MS.minecount += 1
                elif tile_status == 2:
                    p_tile[2] = 4
                    pygame.draw.rect(screen, active_tile_color,
                                    (1 + boarder + p_tile[0] * (tile_size + 1),
                                    1 + top_info_size + p_tile[1] * (tile_size + 1),
                                    tile_size, tile_size))
                    screen.blit(flag_img, (
                        1 + boarder + p_tile[0] * (tile_size + 1),
                        1 + top_info_size + p_tile[1] * (tile_size + 1)))
                    MS.minecount -= 1
                    print(p_tile)
            else:
                is_pressed = True
                was_pressed = True
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            is_pressed = False
            was_pressed = tile_status
    pygame.display.update()
    clock.tick(30)