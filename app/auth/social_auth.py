from flask import redirect, url_for, flash, render_template
from flask_login import current_user, login_user, logout_user, login_required
from flask_oauthlib.client import OAuth

from app import db
from app.auth import bp
from app.auth.forms import SetPasswordForm
from app.models import User
from config import Config

oauth = OAuth()

# Configure OAuth provider (Google)
google = oauth.remote_app(
    'google',
    consumer_key=Config.GOOGLE_CLIENT_ID,
    consumer_secret=Config.GOOGLE_CLIENT_SECRET,
    request_token_params={
        'scope': 'email',  # https://www.googleapis.com/auth/userinfo.profile

    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


@bp.route('/login/google')
def google_login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return google.authorize(callback=url_for('auth.google_authorized', _external=True))


@bp.route('/login/google/authorized')
def google_authorized():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        flash('Authentication failed. Details: {}'.format(response), 'danger')
        return redirect(url_for('auth.login'))

    user_info = google.get('userinfo', token=(response['access_token'], ''))
    email = user_info.data['email']

    # Check if the user already exists in the database
    user = User.query.filter_by(email=email).first()

    # Access additional fields like name
    # name = user_info.data.get('name')

    if not user:
        username = email.split('@')[0]
        new_user = User(username=username, email=email, registration_complete=False)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful.Please set your password.', 'success')
        login_user(new_user, remember=True)
        return redirect(url_for('auth.set_password'))

    elif not user.registration_complete:
        flash('Registration successful. Please set your password.', 'success')
        login_user(user, remember=True)
        return redirect(url_for('auth.set_password'))

    # If the user already exists, and registration completed then log them in
    login_user(user, remember=True)
    return redirect(url_for('main.index'))


@bp.route('/set_password', methods=['GET', 'POST'])
@login_required
def set_password():
    form = SetPasswordForm()
    if form.validate_on_submit():
        current_user.set_password(form.password.data)
        current_user.registration_complete = True
        db.session.commit()
        flash('Password successfully set. You are now logged in.', 'success')
        return redirect(url_for('main.index'))

    return render_template('auth/set_password.html', title='Set Password', form=form)
