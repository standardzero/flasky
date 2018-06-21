from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms.validators import Regexp, Email, EqualTo
from ..models import User


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                                                 Email()])
    blog_id = StringField('Blog ID', validators=[DataRequired(), Length(1, 64),
                            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                   'Usernames must have only letters, numbers, dots or underscores')])
    password = PasswordField('Password', validators=[
                            DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Sign up')

    def validate_username(self, field):
        if User.query.filter_by(blog_id=field.data).first():
            raise ValidationError('Blog ID already in use.')
