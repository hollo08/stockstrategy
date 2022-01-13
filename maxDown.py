#最大回撤
import numpy as np
import matplotlib.pyplot as plt

x = [32,35,22,188,32,34,23,21,192,43]
j = np.argmax(np.maximum.accumulate(x) - x)
print('j is {0}'.format(j))
print(np.maximum.accumulate(x))
print(np.maximum.accumulate(x) - x)
i = np.argmax(x[:j])
print('i is {0}'.format(i))
d = x[i] - x[j]
plt.plot(x)
plt.plot([i, j], [x[i], x[j]], 'o', color='Red', markersize=20)
plt.show()