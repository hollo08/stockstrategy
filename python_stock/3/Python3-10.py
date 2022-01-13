mynum = input("输入一个数字：")
num = int(mynum)
if num % 2 == 0  :
    if num % 3 == 0 :
        print ("\n输入的数字可以整除 2 和 3")
    else:
        print ("\n输入的数字可以整除 2，但不能整除 3")
else:
    if num % 3 == 0 :
        print ("\n输入的数字可以整除 3，但不能整除 2")
    else:
        print  ("\n输入的数字不能整除 2 和 3")
