import timeit
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def get_max_drawdown_slow(array):
    drawdowns = []
    for i in range(len(array)):
        max_array = max(array[:i+1])
        drawdown = max_array - array[i]
        drawdowns.append(drawdown)
    #print(drawdowns)
    return max(drawdowns)

def get_max_drawdown_fast(array):
    drawdowns = []
    max_so_far = array[0]
    for i in range(len(array)):
        if array[i] > max_so_far:
            drawdown = 0
            drawdowns.append(drawdown)
            max_so_far = array[i]
        else:
            drawdown = max_so_far - array[i]
            drawdowns.append(drawdown)
    #print(drawdowns)
    return max(drawdowns)

def get_max_drawdown_pd(array):
    array = pd.Series(array)
    cumsum = array.cummax()
    print(array)
    print(cumsum)
    return max(cumsum - array)

np.random.seed(1)
a = np.random.randn(10)
values = np.cumsum(a)
print(timeit.timeit('get_max_drawdown_slow(values)', setup="from __main__ import get_max_drawdown_slow, values", number=10))
print(timeit.timeit('get_max_drawdown_fast(values)', setup="from __main__ import get_max_drawdown_fast, values", number=10))
#print(timeit.timeit('get_max_drawdown_pd(values)', setup="from __main__ import get_max_drawdown_pd, values", number=10))
print(get_max_drawdown_slow(values))
print(get_max_drawdown_fast(values))
print(get_max_drawdown_pd(values))
plt.plot(values)
plt.show()