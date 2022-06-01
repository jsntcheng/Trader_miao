# 计算数据


# 计算当前交易日d下，n天的涨跌幅
def com_pct_chg(d, n, close,open):
    return ((close[d] - open[d - n - 1]) / open[d - n - 1])


# 计算今日价格距离均线的百分比
def com_avg(d, n, close):
    return (close[d] - sum(close[d - n:d]) / n) / close[d]


# 计算成交量变化率
def com_vol(d, n, vol):
    return (vol[d] - (sum(vol[d - n:d]) / n)) / vol[d]


# 计算换手率变化率
def com_tno(d, n, turnover_rate):
    return (turnover_rate[d] - sum(turnover_rate[d - n:d]) / n) / turnover_rate[d]


# 计算波动率
def com_h_l_pct(d, n, high, low, open):
    hi = max(high[d - n:d + 1])
    lo = min(low[d - n + 1:d + 1])
    avg = sum(open[d - n + 1:d + 1]) / n
    return (hi - lo) / avg


# 计算结果（后n天最大涨跌幅）
def com_result(d, n, high, low, close):
    hi = max(high[d:d + n])
    lo = min(low[d:d + n])
    max_up = (hi - close[d]) / close[d]
    max_down = (lo - close[d]) / close[d]
    try:
        return abs(max_up/max_down)
    except:
        return max_up*50
