from flask import Flask
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fghufh$$0-=jjjgu&&^%#4545__GHDHDGYE.'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# from views.posts import posts_bp
# app.register_blueprint(posts_bp)


if __name__ == '__main__':

    from views.post_with_orm import post
    app.register_blueprint(post)

    app.run()
