import Minesweeper as MS
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from sys import exit
from time import time

clock = pygame.time.Clock()

pygame.init()

pygame.display.set_caption('Minesweeper')

# background colors
behind_tiles_color = (235, 235, 235)
background_color = (191, 196, 199)
# tiles configuration
tile_size = 30
tile_color = (112, 146, 190)
active_tile_color = (142, 176, 220)
open_tile_color = (191, 204, 215)
tiles = tuple([1] * MS.columns for _ in range(MS.rows))
tile_status = 0  # 0 - closed tile/mouse out of screen, 1 - closed, 2 - closed active, 5 - flagged, 6 - flagged active
# images
flag_img = pygame.image.load('flag.png')
flag_img = pygame.transform.scale(flag_img, (tile_size, tile_size))
mine_img = pygame.image.load('mine.png')
mine_img = pygame.transform.scale(mine_img, (tile_size, tile_size))
no_mine_img = pygame.image.load('no_mine.png')
no_mine_img = pygame.transform.scale(no_mine_img, (tile_size, tile_size))

numbers_colors = {
    1: (65, 79, 188),
    2: (29, 105, 0),
    3: (170, 6, 8),
    4: (1, 2, 128),
    5: (123, 0, 0),
    6: (4, 122, 125),
    7: (176, 5, 7),
    8: (168, 6, 15),
}

# window size
boarder = 30
top_info_size = 80
WINDOW_SIZE = (1 + 2 * boarder + MS.columns * (tile_size + 1),
               1 + boarder + top_info_size + MS.rows * (tile_size + 1))
# screen design
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
screen.fill(background_color)
pygame.draw.rect(screen, behind_tiles_color,
                 (boarder - 3, top_info_size - 3, WINDOW_SIZE[0] - 2 * boarder + 6,
                  WINDOW_SIZE[1] - top_info_size - boarder + 6))
# mouse variables
is_pressed = False
was_pressed = False
was_pressed_counter = 0


def clear(x, y, status):
    if 1 <= status <= 4:
        coords = 1 + boarder + x * (tile_size + 1), 1 + top_info_size + y * (tile_size + 1)
        cur_elem = MS.matrix[y][x]
        pygame.draw.rect(screen, open_tile_color, (*coords, tile_size, tile_size))
        if cur_elem > 0 and 1 <= status <= 2:
            number = pygame.font.SysFont('miriam', tile_size, 1).render(str(cur_elem), 1, numbers_colors[cur_elem])
            n_size = number.get_size()
            screen.blit(number, ((tile_size - n_size[0]) / 2 + 2 + boarder + x * (tile_size + 1),
                                 (tile_size - n_size[1]) / 2 + 2 + top_info_size + y * (tile_size + 1)))
        elif status == 3:
            if cur_elem == -1:
                screen.blit(mine_img, (*coords, tile_size, tile_size))
            elif cur_elem:
                number = pygame.font.SysFont('miriam', tile_size, 1).render(str(cur_elem), 1, numbers_colors[cur_elem])
                n_size = number.get_size()
                screen.blit(number, ((tile_size - n_size[0]) / 2 + 2 + boarder + x * (tile_size + 1),
                                     (tile_size - n_size[1]) / 2 + 2 + top_info_size + y * (tile_size + 1)))
        elif status == 4:
            if cur_elem == -1:
                screen.blit(mine_img, (*coords, tile_size, tile_size))
                screen.blit(flag_img, (*coords, tile_size, tile_size))
            else:
                screen.blit(no_mine_img, (*coords, tile_size, tile_size))
        tiles[y][x] = 0
    elif 7 <= status <= 8:
        if status == 7:
            screen.blit(mine_img, (1 + boarder + x * (tile_size + 1), 1 + top_info_size + y * (tile_size + 1)))
        tiles[y][x] = 0


def find_move(x, y):
    if x > 0:
        if MS.matrix[y][x - 1] == 0 and tiles[y][x - 1] == 1:
            return x - 1, y
        if y < MS.rows - 1 and MS.matrix[y + 1][x - 1] == 0 and tiles[y + 1][x - 1] == 1:
            return x - 1, y + 1
        if y > 0 and MS.matrix[y - 1][x - 1] == 0 and tiles[y - 1][x - 1] == 1:
            return x - 1, y - 1

    if x < MS.columns - 1:
        if y > 0 and MS.matrix[y - 1][x + 1] == 0 and tiles[y - 1][x + 1] == 1:
            return x + 1, y - 1
        if MS.matrix[y][x + 1] == 0 and tiles[y][x + 1] == 1:
            return x + 1, y
        if y < MS.rows - 1 and MS.matrix[y + 1][x + 1] == 0 and tiles[y + 1][x + 1] == 1:
            return x + 1, y + 1

    if y < MS.rows - 1 and MS.matrix[y + 1][x] == 0 and tiles[y + 1][x] == 1:
        return x, y + 1
    if y > 0 and MS.matrix[y - 1][x] == 0 and tiles[y - 1][x] == 1:
        return x, y - 1

    return -1, -1


# draw closed tiles
for y in range(MS.rows):
    for x in range(MS.columns):
        pygame.draw.rect(screen, tile_color,
                         (1 + boarder + x * (tile_size + 1), 1 + top_info_size + y * (tile_size + 1),
                          tile_size, tile_size))

time_start = 0
time_now = 0
sum_of_closed_tiles = MS.rows * MS.columns
p_tile = 0
counter_prev = MS.minecount_const
game_is_going = 1
while 1:
    pressed_tile = 0
    # mouse position processing
    mouse_pos = list(pygame.mouse.get_pos())
    cur_tile = [-1, -1]
    if boarder + 1 < mouse_pos[0] < WINDOW_SIZE[0] - 1 - boarder and \
            1 + top_info_size < mouse_pos[1] < WINDOW_SIZE[1] - 1 - boarder:

        cur_tile = [(mouse_pos[0] - boarder - 1) // (tile_size + 1),
                    (mouse_pos[1] - top_info_size - 1) // (tile_size + 1)]
        tile_status = tiles[cur_tile[1]][cur_tile[0]]

        mouse_pos = boarder + 1 + cur_tile[0] * (tile_size + 1), top_info_size + 1 + cur_tile[1] * (tile_size + 1)
    else:
        tile_status = 0

    if tile_status:
        if is_pressed:
            if tile_status in (1, 2):
                pygame.draw.rect(screen, open_tile_color, (mouse_pos[0], mouse_pos[1], tile_size, tile_size))
        elif was_pressed:
            if tile_status in (1, 2):
                tiles[cur_tile[1]][cur_tile[0]] = 0
                pressed_tile = (cur_tile[0], cur_tile[1], 0, MS.matrix[cur_tile[1]][cur_tile[0]])
                was_pressed_counter += 1
                if was_pressed_counter == 1:
                    MS.no_mine = cur_tile[0], cur_tile[1]
                    MS.generate()
                    time_start = time()
            was_pressed = False
        else:
            if tile_status == 1:
                pygame.draw.rect(screen, active_tile_color, (mouse_pos[0], mouse_pos[1], tile_size, tile_size))
                tiles[cur_tile[1]][cur_tile[0]] = 2
            elif tile_status == 5:
                pygame.draw.rect(screen, active_tile_color, (mouse_pos[0], mouse_pos[1], tile_size, tile_size))
                screen.blit(flag_img, (mouse_pos[0], mouse_pos[1]))
                tiles[cur_tile[1]][cur_tile[0]] = 6
        tile_status = tiles[cur_tile[1]][cur_tile[0]]

    # draw tiles
    if p_tile and p_tile[:2] != cur_tile:
        if p_tile[2] in (1, 2):
            pygame.draw.rect(screen, tile_color, (*coords, tile_size, tile_size))
            tiles[p_tile[1]][p_tile[0]] = 1
        elif p_tile[2] == 6:
            pygame.draw.rect(screen, tile_color, (*coords, tile_size, tile_size))
            screen.blit(flag_img,
                        (1 + boarder + p_tile[0] * (tile_size + 1), 1 + top_info_size + p_tile[1] * (tile_size + 1)))
            tiles[p_tile[1]][p_tile[0]] = 5
    # if right button was released on closed tile, draw numbers
    if isinstance(pressed_tile, tuple):
        if pressed_tile[3] == 0:
            x2, y2 = pressed_tile[:2]
            storage = [(x2, y2)]
            while 0 <= x2 <= MS.columns - 1 and 0 <= y2 <= MS.rows - 1:
                x2, y2 = find_move(x2, y2)
                if x2 == -1:
                    if storage:
                        x2, y2 = storage.pop()
                        sum_of_closed_tiles -= 1
                        # looks for closed nums around opened empty tile and opens it 
                        if x2 > 0:
                            if MS.matrix[y2][x2 - 1] != 0 and tiles[y2][x2 - 1] == 1:
                                clear(x2 - 1, y2, 1)
                                sum_of_closed_tiles -= 1
                            if y2 > 0 and MS.matrix[y2 - 1][x2 - 1] != 0 and tiles[y2 - 1][x2 - 1] == 1:
                                clear(x2 - 1, y2 - 1, 1)
                                sum_of_closed_tiles -= 1
                            if y2 < MS.rows - 1 and MS.matrix[y2 + 1][x2 - 1] != 0 and tiles[y2 + 1][x2 - 1] == 1:
                                clear(x2 - 1, y2 + 1, 1)
                                sum_of_closed_tiles -= 1

                        if x2 < MS.columns - 1:
                            if MS.matrix[y2][x2 + 1] != 0 and tiles[y2][x2 + 1] == 1:
                                clear(x2 + 1, y2, 1)
                                sum_of_closed_tiles -= 1
                            if y2 > 0 and MS.matrix[y2 - 1][x2 + 1] != 0 and tiles[y2 - 1][x2 + 1] == 1:
                                clear(x2 + 1, y2 - 1, 1)
                                sum_of_closed_tiles -= 1
                            if y2 < MS.rows - 1 and MS.matrix[y2 + 1][x2 + 1] != 0 and tiles[y2 + 1][x2 + 1] == 1:
                                clear(x2 + 1, y2 + 1, 1)
                                sum_of_closed_tiles -= 1

                        if y2 > 0 and MS.matrix[y2 - 1][x2] != 0 and tiles[y2 - 1][x2] == 1:
                            clear(x2, y2 - 1, 1)
                            sum_of_closed_tiles -= 1
                        if y2 < MS.rows - 1 and MS.matrix[y2 + 1][x2] != 0 and tiles[y2 + 1][x2] == 1:
                            clear(x2, y2 + 1, 1)
                            sum_of_closed_tiles -= 1

                        continue
                    else:
                        break
                storage.append((x2, y2))
                clear(x2, y2, 1)

        # lose
        elif pressed_tile[3] == -1:
            game_is_going = 0
            clear(pressed_tile[0], pressed_tile[1], 3)
            for y, row in enumerate(tiles):
                for x, status in enumerate(row):
                    if 1 <= status <= 2:
                        clear(x, y, 3)
                    if 5 <= status <= 6:
                        clear(x, y, 4)
        else:
            clear(pressed_tile[0], pressed_tile[1], 1)
            sum_of_closed_tiles -= 1

    p_tile = [cur_tile[0], cur_tile[1], tile_status]
    coords = 1 + boarder + p_tile[0] * (tile_size + 1), 1 + top_info_size + p_tile[1] * (tile_size + 1)

    # draw mine counter
    if MS.minecount != counter_prev or was_pressed_counter == 0:
        counter_prev = MS.minecount
        pygame.draw.rect(screen, tile_color,
                         (WINDOW_SIZE[0] / 2 - 30, top_info_size / 2 - 24, 60, 46))
        mine_count = pygame.font.SysFont('arial', 37, 1).render(str(counter_prev), 1, (150, 2, 2))
        mine_count_sz = mine_count.get_size()
        screen.blit(mine_count, (WINDOW_SIZE[0] / 2 - mine_count_sz[0] / 2, top_info_size / 2 - mine_count_sz[1] / 2))

    # draw timer
    if time_now <= 999 and game_is_going:
        if time_start:
            time_now = time() - time_start
        pygame.draw.rect(screen, tile_color,
                         (WINDOW_SIZE[0] * 4 / 5 - 36, top_info_size / 2 - 18, 72, 36))
        timer = pygame.font.SysFont('arial', 29, 1).render(f'{time_now:.1f}', 1, (230, 230, 230))
        timer_size = timer.get_size()
        screen.blit(timer, (WINDOW_SIZE[0] * 4 / 5 - timer_size[0] / 2, top_info_size / 2 - timer_size[1] / 2))

    # win
    if MS.minecount_const == sum_of_closed_tiles and game_is_going:
        game_is_going = 0
        MS.minecount = 0
        clear(pressed_tile[0], pressed_tile[1], pressed_tile[2])
        for y, row in enumerate(tiles):
            for x, status in enumerate(row):
                if status == 1:
                    clear(x, y, 7)
                elif status == 5:
                    clear(x, y, 8)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == MOUSEBUTTONDOWN:
            # flag actions
            if event.button == 3:
                if tile_status == 6:
                    tiles[p_tile[1]][p_tile[0]] = p_tile[2] = 2
                    pygame.draw.rect(screen, active_tile_color, (*coords, tile_size, tile_size))
                    MS.minecount += 1
                elif tile_status == 2:
                    tiles[p_tile[1]][p_tile[0]] = p_tile[2] = 6
                    pygame.draw.rect(screen, active_tile_color, (*coords, tile_size, tile_size))
                    screen.blit(flag_img, coords)
                    MS.minecount -= 1
            else:
                is_pressed = True
                was_pressed = True
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            is_pressed = False
            was_pressed = tile_status
    pygame.display.update()
    clock.tick(60)
