from flask import Flask
from flask import request
from flask_login import LoginManager, login_user
from hashlib import md5
import json
from bubble.data.redis_con import rcon
from bubble.data.home import stock_pool, index_forecast, industry_forecast, get_index_quote
from bubble.data.api import DataApi
from bubble.utils.logger import log
from bubble.utils.func import pack_res
from bubble.api.base import app
from bubble.data.user import User


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'web_login'
login_manager.login_message = '请先登陆或注册'


@app.route('/user/login', methods=['POST'])
def login():
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
    username = param_dic.get('username')
    password = param_dic.get('password')
    user = User.query.filter_by(username=username, password=md5(password.encode('utf8')).hexdigest()).first()
    # if user and user.check_password(request.form.password.data):
    if not user:
        return pack_res({}, code=-1, msg="用户不存在")
    login_user(user)
    return pack_res({}, code=200, msg="success")

@app.route('/user/info', methods=['POST', 'GET'])
def info():
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
    token = param_dic.get('token')
#     user = User.query.filter_by(username=username, password=md5(password.encode('utf8')).hexdigest()).first()
#     # if user and user.check_password(request.form.password.data):
#     if not user:
#         return pack_res({}, code=-1, msg="用户不存在")
    info = {
        "roles": ["admin"],
        "name": "wally",
        "avatar": "",
        "introduction": "a test account"
    }
    return pack_res(info,code=200, msg="success")


@app.route('/user/logout', methods=['POST'])
def logout():
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
    # token = param_dic.get('token')
#     user = User.query.filter_by(username=username, password=md5(password.encode('utf8')).hexdigest()).first()
#     # if user and user.check_password(request.form.password.data):
#     if not user:
#         return pack_res({}, code=-1, msg="用户不存在")
    info = {
        
    }
    return pack_res(info,code=200, msg="success")


@app.route('/user/avatar_upload', methods=['POST'])
def avatar_upload():
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
    print(request.files)
    # todo 完成图片文件的服务器端保存，并返回头像地址
    info = {
        "files": {
            "avatar": "http://www.wallyi.com/img/1.jpg"
        }        
    }
    return pack_res(info,code=200, msg="success")


@app.route('/visit_counter', methods=['get', 'post'])
def visit_counter():
    r = rcon()
    r.incr('count', 1)
    count = int(r.get("count"))
    res = {'counter': f'{count}'}
    return pack_res(res)


@app.route('/home', methods=['get', 'post'])
def home_visit():
    res = {"stock_pool": stock_pool,
           "index_forecast": index_forecast,
           "industry_forecast": industry_forecast}
    return pack_res(res)


@app.route('/data/<table>', methods=['GET', 'POST'])
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
    return pack_res(res)


@app.route('/factor/<table>', methods=['GET', 'POST'])
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
    return pack_res(res)


if __name__ == '__main__':
    app.run(debug=True, port=8888, host='0.0.0.0')
