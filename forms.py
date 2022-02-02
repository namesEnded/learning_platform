import wtforms
from models import Role
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, InputRequired, EqualTo
from wtforms_sqlalchemy.fields import QuerySelectField;


class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[Email()])
    password = PasswordField("Password: ", validators=[DataRequired(), Length(min=4, max=100)])
    remember = BooleanField("Remember me", default=False)
    submit = SubmitField("Login")


def choice_query():
    return Role.query


class SignupForm(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired()])
    username = StringField("Nickname: ", validators=[DataRequired()])
    email = StringField("Email: ", validators=[Email()])
    password_hash = PasswordField("Password: ", validators=[DataRequired(), EqualTo('password_hash2', message="Password must match!"), Length(min=4, max=100)])
    password_hash2 = PasswordField("Confirm password: ", validators=[DataRequired(), Length(min=4, max=100)])
    role_id = QuerySelectField(query_factory=choice_query, allow_blank=False, get_label="name")
    submit = SubmitField("Submit")
