from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Games(db.Model):
    game_id = db.Column(db.Integer, primary_key=True)
    game_title = db.Column(db.String(64), index=True, nullable=False)
    game_genre = db.Column(db.String(64), index=True)
    game_platform = db.Column(db.String(64), index=True)
    game_publisher = db.Column(db.String(64), index=True)
    game_year = db.Column(db.Integer, index=True)
    game_sales_global = db.Column(db.Float, index=True)
    game_sales_ranking = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<Game {}>'.format(self.game_title)

    def get_id(self):
        return str(self.game_id)



@login.user_loader
def load_user(id):
    return User.query.get(int(id))