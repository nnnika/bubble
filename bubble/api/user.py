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

user_bp = Blueprint('user', __name__, url_prefix='/user')


@login_manager.user_loader
def load_user(user_id):
    return str(user_id)


@user_bp.route('/login', methods=['POST'])
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


@user_bp.route('/info', methods=['POST', 'GET'])
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
    user_id = token_to_user_id(token)
    avatar_url = "http://invest.wallyi.com/file/img/{}.jpg".format(user_id)
    info = {
        "user_id": user_id,
        "roles": ["admin"],
        "name": "wally",
        "avatar": avatar_url,
        "introduction": "a test account"
    }
    return pack_res(info, code=200, msg="success")


@user_bp.route('/logout', methods=['POST'])
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


@user_bp.route('/avatar_upload', methods=['POST'])
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
    token = request.headers["Token"]
    try:
        user_id = token_to_user_id(token)
    except ExpiredSignatureError as e:
        return pack_res({}, code=RESP_LOGIN_EXPIRED, msg="token expired.")
    avatar_file = str(user_id) + ".jpg"
    avatar_path = os.path.join(app.config["IMG_UPLOAD_PATH"], avatar_file)
    log.info(avatar_file)
    try:
        save_file(request.files["avatar"].read(), avatar_path)
        info = {
            "files": {
                "avatar": "http://invest.wallyi.com/file/img/{}?ts={}".format(avatar_file, int(time.time()))
            }
        }
    except Exception as e:
        log.exception(e)
        return pack_res({}, code=-1, msg="avatar save failed.")
    return pack_res(info, code=200, msg="success")


@user_bp.route('/info/edit', methods=['GET', "POST"])
def edit_info():
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
    token = request.headers["Token"]
    try:
        user_id = token_to_user_id(token)
    except ExpiredSignatureError as e:
        return pack_res({}, code=RESP_LOGIN_EXPIRED, msg="token expired.")
    info = User.query.get_or_404(user_id)
    info.email = param_dic.get("email")
    db.session.commit()
    return pack_res({}, code=200, msg="email save success")