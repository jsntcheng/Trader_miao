from time import sleep

import pandas as pd
import tushare as ts
import get_info
import get_data
from sqlalchemy import create_engine
from multiprocessing import Pool
import numpy as np


# 把dataframe一列数据转化为list
def dataframe_to_list(data):
    data2 = data.values.flatten()
    return data2.tolist()


# 初始化pro接口
ts.set_token('ec9e45cac4d8e6a8ca6dd797622114a9e883aec1848f1898bf79637e')
pro = ts.pro_api('ec9e45cac4d8e6a8ca6dd797622114a9e883aec1848f1898bf79637e')
conn = create_engine('mysql+pymysql://root:543049601@101.35.49.209:3306/trading_data')
# ts_code为一个列表，包含了所有股票代码
ts_code = get_info.get_ts_code(pro)

print('共有' + str(len(ts_code)) + '支个股')
not_solve = dataframe_to_list(ts_code)

# 循环,遍历列表中所有个股
def f(code):
    try:
        # code = ts_code[i]
        # 获取当前个股的所有数据
        global not_solve
        daily_basic = (get_info.get_daily_basic(pro, code))
        daily = get_info.get_daily(pro, code)
        # 交易日数组
        trade_date = dataframe_to_list(daily_basic['trade_date'])
        all_len = lenth = len(trade_date)
        if all_len >= 2000:
            lenth = 2000
            trade_date = dataframe_to_list(daily_basic['trade_date'][all_len-lenth:])
        # 开盘价数组
        open = dataframe_to_list(daily['open'][all_len-lenth:])
        # 成交量数组
        vol = dataframe_to_list(daily['vol'][all_len-lenth:])
        # 最高价数组
        high = dataframe_to_list(daily['high'][all_len-lenth:])
        # 最低价数组
        low = dataframe_to_list(daily['low'][all_len-lenth:])
        # 收盘价数组
        close = dataframe_to_list(daily_basic['close'][all_len-lenth:])
        # 换手率数组
        turnover_rate = dataframe_to_list(daily_basic['turnover_rate'][all_len-lenth:])
        # 量比数组
        # 循环，计算当前交易日数据
        base = {"日期": None, "开盘价":None,"收盘价":None, "今日涨跌幅": None, "昨日涨跌幅": None, "前日涨跌幅": None,
                "前5日平均涨跌幅": None, "前10日平均涨跌幅": None, "前30日平均涨跌幅": None, "距离5日均值百分比": None,
                "距离10日均值百分比": None, "距离30日均值百分比": None, "距离180日均值百分比": None,
                '今日成交量':None,'昨日成交量':None,'前日成交量':None,
                "当日成交量变化率": None, "昨日成交量变化率": None, "前日成交量变化率": None,
                "今日成交量距离3日平均成交量百分比": None, "今日成交量距离5日平均成交量百分比": None, "今日成交量距离10日平均成交量百分比": None,
                '今日换手率':None,'昨日换手率':None,'前日换手率':None,
                "今日换手率变化率": None, "昨日换手率变化率": None, "前日换手率变化率": None, "今日换手率距离3日平均换手率百分比": None,
                "今日换手率距离5日平均换手率百分比": None, "今日换手率距离10日平均换手率百分比": None,
                "今日波动率": None, "昨日波动率": None, "前日波动率": None, "3日平均波动率": None,
                "5日平均波动率": None, "10日平均波动率": None, "后10天盈亏比": None}
        data = pd.DataFrame([base])
        for d in range(180,len(open) - 11):
            data = get_data.get_oneday_data(data, code, trade_date, d - 1, close, vol, open, high, low, turnover_rate)
        # data.to_csv(r"C:\Users\lcc\Desktop\训练集/" + code + ".csv",encoding='utf8')
        data = data.dropna(axis=0)
        data.to_sql(code,conn,if_exists='replace',index=False)
        print(code + "已添加完成")
        not_solve.remove(code)
    except Exception as e:
        print(e)
        print(code + "添加失败")

if __name__ == '__main__':
    f('002007.SZ')
    pass
    while not_solve != []:
        with Pool(8) as p:
            p.map(f, not_solve)
        print(f'剩余未处理股票{len(not_solve)}个')
