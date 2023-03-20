from flask_sqlalchemy import SQLAlchemy
#from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_login import UserMixin

from datetime import datetime

db = SQLAlchemy()


# Model
# Abstract
class TimestampModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated = db.Column(db.DateTime, onupdate=datetime.now)


# Model
# User
#class Users(db.Model, UserMixin):
class Users(TimestampModel, UserMixin):
    '''
      Die Adresse des Users.
    '''
    #__tablename__ = "users"
    # id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    vorname = db.Column(db.String)
    nachname = db.Column(db.String)
    strasse =  db.Column(db.String)
    ort = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    geboren = db.Column(db.Date)
    aktiv = db.Column(db.Boolean)
    telefon = db.Column(db.String)
    handy = db.Column(db.String)
    admin = db.Column(db.Boolean)
    #messages = db.relationship('Messages', backref='users') #, lazy=True)
    # created = db.Column(db.DateTime)
    # updated = db.Column(db.DateTime)

    def __repr__(self):
        return f'Users {"self.username"}'


# Model
# Message
# class Messages(db.Model, UserMixin):
class Messages(TimestampModel, UserMixin):
    '''
      Hier wird eingetragen wer in welchen Situaltonen alamiert wird.
    '''
    #__tablename__ = "message"
    # id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) #, nullable=False)  # Verbindung zur Tabelle 'users'
    timeAblauf = db.Column(db.Integer)  # z.B. 26; Wenn sich der User 26 Stunden nicht gemeldet hat wird alarm ausgegeben.
    infotype = db.Column(db.String)     # z.B. SMS, email, handyalarm
    aktiv = db.Column(db.Boolean)
    handy = db.Column(db.String)        # Handynummer die benachrichtigt wird
    text = db.Column(db.String)         # Text der in der benachrichtigung steht
    
    def __repr__(self) -> str:
        return f'Messages {"text[:10]"}...'
    
# Model
# Leben
# class Lebens(db.Model, UserMixin):
class Lebens(TimestampModel, UserMixin):
    '''
      Hier wird ein Zeitstempel eingetragen wenn der User sich gemeldet hat.
    '''
    #__tablename__ = "leben"
    # id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)         # Verbindung zur Tabelle 'user'
    zeitstempel = db.Column(db.DateTime)    # Zeitstempel wenn der user sich gemeldet hat
    koordinate = db.Column(db.String)       # die Koordinate wo sich der user bein Zeitstempel befindet


