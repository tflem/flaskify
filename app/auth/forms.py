from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, Length, EqualTo

from ..models import Employee

class RegistrationForm(FlaskForm):
  email = StringField('Email', validators = [DataRequired("Enter your email address."), Email("Enter a valid email address.")])
  username = StringField('Username', validators = [DataRequired("Enter your username.")])
  first_name = StringField('First name', validators = [DataRequired("Enter your first name.")])
  last_name = StringField('Last name', validators = [DataRequired("Enter your last name.")])
  password = PasswordField('Password', validators = [DataRequired("Enter your password."), Length(min=6, message="Must be 6 characters or more."), EqualTo("confirm_password")])
  confirm_password = PasswordField('Confirm Password')
  submit = SubmitField('Register')

  def validate_email(self, field):
      if Employee.query.filter_by(email=field.data).first():
          raise ValidationError('Email is already in use.')

  def validate_username(self, field):
      if Employee.query.filter_by(username=field.data).first():
          raise ValidationError('Username is already in use.')

class LoginForm(FlaskForm):
  email = StringField('Email', validators = [DataRequired("Enter your email address."), Email("Enter your email address")])
  password = PasswordField('Password', validators = [DataRequired("Enter a password.")])
  submit = SubmitField("Login")