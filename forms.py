import wtforms
from models import Role
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, InputRequired
from wtforms_sqlalchemy.fields import QuerySelectField;


class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[Email()])
    password = PasswordField("Password: ", validators=[DataRequired(), Length(min=4, max=100)])
    remember = BooleanField("Remember me", default=False)
    submit = SubmitField("Login")

def choice_query():
    return Role.query

class SignupForm(FlaskForm):
    name = StringField("Name: ", validators=[Email()])
    email = StringField("Email: ", validators=[Email()])
    password = PasswordField("Password: ", validators=[DataRequired(), Length(min=4, max=100)])
    role_id = QuerySelectField(query_factory=choice_query, allow_blank=False, get_label="name")
    submit = SubmitField("Sign up")
