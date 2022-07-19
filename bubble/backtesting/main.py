import numpy as np
import pandas as pd
import datetime
import dateutil
# import matplotlib.pyplot as plt

# 用户输入信息
CASH = 10000
START_DATE = '2019-01-02'
END_DATE = '2019-01-07'
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
        # self.dt = datetime.datetime.strptime("", start_date)
        # self.dt = dateutil.parser.parse(start_date)


context = Context(CASH, START_DATE, END_DATE)  # 全局变量
# print(context.date_range)


class G:
    pass


# def attribute_history(security, count, fileds=('open', 'close', 'high', 'low', 'volume')):
#     end_date = (context.dt - datetime.timedelta(days=1)).strptime
#     start_daye = data[(data['isOpen'] == 1) & (data['calendarDate'] <= end_date)][-count:].iloc[0, :]['calendarDate']
#     print(start_daye, end_date)
#
#
# attribute_history('601318', 10)
