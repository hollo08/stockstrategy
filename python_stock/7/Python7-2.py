class Complex:
    #定义类的特殊方法，即构造方法
    def __init__(self, realpart, imagpart):
        self.k = realpart
        self.i = imagpart
    #定义类的方法
    def prt(self):
        print("self代表的是类的实例，代表当前对象的地址:",self)
        print("self.class 指向类:",self.__class__)
x = Complex(85.3, 75)   #实例化类
print(x.k,"\t",x.i)
x.prt()
