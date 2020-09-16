import sqlite3
from seven import pro_daily_stock, json_to_str

conn = sqlite3.connect('stock-data.db')
c = conn.cursor()


def create_table(name="t_test"):
    c.execute('''CREATE TABLE {0}
                   (ID           INTEGER PRIMARY KEY AUTOINCREMENT  NOT NULL,
                   TIME          TEXT    NOT NULL,
                   CODE          TEXT    NOT NULL,
                   HIGH          REAL,
                   LOW           REAL,
                   CLOSE         REAL,
                   OPEN          REAL,
                   DESCRIPTION CHAR(50));'''.format(name))
    conn.commit()

def drop_table(name="t_test"):
    c.execute("drop table {0}".format(name))
    conn.commit()


def insert_data():
    c.execute("INSERT INTO t_test (ID,TIME,CODE,HIGH,LOW,CLOSE,OPEN,DESCRIPTION) \
                  VALUES (NULL, '2019-1-1', 000002, 10.12, 10.12, 10.12, 10.12,'Buy Signal' )")

    c.execute("INSERT INTO t_test (ID,TIME,CODE,HIGH,LOW,CLOSE,OPEN,DESCRIPTION) \
                  VALUES (NULL, '2019-1-2', 000002, 10.13, 10.13, 10.13, 10.13,'Sell Signal' )")

    c.execute("INSERT INTO t_test (ID,TIME,CODE,HIGH,LOW,CLOSE,OPEN,DESCRIPTION) \
                  VALUES (NULL, '2019-1-3', 000002, 10.14, 10.14, 10.14, 10.14,'Buy Signal' )")

    c.execute("INSERT INTO t_test (ID,TIME,CODE,HIGH,LOW,CLOSE,OPEN,DESCRIPTION) \
                  VALUES (NULL, '2019-1-4', 000002, 10.15, 10.15, 10.15, 10.15,'Sell Signal' )")
    conn.commit()

def query_data(sql):
    c.execute(sql)
    return c.fetchall()

def print_data(result):
    for r in result:
        print(r)

def update_date(sql):
    c.execute(sql)
    conn.commit()


#create_table('t_test')
#insert_data()
#drop_table('t_test')
#update_date("UPDATE t_test set DESCRIPTION = 'None' where ID=1")
#print_data(query_data("select * from t_test"))
#df_gldq = pro_daily_stock('000651.SZ', '20190101', '20190201')
#df_gldq.to_sql(name='STOCK000651',  con=conn, index=False, if_exists='replace')
print_data(query_data("select * from STOCK000651"))
