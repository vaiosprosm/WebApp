from flask_login import UserMixin

from WebApp import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(36), nullable=False)
    profile_image = db.Column(db.String(30), default="default_profile_image.jpg")

    def __repr__(self):
        return f"{self.username}: {self.email}"
