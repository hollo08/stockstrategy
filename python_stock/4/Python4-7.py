import  random          #导入random标准库
num = 1
while num == 1 :
    gameplayer = int(input("\n\n请输入您要出的拳，其中1表示布、2表示剪刀、3表示石头 :"))
    if  gameplayer == 666 :
        print("剪刀、石头、布游戏结束！")
        break 
    gamecomputer = random.randint(1,3)      #产生一个1~3的随机整数
    if ((gameplayer ==1 and gamecomputer == 3 ) or (gameplayer == 2 and gamecomputer == 1) or (gameplayer == 3 and gamecomputer == 2)):
        print("\n您是游戏高手，比赛结果是您赢了！")
    elif  gameplayer == gamecomputer :
        print("\n您玩游戏和计算机一样历害，比赛结果是平了！")
    else :
        print("\n计算机玩游戏就是历害，比赛结果是计算机赢了！")
