import time
import json
import os
from hashlib import md5
from flask import request
from flask import Blueprint
from flask_login import LoginManager, login_user
from flask_restful import Api, Resource, url_for
from bubble.utils.logger import log
from bubble.utils.func import pack_res, save_file
from bubble.data.user import User
from bubble.utils.gen_jwt import user_id_to_token, token_to_user_id
from bubble.utils.const import (RESP_LOGIN_EXPIRED, RESP_SUCCESS)
from jwt.exceptions import ExpiredSignatureError
from bubble.api.base import db


profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

api = Api(profile_bp)


@api.resource('/<int:user_id>')
class UserProfile(Resource):


    def get(self, user_id):
        pass



