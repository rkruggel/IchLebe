
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length


# Form
# Register
class RegisterForm(FlaskForm):
    fullname = StringField("Fullname")
    username = StringField("Username", validators=[DataRequired(), Length(3,10)])
    email = EmailField("eMail", validators=[DataRequired(), Length(7,40)])
    password = PasswordField("Passwort", validators=[DataRequired(), Length(2,30)])
    passwordrepeated = PasswordField("Wiederhole Passwort", validators=[DataRequired(), Length(2,30)])
    submit = SubmitField()

# Form
# Login
class LoginForm(FlaskForm):
    username = StringField("Username oder eMail", validators=[DataRequired(), Length(3,40)])
    password = PasswordField("Passwort", validators=[DataRequired(), Length(2,30)])
    remember = BooleanField("Remember me?")
    submit = SubmitField()

