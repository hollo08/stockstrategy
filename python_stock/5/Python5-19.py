#定义一个集合
stus = {'张平', '李亮', '张可', '赵杰', '李亮', '赵杰',10,52,10,52,"张可","周涛"}
print("输出集合，重复的元素被自动去掉: ",stus)   
# 成员测试
if('张可' in stus) :
    print('\n张可在集合中，所以张可是一名学生！')
else :
    print('\n张可不在集合中，所以张可不是一名学生！')
if('李杰' in stus):
    print('\n李杰在集合中，所以李杰是一名学生！')
else:
    print('\n李杰不在集合中，所以李杰不是一名学生！')