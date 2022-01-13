name = input("请输入用户名：")
pwd = input("请输入用户密码：")
if name == "admin" :
    if pwd == "admin2020" :
        print("用户名和密码都正确，可以成功登录！")
    else :
        print("用户名正确，密码不正确！")
else :
    if pwd == "admin2020" :
        print("用户名不正确，密码正确！")
    else :
        print("用户名和密码都不正确！")
