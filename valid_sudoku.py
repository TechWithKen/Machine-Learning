import numpy as np

board = [["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]


correct_board = np.array(board)


valid_sudoku = 1


def catch_repetition(arr):
    """
    Unique function to identify if an array has any repeated value.
    
    :param arr: Description
    """
    repeated = [x for x in arr.tolist() if x!= "."]
    if len(repeated) == len(set(repeated)):
        return 1
    else:
        return 0



def validate_sudoku(sudoku_board):
    global valid_sudoku
    #get rows
    for i in correct_board:
        valid_sudoku *= catch_repetition(i)


    #get columns
    for col in range(correct_board.shape[1]):
        valid_sudoku *= catch_repetition(correct_board[:, col])


    #get 3x3 sub-grids
    for i in range(0, correct_board.shape[0], 3):
        for j in range(0, correct_board.shape[1], 3):
            valid_sudoku *= catch_repetition((correct_board[i:i+3, j:j+3]).reshape(1, 9)[0])

    return valid_sudoku

print(bool(validate_sudoku(correct_board)))