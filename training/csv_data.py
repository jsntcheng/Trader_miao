import csv
import time


def get_data():
    result = []
    with open("603305.SH.csv") as f:
        reader = csv.reader(f)
        rows = [row for row in reader]
        del rows[0]
        for x in rows:
            temp = []
            for y in range(4,len(x)):
                if x[y] == '':
                    x[y] = '0'
                x[y] = float(x[y])
                temp.append(x[y])
            result.append(temp)
        return result[1:]

def write_result(data):
    this_time = time.ctime().replace(' ','')
    this_time = this_time.replace(':','')
    with open("result"+this_time+".csv", mode="w", encoding="utf-8-sig", newline="") as f:
        # 基于打开的文件，创建 csv.writer 实例
        writer = csv.writer(f)

        # 写入数据。
        # writerows() 一次写入多行。
        writer.writerows(data)
