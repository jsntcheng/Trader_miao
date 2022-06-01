import pandas as pd
import tushare as ts
# 获取标准化代码ts_code,传入pro接口，返回列表
def get_ts_code(pro):
    return pro.query('stock_basic', exchange='', list_status='L', fields='ts_code')['ts_code']

# 获取单个个股所有指标,传入pro接口,ts_code,返回dataframe
def get_daily_basic(pro,ts_code):
    return pro.daily_basic(ts_code=ts_code,fields='ts_code,trade_date,close,turnover_rate,volume_ratio').sort_values('trade_date', ascending=True)


def get_daily(pro,ts_code):
    return pro.daily(ts_code=ts_code,adj='qfq').sort_values('trade_date', ascending=True)

if __name__ == '__main__':
    ts.set_token('ec9e45cac4d8e6a8ca6dd797622114a9e883aec1848f1898bf79637e')
    pro = ts.pro_api('ec9e45cac4d8e6a8ca6dd797622114a9e883aec1848f1898bf79637e')
    print(get_daily())