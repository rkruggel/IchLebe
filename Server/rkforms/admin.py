from flask_wtf import FlaskForm
#from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms import *
from wtforms.validators import DataRequired, Length, Email


# Form
# Userdata
# class UserdataForm(FlaskForm):

#     #aa = formdata
    
#     # s1 = SelectField("username", choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
#     #s1 = SelectField("username" )

#     suchfeld = input("Suchen mit %")
#     submitsuchen = SubmitField(label="suchfeld")



#     username = StringField("Username oder eMail", validators=[DataRequired(), Length(3,40)])
#     password = PasswordField("Passwort", validators=[DataRequired(), Length(2,30)])
#     remember = BooleanField("Remember me?")

#     vorname = StringField("Vorname")
#     nachname = StringField("Nachname")

#     submit = SubmitField()

