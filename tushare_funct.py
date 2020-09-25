#!/usr/bin/python
# coding=utf-8

import os
import tushare as ts

token = os.environ.get('tushare_token')
ts.set_token(token)
pro = ts.pro_api(token)  # 初始化pro接口

def stock_basic():
    """
    查询当前所有正常上市交易的股票列表
    fields = 'ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,list_date,is_hs'
    参考URL：https://tushare.pro/document/2?doc_id=25
    """
    data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    return data

def trade_cal():
    """
    获取各大交易所交易日历数据,默认提取的是上交所
    URL:https://tushare.pro/document/2?doc_id=26
    """
    data = pro.query('trade_cal', start_date='20200101', end_date='20201010')
    return data

def stock_company():
    """
    获取上市公司基础信息
    URL:https://tushare.pro/document/2?doc_id=112
    exchange:交易所代码 ，SSE上交所 SZSE深交所
    """
    return pro.stock_company(exchange='SSE', fields='ts_code,chairman,manager,secretary,reg_capital,setup_date,province')

def daily_data():
    """
    日线行情
    URL:https://tushare.pro/document/2?doc_id=27
    """
    df = pro.query('daily', ts_code='000001.SZ', start_date='20180701', end_date='20180718')
    return df

def daily_basic():
    """
    获取全部股票每日重要的基本面指标，可用于选股分析、报表展示等
    URL:https://tushare.pro/document/2?doc_id=32
    """
    df = pro.query('daily_basic', ts_code='', trade_date='20180726',
                   fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pb')
    return df

def get_bar():
    """
    行情接口
    asset:资产类别：E股票 I沪深指数 C数字货币 FT期货 FD基金 O期权 CB可转债（v1.2.39），默认E
    adj:复权类型(只针对股票)：None未复权 qfq前复权 hfq后复权 , 默认None
    freq: 数据频度 ：支持分钟(min)/日(D)/周(W)/月(M)K线，其中1min表示1分钟（类推1/5/15/30/60分钟） ，默认D
    URL:https://tushare.pro/document/2?doc_id=109
    """
    return ts.pro_bar(ts_code='000001.SZ', adj='qfq', start_date='20180101', end_date='20181011')

def hsgt_top10():
    """
    获取沪股通、深股通每日前十大成交详细数据
    URL:https://tushare.pro/document/2?doc_id=48
    """
    return pro.query('hsgt_top10', ts_code='600519.SH', start_date='20180701', end_date='20180725')

def hk_hold():
    """
    沪深港股通持股明细
    exchange:类型：SH沪股通（北向）SZ深股通（北向）HK港股通（南向持股）
    URL:https://tushare.pro/document/2?doc_id=188
    """
    return pro.hk_hold(trade_date='20200923', exchange='SH')

def ggt_top10():
    """
    获取港股通每日成交数据，其中包括沪市、深市详细数据
    URL:https://tushare.pro/document/2?doc_id=49
    """
    return pro.query('ggt_top10', ts_code='00700', start_date='20200922', end_date='20200923')


#print(stock_basic())
#print(trade_cal())
#print(stock_company())
#print(daily_data())
#print(daily_basic())
#print(get_bar())
#print(hsgt_top10())
#print(hk_hold())
print(ggt_top10())