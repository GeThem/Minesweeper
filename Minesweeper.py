from random import randrange

while 1:
    mode = input('1. Newbie 10 mines (9x9)\n2. '
                     'Amateur 40 mines (16x16)\n3. Professional 99 mines (16x30)\n')
    if mode.isdigit() and (1 <= int(mode) <= 3):
        break
    else:
        print('No such mode')

if mode == '1':
    rows, columns, minecount = 9, 9, 10
elif mode == '2':
    rows, columns, minecount = 16, 16, 40
else:
    rows, columns, minecount = 16, 30, 99

matrix = [[0 for _ in range(columns)] for _ in range(rows)]
minecount_const = minecount
no_mine = ()


def generate():
    mines = [(x, y) for x in range(columns) for y in range(rows)]

    for x, y in ((x, y) for x in (-1, 0, 1) for y in (-1, 0, 1)):
        y_gr, x_gr = no_mine[1] + y, no_mine[0] + x
        if 0 <= x_gr < columns and 0 <= y_gr < rows:
            mines.pop(mines.index((x_gr, y_gr)))

    for _ in range(minecount):
        mine_x, mine_y = mines.pop(randrange(len(mines)))
        matrix[mine_y][mine_x] = -1
        for row, column in ((x, y) for x in (-1, 0, 1) for y in (-1, 0, 1)):
            y_gr, x_gr = mine_y + row, mine_x + column
            if 0 <= x_gr < columns and 0 <= y_gr < rows and matrix[y_gr][x_gr] != -1:
                matrix[y_gr][x_gr] += 1

    print(*(" ".join(map(str, line)).replace('0', '.').replace('-1', '*') for line in matrix), sep='\n')


if __name__ == "__main__":
    generate()