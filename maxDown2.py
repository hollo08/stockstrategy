import matplotlib.pyplot as plt
import numpy as np
np.random.seed(1)
a = np.random.randn(100)
print(a)
values = np.cumsum(a)
print(values)
plt.plot(values)
plt.show()