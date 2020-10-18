from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo,Length


class AddUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(max=25,min=5,message='Username length should between 5~25')])
    email = StringField('Email Address', validators=[DataRequired(),Email()])
    password1 = PasswordField('Password', validators=[DataRequired(message='Not Allowed Empty Password'),Length(min=5,message='Password length should greater than 5')])
    password2 = PasswordField('Please Repeat Password', validators=[DataRequired(), EqualTo('password1')])
    admin_auth = BooleanField('Admin')
    submit = SubmitField('Add a new User')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='Empty Username')])
    password = PasswordField('Password', validators=[DataRequired(message='Empty Password')])
    submit = SubmitField('Login')


class ChangePassword(FlaskForm):
    username = StringField('Please input your Username', validators=[DataRequired(message='Empty Username')])
    password = PasswordField('Old Password', validators=[DataRequired(message='Empty Password'),Length(min=5,message='Password length should greater than 5')])
    password1 = PasswordField('New Password',validators=[DataRequired(message='Not Allowed Empty Password'),Length(min=5,message='Password length should greater than 5')])
    password2 = PasswordField('Please Repeat Password', validators=[DataRequired(), EqualTo('password1')])
    submit = SubmitField('Reset your Password')


class ResetPassword(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(),Email()])
    submit = SubmitField('Reset your Password')