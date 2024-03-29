import wtforms
from models import Role
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, InputRequired, EqualTo
from wtforms_sqlalchemy.fields import QuerySelectField;


class LoginForm(FlaskForm):
    email = StringField("Логин", validators=[Email()])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=4, max=100)])
    remember = BooleanField("Remember me", default=False)
    submit = SubmitField("Войти")


def choice_query():
    return Role.query


class SignupForm(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired()])
    username = StringField("Nickname: ", validators=[DataRequired()])
    email = StringField("Email: ", validators=[Email("Invalid email address.")])
    password_hash = PasswordField("Password: ",
                                  validators=[DataRequired(), EqualTo('password_hash2', message="Password must match!"),
                                              Length(min=4, max=100)])
    password_hash2 = PasswordField("Confirm password: ", validators=[DataRequired(), Length(min=4, max=100)])
    role_id = QuerySelectField('Role',
                               query_factory=choice_query, allow_blank=False,
                               get_label='name', get_pk=lambda a: a.id,
                               blank_text=u'Select a role')
    # role_id = QuerySelectField(query_factory=choice_query, allow_blank=False, get_label="name", default='admin')
    submit = SubmitField("Submit")
