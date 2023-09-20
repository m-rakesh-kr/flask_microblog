from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField, PasswordField
from wtforms.validators import DataRequired, ValidationError, Length, Email, Regexp, EqualTo

from app.models import User


class EditProfileForm(FlaskForm):
    full_name = StringField('Full_Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('This username is already taken by someone. Please use a different username.')

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError('This email is already taken by someone. Please use a different email address.')


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    post = TextAreaField('Say something', validators=[
        DataRequired()], render_kw={"placeholder": "Write your blog here"})
    submit = SubmitField('Submit')


class EditPostForm(FlaskForm):
    new_body = TextAreaField('Edit Post', validators=[DataRequired()])
    submit = SubmitField('Save Changes')
