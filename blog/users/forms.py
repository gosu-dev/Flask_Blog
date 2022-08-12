from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError
from blog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[InputRequired(), Length(min=2, max=20)])

    # should be used EmailField ?
    email = StringField('Email',
                        validators=[InputRequired(), Email()])

    password = PasswordField('Password',
                             validators=[InputRequired()])

    confirm_password = PasswordField('Confirm Password',
                                     validators=[InputRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username taken. Please Choose another')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered.')


class LoginForm(FlaskForm):
    # should be used EmailField ?
    email = StringField('Email',
                        validators=[InputRequired(), Email()])

    password = PasswordField('Password',
                             validators=[InputRequired()])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')
