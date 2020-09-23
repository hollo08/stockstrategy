#!/usr/bin/python
# coding=utf-8

import pandas as pd

def read_stock(file=""):
    stock_list = []
    df = pd.read_csv(file)
    #print(df['Code'].values)
    return [code[:code.index('.')] for code in df['Code'].values]
