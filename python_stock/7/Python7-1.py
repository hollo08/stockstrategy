class MyClass:
    age = 36        #定义类变量
    name = "周文静"
    love = ["跳舞","唱歌","运动"]
    def myfun(self):    #定义类方法
        return "hello world!"
#创建对象
myc = MyClass()
#访问类的属性和方法
print("MyClass 类的属性age,即年龄为：", myc.age)
print("MyClass 类的属性name,即姓名为：", myc.name)
print("MyClass 类的属性love，即爱好为：", myc.love)
print("\n MyClass 类的方法 myfun 输出为：", myc.myfun())
