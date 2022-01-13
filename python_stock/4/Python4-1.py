mysum = 0               #定义两个整型变量
num = 1
while num<=120 :        #条件是num小于等于120，就继续执行while循环体中的代码
    mysum= mysum + num  
    num +=1             #mysum变量就是1+2+……+120的和，而num变量是循环计数
print("1加到120的和为：" ,mysum)
