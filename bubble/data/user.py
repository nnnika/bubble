from bubble.api.base import db


class User(db.Model):
    __tablename__ = 'app_user_info'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))
    nickname = db.Column(db.String(64))
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(11), unique=True)
    role = db.Column(db.String(64))
    freeze = db.Column(db.Integer)
    # posts = db.relationship('Post', backref='author', lazy='dynamic')
    # 下面四种方法的作用具体看flaskweb档案

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get(self):
        return str(self.id)

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)