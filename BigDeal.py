#!/usr/bin/python
# coding=utf-8


import tushare as ts
from toolkit import read_stock
from mysqlUtil import read_data
#pd.set_option('display.max_rows', None)


class MonitorStock():
    def __init__(self):
        self.mystock = read_stock(file='data/mystock.csv')
        self.base = read_data("SELECT * FROM stock_basic")
        print(self.base.head(5))

    # 大于某手的大单
    def getBigDeal(self, code, vol):
        df = ts.get_tick_data(code, date='2020-09-23', src='tt')
        t = df[df['volume'] > vol]
        s = df[df['amount'] > 100000000]
        print('\n')
        if t.size != 0:
            print("Big volume")
            print(self.base[self.base['symbol'] == str(code)]['name'].values[0])
            print(t)
        if s.size != 0:
            print("Big amount: ")
            print(self.base[self.base['symbol'] == str(code)]['name'].values[0])
            print(s)
        r = df[df['volume'] > vol * 10]
        if r.size != 0:
            print("Super amount:")
            print(self.base[self.base['symbol'] == str(code)]['name'].values[0])
            print(r)

    def loops(self):
        for i in self.mystock:
            #print(i)
            self.getBigDeal(i, 5000)


if __name__ == '__main__':
    obj = MonitorStock()
    #obj.getBigDeal('600795', 10000)
    obj.loops()
