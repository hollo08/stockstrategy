#自定义函数
def myprime(n) :
    isprime = 1
    for i in range(2,int(n/2)+1) :
        if n % i ==0 :
            isprime = 0
            break
    return  isprime

flag = 0
n = int(input("请输入一个正整数："))
for i in range(2,int(n/2)+1) :
    #检测判断
    if  myprime(i) == 1 :
        #递归调用myprime()函数
        if myprime(n-i) ==1 :
            print(n,"=",i,"+",n-i)
            flag = 1
if flag == 0 :
    print(n,"不能分解为两个质数")
