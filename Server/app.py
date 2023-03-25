'''
Demo

Prog:       Server
Date:       18.03.2023

Youtube:    Web Development mit Flask - Full Stack App mit SQLAlchemy & Bootstrap
            Coding Crashkurse
            https://www.youtube.com/watch?v=nC7vQn0jZXw
'''


from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
#from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, BooleanField, SubmitField
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
#from wtforms.validators import DataRequired, Length
# from flask_sqlalchemy import SQLAlchemy
from bcrypt import hashpw, checkpw, gensalt
from datetime import date, datetime


from rkdb.db import db, Users, Messages, Lebens
from rkforms.login import RegisterForm, LoginForm
from rkforms.admin import *

from sqlalchemy import and_, select


def get_hashed_pw(plain_password):
    return hashpw(plain_password.encode("utf-8"), gensalt())

def check_password(plain_password, hashed_password):
    return checkpw(plain_password.encode("utf-8"), hashed_password=hashed_password)


# db = SQLAlchemy()


app = Flask(__name__)
app.config["SECRET_KEY"] = "kldsköfhlakvbdskhfj22342tqg"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ichlebe.db"
#app.config["SQLALCHEMY_ECHO"] = True
bootstrap = Bootstrap5(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"      # die Route Classname



@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

db.init_app(app)

# # Model
# # User
# class User(db.Model, UserMixin):
#     __tablename__ = "users"
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String, unique=True, nullable=False)
#     password = db.Column(db.String, nullable=False)
#     fullname = db.Column(db.String)


# # Form
# # Register
# class RegisterForm(FlaskForm):
#     fullname = StringField("Fullname")
#     username = StringField("Username", validators=[DataRequired(), Length(3,10)])
#     password = PasswordField("Passwort", validators=[DataRequired(), Length(2,30)])
#     passwordrepeated = PasswordField("Wiederhole Passwort", validators=[DataRequired(), Length(2,30)])
#     submit = SubmitField()

# # Form
# # Login
# class LoginForm(FlaskForm):
#     username = StringField("Username", validators=[DataRequired(), Length(3,10)])
#     password = PasswordField("Passwort", validators=[DataRequired(), Length(2,30)])
#     remember = BooleanField("Remember me?")
#     submit = SubmitField()



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
# Melden
@app.route("/melden")
#@login_required
def melden():
    return render_template("melden.html", info="n/a")

# Route
# Hilfe rufen
@app.route("/hilferufen")
#@login_required
def hilferufen():
    return render_template("hilferufen.html", info="n/a")

# Route
# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = get_hashed_pw(form.password.data)
        new_user = Users(fullname=form.fullname.data, username=form.username.data, password=hashed_password)
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
        # Hier wird der Userer entweder mit dem Usernamen gesucht oder mit der emailadresse
        if '@' in form.username.data:
            print ("> eine email")
            user = Users.query.filter_by(email=form.username.data).first()
        else:
            print ("> ein username")
            user = Users.query.filter_by(username=form.username.data).first()

        # check password
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
    return render_template("dashboard.html", vorname=current_user.vorname, nachname=current_user.nachname, user=current_user.username)

# Route
# Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

# demodaten einfügen
@app.route("/adddemodata")
def adddemodata():
    '''
      Demodaten einfügen
    '''
    with app.app_context():
        db.drop_all()
        db.create_all() 

    #print (date.today())
    # Userdaten erzeugen wenn keine vorhanden sind
    co = Users.query.count()
    if co == 0:
        newdata = Users(id=100, username="rkruggel", password=get_hashed_pw("12"), 
                        vorname="Roland", nachname="Kruggel", strasse="Beverstr 12", ort="58553 Halver",
                        email="rkruggel@bbf7.de", geboren=date(1959, 1, 2), aktiv=True, 
                        telefon="02353 6699940", handy="0174 2170044", admin=True  
                        )
        db.session.add(newdata)
        newdata = Users(id=101, username="pkruggel", password=get_hashed_pw("12"), 
                        vorname="Petra", nachname="Kruggel", strasse="Beverstr 12", ort="58553 Halver",
                        email="pkruggel@gmx.de", geboren=date(1954, 2, 3), aktiv=True, 
                        telefon="02353 6699940", handy="01525 2637011", admin=False 
                        )        
        db.session.add(newdata)
        newdata = Users(id=102, username="tkarrer", password=get_hashed_pw("12"), 
                        vorname="Tanja", nachname="Orthen", strasse="", ort="",
                        email="orthtaja@gmx.de", geboren=date(1989, 3, 12), aktiv=False, 
                        telefon="02183 3269586", handy="0176 39153897", admin=False  
                        )
        db.session.add(newdata)
        newdata = Users(id=103, username="roland", password=get_hashed_pw("12"), 
                        vorname="roland", nachname="kruggel", strasse="Testweg 12", ort="Testort",
                        email="rkruggel@gmx.de", geboren=date(1959, 1, 1), aktiv=True, 
                        telefon="02353 123456", handy="0174 1234567", admin=True 
                        )
        db.session.add(newdata)
        db.session.commit()

    co = Messages.query.count()
    if co == 0:
        db.session.add(Messages(user_id=100, timeAblauf=25*60, infotype="sms", aktiv=True, 
                                handy="0174 2541225", text="Schnell schnell" ) )
        db.session.add(Messages(user_id=100, timeAblauf=26*60, infotype="sms", aktiv=True, 
                                handy="0174 51254124", text="avanti, es eilt" ) )
        db.session.add(Messages(user_id=100, timeAblauf=30*60, infotype="sms", aktiv=False, 
                                handy="0174 1441522", text="Hilfe Polizei" ) )
        db.session.add(Messages(user_id=101, timeAblauf=15*60, infotype="sms", aktiv=True, 
                                handy="0174 1985214", text="Schnell bei Oma melden" ) )
        db.session.commit()

    co = Lebens.query.count()
    if co == 0:
        db.session.add(Lebens(user_id=100, zeitstempel=datetime.now(), koordinate="51.0010, 23.9389" ))
        db.session.add(Lebens(user_id=101, zeitstempel=datetime.now(), koordinate="51.0010, 23.9389" ))
        db.session.commit()


    return render_template("info.html", infotext="Info: Datenbank zurückgesetzt: " + datetime.now().strftime('%d.%m.%Y %H:%M:%S'))

# Route
# User Data
@app.route("/userdata", methods = ["GET", "POST"])
#@login_required
def userdata():

    if request.method == "GET":
        print (">>GET")

    if request.method == "POST":
        print (">> POST")

        suchenfeld = request.form.get("suchenfeld")
        print (f">> {suchenfeld}")

        #userliste1 = Users.query.fetchall()      #filter_by(username=form.username.data).first()
        #userliste2 = db.session.execute(db.select(Users).order_by(Users.nachname)).scalars()

        #stmt = select(Users)   #.username,Users.vorname,Users.nachname])  
        #stmt= stmt.where(and_(Users.columns.vorname=='joe',Users.columns.nachname==100)  
        #with db.connect() as con:
        #for row in db.execute(stmt):  
        #    print(row)

        # userliste = db.session.execute(
        #     select(Users.username, Users.vorname + " " + Users.nachname).where(Users.aktiv==True)
        # ).all()

        # einen datensatz lesen mit ID
        #print ("-----------------------------------------------------------------------------------------------------------------------")
        userliste = db.session.query(Users).filter(Users.username.like(f'{suchenfeld}'))
        for ii in userliste:
            print (f">>{ii.vorname} {ii.nachname}")
        # userliste = db.session.query(Users).filter(Users.username == f"{suchenfeld}")
        # for ii in userliste:
        #     print (f">>{ii.vorname} {ii.nachname}")



        # print ("-----------------------------------------------------------------------------------------------------------------------")
        # ul1 = db.get_or_404(Users, 102)
        # erg1 = ul1.username
        # print ("------------")
        # print (f">> {ul1}")
        # print (f">> {erg1}")
        # alle Datensätze lesen
        # ul2 = db.session.query(Users).all()
        # print ("------------")
        # print (f">> {ul2}")
        # for ii in ul2:
        #     erg2 = ii.vorname + " " + ii.nachname
        #     print (f">> {erg2}")

        # ??
        # fii  = [(x.username, x.vorname + " " + x.nachname) for x in userliste]
        # form = UserdataForm(obj=fii)
        # form.s1.choices= userliste  # [('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')]
        # form.remember=True

        return render_template("admin/userdata.html", userliste=userliste)

    return render_template("admin/userdata.html")


# Route
# User Data
@app.route("/usersingledata/<userlogin>", methods = ["GET", "POST"])
def usersingledata(userlogin):
    print (f">>> {userlogin}  {request.method}")


    if request.method == "GET":
        print("get")
        userdata = db.session.query(Users).filter(Users.username == userlogin).scalar()
        pass
        return render_template("admin/usersingledata.html", userdata=userdata)

    if request.method == "POST":
        print("post")
        # daten aus der Form lesen
        # username = request.form.get("username")
        # vorname = request.form.get("vorname")
        # nachname = request.form.get("nachname")
        return ""




# Route
# Alarmzeiten
@app.route("/alarmzeiten")
#@login_required
def alarmzeiten():
    return render_template("admin/alarmzeiten.html", info="n/a")




# programmstart für die Entwicklung
# starten mit: python3 app.py
if __name__ == "__main__":
    #app.run(host="127.0.0.1", port=5000, debug=True)
    app.run()

# programmstart in der Bereitstellung
# starten mit: python3 app.py
# if __name__ == '__main__':
#     from waitress import serve
#     serve(app, host='0.0.0.0', port=8080)


