def changeme( mylist1 ):
   print("函数参数mylist1的值：",mylist1)
   #修改传入的列表
   mylist1.append(['青色','黑色'])
   print ("函数内取值: ", mylist1)
   return
mylist = ["红色","绿色","蓝色","黄色"]
print("列表最初数据信息：",mylist)
print()
#调用changeme函数
changeme( mylist )
print()
print ("函数外取值: ", mylist)
