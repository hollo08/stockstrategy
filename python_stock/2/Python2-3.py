a1 = 126         #整型变量
a2 = -256        #整型变量
a3 = 0o36        #八进制整型变量
a4 = -0x49       #十六进制整型变量
a5 = -86.26       #浮点型变量
a6 = 6.4E+8     #浮点型变量用科学计数法表示
a7 = 8+9j       #复数变量
                #显示各变量的值
print("整型变量a1：",a1)
print("整型变量a2：",a2)
print("八进制整型变量a3：",a3)
print("十六进制整型变量a4：",a4)
print("浮点型变量a5:",a5)
print("浮点型变量a6:",a6)
print("复数变量a7:",a7)
print()         #换行
                #数据类型的转换
print("把整型变量a1转化为浮点型变量：",float(a1))
print("把浮点型变量a6转化为整型变量：",int(a6))
print("把整型变量a2转化为复数：",complex(a2))
print("把整型变量a1和浮点型变量a6转化为复数：",complex(a1,a6))