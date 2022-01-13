import random                      #首先导入random标准库
print("小学四则运算测试（输入8888结束）：")
ops = ['+', '-', '*', '/']          #运算符
ans = ""                            #用户回答
i = 1                               #统计题号
while ans != "8888":
    add1 = random.randint(10, 20)    #随机产生第一个数
    add2 = random.randint(10, 20)    #随机产生第二个数
    op = random.randint(0, 3)         #随机产生运算符
    eq = str(add1) + ops[op] + str(add2)    #算式
    # eval()函数，可以将字符串str当成有效的表达式来求值并返回计算结果
    val = eval(eq)                          #算式答案
    print("第%d题: %s=" %(i,eq) )              #显示提问问题
    ans = input("请答题，把正确答案写在其后: ")     #用户回答
    if ans == '8888':                       #退出循环
        break
    elif val == int(ans):                   #正确
        print("你牛，你的回答正确！")
    else:                                   #错误
        print("对不起，你的回答错误！正确答案是：%d" % val)     
    i = i +1                                  #题号加1
    print()
