# 导入mypack包，实际上就是导入包下__init__.py文件
import mypack
# 导入mypack包下的mymod1模块，实际上就是导入mypack文件夹下的mymod1.py
import mypack.mymod1
# 导入mypack包下的mymod2模块
from mypack import mymod2

mypack.mymod1.mydef1()
print()
mypack.mymod1.mydef2()
print()
mypack.mymod2.myd1()
print()
mypack.mymod2.myd2()
