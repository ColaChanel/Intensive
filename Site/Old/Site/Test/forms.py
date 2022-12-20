from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import Email, Length, DataRequired


class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[Email()])
    psw = PasswordField("Password: ", validators=[DataRequired(), Length(min=4, max=100)])
    remember = BooleanField("Remember", default=False)
    submit = SubmitField("Login")