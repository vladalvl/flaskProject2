from app import db
from datetime import datetime


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.now())
    title = db.Column(db.Text)
    content = db.Column(db.Text)
