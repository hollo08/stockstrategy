year = input("请输入一个年份：")
myyear  =  int(year)
if   myyear % 4 ==0 and myyear % 100 !=0 :
    print("\n您输入的年份是：",myyear,",这一年是普通润年！")
elif  myyear % 400 ==0 :
    print("\n您输入的年份是：",myyear,"，这一年是世纪润年。" )
else :
    print("\n您输入的年份是：",myyear,"，这一年是平年。")

