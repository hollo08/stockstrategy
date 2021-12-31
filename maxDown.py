import numpy as np
import matplotlib.pyplot as plot

x = [32,35,66,88,32,34,23]
j = np.argmax(np.maximum.accumulate(x) - x)
print('j is {j}'.format(j=j))
print(np.maximum.accumulate(x))