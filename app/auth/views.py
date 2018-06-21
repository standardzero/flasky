from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User
from .forms import LoginForm, GetPasswordForm, ResetPasswordForm
from .. import db
from ..email import send_email
from ..main.token import confirm_token, generate_confirmation_token


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('auth.login'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(blog_id=form.blog_id.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.welcome'))
        flash('Invalid username or password')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect('main.index')


@auth.route('/get_password', methods=['GET', 'POST'])
def get_password():
    form = GetPasswordForm()
    if form.validate_on_submit():
        print("blog_id: %s, email: %s" % (form.blog_id.data, form.email.data))
        user = User.query.filter_by(blog_id=form.blog_id.data,
                                    email=form.email.data).first()
        if user is None:
            flash('Blog ID or Email is Error!', 'danger')
            return render_template('auth/get_password.html', form=form)
        user_info = [form.blog_id.data, form.email.data]
        token = generate_confirmation_token(user_info)
        send_email(form.email.data, "Get Password",
                   "auth/email/reset_password", token=token)
        user.reset_password_link_visited = False
        db.session.commit()
        return '<h1>The get password link send to your email!</h1>'
    return render_template('auth/get_password.html', form=form)


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user_info =  confirm_token(token)
    if user_info is None:
        return '<h1>The link is invaild or expired!</h1>'
    user = User.query.filter_by(blog_id=user_info[0],
                                email=user_info[1]).first()
    if user is None:
        return '<h1>The link is invaild or expired!</h1>'
    if user.reset_password_link_visited:
        return '<h1/>The link is invaild or expired!</h1>'
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.reset_password_link_visited = True
        password = form.password.data
        user.password = password
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/confirm/<token>')
def confirm(token):
    blog_id = confirm_token(token)
    if blog_id is None:
        flash('The confirmation link is invalid or has expired.', 'danger')
        print('The confirmation link is invalid or has expired.')
        return redirect(url_for('auth.login'))
    print('blog_id: %s' % blog_id)
    user = User.query.filter_by(blog_id=blog_id).first()
    if user is None:
        flash('The confirmation link is invalid or has expired.', 'danger')
        print('The confirmation link is invalid or has expired.')
        return redirect(url_for('auth.login'))

    if user.confirmed:
        print('current_user name: %s' % user.blog_id)
        return redirect(url_for('auth.login'))
    else:
        user.confirmed = True
        db.session.commit()
        print('You have confirmed your account. Thanks!')
        flash('You have confirmed your account. Thanks!', 'success')
        return redirect(url_for('auth.login'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.blog_id)
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('auth.login'))
