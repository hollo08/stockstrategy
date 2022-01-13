n = int(input("请输入要显示弗洛伊德三角形的行数:"))
j = 1
#利用i控制行数
for i in range(1,n+1) :
	#利用l控制每行有多个数，利用j输入每行的具体数值
    for l in range (1,i+1) :
        print(j,"\t",end="")
        j = j + 1
#换行
    print()
