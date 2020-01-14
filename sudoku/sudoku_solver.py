sudoku = [
[0,0,5,3,0,0,0,0,0],
[8,0,0,0,0,0,0,2,0],
[0,7,0,0,1,0,5,0,0],
[4,0,0,0,0,5,3,0,0],
[0,1,0,0,7,0,0,0,6],
[0,0,3,2,0,0,0,8,0],
[0,6,0,5,0,0,0,0,9],
[0,0,4,0,0,0,0,3,0],
[0,0,0,0,0,9,7,0,0],
]

def get_usable_nums(pos,sudoku):
    # posで指定したマスに入力できる数字のリストを返す
    # pos[y,x]
    block_x = pos[1]//3 * 3
    block_y = pos[0]//3 * 3

    row = set(sudoku[pos[0]])
    col = {line[pos[1]] for line in sudoku}
    block = set(sum([line[block_x:block_x+3] for line in sudoku][block_y:block_y+3],[]))

    usable_nums = list(set(range(1,10)) - (row|col|block))

    return usable_nums


def solve_sudoku(sudoku,x=0,y=0):
    if y > 8: # yが8より大きい = すべてのマスに数字を配置した状態
        return True
    elif sudoku[y][x] != 0: # 空きマスじゃないとき
        if x == 8: # xが8 = その行のすべてのマスに数字を配置した状態
            if solve_sudoku(sudoku, 0, y+1): # 次の行の先頭から見ていく
                return True
        else:
            if solve_sudoku(sudoku, x+1, y): # 次の列を見る
                return True
    else: # 空きマスのとき
        for num in get_usable_nums([y,x],sudoku): # 入力できる数字を順に入れていく
            sudoku[y][x] = num
            if x == 8:
                if solve_sudoku(sudoku,0,y+1):
                    return True
            else:
                if solve_sudoku(sudoku,x+1,y):
                    return True
        sudoku[y][x] = 0
        return False
        

def show_sudoku(sudoku):
    for line in sudoku:
        print(line)


solve_sudoku(sudoku)
show_sudoku(sudoku)
