myyear = input("请输入您的年龄：")      #动态输入年龄放到myyear变量中
nyear = int(myyear)                     #把myyear变量转化为整型放到nyear变量中
if nyear<18 :
    print("\n您的年龄是：",nyear)
    print("您还未成年，不能登录游戏系统玩游戏！")
else :
    print("\n您的年龄是：",nyear)
    print("欢迎您登录游戏系统，正在登录，请耐心等待!")
