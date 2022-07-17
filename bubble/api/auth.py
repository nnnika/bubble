import time
import json
import os
from hashlib import md5
from flask import request
from flask import Blueprint
from flask_login import LoginManager, login_user
from bubble.utils.logger import log
from bubble.utils.func import pack_res, save_file
from bubble.data.user import User
from bubble.utils.gen_jwt import user_id_to_token, token_to_user_id
from bubble.utils.const import (RESP_LOGIN_EXPIRED, RESP_SUCCESS)
from jwt.exceptions import ExpiredSignatureError
from bubble.api.base import db,login_manager


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@login_manager.user_loader
def load_user(user_id):
    return str(user_id)


@auth_bp.route('/login', methods=['POST'])
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

    print(user.id)
    token = user_id_to_token(user.id)
    return pack_res({
        "token": token
    }, code=200, msg="success")


@auth_bp.route('/logout', methods=['POST'])
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
    return pack_res(info, code=200, msg="success")