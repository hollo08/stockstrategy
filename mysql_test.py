import pandas as pd
import os
import time
import tushare as ts
from sqlalchemy import create_engine
from concurrent.futures import ThreadPoolExecutor

engine_ts = create_engine('mysql://root:123456@localhost:3306/stock_data?charset=utf8&use_unicode=1')

def read_data():
    sql = """SELECT * FROM stock_basic"""
    df = pd.read_sql_query(sql, engine_ts)
    return df

def write_data(df, name='stock_basic'):
    res = df.to_sql(name, engine_ts, index=True, if_exists='append', chunksize=5000)
    print(res)

token = os.environ.get('tushare_token')
def get_data():
    pro = ts.pro_api(token)
    df = pro.stock_basic(fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,'
                                       'list_status,list_date,list_date,is_hs')
    return df

token = os.environ.get('tushare_token')
pro = ts.pro_api(token)  # 初始化pro接口

table_name = 'stock_day_data'

start = '20120916'
end = '20200915'
def to_sql(ts_code):
    print(ts_code)
    data = pro.daily(ts_code=ts_code, start_date=start, end_date=end)
    time.sleep(0.2)
    # table_name = df.iloc[1, df.columns.get_loc('symbol')]
    data.to_sql(table_name, engine_ts, index=False, if_exists='append')

def mult_thread(df, count=8):
    with ThreadPoolExecutor(max_workers=count) as executor:
        executor.map(to_sql, df['ts_code'].values)

if __name__ == '__main__':
    #获取所有股票代码
    #df = get_data()
    #write_data(df, name='stock_basic')


    #获取每日股票价格信息
    df = read_data()
    mult_thread(df)

    #print(df.iloc[1, df.columns.get_loc('symbol')])

    # for idx, ts_code in enumerate(df['ts_code'].values):
    #     print(idx)
