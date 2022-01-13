def ChangeInt( a ):
    print("函数参数a的值：",a)      #结果是2
    a = 10
    print("函数参数重新赋值后的值：",a,"\n")   #结果是10
    return a
b = 2
print()
print("调用函数，并显示函数返回值：",ChangeInt(b))    #返回值是10
print( "\n变量b的值：",b )                            # 结果是2
