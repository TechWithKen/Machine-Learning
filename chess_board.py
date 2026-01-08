import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


size = 8
board = np.ones([size, size])

board[0:10:2,  1:9:2] = 0 # creating black squares.
board[1:9:2, 0:10:2] = 0 # creating black squares on the remaining square.


chessboard = pd.DataFrame(board)


plt.figure(figsize=(6,6))
plt.imshow(chessboard, cmap='gray', interpolation='none')
plt.xticks([])  # hide x-axis ticks
plt.yticks([])  # hide y-axis ticks
plt.show()