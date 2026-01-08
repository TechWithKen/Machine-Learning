import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



the_ones = np.ones([8, 8])
the_ones[0:10:2,  1:9:2] = 0
the_ones[1:9:2, 0:10:2] = 0
ones_dataframe = pd.DataFrame(the_ones)
ones_dataframe

plt.figure(figsize=(6,6))
plt.imshow(ones_dataframe, cmap='gray', interpolation='none')
plt.xticks([])  # hide x-axis ticks
plt.yticks([])  # hide y-axis ticks
plt.show()