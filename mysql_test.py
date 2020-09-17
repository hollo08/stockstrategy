import pandas as pd
import os
import tushare as ts
from sqlalchemy import create_engine

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


if __name__ == '__main__':
    df = read_data()
    #df = get_data()
    #write_data(df, name='stock_basic')
    for ts_code in df['ts_code'].values:
        print(ts_code)