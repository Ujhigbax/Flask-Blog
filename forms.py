from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    username = TextField('Enter Username: ',validators=[DataRequired()])
    password = PasswordField('Enter Password: ',validators=[DataRequired()])

class RegisterForm(FlaskForm):
    username=TextField('Enter a Username: ',validators=[DataRequired(),Length(min=3,max=25)])
    email=TextField('Enter an Email: ',validators=[DataRequired(),Email(),Length(min=6,max=40)])
    password=PasswordField('Enter a Password: ',validators=[DataRequired(),Length(min=6,max=25)])
    confirm=PasswordField('Confirm Password: ',validators=[DataRequired(),EqualTo('password',message='Passwords must match')])

class MessageForm(FlaskForm):
    title = TextField('Enter a Title: ',validators=[DataRequired()])
    description=TextField('Enter Post: ',validators=[DataRequired(),Length(max=140)])