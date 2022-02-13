import time

# 今日最佳股票
stock_pool = {
    "best_stock": [{
        "name": "比亚迪", "code": "002594.SZ", "strategy": "樱盘策略1", "strategy_profit": 0.05
    }]
}

# 未来一周大盘走势预测 (过去30天+未来5天), x轴为日期，y轴为收盘价
index_forecast = {
    "forecast": {"date": [], "close": []},     # 5days
    "real": {"date": [], "close": []}           # 30days
}


def get_index_quote(code, start, end, fields):
    print(code, start, end, fields)
    return {}


# 未来一周上涨行业预测
industry_forecast = {
    "info": [{
        "industry": "新能源", "name": "比亚迪", "code": "002594.SZ", "forecast_profit": 0.05
    }]
}
