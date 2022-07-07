from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger, swag_from
from flask_login import LoginManager, login_user

app = Flask(__name__)
app.config.from_object('bubble.config.Config')
db = SQLAlchemy(app)
db.init_app(app)
app.config['SWAGGER'] = {
    'title': 'Flasgger RESTful',
    'uiversion': 2
}
swag = Swagger(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/user/login'
login_manager.login_message = '请先登陆或注册'