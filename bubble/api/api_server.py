from flask import Flask
from flask import request
import json
from bubble.data.redis_con import rcon
from bubble.data.home import stock_pool, index_forecast, industry_forecast, get_index_quote
from bubble.data.api import DataApi
from bubble.utils.logger import log

server = Flask(__name__)


@server.route('/login', methods=['get', 'post'])
def login():
    # 获取通过url请求传参的数据
    username = request.values.get('name')
    # 获取url请求传的密码，明文　
    pwd = request.values.get('pwd')
    # 判断用户名、密码都不为空，如果不传用户名、密码则username和pwd为None
    if username and pwd:
        if username == 'xsnimm' and pwd == '111':
            res = {'code': 200, 'message': '登录成功'}
            return json.dumps(res, ensure_ascii=False)  # 将字典转换为Json串，json是字符串
        else:
            res = {'code': -1, 'message':'账号密码错误'}
            return json.dumps(res, ensure_ascii=False)
    else:
        res = {'code': 1001, 'message': '参数不能为空'}
        return json.dumps(res, ensure_ascii=False)


@server.route('/visit_counter', methods=['get', 'post'])
def visit_counter():
    r = rcon()
    r.incr('count', 1)
    count = int(r.get("count"))
    res = {'counter': f'{count}'}
    return json.dumps(res, ensure_ascii=False)


@server.route('/home', methods=['get', 'post'])
def home_visit():
    res = {"stock_pool": stock_pool,
           "index_forecast": index_forecast,
           "industry_forecast": industry_forecast}
    return json.dumps(res, ensure_ascii=False)


@server.route('/data/<table>', methods=['GET', 'POST'])
def table_data(table):
    log.debug(table)
    param_dic = {}
    if request.method == "GET":
        param_dic = request.args
    if request.method == "POST":
        if request.content_type is None:
            pass
        elif request.content_type.startswith('application/json'):
            param_dic = request.json
        elif request.content_type.startswith('multipart/form-data'):
            param_dic = request.form
        else:
            param_dic = request.values

    start = param_dic.get('start')
    end = param_dic.get('end')
    fields = param_dic.get('fields')
    code = param_dic.get('code')
    res = DataApi().get_factor(table, code, start, end)
    return json.dumps(res, ensure_ascii=False)


@server.route('/factor/<table>', methods=['GET', 'POST'])
def factor_data(table):
    log.debug(table)
    param_dic = {}
    if request.method == "GET":
        param_dic = request.args
    if request.method == "POST":
        if request.content_type is None:
            pass
        elif request.content_type.startswith('application/json'):
            param_dic = request.json
        elif request.content_type.startswith('multipart/form-data'):
            param_dic = request.form
        else:
            param_dic = request.values

    start = param_dic.get('start')
    end = param_dic.get('end')
    code = param_dic.get('code')
    res = DataApi().get_factor(table, code, start, end)
    return json.dumps(res, ensure_ascii=False)


if __name__ == '__main__':
    server.run(debug=True,port=8888,host='0.0.0.0')