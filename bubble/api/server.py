from flask import Flask
from flask import request
from flask_login import LoginManager, login_user
import sqlalchemy
from numpy import unicode
import json
from bubble.data.redis_con import rcon
from bubble.data.home import stock_pool, index_forecast, industry_forecast, get_index_quote
from bubble.data.api import DataApi
from bubble.utils.logger import log
from bubble.utils.func import pack_res



# @app.route('/login', methods=['get', 'post'])
# def login():
#     # 获取通过url请求传参的数据
#     username = request.values.get('name')
#     # 获取url请求传的密码，明文　
#     pwd = request.values.get('pwd')
#     # 判断用户名、密码都不为空，如果不传用户名、密码则username和pwd为None
#     if username and pwd:
#         if username == 'xsnimm' and pwd == '111':
#             res = {'code': 200, 'message': '登录成功'}
#             return pack_res(res)  # 将字典转换为Json串，json是字符串
#         else:
#             res = {'code': -1, 'message': '账号密码错误'}
#             return pack_res(res)
#     else:
#         res = {'code': 1001, 'message': '参数不能为空'}
#         return pack_res(res)


# def create_app():
app = Flask(__name__)
app.config.from_object('app.secure')
app.config.from_object('app.setting')
db = sqlalchemy(app)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'web_login'
login_manager.login_message = '请先登陆或注册'


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), unique = True)
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
    # 下面四种方法的作用具体看flaskweb档案
    def is_authenticated(self):
        return True
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.nickname)


@app.route('/login', methods=['POST'])
def login():
    user_id = request.form.get('user_id')
    passwd = request.form.get('passwd')
    user = User.query.filter_by(user_id=user_id, passwd=md5(passwd)).first()
    if user and user.check_password(form.password.data):
        if not user:
            return Response('用户不存在')
        login_user(user)
        return Response('ok')


@app.route('/login', methods=['get', 'post'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by()


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