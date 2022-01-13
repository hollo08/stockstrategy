def printinfo( arg1, *vartuple ):
   "打印任何传入的参数"
   print ("必需参数的值: ",arg1)
   print()
   if len(vartuple)==0 :
       print("没有可变参数传入")
   else:
       for var in vartuple:
          print ("可变参数的值：",var)
   return
 # 第一次调用printinfo 函数
printinfo( 80 );
print ("------------------------")
#第二次调用printinfo 函数
printinfo( 120, 110, 40,90,50 )
