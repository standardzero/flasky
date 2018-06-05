from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required


class LoginForm(FlaskForm):
    blog_id = StringField('Blog ID', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Login')
