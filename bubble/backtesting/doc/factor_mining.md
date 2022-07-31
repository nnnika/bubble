# 因子挖掘框架


## 投研阶段

1. 批量计算
2. 因子存储
3. 回测
4. 建模

### 数据集
* 逐笔成交（每天3G）
* 快照（每天10G）
* 分钟K线（1年20G）
* 日K线（10年1G）

#### 面板数据模式
* e.g. alpha001:
def alphaPanel(close):
    return rowRank(X=minmax(pow(if(ratios(close) - 1 < 0, mstd(ratios(close) - 1, 20), close), 2.0), 5), percent=True) = 0.5

#### SQL 模式
* e.g. double EMA 双指数移动平均指标
def sum_diff(x, y):
    return (x-y)\(x+y)
def factorDoubleEMA(price):
    ema_2 = ema(price, 2)
    ema_4 = ema(price, 4)
    sum_diff_1000 = 1000 * sum_diff(ema_2, ema_4)
    return ema(sum_diff_1000, 2) - ema(sum_diff_1000, 3)
res = factorDoubleEMA(close) as val from t context by securityID

## 生产阶段
### 实时计算
### 任务调度


## 结果推算
### 策略平台
### 交易系统
