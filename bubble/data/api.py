import pymysql
from bubble.utils.logger import log
from bubble.config import host, user, passwd, db, port, charset

connection = pymysql.Connect(host=host, user=user, passwd=passwd, db=db, port=port, charset=charset)


class DataApi(object):

    def __init__(self):
        pass

    def get(self, table, code, start, end, fields):
        return getattr(self, table)(code, start, end, fields)

    def get_factor(self, table, code, start, end):
        try:
            connection.ping(reconnect=True)
            cur = connection.cursor()  # 创建mysql数据库游标对象
            sql = f"SELECT datetime, value, code FROM {table} WHERE datetime BETWEEN '{start}' AND '{end}'"
            cur.execute(sql)
            data = cur.fetchall()
            cur.close()
            # 循环读取元组数据
            date_list = []
            value_list = []
            for row in data:
                date_list.append(row[0].strftime('%Y-%m-%d'))
                value_list.append(float(row[1]))
            Packed = {f"{code}": {"date": date_list, "value": value_list}}
        except Exception as e:
            log.debug(start, end, code, table)
            log.exception(e)
            print('MySQL connect fail...')
            return {}
        else:
            return Packed   # return {"000001.SH": {"date": ['2021-01-01', ], "value": [3600, ]}}
