import numpy as np

list_square = [
    [5, 3, 7],
    [1, 5, 9],
    [6, 2, 8]
    ]

square = np.array(list_square)


magic_square_count = np.sum(square, axis=0)[0]

def magic_square(squre):

    #rows
    for i in square:
        if np.sum(i) != magic_square_count:
            return "NOT A MAGIC SQUARE!"

    #columns    
    for i in range(square.shape[1]):
        if np.sum(square[:, i]) != magic_square_count:
            return "NOT A MAGIC SQUARE!"
    
    #first diagonal
    if square.diagonal().sum() != magic_square_count:
        return "NOT A MAGIC SQUARE!"

    #second diagonal
    if np.fliplr(square).diagonal().sum() != magic_square_count:
        return "NOT A MAGIC SQUARE!"
    

    return "A MAGIC SQUARE!"


print(magic_square(square))
