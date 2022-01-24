import json
import pymysql


class DataApi(object):

    def __init__(self):
        pass

    def get(self, table, code, start, end, fields):
        return getattr(self, table)(code, start, end, fields)

    def get_factor(self, table, code, start, end):
        try:
            # 数据库读写, 创建mysql数据库连接对象
            connection = pymysql.Connect(host='122.112.170.96', user='bubble', passwd='bubble', db='db_bubble',
                                         port=3306, charset='utf8')
            cur = connection.cursor()  # 创建mysql数据库游标对象   port要不要？
            sql = "SELECT datetime, value, code FROM factor_index_quote_close"
            cur.execute(sql)
            data = cur.fetchall()
            cur.close()
            connection.close()
            # 循环读取元组数据
            jsonData = []
            for row in data:
                result = {}
                result['datetime'] = row[0]
                result['value'] = row[1]
                jsonData.append(result)
        except:
            print('MySQL connect fail...')
        else:
            # ensure_ascii=False，能够防止中文乱码。
            # json.dumps()是将原始数据转为json，而json.loads()是将json转为原始数据。
            jsondatar = json.dumps(jsonData, ensure_ascii=False)
            return jsondatar[1:len(jsondatar) - 1]  # 去除首尾的中括号

        # return {
        #     "000001.SH": {"date": ['2021-01-05', ], "value": [3600, ]}
        # }
