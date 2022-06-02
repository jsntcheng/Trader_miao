import queue
import random
from multiprocessing import Pool
from time import sleep

import pandas as pd
from multiprocessing.managers import BaseManager

from sqlalchemy import create_engine

from sql import SqlAction
from trader import trader

brain_num = 34
trade_gen = 50
trader_num = 20
change = 1

trader_genius_db = SqlAction('101.35.49.209', 'root', '543049601', 'trader_genius')
trading_data_db = SqlAction('101.35.49.209', 'root', '543049601', 'trading_data')
conn = create_engine('mysql+pymysql://root:543049601@101.35.49.209:3306/trader_genius')
header = []
for i in range(1, brain_num + 1):
    header.append(f'参数{i}')
header.append('得分')

def training(h):
    sleep(0.5+abs(random.random()))
    global brain_num
    global trade_gen
    global trader_num
    global change
    global trader_genius_db
    global trading_data_db
    global conn
    global header
    now_version = max(trader_genius_db.get_data_from_mysql('training_result','version'))
    # 迭代代数
    code = trader_genius_db.get_data_from_mysql('training_per','code',f"status='ready' and version={now_version} limit 1")
    trader_genius_db.update_data_into_mysql('training_per','`status`="busy"',f'`code`="{code}"')
    try:
        temp=[]
        trading_data = trading_data_db.get_data_from_mysql(code)
        try:
            genius = list(trader_genius_db.get_data_from_mysql('temp_genius','`参数1`,`参数2`,`参数3`,`参数4`,`参数5`,`参数6`,`参数7`,`参数8`,`参数9`,`参数10`,`参数11`,`参数12`,`参数13`,`参数14`,`参数15`,`参数16`,`参数17`,`参数18`,`参数19`,`参数20`,`参数21`,`参数22`,`参数23`,`参数24`,`参数25`,`参数26`,`参数27`,`参数28`,`参数29`,`参数30`,`参数31`,`参数32`,`参数33`,`参数34`,`得分`',f'code="{code}"'))
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
            for i in range(int(len(genius)-9)):
                score_min = min(temp)
                index = temp.index(score_min)
                del temp[index]
                del genius[index]
        code_header = [code]*len(genius)
        genius_pd = pd.DataFrame(genius)
        genius_pd.columns = header
        genius_pd['code'] = code_header
        genius_pd.to_sql('all_genius',conn,if_exists='append',index=False)
        print (f'{code}训练完成')
        trader_genius_db.update_data_into_mysql('training_per', f'`status`="ready",version={str(int(now_version)+1)}', f'`code`="{code}"')
    except Exception as e:
        print(e)
        trader_genius_db.update_data_into_mysql('training_per', '`status`="ready"', f'`code`="{code}"')


if __name__ == '__main__':
    while True:
        with Pool(8) as p:
            p.map(training,range(99999))
