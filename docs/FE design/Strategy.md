# 量化策略

CTA
## R-Breaker策略
R-Breaker 是一种短线日内交易策略，它结合了趋势和反转两种交易方式。该策略的主要特点如下：

第一、根据前一个交易日的收盘价、最高价和最低价数据通过一定方式计算出六个价位，从大到小依次为突破买入价、观察卖出价、反转卖出价、反转买入价、观察买入价和突破卖出价，以此来形成当前交易日盘中交易的触发条件。通过对计算方式的调整，可以调节六个价格间的距离，进一步改变触发条件。
第二、根据盘中价格走势，实时判断触发条件，具体条件如下：
1) 当日内最高价超过观察卖出价后，盘中价格出现回落，且进一步跌破反转卖出价构成的支撑线时，采取反转策略，即在该点位（反手、开仓）做空；
2) 当日内最低价低于观察买入价后，盘中价格出现反弹，且进一步超过反转买入价构成的阻力线时，采取反转策略，即在该点位（反手、开仓）做多；
3) 在空仓的情况下，如果盘中价格超过突破买入价，则采取趋势策略，即在该点位开仓做多；
4) 在空仓的情况下，如果盘中价格跌破突破卖出价，则采取趋势策略，即在该点位开仓做空。
第三、设定止损以及止盈条件；
第四、设定过滤条件；
第五、在每日收盘前，对所持合约进行平仓。

六个价位形成的阻力和支撑位计算过程如下：
* 观察卖出价 = High + 0.35 * (Close – Low)
* 观察买入价 = Low – 0.35 * (High – Close)
* 反转卖出价 = 1.07 / 2 * (High + Low) – 0.07 * Low
* 反转买入价 = 1.07 / 2 * (High + Low) – 0.07 * High
* 突破买入价 = 观察卖出价 + 0.25 * (观察卖出价 – 观察买入价)
* 突破卖出价 = 观察买入价 – 0.25 * (观察卖出价 – 观察买入价)
  
### 实时判断触发条件，数据用五分钟线
        1. 趋势
        if before_2_close <= bbreak and before_1_close > bbreak:
            if long_position == 0:
                print context.now, '趋势向上突破，买入开仓', amount
                futures_account.order(symbol, amount, 'open')
            if short_position != 0:
                print context.now, '趋势向上突破，买入平仓', short_position
                futures_account.order(symbol, short_position, 'close')
        if before_2_close >= sbreak and before_1_close < sbreak:
            if short_position == 0:
                print context.now, '趋势向下突破，卖出开仓', amount
                futures_account.order(symbol, -amount, 'open')
            if long_position != 0:
                print context.now, '趋势向下突破，卖出平仓', long_position
                futures_account.order(symbol, -long_position, 'close')
                
        2. 反转,多单反转
        if before_1_high > ssetup and before_1_close > senter:
            context.count1 = 1
        if context.count1 == 1 and before_1_close < senter:
            # print context.now, '趋势向下反转，卖出', long_position
            if long_position > 0:
                print context.now, '趋势向下反转，卖出平仓', long_position, '买入开仓', amount
                futures_account.order(symbol, -long_position, 'close')
                futures_account.order(symbol, -amount, 'open')

        3. 空单反转
        if before_1_low < bsetup:
            context.count2 = 1
        if context.count2 == 1 and before_1_close > benter:
            # print '趋势向上反转，买入'
            if short_position != 0:
                print context.now, '趋势向上反转，买入平仓', short_position, '卖出开仓', amount
                futures_account.order(symbol, short_position, 'close')
                futures_account.order(symbol, amount, 'open')

    elif current_time >= '14:55:00':
        if futures_account.get_positions():
            futures_account.close_all_positions()


## 股票多因子对冲


##


##


##