from flask import Flask
from flask import request
import json
from bubble.data.redis_con import rcon
from bubble.data.home import stock_pool, index_forecast, industry_forecast

server = Flask(__name__)


@server.route('/login',methods=['get','post'])
def login():
    # 获取通过url请求传参的数据
    username = request.values.get('name')
    # 获取url请求传的密码，明文　
    pwd=request.values.get('pwd')
    # 判断用户名、密码都不为空，如果不传用户名、密码则username和pwd为None
    if username and pwd:
        if username == 'xiaoshi' and pwd == '111':
            resu={'code':200,'message':'登录成功'}
            return json.dumps(resu,ensure_ascii=False)# 将字典转换为Json串，json是字符串
        else:
            resu={'code':-1,'message':'账号密码错误'}
            return json.dumps(resu,ensure_ascii=False)

    else:
        res={'code':1001,'message':'参数不能为空'}
        return json.dumps(res,ensure_ascii=False)


@server.route('/visit_counter',methods=['get','post'])
def visit_counter():
    r = rcon()
    r.incr('count', 1)
    count = int(r.get("count"))
    res = {'counter':f'{count}'}
    return json.dumps(res, ensure_ascii=False)


@server.route('/home', methods=['get', 'post'])
def home_visit():
    res = {"stock_pool": stock_pool,
           "index_forecast": index_forecast,
           "industry_forecast": industry_forecast}
    return json.dumps(res, ensure_ascii=False)


@server.route('/data/{table_name}', methods=['get', 'post'])
def table_data():
    res = {}
    return json.dumps(res, ensure_ascii=False)


if __name__== '__main__':
    server.run(debug=True,port=8888,host='0.0.0.0')