import os
print(os.environ.get('tushare_token'))

import numpy as np
print(np.__version__)  # 1.15.1

import matplotlib
print(matplotlib.matplotlib_fname())

import matplotlib.pyplot as plt
x=[1,2,3,4,5,6]
y=[10,5,15,10,30,20]
plt.plot(x,y,color='blue')
plt.show()
plt.savefig('testblueline.jpg')#将生成的图表保存为图片

