from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(Form):
  first_name = StringField('First name', validators = [DataRequired("Enter your first name.")])
  last_name = StringField('Last name', validators = [DataRequired("Enter your last name.")])
  email = StringField('Email', validators = [DataRequired("Enter your email address."), Email("Enter a valid email address.")])
  password = PasswordField('Password', validators = [DataRequired("Enter your password."), Length(min=6, message="Must be 6 characters or more.")])
  submit = SubmitField('sign up')

