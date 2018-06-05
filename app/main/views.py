from flask import render_template, session, redirect, url_for, flash
from .forms import LoginForm

from . import main
from ..email import send_mail


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/explore')
def explore():
    return render_template('explore.html')


@main.route('/help')
def help():
    return render_template('help.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print('BlogID: %s Login' % form.blog_id)
        flash('username error or password error!')
        return redirect(url_for('main.login'))
    if(session.get('form')):
        form = session.get('form')
    return render_template('login.html', form=form)


@main.route('/get_password')
def get_password():
    return render_template('get_password.html')


@main.route('/send_mail')
def sendmail():
    return send_mail()
