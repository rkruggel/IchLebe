'''
Demo

Prog:       Demo_2
Date:       17.03.2023

Youtube:    Web Development mit Flask - Full Stack App mit SQLAlchemy & Bootstrap
            Coding Crashkurse
            https://www.youtube.com/watch?v=nC7vQn0jZXw
'''


from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from wtforms.validators import DataRequired, Length
from flask_sqlalchemy import SQLAlchemy
from bcrypt import hashpw, checkpw, gensalt

def get_hashed_pw(plain_password):
    return hashpw(plain_password.encode("utf-8"), gensalt())

def check_password(plain_password, hashed_password):
    return checkpw(plain_password.encode("utf-8"), hashed_password=hashed_password)


db = SQLAlchemy()


app = Flask(__name__)
app.config["SECRET_KEY"] = "kldsköfhlakvbdskhfj22342tqg"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
bootstrap = Bootstrap5(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"      # die Route Classname

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

db.init_app(app)

# Model
# User
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

# Form
# Register
class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(3,10)])
    password = PasswordField("Passwort", validators=[DataRequired(), Length(2,30)])
    passwordrepeated = PasswordField("Wiederhole Passwort", validators=[DataRequired(), Length(2,30)])
    submit = SubmitField()

# Form
# Login
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(3,10)])
    password = PasswordField("Passwort", validators=[DataRequired(), Length(2,30)])
    remember = BooleanField("Remember me?")
    submit = SubmitField()

# Erstellt die Datenbank
with app.app_context():
    db.create_all()


# Route
# Index
@app.route("/")
def index():
    if current_user.is_active:
        return render_template("index.html", user=current_user.username)
    return render_template("index.html")

# Route
# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = get_hashed_pw(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("register.html", form=form)

# Route
# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password(form.password.data, user.password):
            login_user(user, remember=form.remember.data)
            flash("Du wurdest erfolgreich eingelogged")
            return redirect(url_for("dashboard"))
        return render_template("login.html", form=form, error="Invalide Credentials")
    return render_template("login.html", form=form)

# Route
# Dashboard
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user.username)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))



