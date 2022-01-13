#定义函数mydef1()，打印9*9乘法表
def  mydef1() :
    for i in range(1, 10):
        print()
        for j in range(1, i+1):
            print("%d*%d=%d  " % (i, j, i*j),end='')
#定义函数mydef2()，显示学生的姓名信息
def  mydef2() :
    names = ["周涛", "王佳欣", "王雨欣", "张高远","高飞","李硕","周文康","宫志伟"]
    print("\n遍历显示学生的姓名：\n")
    for stuname in names:
        print(stuname)

