#! /usr/bin/env python
# -*- encoding: utf-8 -*-


# 第九章 构建股票量化交易策略体系——风险和收益评估

import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader.data as web
import pandas as pd
import datetime
import talib
import time
import sys
import mpl_finance as mpf  # 替换 import matplotlib.finance as mpf
import matplotlib.gridspec as gridspec  # 分割子图

# use other chapters program
from seven import bs_k_data_stock, pro_daily_stock, json_to_str
from MplVisualIf import DefTypesPool, MplTypesDraw, MplVisualIf
from MultiGraphIf import MultiGraphIf

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 参数设置
pd.set_option('display.expand_frame_repr', False)  # False不允许换行
pd.set_option('display.max_rows', 10)  # 显示的最大行数
pd.set_option('display.max_columns', 10)  # 显示的最大列数
pd.set_option('precision', 2)  # 显示小数点后的位数

###########################################  decorator   ############################################################

app = MplVisualIf()


def get_trade_signal(stock_dat):
    df_csvload_trade = pd.read_csv('GLDQ000651.csv', index_col=None, parse_dates=[2, 3], encoding='gb2312')
    # print(df_csvload_trade)
    """
            Code  Name    Buy-Time  Sell-Time   Number  Buy-Price Sell-Price
    0  000651.SZ  格力电器  20180601   20180613    1000     46.71     49.28
    1  000651.SZ  格力电器  20180706   20180801    1000     43.19     42.45
    2  000651.SZ  格力电器  20180912   20181008    1000     35.64     37.33
    3  000651.SZ  格力电器  20181227   20190307    1000     35.85     45.74
    4  000651.SZ  格力电器  20190327   20190422    1000     45.08     61.14
    5  000651.SZ  格力电器  20190514   20190530    1000     53.25     52.94
    """
    stock_dat = stock_dat.assign(Signal=np.nan)
    stock_dat.loc[df_csvload_trade["Buy-Time"], 'Signal'] = 1
    stock_dat.loc[df_csvload_trade["Sell-Time"], 'Signal'] = -1
    """
    for kl_index, today in df_csvload_trade.iterrows():
        stock_dat.iloc[stock_dat.index.get_loc(today["Buy-Time"]),stock_dat.columns.get_indexer(['Signal'])] = 1
        stock_dat.iloc[stock_dat.index.get_loc(today["Sell-Time"]),stock_dat.columns.get_indexer(['Signal'])] = -1
    """

    # print(f'Buy-Time: \n {stock_dat[stock_dat.Signal == 1]}')
    # print(f'Sell-Time: \n {stock_dat[stock_dat.Signal == -1]}')
    """
    Buy-Time: 
                  High    Low   Open  Close     Volume  Signal
    Date                                                     
    2018-06-01  47.30  46.26  47.30  46.58  495741.21     1.0
    2018-07-06  44.68  43.31  43.79  44.20  487745.01     1.0
    2018-09-12  36.26  35.60  36.24  35.77  391317.41     1.0
    2018-12-27  36.58  35.66  36.45  35.68  327593.84     1.0
    2019-03-27  45.78  44.85  45.08  45.60  430795.60     1.0
    2019-05-14  54.49  53.02  53.25  53.36  508396.33     1.0    
    """
    """
    Sell-Time: 
                  High    Low   Open  Close    Volume  Signal
    Date                                                    
    2018-06-13  50.76  49.75  50.20  49.88  5.65e+05    -1.0
    2018-08-01  44.51  42.98  44.45  43.05  5.01e+05    -1.0
    2018-10-08  39.13  37.91  38.75  37.93  7.15e+05    -1.0
    2019-03-07  47.11  45.50  47.10  45.74  6.36e+05    -1.0
    2019-04-22  64.29  60.88  63.73  61.14  1.27e+06    -1.0
    2019-05-30  53.79  52.63  53.64  52.94  4.55e+05    -1.0
    """
    stock_dat['Signal'].fillna(method='ffill', inplace=True)  # 与前面元素值保持一致
    stock_dat['Signal'].fillna(value=-1, inplace=True)  # 序列最前面几个NaN值用-1填充

    return stock_dat


def draw_trade_chart(stock_dat):
    # 交易获利/亏损区间可视化

    layout_dict = {'figsize': (14, 7),
                   'index': stock_dat.index,
                   'draw_kind': {'filltrade':
                                     {'signal': stock_dat.Signal,
                                      'jdval': stock_dat.Close,
                                      'va': 'top',
                                      'xy_y': 'Close',
                                      'xytext': (0, stock_dat['Close'].mean()),
                                      'fontsize': 8,
                                      'arrow': dict(facecolor='yellow', shrink=0.1)
                                      }
                                 },
                   'title': u"000651 格力电器-交易持股区间",
                   'ylabel': u"Close",
                   'xlabel': u"日期",
                   'xticks': 20,
                   'xticklabels': '%Y-%m-%d'
                   }
    app.fig_output(**layout_dict)


# 交易概览信息的统计
def log_trade_info(stock_dat):
    signal_shift = stock_dat.Signal.shift(1)
    signal_shift.fillna(value=-1, inplace=True)  # 序列最前面的NaN值用-1填充
    list_signal = np.sign(stock_dat.Signal - signal_shift)

    buy_singal = stock_dat[list_signal.isin([1])]
    sell_singal = stock_dat[list_signal.isin([-1])]

    trade_info = pd.DataFrame({'BuyTime': buy_singal.index.strftime("%y.%m.%d"),
                               'SellTime': sell_singal.index.strftime("%y.%m.%d"),
                               'BuyPrice': buy_singal.Close.values,
                               'SellPrice': sell_singal.Close.values})

    trade_info['DiffPrice'] = trade_info.SellPrice - trade_info.BuyPrice
    trade_info['PctProfit'] = np.round(trade_info.DiffPrice / trade_info.BuyPrice * 100, 2)

    win_count = (trade_info.DiffPrice >= 0).sum()
    loss_count = (trade_info.DiffPrice < 0).sum()
    win_profit = trade_info[trade_info.PctProfit >= 0].PctProfit.sum()
    loss_profit = trade_info[trade_info.PctProfit < 0].PctProfit.sum()

    # 临时把标准输出重定向到一个文件，然后再恢复正常
    with open('logtrade.txt', 'w') as f:
        oldstdout = sys.stdout
        sys.stdout = f
        try:
            print(trade_info)
            """
                BuyTime  SellTime  BuyPrice  SellPrice  DiffPrice  PctProfit
            0  18.06.01  18.06.13     46.58      49.88       3.30       0.07
            1  18.07.06  18.08.01     44.20      43.05      -1.15      -0.03
            2  18.09.12  18.10.08     35.77      37.93       2.16       0.06
            3  18.12.27  19.03.07     35.68      45.74      10.06       0.28
            4  19.03.27  19.04.22     45.60      61.14      15.54       0.34
            5  19.05.14  19.05.30     53.36      52.94      -0.42      -0.01
            """
            # print(win_count,loss_count,win_profit,loss_profit)
            print(f'亏损次数:{loss_count}, 盈利次数:{win_count}, 胜率:{round(win_count / (win_count + loss_count) * 100, 2)}%')
            print(f'平均亏损:{round((loss_profit / loss_count), 2)}% 平均盈利:{round((win_profit / win_count), 2)}%')

        finally:
            sys.stdout = oldstdout


# 度量策略绝对收益和相对收益
def draw_absolute_profit(stock_dat):
    cash_hold = 100000  # 初始资金
    posit_num = 0  # 持股数目
    skip_days = False  # 持股/持币状态
    slippage = 0.01  # 滑点，默认为0.01
    c_rate = 5.0 / 10000  # 手续费，commission，默认万分之5
    t_rate = 1.0 / 1000  # 印花税，tax，默认千分之1

    # 绝对收益—资金的度量
    for kl_index, today in stock_dat.iterrows():
        # 买入/卖出执行代码
        if today.Signal == 1 and skip_days == False:  # 买入
            skip_days = True
            posit_num = int(cash_hold / (today.Close + slippage))  # 资金转化为股票
            posit_num = int(posit_num / 100) * 100  # 买入股票最少100股，对posit_num向下取整百
            buy_cash = posit_num * (today.Close + slippage)  # 计算买入股票所需现金
            # 计算手续费，不足5元按5元收，并保留2位小数
            commission = round(max(buy_cash * c_rate, 5), 2)
            cash_hold = cash_hold - buy_cash - commission
        elif today.Signal == -1 and skip_days == True:  # 卖出，避免未买先卖
            skip_days = False
            sell_cash = posit_num * (today.Close - slippage)  # 计算卖出股票得到的现金 卖出股票可以不是整百。
            # 计算手续费，不足5元按5元收，并保留2位小数
            commission = round(max(sell_cash * c_rate, 5), 2)
            # 计算印花税，保留2位小数
            tax = round(sell_cash * t_rate, 2)
            cash_hold = cash_hold + sell_cash - commission - tax  # 剩余现金
        if skip_days == True:  # 持股
            stock_dat.loc[kl_index, 'total'] = posit_num * today.Close + cash_hold
        else:  # 空仓
            stock_dat.loc[kl_index, 'total'] = cash_hold
    """
    plt.figure(figsize=(14, 5), dpi=100, facecolor="white")
    plt.plot(stock_dat['total'],
             label='Profit %d and rise %.2f'%(stock_dat['total'][-1],(stock_dat['total'][-1]-100000)/100000),lw=1.0)
    plt.legend(loc='best')
    plt.xlabel('Time')
    plt.ylabel('Profit-Total')
    plt.title(u'格力电器-资金总体收益')
    plt.show()
    """
    line_key = "资金总体收益%d；上涨幅度 %.2f%%" % (stock_dat['total'][-1], (stock_dat['total'][-1] - 100000) / 100000 * 100)
    print(line_key)

    layout_dict = {'figsize': (14, 5),
                   'index': stock_dat.index,
                   'draw_kind': {'line':
                                     {line_key: stock_dat.total
                                      }
                                 },
                   'title': u"000651 格力电器-资金总体收益",
                   'ylabel': u"总体收益",
                   'xlabel': u"日期",
                   'xticks': 20,
                   'legend': u'best',
                   'xticklabels': '%Y-%m-%d'
                   }
    app.fig_output(**layout_dict)


def draw_relative_profit(stock_dat):
    # 相对收益—策略VS基准
    pct_close = stock_dat['Close'].pct_change()
    # 交易信号与股票每日涨跌幅相乘，即可得策略的每日涨跌幅,累乘后计算策略累计收益 
    trend_profit_pct = (1 + stock_dat['Signal'] * pct_close).cumprod()
    # 把股票价格转换成从1开始，即波动的幅度 
    benchmark_profit_pct = stock_dat['Close'] / stock_dat['Close'][0]

    stock_dat['benchmark_profit_log'] = np.log(stock_dat.Close / stock_dat.Close.shift(1))
    stock_dat.loc[stock_dat.Signal == -1, 'Signal'] = 0
    stock_dat['trend_profit_log'] = stock_dat['Signal'] * stock_dat.benchmark_profit_log
    line_trend_key = "策略收益%.2f" % (stock_dat['trend_profit_log'].cumsum()[-1])
    line_bench_key = "基准收益%.2f" % (stock_dat['benchmark_profit_log'].cumsum()[-1])

    print("资金相对收益：%s VS %s" % (line_trend_key, line_bench_key))

    """
    plt.figure(figsize=(14, 5), dpi=100, facecolor="white")

    plt.plot(stock_dat['benchmark_profit_log'].cumsum(), label='benchmark_profit_log')
    plt.plot(stock_dat['trend_profit_log'].cumsum(), label='trend_profit_log')
    plt.plot(trend_profit_pct, label='trend_profit_pct')
    plt.plot(benchmark_profit_pct, label='benchmark_profit_pct')
    plt.legend(loc='best')
    plt.xlabel('Time')
    plt.ylabel('Profit-Relative')
    plt.title(u'格力电器-相对收益率')
    plt.show()
    """
    layout_dict = {'figsize': (14, 5),
                   'index': stock_dat.index,
                   'draw_kind': {'line':
                                     {line_bench_key: stock_dat['benchmark_profit_log'].cumsum(),
                                      line_trend_key: stock_dat['trend_profit_log'].cumsum()
                                      # 'benchmark_profit_pct': benchmark_profit_pct,
                                      # 'trend_profit_pct': trend_profit_pct
                                      }
                                 },
                   'title': u"000651 格力电器-相对收益率",
                   'ylabel': u"相对收益率",
                   'xlabel': u"日期",
                   'xticks': 20,
                   'legend': u'best',
                   'xticklabels': '%Y-%m-%d'
                   }  # strftime
    app.fig_output(**layout_dict)


def draw_closemax_risk(stock_dat):
    # 度量策略最大风险回撤——收盘价最大回撤

    # 计算收盘价曲线当前的滚动最高值
    stock_dat['max_close'] = stock_dat['Close'].expanding().max()
    # 计算收盘价曲线在滚动最高值之后所回撤的百分比
    stock_dat['per_close'] = stock_dat['Close'] / stock_dat['max_close']

    # 寻找出收盘价最大回撤率交易日
    min_point_df = stock_dat.sort_values(by=['per_close'])[0:1]
    min_point_close = min_point_df.per_close
    # min_point_close = stock_dat.sort_values(by=['per_close']).iloc[[0], stock_dat.columns.get_loc('per_close')]

    # 寻找出收盘价最高值交易日
    max_point_df = stock_dat[stock_dat.index <= min_point_close.index[0]].sort_values(by=['Close'], ascending=False)[
                   0:1]
    max_point_close = max_point_df.Close
    # max_point_close = stock_dat[stock_dat.index <= min_point_close.index[0]].sort_values \
    #    (by=['Close'], ascending=False).iloc[[0], stock_dat.columns.get_loc('Close')]

    # 打印收盘价的最大回撤率与所对应的最高值交易日和最大回撤交易日
    print("股价最大回撤%5.2f%% 从%s开始至%s结束" % ((1 - min_point_close.values) * 100, \
                                        max_point_close.index[0], min_point_close.index[0]))
    # 最大股价回撤 29.21% 从2018-06-12 00:00:00开始至2018-12-27 00:00:00结束

    """
    plt.figure(figsize=(14, 5), dpi=100, facecolor="white")
    plt.annotate(u"最大股价回撤\n{}".format(1 - min_point_close.values),
                       xy=(min_point_close.index[0], stock_dat.loc[min_point_close.index[0],'Close']),
                       xycoords='data',
                       xytext=(0, stock_dat['High'].mean()),
                       va='bottom',  # 点在标注下方
                       textcoords='offset points',
                       fontsize=8,
                       arrowprops=dict(facecolor='green', shrink=0.1))

    plt.plot(stock_dat['max_close'], label='max_close')
    plt.plot(stock_dat['Close'], label='Close')
    plt.legend(loc='best')
    plt.xlabel('Time')
    plt.ylabel('Close Max Drawdown')
    plt.title(u'格力电器-收盘价最大回撤')
    plt.show()
    """
    layout_dict = {'figsize': (14, 5),
                   'index': stock_dat.index,
                   'draw_kind': {'line':
                                     {'最大收盘价': stock_dat.max_close,
                                      '收盘价': stock_dat.Close
                                      },
                                 'annotate':
                                     {u"股价最大回撤\n{}".format(1 - min_point_close.values):
                                          {'andata': min_point_df,
                                           'va': 'top',
                                           'xy_y': 'Close',
                                           'xytext': (0, stock_dat['High'].mean()),
                                           'fontsize': 8,
                                           'arrow': dict(facecolor='green', shrink=0.1)
                                           },
                                      }
                                 },
                   'title': u"000651 格力电器-收盘价最大回撤",
                   'ylabel': u"收盘价最大回撤",
                   'xlabel': u"日期",
                   'xticks': 20,
                   'legend': u'best',
                   'xticklabels': '%Y-%m-%d'}
    app.fig_output(**layout_dict)


def draw_profitmax_risk(stock_dat):
    # 度量策略最大风险回撤——资金最大回撤
    cash_hold = 100000  # 初始资金
    posit_num = 0  # 持股数目
    skip_days = False  # 持股/持币状态
    slippage = 0.01  # 滑点，默认为0.01
    c_rate = 5.0 / 10000  # 手续费，commission，默认万分之5
    t_rate = 1.0 / 1000  # 印花税，tax，默认千分之1

    # 绝对收益—资金的度量
    for kl_index, today in stock_dat.iterrows():
        # 买入/卖出执行代码
        if today.Signal == 1 and skip_days == False:  # 买入
            skip_days = True
            posit_num = int(cash_hold / (today.Close + slippage))  # 资金转化为股票
            posit_num = int(posit_num / 100) * 100  # 买入股票最少100股，对posit_num向下取整百
            buy_cash = posit_num * (today.Close + slippage)  # 计算买入股票所需现金
            # 计算手续费，不足5元按5元收，并保留2位小数
            commission = round(max(buy_cash * c_rate, 5), 2)
            cash_hold = cash_hold - buy_cash - commission

        elif today.Signal == -1 and skip_days == True:  # 卖出 避免未买先卖
            skip_days = False
            sell_cash = posit_num * (today.Close - slippage)  # 计算卖出股票得到的现金 卖出股票可以不是整百。
            # 计算手续费，不足5元按5元收，并保留2位小数
            commission = round(max(sell_cash * c_rate, 5), 2)
            # 计算印花税，保留2位小数
            tax = round(sell_cash * t_rate, 2)
            cash_hold = cash_hold + sell_cash - commission - tax  # 剩余现金

        if skip_days == True:  # 持股
            stock_dat.loc[kl_index, 'total'] = posit_num * today.Close + cash_hold
        else:  # 空仓
            stock_dat.loc[kl_index, 'total'] = cash_hold

        # expanding()计算资金曲线当前的滚动最高值
        stock_dat['max_total'] = stock_dat['total'].expanding().max()

        # 计算资金曲线在滚动最高值之后所回撤的百分比
        stock_dat['per_total'] = stock_dat['total'] / stock_dat['max_total']

    min_point_df = stock_dat.sort_values(by=['per_total'])[0:1]
    min_point_total = min_point_df.per_total
    max_point_df = stock_dat[stock_dat.index <= min_point_total.index[0]].sort_values(by=['total'], ascending=False)[
                   0:1]
    max_point_total = max_point_df.total
    # min_point_total = stock_dat.sort_values(by=['per_total']).iloc[[0], stock_dat.columns.get_loc('per_total')]
    # max_point_total = stock_dat[stock_dat.index <= min_point_total.index[0]].sort_values \
    #    (by=['total'], ascending=False).iloc[[0], stock_dat.columns.get_loc('total')]

    print("资金最大回撤%5.2f%% 从%s开始至%s结束" % ((1 - min_point_total.values) * 100, \
                                        max_point_total.index[0], min_point_total.index[0]))
    # 最大资金回撤 7.49%从2018-07-13 00:00:00开始至2018-09-12 00:00:00结束

    """
    plt.figure(figsize=(14, 5), dpi=100, facecolor="white")
    plt.annotate(u"最大资金回撤\n{}".format(1 - min_point_total.values),
                       xy=(min_point_total.index[0], stock_dat.loc[min_point_total.index[0],'total']),
                       xycoords='data',
                       xytext=(0, 100),
                       va='bottom',  # 点在标注下方
                       textcoords='offset points',
                       fontsize=8,
                       arrowprops=dict(facecolor='green', shrink=0.1))

    plt.plot(stock_dat['max_total'], label='max_total')
    plt.plot(stock_dat['total'], label='total')
    plt.legend(loc='best')
    plt.xlabel('Time')
    plt.ylabel('Total Max Drawdown')
    plt.title(u'格力电器-资金最大回撤')
    plt.show()
    """
    layout_dict = {'figsize': (14, 5),
                   'index': stock_dat.index,
                   'draw_kind': {'line':
                                     {'最大资金': stock_dat.max_total,
                                      '资金': stock_dat.total
                                      },
                                 'annotate':
                                     {u"资金最大回撤\n{}".format(1 - min_point_total.values):
                                          {'andata': min_point_df,
                                           'va': 'top',
                                           'xy_y': 'total',
                                           'xytext': (0, stock_dat['High'].mean()),
                                           'fontsize': 8,
                                           'arrow': dict(facecolor='green', shrink=0.1)
                                           },
                                      }
                                 },
                   'title': u"000651 格力电器-资金最大回撤",
                   'ylabel': u"资金最大回撤",
                   'xlabel': u"日期",
                   'xticks': 20,
                   'legend': u'best',
                   'xticklabels': '%Y-%m-%d'}
    app.fig_output(**layout_dict)


def draw_mult_trace():
    layout_dict = {'figsize': (14, 8),
                   'nrows': 3,
                   'ncols': 1,
                   'left': 0.08,
                   'bottom': 0.15,
                   'right': 0.95,
                   'top': 0.95,
                   'wspace': None,
                   'hspace': 0,
                   'height_ratios': [1.5, 1, 1],
                   'subplots': ['kgraph', 'cashgraph', 'cmppfgraph']}

    subplots_dict = {'graph_fst': {'graph_name': 'kgraph',
                                   'graph_type': {'trade': None,
                                                  'close_retrace': None
                                                  },
                                   'title': u"000651 格力电器-回测分析",
                                   'ylabel': u"价格",
                                   'xticks': 15,
                                   'legend': 'best'
                                   },
                     'graph_sec': {'graph_name': 'cashgraph',
                                   'graph_type': {'cash_profit': 100000  # 初始资金
                                                  },
                                   'ylabel': u"资金收益和回撤",
                                   'xticks': 15,
                                   'legend': 'best',
                                   },
                     'graph_fth': {'graph_name': 'cmppfgraph',
                                   'graph_type': {'cmp_profit': None
                                                  },
                                   'ylabel': u"策略收益VS基准收益",
                                   'xlabel': u"日期",
                                   'xticks': 15,
                                   'legend': 'best',
                                   'xticklabels': '%Y-%m-%d'
                                   },
                     }
    draw_stock = MultiGraphIf(**layout_dict)
    draw_stock.graph_run(get_trade_signal(df_stockload.copy(deep=True)), **subplots_dict)


if __name__ == '__main__':

    df_stockload = pro_daily_stock("600795.SH", '20180601', '20190601')
    print(df_stockload.head())


    print(get_trade_signal(df_stockload.copy(deep=True)))
    """
                  High    Low   Open  Close    Volume  Signal
    Date                                                    
    2018-06-01  47.30  46.26  47.30  46.58  4.96e+05     1.0
    2018-06-04  48.31  46.99  47.00  47.81  1.02e+06     1.0
    [238 rows x 6 columns]
    """
    #draw_trade_chart(get_trade_signal(df_stockload.copy(deep=True)))  # 交易获利/亏损区间可视化
    #log_trade_info(get_trade_signal(df_stockload.copy(deep=True))) # 交易概览信息的统计
    #draw_absolute_profit(get_trade_signal(df_stockload.copy(deep=True)))  # 绝对收益—资金的度量
    #draw_relative_profit(get_trade_signal(df_stockload.copy(deep=True)))  # 相对收益—策略VS基准
    #draw_closemax_risk(get_trade_signal(df_stockload.copy(deep=True)))  # 度量策略最大风险回撤——收盘价最大回撤
    #draw_profitmax_risk(get_trade_signal(df_stockload.copy(deep=True)))  # 度量策略最大风险回撤——资金最大回撤

    draw_mult_trace()

