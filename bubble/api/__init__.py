
from flask_login import LoginManager, login_user
from bubble.api.user import user_bp
from bubble.api.factor import factor_bp
from bubble.api.home import home_bp
from bubble.api.profile import profile_bp
from bubble.api.base import app, db


app.register_blueprint(user_bp)
app.register_blueprint(factor_bp)
app.register_blueprint(home_bp)
app.register_blueprint(profile_bp)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/user/login'
login_manager.login_message = '请先登陆或注册'