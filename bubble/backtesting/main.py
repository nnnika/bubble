import numpy as np
import pandas as pd
import datetime
import dateutil
import tushare
import matplotlib.pyplot as plt

# 用户输入信息
CASH = 1000000
START_DATE = '2022/1/5'
END_DATE = '2022/7/26'
# 交易日信息(举例）
data = pd.read_csv('002594.csv')


class Context:
    def __init__(self, cash, start_date, end_date):
        self.cash = cash
        self.start_date = start_date  # datetime.datetime.strptime(start_date, '%Y/%m/%d')
        self.end_date = end_date  # datetime.datetime.strptime(end_date, '%Y/%m/%d')
        self.positions = {}
        self.benchmark = None
        self.date_range = data[(data['isOpen'] == 1) &
                               (data['date'] >= start_date) &
                               (data['date'] <= end_date)]['date'].values
        # self.dt = datetime.datetime.strptime(start_date, '%Y-%m-%d')  # + datetime.timedelta(days=1)
        self.dt = dateutil.parser.parse(start_date) + datetime.timedelta(days=1)
        # self.dt = None


context = Context(CASH, START_DATE, END_DATE)  # 全局变量
# print(context.date_range)


class G:
    pass


g = G()


def set_branchmark(security):
    context.benchmark = security


def attribute_history(security, count, fields=('open', 'close', 'high', 'low', 'volume')):
    end_date = (context.dt - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    if count > len(data):
        print('数据不足')
        return IndexError
    start_date = data[(data['isOpen'] == 1) & (data['date'] <= end_date)][-count:].iloc[0, :]['date']
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
        info = pd.read_csv(f, index_col='date', parse_dates=['date']).loc[today, :]
    except FileNotFoundError:
        info = tushare.get_k_data(security, today, today).iloc[0, :]
    # except KeyError:
    #     info = pd.Series()
    return info


# print(get_today_data('002594'))


# 开盘价应该要加一个滑点（上下波动价买入）
def _order(today_data, security, amount):
    p = today_data['open']
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


def order(security, amount):
    today_data = get_today_data(security)
    _order(today_data, security, amount)


def order_target(security, amount):
    # 参数amount不能是负的，清仓是0
    if amount < 0:
        print('数量不能为负， 已调整为0')
        amount = 0
    today_data = get_today_data(security)
    hold_amount = context.positions.get(security, 0)  # ToDo: T+1
    delta_amount = amount - hold_amount
    _order(today_data, security, delta_amount)


def order_value(security,  value):
    today_data = get_today_data(security)
    amount = int(value / today_data['open'])
    _order(today_data, security, amount)


def order_target_value(security, value):
    # 结合order_target & order_value
    today_data = get_today_data(security)
    if value < 0:
        print('股票价值不能为负， 已调整为0')
        value = 0
    hold_value = context.positions.get(security, 0) * today_data['open']
    delta_value = value - hold_value
    order_value(security, delta_value)


# order('002594', 400)
# print(context.positions)
# order_target('002594', 0)
# print(context.positions)
# order_value('002594', 19995)
# print(context.positions)
# order_target_value('002594', 500000)
# print(context.positions)


def run():
    plt_df = pd.DataFrame(index=pd.to_datetime(context.date_range), columns=['value'])
    init_value = context.cash
    initialize(context)
    last_price = {}
    for dt in context.date_range:
        context.dt = dateutil.parser.parse(dt)
        handle_data(context)
        value = context.cash
        for stock in context.positions:
            # 考虑停牌的情况
            today_data = get_today_data(stock)
            if len(today_data) == 0:
                p = last_price[stock]
            else:
                p = today_data['open']
                last_price[stock] = p
            value += p * context.positions[stock]
        plt_df.loc[dt, 'value'] = value
    plt_df['change'] = (plt_df['value'] - init_value) / init_value
    bm_df = attribute_date_range_history(context.benchmark, context.start_date, context.end_date)
    bm_init = bm_df['open'][0]
    plt_df['benchmark_chg'] = (bm_df['open'] - bm_init) / bm_init
    # print(plt_df)
    plt_df[['change', 'benchmark_chg']].plot()
    plt.show()


def initialize(context):
    set_branchmark('002594')
    g.p1 = 5
    g.p2 = 60
    g.security = '002594'


def handle_data(context):
    # order('002594', 100)
    hist = attribute_history(g.security, g.p2)
    ma5 = hist['close'][-g.p1:].mean()
    ma60 = hist['close'].mean()

    if ma5 > ma60 and g.security not in context.positions:
        order_value(g.security, context.cash)
    elif ma5 < ma60 and g.security in context.positions:
        order_target(g.security, 0)


run()
