host='122.112.170.96'
user='bubble'
passwd='bubble'
db='db_bubble'
port=3306
charset='utf8'


SECRET_KEY = 'bubble123456'

class Config(object):
    TESTING = False
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}?charset={charset}'
    SECRET_KEY = SECRET_KEY
    IMG_UPLOAD_PATH = "d:/"
    AUTH_HEADER_NAME = "token"
