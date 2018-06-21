from flask import render_template, session, redirect, url_for, flash
from flask_login import login_required
from .forms import RegistrationForm
from ..models import User

from . import main
from ..email import send_email
from .. import db
from ..auth import auth
from .token import generate_confirmation_token

@main.route('/', methods=['GET', 'POST'])
def index():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(blog_id=form.blog_id.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = generate_confirmation_token(user.blog_id)
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        print('You can now login')
        return redirect(url_for('auth.login'))
    return render_template('index.html', form=form)


@main.route('/explore')
def explore():
    return render_template('explore.html')


@main.route('/help')
def help():
    return render_template('help.html')


@main.route('/secret')
@login_required
def secret():
    return 'Only authenticated users ara allowed!'


@main.route('/welcome')
def welcome():
    return render_template('welcome.html')
