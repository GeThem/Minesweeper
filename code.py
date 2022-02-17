import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from sys import exit
from time import time
from random import randrange
from os.path import join as join_path

clock = pygame.time.Clock()

pygame.init()

# ------------------------------------------PLAYGROUND GENERATION------------------------------------------- #
matrix = []  # creates in game.py


def generate(rows, columns, minecount, no_mine):
    global matrix
    matrix = [[0] * columns for _ in range(rows)]
    mines = [(x, y) for x in range(columns) for y in range(rows)]

    for x, y in ((x, y) for x in range(-1, 2) for y in range(-1, 2)):
        y_gr, x_gr = no_mine[1] + y, no_mine[0] + x
        if 0 <= x_gr < columns and 0 <= y_gr < rows:
            mines.pop(mines.index((x_gr, y_gr)))

    for _ in range(minecount):
        mine_x, mine_y = mines.pop(randrange(len(mines)))
        matrix[mine_y][mine_x] = -1
        for row, column in ((x, y) for x in range(-1, 2) for y in range(-1, 2)):
            y_gr, x_gr = mine_y + row, mine_x + column
            if 0 <= x_gr < columns and 0 <= y_gr < rows and matrix[y_gr][x_gr] != -1:
                matrix[y_gr][x_gr] += 1


# ------------------------------------------MODE MENU VARIABLES--------------------------------------------- #
WINDOW_SIZE_options = (500, 300)
win_half = WINDOW_SIZE_options[0] // 2
win_div_4 = WINDOW_SIZE_options[1] // 4

background_color = (191, 196, 205)

buttons_text = {
        0: pygame.font.SysFont('miriam', 22, 1).render('Newbie 10 mines (9x9)', 1, (70, 70, 70)),
        1: pygame.font.SysFont('miriam', 22, 1).render('Amateur 40 mines (16x16)', 1, (70, 70, 70)),
        2: pygame.font.SysFont('miriam', 22, 1).render('Professional 99 mines (16x30)', 1, (70, 70, 70)),
        10: pygame.font.SysFont('miriam', 22, 1).render('Newbie 10 mines (9x9)', 1, (230, 230, 230)),
        11: pygame.font.SysFont('miriam', 22, 1).render('Amateur 40 mines (16x16)', 1, (230, 230, 230)),
        12: pygame.font.SysFont('miriam', 22, 1).render('Professional 99 mines (16x30)', 1, (230, 230, 230)),
    }
_, text_y = buttons_text[1].get_size()
button_x, button_y = win_div_4, win_div_4 * 2 // 3
button_size = WINDOW_SIZE_options[0] - 2 * win_div_4, 2 * win_div_4 // 3

buttons = (
    ((buttons_text[0], (win_half - buttons_text[0].get_size()[0] // 2, win_div_4 - text_y // 2)),
     pygame.Rect(button_x, button_y, *button_size)),

    ((buttons_text[1], (win_half - buttons_text[1].get_size()[0] // 2, 2 * win_div_4 - text_y // 2)),
     pygame.Rect(win_div_4, button_y + win_div_4, *button_size)),

    ((buttons_text[2], (win_half - buttons_text[2].get_size()[0] // 2, 3 * win_div_4 - text_y // 2)),
     pygame.Rect(win_div_4, button_y + 2 * win_div_4, *button_size))
)

# ----------------------------------------------GAME VARIABLES------------------------------------------------- #
# background colors
behind_tiles_color = (225, 225, 225)
buttons_color = (210, 220, 220)
# tiles configuration
tile_size = 34
tile_color = (102, 146, 233)
active_tile_color = (142, 176, 220)
open_tile_color = (191, 204, 225)
# images
path_imgs = 'data/images'
flag_img = pygame.image.load(join_path(path_imgs, 'flag.png'))
mine_img = pygame.image.load(join_path(path_imgs, 'mine.png'))
no_mine_img = pygame.image.load(join_path(path_imgs, 'no_mine.png'))

go_to_menu = pygame.image.load(join_path(path_imgs, 'go_to_menu.png'))
go_to_menu_activated = go_to_menu.copy()
go_to_menu_activated.set_alpha(200)

beybo = pygame.image.load(join_path(path_imgs, 'beybo.png'))
re_press = pygame.image.load(join_path(path_imgs, 'r_button_pressed.png'))
oh_no = pygame.image.load(join_path(path_imgs, 'oh_no.png'))
static = pygame.image.load(join_path(path_imgs, 'static.png'))
win = pygame.image.load(join_path(path_imgs, 'win.png'))

nums = {
    1: pygame.font.SysFont('miriam', tile_size, 1).render('1', 1, (65, 79, 188)),
    2: pygame.font.SysFont('miriam', tile_size, 1).render('2', 1, (29, 105, 0)),
    3: pygame.font.SysFont('miriam', tile_size, 1).render('3', 1, (170, 6, 8)),
    4: pygame.font.SysFont('miriam', tile_size, 1).render('4', 1, (1, 2, 128)),
    5: pygame.font.SysFont('miriam', tile_size, 1).render('5', 1, (123, 0, 0)),
    6: pygame.font.SysFont('miriam', tile_size, 1).render('6', 1, (4, 122, 125)),
    7: pygame.font.SysFont('miriam', tile_size, 1).render('7', 1, (176, 5, 7)),
    8: pygame.font.SysFont('miriam', tile_size, 1).render('8', 1, (168, 6, 15)),
    'size': 0
}
nums['size'] = nums[1].get_size()


# -------------------------------------------MAIN MENU------------------------------------------------------ #
def main_menu():
    pygame.display.set_caption('Minesweeper: Mode selection')
    pygame.display.set_icon(pygame.image.load(join_path(path_imgs, 'mine.png')))
    screen = pygame.display.set_mode(WINDOW_SIZE_options, 0, 32)
    screen.fill(background_color)
    was_pressed = 0
    is_pressed = 0
    while 1:
        on_button = 0

        for button in buttons:
            pygame.draw.rect(screen, (150, 150, 150), button[1])
            screen.blit(*button[0])

        mouse_pos = pygame.mouse.get_pos()

        for i, button in enumerate(buttons):
            if on_button := button[1].collidepoint(*mouse_pos):
                mode = i
                if is_pressed:
                    pygame.draw.rect(screen, (100, 100, 100), buttons[mode][1])
                    screen.blit(buttons_text[mode + 10], buttons[mode][0][1])
                elif was_pressed:
                    if mode == 0:
                        rows, columns, minecount = 9, 9, 10
                    elif mode == 1:
                        rows, columns, minecount = 16, 16, 40
                    else:
                        rows, columns, minecount = 16, 30, 99

                    while game(rows, columns, minecount):
                        pass

                    was_pressed = False
                    pygame.display.set_caption('Minesweeper: Mode selection')
                    screen = pygame.display.set_mode(WINDOW_SIZE_options, 0, 32)
                    screen.fill(background_color)
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
        clock.tick(60)


# -------------------------------------------GAME EXECUTION------------------------------------------------------ #
def game(rows, columns, minecount):
    global beybo, re_press
    # window size
    boarder = 30
    top_info_size = 80
    WINDOW_SIZE = (1 + 2 * boarder + columns * (tile_size + 1),
                   1 + boarder + top_info_size + rows * (tile_size + 1))

    minecount_const = minecount
    # screen design
    pygame.display.set_caption('Minesweeper')
    screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
    screen.fill(background_color)
    pygame.draw.rect(screen, (80, 80, 80),
                     (boarder - 2, top_info_size - 2, WINDOW_SIZE[0] - 2 * boarder + 4,
                      WINDOW_SIZE[1] - top_info_size - boarder + 4))
    pygame.draw.rect(screen, behind_tiles_color,
                     (boarder, top_info_size, WINDOW_SIZE[0] - 2 * boarder,
                      WINDOW_SIZE[1] - top_info_size - boarder))

    tiles = tuple([1] * columns for _ in range(rows))
    tile_status = 0  # 0 - closed tile/mouse out of screen, 1 - closed, 2 - closed active, 5 - flagged, 6 - flagged active

    # mouse variables
    is_pressed = False
    was_pressed = False
    was_pressed_counter = 0
    was_pressed_normal = False

    def open(x, y, status):
        """
        Opens a tile

        status variations:
            1-3: open everything
            for the end of a game:
                4: for opening flag tiles
                7: diactivate closed tile with mine
                8: diactivate closed flagged tile
        """
        if 1 <= status <= 4:
            coords = 1 + boarder + x * (tile_size + 1), 1 + top_info_size + y * (tile_size + 1)
            cur_elem = matrix[y][x]
            pygame.draw.rect(screen, open_tile_color, (*coords, tile_size, tile_size))
            if 1 <= status <= 3:
                if cur_elem == -1:
                    screen.blit(mine_img, (*coords, tile_size, tile_size))
                elif cur_elem:
                    screen.blit(nums[cur_elem], ((tile_size - nums['size'][0]) / 2 + 2 + boarder + x * (tile_size + 1),
                                         (tile_size - nums['size'][1]) / 2 + 2 + top_info_size + y * (tile_size + 1)))
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
        """Finds closed empty tile around tile[y][x]"""
        if x > 0:
            if matrix[y][x - 1] == 0 and tiles[y][x - 1] == 1:
                return x - 1, y
            if y < rows - 1 and matrix[y + 1][x - 1] == 0 and tiles[y + 1][x - 1] == 1:
                return x - 1, y + 1
            if y > 0 and matrix[y - 1][x - 1] == 0 and tiles[y - 1][x - 1] == 1:
                return x - 1, y - 1

        if x < columns - 1:
            if y > 0 and matrix[y - 1][x + 1] == 0 and tiles[y - 1][x + 1] == 1:
                return x + 1, y - 1
            if matrix[y][x + 1] == 0 and tiles[y][x + 1] == 1:
                return x + 1, y
            if y < rows - 1 and matrix[y + 1][x + 1] == 0 and tiles[y + 1][x + 1] == 1:
                return x + 1, y + 1

        if y < rows - 1 and matrix[y + 1][x] == 0 and tiles[y + 1][x] == 1:
            return x, y + 1
        if y > 0 and matrix[y - 1][x] == 0 and tiles[y - 1][x] == 1:
            return x, y - 1

        return -1, -1

    # draw closed tiles
    for y in range(rows):
        for x in range(columns):
            pygame.draw.rect(screen, tile_color,
                             (1 + boarder + x * (tile_size + 1), 1 + top_info_size + y * (tile_size + 1),
                              tile_size, tile_size))

    time_start = 0
    time_now = 0
    sum_of_closed_tiles = rows * columns
    p_tile = 0
    counter_prev = minecount_const
    game_is_going = 1

    restart_button = pygame.Rect(77, 13, 54, 54)
    menu_button = pygame.Rect(boarder - 1, 13, 40, 54)
    # minecounter and timer outline
    pygame.draw.rect(screen, behind_tiles_color, (WINDOW_SIZE[0] / 2 - 31, top_info_size / 2 - 25, 62, 48))
    pygame.draw.rect(screen, behind_tiles_color, (WINDOW_SIZE[0] * 4 / 5 - 37, top_info_size / 2 - 19, 74, 38))

    pygame.draw.rect(screen, (100, 100, 100), menu_button)
    pygame.draw.rect(screen, buttons_color, (boarder - 1, 13, 39, 53))
    screen.blit(go_to_menu, menu_button)
    while 1:
        pressed_tile = 0

        pygame.draw.rect(screen, (100, 100, 100), (77, 13, 54, 54))
        pygame.draw.rect(screen, buttons_color, (77, 13, 53, 53))

        if game_is_going:
            screen.blit(static, restart_button)
        elif lose:
            screen.blit(beybo, restart_button)
        else:
            screen.blit(win, restart_button)

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

        # buttons
        if restart_button.collidepoint(*mouse_pos):
            if is_pressed:
                pygame.draw.rect(screen, (100, 100, 100), (77, 13, 54, 54))
                pygame.draw.rect(screen, (180, 180, 180), (78, 14, 53, 53))
                screen.blit(re_press, restart_button)
                was_pressed_normal = True
            elif was_pressed_normal:
                return True
        elif menu_button.collidepoint(*mouse_pos):
            if is_pressed:
                pygame.draw.rect(screen, (100, 100, 100), menu_button)
                pygame.draw.rect(screen, (180, 180, 180), (boarder, 14, 39, 53))
                screen.blit(go_to_menu_activated, menu_button)
                was_pressed_normal = True
            elif was_pressed_normal:
                return False
        elif was_pressed_normal:
            pygame.draw.rect(screen, (100, 100, 100), menu_button)
            pygame.draw.rect(screen, buttons_color, (boarder - 1, 13, 39, 53))
            screen.blit(go_to_menu, menu_button)
            was_pressed_normal = False

        if tile_status:
            if is_pressed:
                if tile_status in (1, 2):
                    pygame.draw.rect(screen, buttons_color, (77, 13, 53, 53))
                    screen.blit(oh_no, restart_button)
                    pygame.draw.rect(screen, open_tile_color, (mouse_pos[0], mouse_pos[1], tile_size, tile_size))
            elif was_pressed:
                if tile_status in (1, 2):
                    if was_pressed_counter == 0:
                        generate(rows, columns, minecount_const, cur_tile)
                        time_start = time()
                        was_pressed_counter += 1
                    pressed_tile = (*cur_tile, 0, matrix[cur_tile[1]][cur_tile[0]])
                    tiles[cur_tile[1]][cur_tile[0]] = 0
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
                open(x2, y2, 1)
                storage = [(x2, y2)]
                while 0 <= x2 < columns and 0 <= y2 < rows:
                    x2, y2 = find_move(x2, y2)
                    if x2 == -1:
                        if storage:
                            x2, y2 = storage.pop()
                            sum_of_closed_tiles -= 1

                            # looks for closed nums around opened empty tile and opens it
                            if x2 > 0:
                                if matrix[y2][x2 - 1] != 0 and tiles[y2][x2 - 1] == 1:
                                    open(x2 - 1, y2, 1)
                                    sum_of_closed_tiles -= 1
                                if y2 > 0 and matrix[y2 - 1][x2 - 1] != 0 and tiles[y2 - 1][x2 - 1] == 1:
                                    open(x2 - 1, y2 - 1, 1)
                                    sum_of_closed_tiles -= 1
                                if y2 < rows - 1 and matrix[y2 + 1][x2 - 1] != 0 and tiles[y2 + 1][x2 - 1] == 1:
                                    open(x2 - 1, y2 + 1, 1)
                                    sum_of_closed_tiles -= 1
                            if x2 < columns - 1:
                                if matrix[y2][x2 + 1] != 0 and tiles[y2][x2 + 1] == 1:
                                    open(x2 + 1, y2, 1)
                                    sum_of_closed_tiles -= 1
                                if y2 > 0 and matrix[y2 - 1][x2 + 1] != 0 and tiles[y2 - 1][x2 + 1] == 1:
                                    open(x2 + 1, y2 - 1, 1)
                                    sum_of_closed_tiles -= 1
                                if y2 < rows - 1 and matrix[y2 + 1][x2 + 1] != 0 and tiles[y2 + 1][x2 + 1] == 1:
                                    open(x2 + 1, y2 + 1, 1)
                                    sum_of_closed_tiles -= 1
                            if y2 > 0 and matrix[y2 - 1][x2] != 0 and tiles[y2 - 1][x2] == 1:
                                open(x2, y2 - 1, 1)
                                sum_of_closed_tiles -= 1
                            if y2 < rows - 1 and matrix[y2 + 1][x2] != 0 and tiles[y2 + 1][x2] == 1:
                                open(x2, y2 + 1, 1)
                                sum_of_closed_tiles -= 1

                            continue
                        break
                    storage.append((x2, y2))
                    open(x2, y2, 1)

            # lose
            elif pressed_tile[3] == -1:
                lose = 1
                game_is_going = 0
                open(pressed_tile[0], pressed_tile[1], 3)
                for y, row in enumerate(tiles):
                    for x, status in enumerate(row):
                        if 1 <= status <= 2:
                            open(x, y, 3)
                        if 5 <= status <= 6:
                            open(x, y, 4)
            else:
                open(pressed_tile[0], pressed_tile[1], 1)
                sum_of_closed_tiles -= 1

        p_tile = [cur_tile[0], cur_tile[1], tile_status]
        coords = 1 + boarder + p_tile[0] * (tile_size + 1), 1 + top_info_size + p_tile[1] * (tile_size + 1)

        # draw mine counter
        if minecount != counter_prev or was_pressed_counter == 0:
            counter_prev = minecount
            pygame.draw.rect(screen, active_tile_color,
                             (WINDOW_SIZE[0] / 2 - 30, top_info_size / 2 - 24, 60, 46))

            mine_count = pygame.font.SysFont('arial', 37, 1).render(str(counter_prev), 1, (180, 0, 0))
            mine_count_sz = mine_count.get_size()
            screen.blit(mine_count, (WINDOW_SIZE[0] / 2 - mine_count_sz[0] / 2, top_info_size / 2 - mine_count_sz[1] / 2))

        # draw timer
        if time_now <= 999 and game_is_going:
            if time_start:
                time_now = time() - time_start
            pygame.draw.rect(screen, active_tile_color,
                             (WINDOW_SIZE[0] * 4 / 5 - 36, top_info_size / 2 - 18, 72, 36))
            timer = pygame.font.SysFont('arial', 29, 1).render(f'{time_now:.1f}', 1, (230, 230, 230))
            timer_size = timer.get_size()
            screen.blit(timer, (WINDOW_SIZE[0] * 4 / 5 - timer_size[0] / 2, top_info_size / 2 - timer_size[1] / 2))

        # win
        if minecount_const == sum_of_closed_tiles and game_is_going:
            lose = 0
            game_is_going = 0
            minecount = 0
            open(pressed_tile[0], pressed_tile[1], pressed_tile[2])
            for y, row in enumerate(tiles):
                for x, status in enumerate(row):
                    if status == 1:
                        open(x, y, 7)
                    elif status == 5:
                        open(x, y, 8)

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
                        minecount += 1
                    elif tile_status == 2:
                        tiles[p_tile[1]][p_tile[0]] = p_tile[2] = 6
                        pygame.draw.rect(screen, active_tile_color, (*coords, tile_size, tile_size))
                        screen.blit(flag_img, coords)
                        minecount -= 1
                else:
                    is_pressed = True
                    was_pressed = True
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                is_pressed = False
                was_pressed = tile_status

        pygame.display.update()
        clock.tick(60)


main_menu()
