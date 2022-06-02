from sql import SqlAction
from time import sleep
import time
trader_genius_db = SqlAction('101.35.49.209', 'root', '543049601', 'trader_genius')
start_version = max(trader_genius_db.get_data_from_mysql('training_result','version'))
trader_genius_db.update_data_into_mysql('training_per','status = "ready"','status="busy"')
print(f'本次训练，继续训练{int(start_version)+1}号版本')
count = 0
while True:
    # 每分钟检查版本
    sleep(10)
    trader_genius_db = SqlAction('101.35.49.209', 'root', '543049601', 'trader_genius')
    now_version = min(trader_genius_db.get_data_from_mysql('training_per', 'version'))
    count += 1
    print(f'当前训练基于版本{start_version},检查次数{count}')
    if int(now_version) > int(start_version):
        print(f'{start_version}号版本训练完成')
        trader_genius_db.drop_table('temp_genius')
        sleep(3)
        trader_genius_db.rename_table('all_genius','temp_genius')
        sleep(3)
        trader_genius_db.insert_data_into_mysql('training_result',(now_version,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ))
        count = 0
        start_version = now_version
    print(f'继续训练{int(start_version) + 1}号版本')
    del trader_genius_db