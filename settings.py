from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fghufh$$0-=jjjgu&&^%#4545__GHDHDGYE.'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# from views.posts import posts_bp
# app.register_blueprint(posts_bp)

from views.post_with_orm import post
app.register_blueprint(post)

from account.auth import auth
app.register_blueprint(auth)

from account.model import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
