import numpy as np
import pandas as pd
import datetime
import dateutil
import tushare
# import matplotlib.pyplot as plt

# 用户输入信息
CASH = 100000
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
        self.dt = dateutil.parser.parse(start_date)  # ToDO: start_date 后一个交易日


context = Context(CASH, START_DATE, END_DATE)  # 全局变量
# print(context.date_range)


class G:
    pass


g = G()


def attribute_history(security, count, fields=('open', 'close', 'high', 'low', 'volume')):
    end_date = (context.dt - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    if count > len(data):
        print('数据不足')
        return IndexError
    start_date = data[(data['isOpen'] == 1) & (data['calendarDate'] <= end_date)][-count:].iloc[0, :]['calendarDate']
    # print(start_date, end_date)    # end_date是START_DATE前一天，start_date是START_DATE往前回溯3天（满足条件）
    return attribute_date_range_history(security, start_date, end_date, fields)


def attribute_date_range_history(security, start_date, end_date, fields=('open', 'close', 'high', 'low', 'volume')):
    try:
        f = open(security+'.csv', 'r')
        df = pd.read_csv(f, index_col='date', parse_dates=['date']).loc[start_date:end_date, :]
    except FileNotFoundError:
        df = tushare.get_k_data(security, start_date, end_date)
    return df[list(fields)]


# print(attribute_date_range_history('002594', '2019-01-01', '2019-01-11'))
# print(attribute_history('002594', 3))


# 下单函数
def get_today_data(security):
    today = context.dt.strftime('%Y-%m-%d')  # 用户输入的START_DATE
    try:
        f = open(security+'.csv', 'r')
        data = pd.read_csv(f, index_col='date', parse_dates=['date']).loc[today, :]
    except FileNotFoundError:
        data = tushare.get_k_data(security, today, today).iloc[0, :]
    except KeyError:
        data = pd.Series()
    return data


# print(get_today_data('002594'))


# 开盘价应该要加一个滑点（上下波动价买入）
def _order(today_data, security, amount):
    p = today_data['close']

    if len(today_data) == 0:
        print('今日停牌')
        return

    if context.cash - amount * p < 0:
        amount = int(context.cash / p)
        print('现金不足，已调整为%d' % amount)

    if amount % 100 != 0:
        if amount != -context.positions.get(security, 0):
            # 全仓买入
            amount = int(amount / 100) * 100
            print('已调整为100的倍数%d' % amount)

    if context.positions.get(security, 0) < -amount:
        amount = - context.positions.get(security, 0)
        print('卖出股票不能超过持仓的数量，已调整为%d' % amount)

    context.positions[security] = context.positions.get(security, 0) + amount
    context.cash -= amount * p

    if context.positions[security] == 0:
        del context.positions[security]


# _order(get_today_data('002594'), '002594', 400)
# print(context.positions)
# _order(get_today_data('002594'), '002594', -100)
# print(context.positions)


def order(security, amount):
    today_data = get_today_data(security)
    _order(today_data, security, amount)


def order_target(security, amount):
    # 参数amount不能是负的，清仓是0
    if amount < 0:
        print('数量不能为负')
        return

    today_data = get_today_data(security)
    hold_amount = context.positions.get(security, 0)  # ToDo: T+1
    delta_amount = amount - hold_amount
    _order(today_data, security, delta_amount)
