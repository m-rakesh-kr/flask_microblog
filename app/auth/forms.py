from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Regexp
from app.models import User


class LoginForm(FlaskForm):
    username_or_email = StringField('Username or Email', validators=[DataRequired()],
                                    render_kw={"placeholder": "Enter your username or email"})
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={"placeholder": "Enter your password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    full_name = StringField('Your Name', validators=[
        validators.DataRequired(message='Full Name is required.'),
        validators.Length(min=2, max=128, message='Full Name must be between 2 and 128 characters.'),
    ], render_kw={"placeholder": "Enter your full name (min-2 max-128)"})
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=4, max=20),  # Set a range for username length
        Regexp('^[a-zA-Z0-9_]*$', message='Username must contain only letters, numbers, or underscores')
    ], render_kw={"placeholder": "Enter your username (min-4 max-20)"})

    email = StringField('Email', validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "Enter your Email"})

    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long'),
        Regexp(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_+{}|:"<>?~]).{8,}$',
               message='Password must contain at least one digit, one lowercase and uppercase letter, and one special character')
    ], render_kw={"placeholder": "Enter your Password"})

    password2 = PasswordField('Repeat Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ], render_kw={"placeholder": "Enter your Confirm Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username, This one is taken by someone')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address, This one is taken by someone')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter your Email"})
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                'Your email is not registered with my microblog database? Try again with registered email')


class SetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long'),
        Regexp(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_+{}|:"<>?~]).{8,}$',
               message='Password must contain at least one digit, one lowercase and uppercase letter, and one special character')
    ], render_kw={"placeholder": "Enter your Password"})

    password2 = PasswordField('Repeat Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ], render_kw={"placeholder": "Enter your Confirm Password"})

    submit = SubmitField('Submit')
