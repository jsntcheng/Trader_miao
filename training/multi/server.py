from sql import SqlAction
from time import sleep
import time
trader_genius_db = SqlAction('101.35.49.209', 'root', '543049601', 'trader_genius')
trading_data_db = SqlAction('101.35.49.209', 'root', '543049601', 'trading_data')
start_version = max(trader_genius_db.get_data_from_mysql('training_result','version'))
trader_genius_db.update_data_into_mysql('training_per','status = "ready"','status="busy"')
print(f'本次训练，继续进行{int(start_version)+1}号版本')
while True:
    # 每分钟检查版本
    sleep(60)
    now_version = min(trader_genius_db.get_data_from_mysql('training_per', 'version'))
    if int(now_version) > int(start_version):
        print(f'{now_version}号版本训练完成')
        trader_genius_db.drop_table('temp_genius')
        trader_genius_db.rename_table('all_genius','temp_genius')
        trader_genius_db.insert_data_into_mysql('training_result',(now_version,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ))
        start_version = now_version
    print(f'继续进行{int(start_version) + 1}号版本')