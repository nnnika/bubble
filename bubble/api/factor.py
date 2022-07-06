import time
import json
import os
from hashlib import md5
from flask import request
from flask import Blueprint
from flask_login import LoginManager, login_user
from bubble.utils.logger import log
from bubble.utils.func import pack_res, save_file
from bubble.api.base import app
from bubble.data.user import User
from bubble.utils.gen_jwt import user_id_to_token, token_to_user_id
from bubble.utils.const import (RESP_LOGIN_EXPIRED, RESP_SUCCESS)
from jwt.exceptions import ExpiredSignatureError
from bubble.data.api import DataApi
from bubble.utils.logger import log

factor_bp = Blueprint('factor', __name__, url_prefix='/factor')


@factor_bp.route('/<table>', methods=['GET', 'POST'])
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


# @app.route('/data/<table>', methods=['GET', 'POST'])
# def table_data(table):
#     log.debug(table)
#     param_dic = {}
#     if request.method == "GET":
#         param_dic = request.args
#     if request.method == "POST":
#         if request.content_type is None:
#             pass
#         elif request.content_type.startswith('application/json'):
#             param_dic = request.json
#         elif request.content_type.startswith('multipart/form-data'):
#             param_dic = request.form
#         else:
#             param_dic = request.values
#
#     start = param_dic.get('start')
#     end = param_dic.get('end')
#     fields = param_dic.get('fields')
#     code = param_dic.get('code')
#     res = DataApi().get_factor(table, code, start, end)
#     return pack_res(res)