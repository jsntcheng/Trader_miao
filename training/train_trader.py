import pandas as pd
from sqlalchemy import create_engine
from multiprocessing import Pool
from sql import *
from trader import trader

brain_num = 34
trade_gen = 100
trader_num = 20
change = 1

trader_genius_db = SqlAction('101.35.49.209', 'root', '543049601', 'trader_genius')
trading_data_db = SqlAction('101.35.49.209', 'root', '543049601', 'trading_data')
conn = create_engine('mysql+pymysql://root:543049601@101.35.49.209:3306/trader_genius')

codes = trading_data_db.tables_list
# solved = trader_genius_db.tables_list
# not_solved = []
# for i in codes:
#     if i not in solved:
#         not_solved.append(i)
header = []
for i in range(1, brain_num + 1):
    header.append(f'参数{i}')
header.append('得分')

def training(code):
    global brain_num
    global trade_gen
    global trader_num
    global change
    global trader_genius_db
    global trading_data_db
    global conn
    global header
    # 迭代代数
    temp=[]
    trading_data = trading_data_db.get_data_from_mysql(code)
    try:
        genius = list(trader_genius_db.get_data_from_mysql('all_genius','*',f'code="{code}"'))
        if genius == []:
            genius = [[0] * (brain_num + 1)]
    except:
        genius = [[0]*(brain_num+2)]
    for i in genius:
        temp.append(i[-2])
    for gen in range(trade_gen):
        trader_dic = {}
        for no in range(trader_num):
            # 创造交易员
            this_trader = trader(gen, no, brain_num, genius, temp, change)
            # 跑遍所有天数
            try:
                for date, data in enumerate(trading_data):
                    this_trader.trade(data[3:], False)
                    this_trader.get_result(data[-1])
            except Exception as e:
                print(e)
                pass
            profit = this_trader.result_score
            trader_dic[this_trader] = profit
        sort_list = sorted(trader_dic.items(), key=lambda x: x[1], reverse=True)
        think_temp = list(sort_list[0][0].think)
        think_temp.append(sort_list[0][1])
        genius.append(think_temp)
        temp.append(sort_list[0][1])
        # 随机丢失基因(意外夭折)
        for i in range(int(len(genius) * 0.1)):
            score_min = min(temp)
            index = temp.index(score_min)
            del temp[index]
            del genius[index]
    code_header = [code]*len(genius)
    genius_pd = pd.DataFrame(genius)
    genius_pd.columns = header
    genius_pd['code'] = code_header
    genius_pd.to_sql('all_genius',conn,if_exists='append',index=False)
    print(f'{code}训练完成')


if __name__ == '__main__':
    training('000001.SZ')
    with Pool(processes=8) as p:
        p.map(training,codes)
