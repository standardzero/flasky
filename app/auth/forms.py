from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    blog_id = StringField('Blog ID', validators=[DataRequired(),
                                                 Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class GetPasswordForm(FlaskForm):
    blog_id = StringField('Blog ID', validators=[DataRequired(),
                                                 Length(1, 64)])
    email = StringField('Password', validators=[DataRequired(),
                                                Length(1, 64), Email()])
    submit = SubmitField('Submit')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Passowrd', validators=[DataRequired(),
        EqualTo('password2', message='Password must match'),Length(1, 64)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(),
                                                              Length(1, 64)])
    submit = SubmitField('Submit')
