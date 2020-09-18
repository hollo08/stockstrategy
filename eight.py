#! /usr/bin/env python
# -*- encoding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader.data as web
import pandas as pd
import datetime
import time
import talib

from seven import bs_k_data_stock, pro_daily_stock, json_to_str
from MplVisualIf import MplVisualIf, MplTypesDraw, DefTypesPool
from MultiGraphIf import MultiGraphIf

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 参数设置
pd.set_option('display.expand_frame_repr', False)  # False不允许换行
pd.set_option('display.max_rows', 20)  # 显示的最大行数
pd.set_option('display.max_columns', 10)  # 显示的最大列数
pd.set_option('precision', 2)  # 显示小数点后的位数


app = MplVisualIf()


########################################### basic  ################################################################

def draw_kline_chart(stock_dat):
    # 绘制K线图
    """
    fig = plt.figure(figsize=(14, 7), dpi=100, facecolor="white") # 创建fig对象
    graph_kline = fig.add_subplot(1, 1, 1) # 创建子图
    mpf.candlestick2_ochl(graph_kline, stock_dat.Open, stock_dat.Close, stock_dat.High, stock_dat.Low, width=0.5,
               colorup='r', colordown='g') # 绘制K线走势

    ohlc = list(zip(np.arange(0,len(stock_dat.index)),stock_dat.Open,stock_dat.Close,stock_dat.High,stock_dat.Low)) # 使用zip方法生成数据列表
    mpf.candlestick_ochl(graph_kline, ohlc, width=0.2, colorup='r', colordown='g', alpha=1.0) # 绘制K线走势

    graph_kline.set_title(u"000651 格力电器-日K线")
    graph_kline.set_xlabel("日期")
    graph_kline.set_ylabel(u"价格")
    graph_kline.set_xlim(0, len(stock_dat.index)) # 设置x轴的范围
    graph_kline.set_xticks(range(0, len(stock_dat.index), 15)) # X轴刻度设定 每15天标一个日期
    graph_kline.set_xticklabels([stock_dat.index.strftime('%Y-%m-%d')[index] \
                  for index in graph_kline.get_xticks()]) # 标签设置为日期
    fig.autofmt_xdate(rotation=45) # 避免x轴日期刻度标签的重叠 将每个ticker标签倾斜45度
    plt.show()
    """
    layout_dict = {'figsize': (12, 6),
                   'index': stock_dat.index,
                   'draw_kind': {'ochl':
                                     {'Open': stock_dat.Open,
                                      'Close': stock_dat.Close,
                                      'High': stock_dat.High,
                                      'Low': stock_dat.Low
                                      }
                                 },
                   'title': u"000651 格力电器-日K线",
                   'ylabel': u"价格"}

    app.fig_output(**layout_dict)


def draw_volume_chart(stock_dat):
    # 绘制成交量图
    bar_red = np.where(stock_dat.Open < stock_dat.Close, stock_dat.Volume, 0)  # 绘制BAR>0 柱状图
    bar_green = np.where(stock_dat.Open > stock_dat.Close, stock_dat.Volume, 0)  # 绘制BAR<0 柱状图

    layout_dict = {'figsize': (14, 5),
                   'index': stock_dat.index,
                   'draw_kind': {'bar':
                                     {'bar_red': bar_red,
                                      'bar_green': bar_green
                                      }
                                 },
                   'title': u"000651 格力电器-成交量",
                   'ylabel': u"成交量"}

    app.fig_output(**layout_dict)


def draw_sma_chart(stock_dat):
    # 绘制移动平均线图

    stock_dat['SMA20'] = stock_dat.Close.rolling(window=20).mean()
    stock_dat['SMA30'] = stock_dat.Close.rolling(window=30).mean()
    stock_dat['SMA60'] = stock_dat.Close.rolling(window=60).mean()
    """
    fig = plt.figure(figsize=(14, 5), dpi=100, facecolor="white") # 创建fig对象
    graph_sma = fig.add_subplot(1,1,1) # 创建子图
    graph_sma.plot(np.arange(0, len(stock_dat.index)), stock_dat['SMA20'],'black', label='SMA20',lw=1.0)
    graph_sma.plot(np.arange(0, len(stock_dat.index)), stock_dat['SMA30'],'green',label='SMA30', lw=1.0)
    graph_sma.plot(np.arange(0, len(stock_dat.index)), stock_dat['SMA60'],'blue',label='SMA60', lw=1.0)
    graph_sma.legend(loc='best')
    graph_sma.set_title(u"000651 格力电器-均线")
    graph_sma.set_ylabel(u"价格")
    graph_sma.set_xlim(0,len(stock_dat.index)) # 设置x轴的范围
    graph_sma.set_xticks(range(0,len(stock_dat.index),15)) # X轴刻度设定 每15天标一个日期
    graph_sma.set_xticklabels([stock_dat.index.strftime('%Y-%m-%d')[index] \
                  for index in graph_sma.get_xticks()]) # 标签设置为日期
    fig.autofmt_xdate(rotation=45) # 避免x轴日期刻度标签的重叠 将每个ticker标签倾斜45度
    plt.show()
    """
    layout_dict = {'figsize': (14, 5),
                   'index': stock_dat.index,
                   'draw_kind': {'line':
                                     {'SMA20': stock_dat.SMA20,
                                      'SMA30': stock_dat.SMA30,
                                      'SMA60': stock_dat.SMA60
                                      }
                                 },
                   'title': u"000651 格力电器-均线",
                   'ylabel': u"价格",
                   'xlabel': u"日期",
                   'xticks': 15,
                   'legend': u'best',
                   'xticklabels': '%Y-%m-%d'}
    app.fig_output(**layout_dict)


def draw_kdj_chart(stock_dat):
    # 绘制KDJ图

    low_list = stock_dat['Low'].rolling(9, min_periods=1).min()
    high_list = stock_dat['High'].rolling(9, min_periods=1).max()
    rsv = (stock_dat['Close'] - low_list) / (high_list - low_list) * 100
    stock_dat['K'] = rsv.ewm(com=2, adjust=False).mean()
    stock_dat['D'] = stock_dat['K'].ewm(com=2, adjust=False).mean()
    stock_dat['J'] = 3 * stock_dat['K'] - 2 * stock_dat['D']

    """
    fig = plt.figure(figsize=(14, 5), dpi=100, facecolor="white")#创建fig对象
    graph_kdj = fig.add_subplot(1,1,1) #创建子图
    graph_kdj.plot(np.arange(0, len(stock_dat.index)), stock_dat['K'], 'blue', label='K') # K
    graph_kdj.plot(np.arange(0, len(stock_dat.index)), stock_dat['D'], 'g--', label='D') # D
    graph_kdj.plot(np.arange(0, len(stock_dat.index)), stock_dat['J'], 'r-', label='J') # J
    graph_kdj.legend(loc='best', shadow=True, fontsize='10')
    graph_kdj.set_ylabel(u"KDJ")
    graph_kdj.set_xlabel("日期")
    graph_kdj.set_xlim(0, len(stock_dat.index)) # 设置x轴的范围
    graph_kdj.set_xticks(range(0, len(stock_dat.index), 15)) # X轴刻度设定 每15天标一个日期
    graph_kdj.set_xticklabels([stock_dat.index.strftime('%Y-%m-%d')[index] \
                  for index in graph_kdj.get_xticks()]) # 标签设置为日期
    fig.autofmt_xdate(rotation=45) # 避免x轴日期刻度标签的重叠 将每个ticker标签倾斜45度
  
    plt.show()
    """
    layout_dict = {'figsize': (14, 5),
                   'index': stock_dat.index,
                   'draw_kind': {'line':
                                     {'K': stock_dat.K,
                                      'D': stock_dat.D,
                                      'J': stock_dat.J
                                      }
                                 },
                   'title': u"000651 格力电器-KDJ",
                   'ylabel': u"KDJ",
                   'legend': u'best'}
    app.fig_output(**layout_dict)


def draw_kdj1_chart(stock_dat):
    # 绘制KDJ-for in
    xd = 9 - 1
    date = stock_dat.index.to_series()
    RSV = pd.Series(np.zeros(len(date) - xd), index=date.index[xd:])
    Kvalue = pd.Series(0.0, index=RSV.index)
    Dvalue = pd.Series(0.0, index=RSV.index)
    Kvalue[0], Dvalue[0] = 50, 50

    for day_ind in range(xd, len(stock_dat.index)):
        RSV[date[day_ind]] = (stock_dat.Close[day_ind] - stock_dat.Low[day_ind - xd:day_ind + 1].min()) / \
                             (stock_dat.High[day_ind - xd:day_ind + 1].max() - stock_dat.Low[
                                                                               day_ind - xd:day_ind + 1].min()) * 100
        if day_ind > xd:
            index = day_ind - xd
            Kvalue[index] = 2.0 / 3 * Kvalue[index - 1] + RSV[date[day_ind]] / 3
            Dvalue[index] = 2.0 / 3 * Dvalue[index - 1] + Kvalue[index] / 3
        stock_dat['RSV'] = RSV
    stock_dat['K'] = Kvalue
    stock_dat['D'] = Dvalue
    stock_dat['J'] = 3 * Kvalue - 2 * Dvalue

    layout_dict = {'figsize': (14, 5),
                   'index': stock_dat.index,
                   'draw_kind': {'line':
                                     {'K': stock_dat.K,
                                      'D': stock_dat.D,
                                      'J': stock_dat.J
                                      }
                                 },
                   'title': u"000651 格力电器-KDJ",
                   'ylabel': u"KDJ",
                   'legend': u'best'}
    app.fig_output(**layout_dict)


def draw_macd_chart(stock_dat):
    # 绘制MACD

    macd_dif = stock_dat['Close'].ewm(span=12, adjust=False).mean() - stock_dat['Close'].ewm(span=26,
                                                                                             adjust=False).mean()
    macd_dea = macd_dif.ewm(span=9, adjust=False).mean()
    macd_bar = 2 * (macd_dif - macd_dea)

    bar_red = np.where(macd_bar > 0, macd_bar, 0)  # 绘制BAR>0 柱状图
    bar_green = np.where(macd_bar < 0, macd_bar, 0)  # 绘制BAR<0 柱状图

    # macd_dif, macd_dea, macd_bar = talib.MACD(stock_dat['Close'].values, fastperiod=12, slowperiod=26, signalperiod=9)
    """
    fig = plt.figure(figsize=(14, 5), dpi=100, facecolor="white") # 创建fig对象
    graph_macd = fig.add_subplot(1,1,1) # 创建子图
    graph_macd.plot(np.arange(0, len(stock_dat.index)), macd_dif, 'red', label='macd dif') # dif
    graph_macd.plot(np.arange(0, len(stock_dat.index)), macd_dea, 'blue', label='macd dea') # dea
    graph_macd.bar(np.arange(0, len(stock_dat.index)), bar_red, facecolor='red')
    graph_macd.bar(np.arange(0, len(stock_dat.index)), bar_green, facecolor='green')
    graph_macd.legend(loc='best',shadow=True, fontsize ='10')
    graph_macd.set_ylabel(u"MACD")
    graph_macd.set_xlabel("日期")
    graph_macd.set_xlim(0,len(stock_dat.index)) # 设置x轴的范围
    graph_macd.set_xticks(range(0,len(stock_dat.index),15)) # X轴刻度设定 每15天标一个日期
    graph_macd.set_xticklabels([stock_dat.index.strftime('%Y-%m-%d')[index] for index in graph_macd.get_xticks()]) # 标签设置为日期
    fig.autofmt_xdate(rotation=45) # 避免x轴日期刻度标签的重叠 将每个ticker标签倾斜45度
    plt.show()
    """
    layout_dict = {'figsize': (14, 5),
                   'index': stock_dat.index,
                   'draw_kind': {'bar':
                                     {'bar_red': bar_red,
                                      'bar_green': bar_green
                                      },
                                 'line':
                                     {'macd dif': macd_dif,
                                      'macd dea': macd_dea
                                      }
                                 },
                   'title': u"000651 格力电器-MACD",
                   'ylabel': u"MACD",
                   'legend': u'best'}

    app.fig_output(**layout_dict)


########################################### advance ################################################################
def draw_cross_annotate(stock_dat):
    # 绘制均线金叉和死叉

    # graph_sma.legend(loc='upper left')
    # graph_range = stock_dat.High.max() - stock_dat.Low.min()
    # graph_sma.set_ylim(stock_dat.Low.min() - graph_range * 0.25, stock_dat.High.max()) # 设置y轴的范围

    # 绘制移动平均线图
    stock_dat['Ma20'] = stock_dat.Close.rolling(window=20).mean()  # pd.rolling_mean(stock_dat.Close,window=20)
    stock_dat['Ma30'] = stock_dat.Close.rolling(window=30).mean()  # pd.rolling_mean(stock_dat.Close,window=30)

    # 长短期均线序列相减取符号
    list_diff = np.sign(stock_dat['Ma20'] - stock_dat['Ma30'])
    # print(list_diff)
    list_signal = np.sign(list_diff - list_diff.shift(1))
    # print(list_signal)

    down_cross = stock_dat[list_signal < 0]
    up_cross = stock_dat[list_signal > 0]

    # 循环遍历 显示均线金叉/死叉提示符
    layout_dict = {'figsize': (14, 5),
                   'index': stock_dat.index,
                   'draw_kind': {'line':
                                     {'SMA-20': stock_dat.Ma20,
                                      'SMA-30': stock_dat.Ma30
                                      },
                                 'annotate':
                                     {u'死叉':
                                          {'andata': down_cross,
                                           'va': 'top',
                                           'xy_y': 'Ma20',
                                           'xytext': (-30, -stock_dat['Ma20'].mean() * 0.5),
                                           'fontsize': 8,
                                           'arrow': dict(facecolor='green', shrink=0.1)
                                           },
                                      u'金叉':
                                          {'andata': up_cross,
                                           'va': 'bottom',
                                           'xy_y': 'Ma20',
                                           'xytext': (-30, stock_dat['Ma20'].mean() * 0.5),
                                           'fontsize': 8,
                                           'arrow': dict(facecolor='red', shrink=0.1)
                                           }
                                      }
                                 },
                   'title': u"000651 格力电器-均线交叉",
                   'ylabel': u"价格",
                   'xlabel': u"日期",
                   'legend': u'best'}
    app.fig_output(**layout_dict)


def apply_gap(changeRatio, preLow, preHigh, Low, High, threshold):
    jump_power = 0
    if (changeRatio > 0) and ((Low - preHigh) > threshold):
        # 向上跳空 (今最低-昨最高)/阈值
        jump_power = (Low - preHigh) / threshold  # 正数
    elif (changeRatio < 0) and ((preLow - High) > threshold):
        # 向下跳空 (今最高-昨最低)/阈值
        jump_power = (High - preLow) / threshold  # 负数
    return jump_power


def draw_gap_annotate(stock_dat):
    # 绘制K线图
    # 挖掘跳空缺口
    jump_threshold = stock_dat.Close.median() * 0.01  # 跳空阈值 收盘价中位数*0.01
    stock_dat['changeRatio'] = stock_dat.Close.pct_change() * 100  # 计算涨/跌幅 (今收-昨收)/昨收*100% 判断向上跳空缺口/向下跳空缺口
    stock_dat['preLow'] = stock_dat.Low.shift(1)  # 增加昨日最低价序列
    stock_dat['preHigh'] = stock_dat.High.shift(1)  # 增加昨日最高价序列
    stock_dat = stock_dat.assign(jump_power=0)

    # for kl_index in np.arange(0, df_stockload.shape[0]):
    #  today = df_stockload.iloc[kl_index]
    # note: A value is trying to be set on a copy of a slice from a DataFrame
    # involve change the value of df_stockload but iloc just copy the dataframe

    stock_dat['jump_power'] = stock_dat.apply(lambda row: apply_gap(row['changeRatio'],
                                                                    row['preLow'],
                                                                    row['preHigh'],
                                                                    row['Low'],
                                                                    row['High'],
                                                                    jump_threshold),
                                              axis=1)
    up_jump = stock_dat[(stock_dat.changeRatio > 0) & (stock_dat.jump_power > 0)]
    down_jump = stock_dat[(stock_dat.changeRatio < 0) & (stock_dat.jump_power < 0)]

    layout_dict = {'figsize': (14, 7),
                   'index': stock_dat.index,
                   'draw_kind': {'ochl':  # 绘制K线图
                                     {'Open': stock_dat.Open,
                                      'Close': stock_dat.Close,
                                      'High': stock_dat.High,
                                      'Low': stock_dat.Low
                                      },
                                 'annotate':
                                     {u'up':
                                          {'andata': up_jump,
                                           'va': 'top',
                                           'xy_y': 'preHigh',
                                           'xytext': (0, -stock_dat['Close'].mean() * 0.5),
                                           'fontsize': 8,
                                           'arrow': dict(facecolor='red', shrink=0.1)
                                           },
                                      u'down':
                                          {'andata': down_jump,
                                           'va': 'bottom',
                                           'xy_y': 'preLow',
                                           'xytext': (0, stock_dat['Close'].mean() * 0.5),
                                           'fontsize': 8,
                                           'arrow': dict(facecolor='green', shrink=0.1)
                                           }
                                      }
                                 },
                   'title': u"000651 格力电器-跳空缺口",
                   'ylabel': u"价格"}
    app.fig_output(**layout_dict)

    print(up_jump.filter(['jump_power', 'preClose', 'changeRatio', 'Close', 'Volume']))  # 向上跳空缺口 按顺序显示列
    """
          jump_power changeRatio Close  Volume
    Date                        
    2018-10-22    1.07     3.83 40.11 8.51e+07
    2019-01-09    1.58     3.22 37.51 1.06e+08
    2019-04-09    11.48    10.00 51.93 1.08e+07
    2019-04-10    6.40     9.99 57.12 3.23e+08
    """
    print(down_jump.filter(['jump_power', 'preClose', 'changeRatio', 'Close', 'Volume']))  # 向下跳空缺口 按顺序显示列
    """
          jump_power changeRatio Close  Volume
    Date                        
    2018-10-08    -1.22    -5.65 37.93 7.15e+07
    """

    format = lambda x: '%.2f' % x
    up_jump = up_jump[(np.abs(up_jump.changeRatio) > 2) & (up_jump.Volume > up_jump.Volume.median())]  # abs取绝对值
    up_jump = up_jump.applymap(format)  # 处理后数据为str
    print(up_jump.filter(['jump_power', 'preClose', 'changeRatio', 'Close', 'Volume']))  # 按顺序只显示该列
    """
          jump_power changeRatio Close    Volume
    Date                         
    2019-01-09    1.58    3.22 37.51 105806077.00
    2019-04-10    6.40    9.99 57.12 322875034.00
    """
    down_jump = down_jump[
        (np.abs(down_jump.changeRatio) > 2) & (down_jump.Volume > down_jump.Volume.median())]  # abs取绝对值
    down_jump = down_jump.applymap(format)  # 处理后数据为str
    print(down_jump.filter(['jump_power', 'preClose', 'changeRatio', 'Close', 'Volume']))  # 按顺序只显示该列
    """
    Empty DataFrame
    Columns: [jump_power, changeRatio, Close, Volume]
    Index: []
    """


def draw_kweek_chart(stock_dat):
    # 周期重采样
    # rule='W'周 how=last()最后一天 closed='right'右闭合 label='right'右标签
    # print(stock_dat.resample('W', closed='right', label='right').last().head())

    Freq_T = 'W-FRI'
    # print(stock_dat.resample(Freq_T, closed='right', label='right').last().head())

    # 周线Close等于一周中最后一个交易日Close
    week_dat = stock_dat.resample(Freq_T, closed='right', label='right').last()
    # 周线Open等于一周中第一个交易日Open
    week_dat.Open = stock_dat.Open.resample(Freq_T, closed='right', label='right').first()
    # 周线High等于一周中High的最大值
    week_dat.High = stock_dat.High.resample(Freq_T, closed='right', label='right').max()
    # 周线Low等于一周中Low的最小值
    week_dat.Low = stock_dat.Low.resample(Freq_T, closed='right', label='right').min()
    # 周线Volume等于一周中Volume的总和
    week_dat.Volume = stock_dat.Volume.resample(Freq_T, closed='right', label='right').sum()
    # print(week_dat.head())

    layout_dict = {'figsize': (14, 7),
                   'index': week_dat.index,
                   'draw_kind': {'ochl':
                                     {'Open': week_dat.Open,
                                      'Close': week_dat.Close,
                                      'High': week_dat.High,
                                      'Low': week_dat.Low
                                      }
                                 },
                   'title': u"000651 格力电器-周K线",
                   'ylabel': u"价格"}
    app.fig_output(**layout_dict)


def draw_fibonacci_chart(stock_dat):
    # 黄金分割线
    Fib_max = stock_dat.Close.max()
    Fib_maxid = stock_dat.index.get_loc(stock_dat.Close.idxmax())
    Fib_min = stock_dat.Close.min()
    Fib_minid = stock_dat.index.get_loc(stock_dat.Close.idxmin())
    Fib_382 = (Fib_max - Fib_min) * 0.382 + Fib_min
    Fib_618 = (Fib_max - Fib_min) * 0.618 + Fib_min
    print(u'黄金分割0.382：{}'.format(round(Fib_382, 2)))
    print(u'黄金分割0.618：{}'.format(round(Fib_618, 2)))
    # 黄金分割0.382：46.88
    # 黄金分割0.618：53.8

    max_df = stock_dat[stock_dat.Close == stock_dat.Close.max()]
    min_df = stock_dat[stock_dat.Close == stock_dat.Close.min()]
    print(max_df)
    print(min_df)

    # graph_kline.legend(['0.382', '0.618'], loc='upper left')

    # 绘制K线图+支撑/阻力
    layout_dict = {'figsize': (14, 7),
                   'index': stock_dat.index,
                   'draw_kind': {'ochl':  # 绘制K线图
                                     {'Open': stock_dat.Open,
                                      'Close': stock_dat.Close,
                                      'High': stock_dat.High,
                                      'Low': stock_dat.Low
                                      },
                                 'hline':
                                     {'Fib_382':
                                          {'pos': Fib_382,
                                           'c': 'r'
                                           },
                                      'Fib_618':
                                          {'pos': Fib_618,
                                           'c': 'g'
                                           }
                                      },
                                 'annotate':
                                     {u'max':
                                          {'andata': max_df,
                                           'va': 'top',
                                           'xy_y': 'High',
                                           'xytext': (-30, stock_dat.Close.mean()),
                                           'fontsize': 8,
                                           'arrow': dict(facecolor='red', shrink=0.1)
                                           },
                                      u'min':
                                          {'andata': min_df,
                                           'va': 'bottom',
                                           'xy_y': 'Low',
                                           'xytext': (-30, -stock_dat.Close.mean()),
                                           'fontsize': 8,
                                           'arrow': dict(facecolor='green', shrink=0.1)
                                           }
                                      }
                                 },
                   'title': u"000651 格力电器-支撑/阻力位",
                   'ylabel': u"价格",
                   'legend': u'best'}
    app.fig_output(**layout_dict)


########################################### talib ################################################################

def draw_tasma_chart(stock_dat):
    # 绘制talib SMA

    stock_dat['SMA20'] = talib.SMA(stock_dat.Close, timeperiod=20)
    stock_dat['SMA30'] = talib.SMA(stock_dat.Close, timeperiod=30)
    stock_dat['SMA60'] = talib.SMA(stock_dat.Close, timeperiod=60)
    stock_dat['SMA20'].fillna(method='bfill', inplace=True)
    stock_dat['SMA30'].fillna(method='bfill', inplace=True)
    stock_dat['SMA60'].fillna(method='bfill', inplace=True)

    # stock_dat['Ma20'] = talib.MA(stock_dat.Close, timeperiod=20, matype=0)
    # stock_dat['Ma30'] = talib.MA(stock_dat.Close, timeperiod=30, matype=1)
    # stock_dat['Ma60'] = talib.MA(stock_dat.Close, timeperiod=60, matype=2)

    """
    fig = plt.figure(figsize=(14, 5), dpi=100, facecolor="white")#创建fig对象
    graph_sma = fig.add_subplot(1,1,1) #创建子图
    graph_sma.plot(np.arange(0, len(stock_dat.index)), stock_dat['Ma20'],'black', label='M20',lw=1.0)
    graph_sma.plot(np.arange(0, len(stock_dat.index)), stock_dat['Ma30'],'green',label='M30', lw=1.0)
    graph_sma.plot(np.arange(0, len(stock_dat.index)), stock_dat['Ma60'],'blue',label='M60', lw=1.0)
    graph_sma.legend(loc='best')
    graph_sma.set_title(u"000651 格力电器-MA-talib")
    graph_sma.set_ylabel(u"价格")
    graph_sma.set_xlim(0,len(stock_dat.index)) #设置x轴的范围
    graph_sma.set_xticks(range(0,len(stock_dat.index),15))#X轴刻度设定 每15天标一个日期
    graph_sma.set_xticklabels([stock_dat.index.strftime('%Y-%m-%d')[index] for index in graph_sma.get_xticks()])#标签设置为日期
    fig.autofmt_xdate(rotation=45) #避免x轴日期刻度标签的重叠 将每个ticker标签倾斜45度
    plt.show()
    """
    layout_dict = {'figsize': (14, 5),
                   'index': stock_dat.index,
                   'draw_kind': {'line':
                                     {'SMA20': stock_dat.SMA20,
                                      'SMA30': stock_dat.SMA30,
                                      'SMA60': stock_dat.SMA60
                                      }
                                 },
                   'title': u"000651 格力电器-SMA-talib",
                   'ylabel': u"价格",
                   'legend': u'best'}
    app.fig_output(**layout_dict)


def draw_tamacd_chart(stock_dat):
    # 绘制talib MACD

    macd_dif, macd_dea, macd_bar = talib.MACD(stock_dat['Close'].values, fastperiod=12, slowperiod=26, signalperiod=9)

    # RuntimeWarning: invalid value encountered in greater
    # RuntimeWarning: invalid value encountered in less
    # solve the problem
    macd_dif[np.isnan(macd_dif)], macd_dea[np.isnan(macd_dea)], macd_bar[np.isnan(macd_bar)] = 0, 0, 0
    bar_red = np.where(macd_bar > 0, 2 * macd_bar, 0)  # 绘制BAR>0 柱状图
    bar_green = np.where(macd_bar < 0, 2 * macd_bar, 0)  # 绘制BAR<0 柱状图
    """
    fig = plt.figure(figsize=(14, 5), dpi=100, facecolor="white")#创建fig对象
    graph_macd = fig.add_subplot(1,1,1) #创建子图
    graph_macd.plot(np.arange(0, len(stock_dat.index)), macd_dif, 'red', label='macd dif') # dif
    graph_macd.plot(np.arange(0, len(stock_dat.index)), macd_dea, 'blue', label='macd dea') # dea
    graph_macd.bar(np.arange(0, len(stock_dat.index)), bar_red, facecolor='red')
    graph_macd.bar(np.arange(0, len(stock_dat.index)), bar_green, facecolor='green')
    graph_macd.legend(loc='best',shadow=True, fontsize ='10')
    graph_macd.set_ylabel(u"MACD-talib")
    graph_macd.set_xlabel("日期")
    graph_macd.set_xlim(0,len(stock_dat.index)) #设置x轴的范围
    graph_macd.set_xticks(range(0,len(stock_dat.index),15))#X轴刻度设定 每15天标一个日期
    graph_macd.set_xticklabels([stock_dat.index.strftime('%Y-%m-%d')[index] for index in graph_macd.get_xticks()]) # 标签设置为日期
    fig.autofmt_xdate(rotation=45) #避免x轴日期刻度标签的重叠 将每个ticker标签倾斜45度
    plt.show()
    """
    layout_dict = {'figsize': (14, 5),
                   'index': stock_dat.index,
                   'draw_kind': {'bar':
                                     {'bar_red': bar_red,
                                      'bar_green': bar_green
                                      },
                                 'line':
                                     {'macd dif': macd_dif,
                                      'macd dea': macd_dea
                                      }
                                 },
                   'title': u"000651 格力电器-MACD-talib",
                   'ylabel': u"MACD",
                   'legend': u'best'}
    app.fig_output(**layout_dict)


def draw_takdj_chart(stock_dat):
    # 绘制talib KDJ

    stock_dat['K'], stock_dat['D'] = talib.STOCH(stock_dat.High.values, stock_dat.Low.values, stock_dat.Close.values, \
                                                 fastk_period=9, slowk_period=3, slowk_matype=0, slowd_period=3,
                                                 slowd_matype=0)
    stock_dat['K'].fillna(0, inplace=True), stock_dat['D'].fillna(0, inplace=True)
    stock_dat['J'] = 3 * stock_dat['K'] - 2 * stock_dat['D']
    """
    fig = plt.figure(figsize=(14, 5), dpi=100, facecolor="white") # 创建fig对象
    graph_kdj = fig.add_subplot(1,1,1) # 创建子图
    graph_kdj.plot(np.arange(0, len(stock_dat.index)), stock_dat['K'], 'blue', label='K') # K
    graph_kdj.plot(np.arange(0, len(stock_dat.index)), stock_dat['D'], 'g--', label='D') # D
    graph_kdj.plot(np.arange(0, len(stock_dat.index)), stock_dat['J'], 'r-', label='J') # J
    graph_kdj.legend(loc='best', shadow=True, fontsize='10')
    graph_kdj.set_ylabel(u"KDJ-talib")
    graph_kdj.set_xlabel("日期")
    graph_kdj.set_xlim(0, len(stock_dat.index)) # 设置x轴的范围
    graph_kdj.set_xticks(range(0, len(stock_dat.index), 15)) # X轴刻度设定 每15天标一个日期
    graph_kdj.set_xticklabels([stock_dat.index.strftime('%Y-%m-%d')[index] for index in graph_kdj.get_xticks()]) # 标签设置为日期
    fig.autofmt_xdate(rotation=45) # 避免x轴日期刻度标签的重叠 将每个ticker标签倾斜45度
    plt.show()
    """
    layout_dict = {'figsize': (14, 5),
                   'index': stock_dat.index,
                   'draw_kind': {'line':
                                     {'K': stock_dat.K,
                                      'D': stock_dat.D,
                                      'J': stock_dat.J
                                      }
                                 },
                   'title': u"000651 格力电器-KDJ-talib",
                   'ylabel': u"KDJ",
                   'legend': u'best'}
    app.fig_output(**layout_dict)


def draw_takpattern_annotate(stock_dat):
    # 绘制 talib K线形态 乌云压顶
    # CDL2CROWS = talib.CDL2CROWS(stock_dat.Open.values, stock_dat.High.values, stock_dat.Low.values,stock_dat.Close.values)
    # CDLHAMMER = talib.CDLHAMMER(stock_dat.Open.values, stock_dat.High.values, stock_dat.Low.values,stock_dat.Close.values)
    # CDLMORNINGSTAR = talib.CDLMORNINGSTAR(stock_dat.Open.values, stock_dat.High.values, stock_dat.Low.values,stock_dat.Close.values)
    CDLDARKCLOUDCOVER = talib.CDLDARKCLOUDCOVER(stock_dat.Open.values, stock_dat.High.values, stock_dat.Low.values,
                                                stock_dat.Close.values)

    # 绘制K线图
    pattern = stock_dat[(CDLDARKCLOUDCOVER == 100) | (CDLDARKCLOUDCOVER == -100)]

    layout_dict = {'figsize': (14, 7),
                   'index': stock_dat.index,
                   'draw_kind': {'ochl':  # 绘制K线图
                                     {'Open': stock_dat.Open,
                                      'Close': stock_dat.Close,
                                      'High': stock_dat.High,
                                      'Low': stock_dat.Low
                                      },
                                 'annotate':
                                     {u'CDLDARKCLOUDCOVER':
                                          {'andata': pattern,
                                           'va': 'bottom',
                                           'xy_y': 'High',
                                           'xytext': (0, stock_dat['Close'].mean()),
                                           'fontsize': 8,
                                           'arrow': dict(arrowstyle='->', facecolor='blue',
                                                         connectionstyle="arc3,rad=.2")
                                           }
                                      }
                                 },
                   'title': u"000651 格力电器-日K线-CDLDARKCLOUDCOVER",
                   'ylabel': u"价格"}
    app.fig_output(**layout_dict)


def talib_speed_example():
    # 对比效率上的差别
    close_price = np.random.random(1000000)
    df_random = pd.DataFrame(close_price, columns=['close_price'])

    start_a = time.perf_counter()
    talib.SMA(close_price, timeperiod=20)
    end_a = time.perf_counter()
    print("Time talib：", end_a - start_a)  # talib time consuming

    start_p = time.perf_counter()
    df_random.rolling(20).mean()
    end_p = time.perf_counter()
    print("Time pandas：", end_p - start_p)  # Pandas time consuming

def draw_mult_chart():
    layout_dict = {'figsize': (12, 6),
                   'nrows': 4,
                   'ncols': 1,
                   'left': 0.07,
                   'bottom': 0.15,
                   'right': 0.99,
                   'top': 0.96,
                   'wspace': None,
                   'hspace': 0,
                   'height_ratios': [3.5, 1, 1, 1],
                   'subplots': ['kgraph', 'volgraph', 'kdjgraph', 'macdgraph']}

    subplots_dict = {'graph_fst': {'graph_name': 'kgraph',
                                   'graph_type': {'ochl': None,
                                                  'sma': [20, 30, 60, ]
                                                  },
                                   'title': u"000651 格力电器-日K线",
                                   'ylabel': u"价格",
                                   'xticks': 15,
                                   'legend': 'best'
                                   },
                     'graph_sec': {'graph_name': 'volgraph',
                                   'graph_type': {'vol': None
                                                  },
                                   'ylabel': u"成交量",
                                   'xticks': 15,
                                   },
                     'graph_thd': {'graph_name': 'kdjgraph',
                                   'graph_type': {'kdj': None
                                                  },
                                   'ylabel': u"KDJ",
                                   'xticks': 15,
                                   'legend': 'best',
                                   },
                     'graph_fth': {'graph_name': 'macdgraph',
                                   'graph_type': {'macd': None
                                                  },
                                   'ylabel': u"MACD",
                                   'xlabel': u"日期",
                                   'xticks': 15,
                                   'legend': 'best',
                                   'xticklabels': '%Y-%m-%d'  # strftime
                                   },
                     }

    draw_stock = MultiGraphIf(**layout_dict)
    draw_stock.graph_run(df_stockload, **subplots_dict)



if __name__ == '__main__':
    df_stockload = pro_daily_stock('600795.SH', '20190601', '20200507')
    #df_stockload = bs_k_data_stock("sz.000651", '2018-06-01', '2019-06-01')  # 采用未复权数据
    print(df_stockload.head(10))

    # basic
    #draw_kline_chart(df_stockload.copy(deep=True))  # K线图
    #draw_volume_chart(df_stockload.copy(deep=True))  # 成交量图
    #draw_sma_chart(df_stockload.copy(deep=True))  # 移动平均线图
    #draw_macd_chart(df_stockload.copy(deep=True))  # MACD图
    draw_kdj_chart(df_stockload.copy(deep=True))  # KDJ图
    #draw_kdj1_chart(df_stockload.copy(deep=True))  # KDJ图-for in
    #draw_cross_annotate(df_stockload.copy(deep=True))  # 均线交叉提示
    #draw_gap_annotate(df_stockload.copy(deep=True))  # 跳空缺口提示
    #draw_kweek_chart(df_stockload.copy(deep=True))  # 重采样周K线图形
    #draw_fibonacci_chart(df_stockload.copy(deep=True))  # 黄金分割率绘制支撑与阻力线
    #draw_tasma_chart(df_stockload.copy(deep=True))  # talib SMA 普通移动平均线
    #draw_tamacd_chart(df_stockload.copy(deep=True))  # talib MACD
    #draw_takdj_chart(df_stockload.copy(deep=True))  # talib KDJ
    #draw_takpattern_annotate(df_stockload.copy(deep=True))  # talib K-line pattern标注
    #talib_speed_example()  # 对比效率上的差别
    #draw_mult_chart()

