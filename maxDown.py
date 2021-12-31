import numpy as np
import matplotlib.pyplot as plot

x = [32,35,66,188,32,34,23,201,19]
j = np.argmax(np.maximum.accumulate(x) - x)
print('j is {0}'.format(j))
print(np.maximum.accumulate(x))
print(np.maximum.accumulate(x)-x)