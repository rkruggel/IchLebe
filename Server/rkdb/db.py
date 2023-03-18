from flask_sqlalchemy import SQLAlchemy
#from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_login import UserMixin

db = SQLAlchemy()


# Model
# User
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    fullname = db.Column(db.String)







