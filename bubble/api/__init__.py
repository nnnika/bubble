

from bubble.api.user import user_bp
from bubble.api.factor import factor_bp
from bubble.api.home import home_bp
from bubble.api.profile import profile_bp
from bubble.api.base import app, db


app.register_blueprint(user_bp)
app.register_blueprint(factor_bp)
app.register_blueprint(home_bp)
app.register_blueprint(profile_bp)

