import numpy as np
import pandas as pd
import datetime
import dateutil
import tushare
# import matplotlib.pyplot as plt

# 用户输入信息
CASH = 10000
START_DATE = '2019-01-10'
END_DATE = '2019-01-17'
# 交易日信息(举例）
data = pd.read_csv('trade_cal.csv')


class Context:
    def __init__(self, cash, start_date, end_date):
        self.cash = cash
        self.start_date = start_date
        self.end_date = end_date
        self.positions = {}
        self.benchmark = None
        self.date_range = data[(data['isOpen'] == 1) &
                               (data['calendarDate'] >= start_date) &
                               (data['calendarDate'] <= end_date)]['calendarDate'].values
        # self.dt = datetime.datetime.strptime('%Y-%m-%d', start_date)
        self.dt = dateutil.parser.parse(start_date)


context = Context(CASH, START_DATE, END_DATE)  # 全局变量
# print(context.date_range)


class G:
    pass


g = G()


def attribute_history(security, count, fields=('open', 'close', 'high', 'low', 'volume')):
    end_date = (context.dt - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    if count > len(data):
        return IndexError
    start_date = data[(data['isOpen'] == 1) & (data['calendarDate'] <= end_date)][-count:].iloc[0, :]['calendarDate']
    # print(start_date, end_date)    # end_date是START_DATE前一天，start_date是START_DATE往前回溯3天（满足条件）
    return attribute_date_range_history(security, start_date, end_date, fields)


def attribute_date_range_history(security, start_date, end_date, fields=('open', 'close', 'high', 'low', 'volume')):
    try:
        f = open(security+'.csv', 'r')
        df = pd.read_csv(f, index_col='date', parse_dates=['date']).loc[start_date:end_date, :]
    except:
        df = tushare.get_k_data(security, start_date, end_date)
    return df[list(fields)]


# print(attribute_date_range_history('002594', '2019-01-01', '2019-01-11'))
# print(attribute_history('002594', 3))