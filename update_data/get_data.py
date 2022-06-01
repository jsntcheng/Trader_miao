import compute
import pandas as pd


def get_oneday_data(old_data,code, trade_date, d, close, vol, open, high, low, turnover_rate):
    date = trade_date[d]
    # 计算今日涨跌幅
    today_pct_chg = compute.com_pct_chg(d, 1, close, open)
    # 计算昨日涨跌幅
    yest_pct_chg = compute.com_pct_chg(d - 1, 1, close, open)
    # 计算前日涨跌幅
    yyes_pct_chg = compute.com_pct_chg(d - 2, 1, close, open)
    # 计算前5日平均涨跌幅
    day_5_chg = compute.com_pct_chg(d, 5, close, open)
    # 计算前10日平均涨跌幅
    day_10_chg = compute.com_pct_chg(d, 10, close, open)
    # 计算前30日平均涨跌幅
    day_30_chg = compute.com_pct_chg(d, 30, close, open)
    # 计算距离5日均值百分比
    avg_5_pct = compute.com_avg(d, 5, close)
    # 计算距离10日均值百分比
    avg_10_pct = compute.com_avg(d, 10, close)
    # 计算距离30日均值百分比
    avg_30_pct = compute.com_avg(d, 30, close)
    # 计算距离180日均值百分比
    avg_180_pct = compute.com_avg(d, 180, close)
    # 今日成交量
    today_vol = vol[d]
    # 昨日成交量
    yest_vol = vol[d - 1]
    # 前日成交量
    yyest_vol = vol[d - 2]
    # 计算当日成交量变化率
    today_vol_chg = compute.com_vol(d, 1, vol)
    # 计算昨日成交量变化率
    yest_vol_chg = compute.com_vol(d - 1, 1, vol)
    # 计算前日成交量变化率
    yyest_vol_chg = compute.com_vol(d - 2, 1, vol)
    # 计算今日成交量距离3日平均成交量百分比
    avg_3_vol_pct = compute.com_vol(d, 3, vol)
    # 计算今日成交量距离5日平均成交量百分比
    avg_5_vol_pct = compute.com_vol(d, 5, vol)
    # 计算今日成交量距离10日平均成交量百分比
    avg_10_vol_pct = compute.com_vol(d, 10, vol)
    # 今日换手率
    today_tno = turnover_rate[d]
    # 昨日换手率
    yest_tno = turnover_rate[d - 1]
    # 前日换手率
    yyest_tno = turnover_rate[d - 2]
    # 计算今日换手率变化率
    today_tno_chg = compute.com_tno(d, 1, turnover_rate)
    # 计算昨日换手率变化率
    yest_tno_chg = compute.com_tno(d - 1, 1, turnover_rate)
    # 计算前日换手率变化率
    yyest_tno_chg = compute.com_tno(d - 2, 1, turnover_rate)
    # 计算今日换手率距离3日平均换手率百分比
    avg_3_tno_pct = compute.com_tno(d, 3, turnover_rate)
    # 计算今日换手率距离5日平均换手率百分比
    avg_5_tno_pct = compute.com_tno(d, 5, turnover_rate)
    # 计算今日换手率距离10日平均换手率百分比
    avg_10_tno_pct = compute.com_tno(d, 10, turnover_rate)
    # 计算今日波动率
    today_hl = compute.com_h_l_pct(d, 1, high, low, open)
    # 计算昨日波动率
    yest_hl = compute.com_h_l_pct(d - 1, 1, high, low, open)
    # 计算前日波动率
    yyesy_hl = compute.com_h_l_pct(d - 2, 1, high, low, open)
    # 计算3日平均波动率
    avg_3_hl_pct = compute.com_h_l_pct(d, 3, high, low, open)
    # 计算5日平均波动率
    avg_5_hl_pct = compute.com_h_l_pct(d, 5, high, low, open)
    # 计算10日平均波动率
    avg_10_hl_pct = compute.com_h_l_pct(d, 10, high, low, open)
    # 计算后面10日内最大涨跌幅
    result=compute.com_result(d,10,high,low,close)
    base = {"日期": date, "开盘价":open[d],"收盘价":close[d], "今日涨跌幅": today_pct_chg, "昨日涨跌幅": yest_pct_chg, "前日涨跌幅": yyes_pct_chg,
            "前5日平均涨跌幅": day_5_chg, "前10日平均涨跌幅": day_10_chg, "前30日平均涨跌幅": day_30_chg, "距离5日均值百分比": avg_5_pct,
            "距离10日均值百分比": avg_10_pct, "距离30日均值百分比": avg_30_pct, "距离180日均值百分比": avg_180_pct,
            '今日成交量':today_vol,'昨日成交量':yest_vol,'前日成交量':yyest_vol,
            "当日成交量变化率": today_vol_chg,"昨日成交量变化率": yest_vol_chg, "前日成交量变化率": yyest_vol_chg,
            "今日成交量距离3日平均成交量百分比": avg_3_vol_pct,"今日成交量距离5日平均成交量百分比": avg_5_vol_pct, "今日成交量距离10日平均成交量百分比": avg_10_vol_pct,
            '今日换手率':today_tno,'昨日换手率':yest_tno,'前日换手率':yyest_tno,
            "今日换手率变化率": today_tno_chg,"昨日换手率变化率": yest_tno_chg, "前日换手率变化率": yyest_tno_chg, "今日换手率距离3日平均换手率百分比": avg_3_tno_pct,
            "今日换手率距离5日平均换手率百分比": avg_5_tno_pct, "今日换手率距离10日平均换手率百分比": avg_10_tno_pct,
            "今日波动率": today_hl, "昨日波动率": yest_hl, "前日波动率": yyesy_hl, "3日平均波动率": avg_3_hl_pct,
            "5日平均波动率": avg_5_hl_pct, "10日平均波动率": avg_10_hl_pct,"后10天盈亏比":result}
    new_data = pd.DataFrame([base])
    return pd.concat([old_data,new_data])
