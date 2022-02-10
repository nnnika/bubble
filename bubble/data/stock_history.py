# 最近3个交易日的累计最高收益率，没有涨停

import tushare as ts
# ts.set_token('c887114ec2f20223fccd4c2fc53138ddfc2e4c2f5a20ede5b3797bd2')
# api = ts.pro_api()
api = ts.pro_api('c887114ec2f20223fccd4c2fc53138ddfc2e4c2f5a20ede5b3797bd2')

df = api.stock_basic(fields='ts_code,name,list_date')

print(df)
