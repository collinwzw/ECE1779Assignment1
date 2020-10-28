from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo,Length;


class AddUserForm(FlaskForm):
    """
        AddUserForm class is to define the form on /adduser page.
        """
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(max=25,min=5,message='Username length should between 5~25')])
    email = StringField('Email Address', validators=[DataRequired(),Email()])
    password1 = PasswordField('Password', validators=[DataRequired(message='Not Allowed Empty Password'),
                                                      Length(max=25,min=5,message='Password length should between 5~25')])
    password2 = PasswordField('Please Repeat Password',
                              validators=[DataRequired(),
                                          EqualTo("password1",message='Your password and repeat password do not match')])
    admin_auth = BooleanField('Admin')
    submit = SubmitField('Add a new User')


class LoginForm(FlaskForm):
    """
          LoginForm class is to define the form on /login page. username, password of user needs to be input.
          """
    username = StringField('Username', validators=[DataRequired(message='Empty Username')])
    password = PasswordField('Password', validators=[DataRequired(message='Empty Password')])
    submit = SubmitField('Login')


class ChangePassword(FlaskForm):
    """
          ChangePassword class is to define the form on /changemypassword page.
          """
    username = StringField('Please input your Username', validators=[DataRequired(message='Empty Username')])
    password = PasswordField('Old Password', validators=[DataRequired(message='Empty Password'),
                                                         Length(max=25, min=5,message='Password length should between 5~25')])
    password1 = PasswordField('New Password',validators=[DataRequired(message='Not Allowed Empty Password'),
                                                         Length(max=25, min=5 ,message='Password length should between 5~25'),
                                                         ])
    password2 = PasswordField('Please Repeat Password',
                              validators=[DataRequired(),
                                          EqualTo('password1', message='Your password and repeat password do not match')])
    submit = SubmitField('Reset your Password')


class ResetPassword(FlaskForm):
    """
              AddUserForm class is to define the form on /resetpasword page
              """
    email = StringField('Email Address', validators=[DataRequired(),Email()])
    submit = SubmitField('Reset your Password')