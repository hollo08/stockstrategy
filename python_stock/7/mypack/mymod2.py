#定义函数myd1()，显示100之内的偶数
def myd1() :
    print("显示100之内的偶数")
    for i in  range(1,101) :
        if  i % 2 == 0 :
            print(i,"\t",end="")

#定义函数myd2()，绘制※的菱形
def myd2() :
    print("绘制※的菱形\n")
    for i in range(4):                  
        for j in range(2 - i + 1):
            print("  ",end="")
        for k in range(2 * i + 1):
            print('※',end="")
        print()
    for i in range(3):
        for j in range(i + 1):
            print("  ",end="")
        for k in range(4 - 2 * i + 1):
            print('※',end="")
        print()

