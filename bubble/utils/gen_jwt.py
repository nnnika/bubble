import time
import jwt
from bubble.config import SECRET_KEY


def user_id_to_token(user_id):
    """生成一个JWT Token:param user::return:"""
    # 设置token的过期时间戳# 比如：设置1天过期
    timestamp = int(time.time()) + 60 * 60 * 24 * 1
    # 加密生成Token# 加密方式：HS256
    return jwt.encode({"user_id": user_id, "exp": timestamp}, SECRET_KEY,'HS256')


def token_to_user_id(token):
    payload = jwt.decode(token, key=SECRET_KEY, algorithms='HS256')
    return payload["user_id"]