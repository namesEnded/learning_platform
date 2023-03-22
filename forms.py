from datetime import datetime
import re

import wtforms
from wtforms.widgets import EmailInput

from models import Role
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email, InputRequired, EqualTo, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField;


class LoginForm(FlaskForm):
    email = StringField("Логин", validators=[Email()])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=4, max=100)])
    remember = BooleanField("Remember me", default=False)
    submit = SubmitField("Войти")


def choice_query():
    return Role.query


class SignupForm(FlaskForm):
    email = StringField("Email: ", validators=[Email("Invalid email address.")], widget=EmailInput())
    password_hash = PasswordField("Password: ",
                                  validators=[DataRequired(), EqualTo('password_hash2', message="Password must match!"),
                                              Length(min=4, max=100)])
    password_hash2 = PasswordField("Confirm password: ", validators=[DataRequired(), Length(min=4, max=100)])

    first_name = StringField("First name: ", validators=[DataRequired(),InputRequired()])
    last_name = StringField("Last name: ", validators=[DataRequired(),InputRequired()])
    username = StringField("Nickname: ", validators=[DataRequired(),InputRequired()])
    gender = RadioField('Пол', choices=[('1', 'Мужской'), ('0', 'Женский')])

    date_of_birth = StringField("Date of bitrh: ", validators=[DataRequired(), InputRequired()])
    def validate_date_of_birth(form, field):
        try:
            datetime.strptime(field.data, '%Y-%m-%d')
        except ValueError:
            raise ValidationError('Not a date')

    country = StringField("Country: ", validators=[DataRequired()])
    city = StringField("City: ", validators=[DataRequired()])

    phone_number = StringField("Phone number: ", validators=[DataRequired()])
    # def validate_phone_number(form, field):
    #     # This code creates a regular expression to match Russian phone numbers in two different formats.
    #     # The first format is 8 (XXX) XXX-XX-XX, and the second format is +7 (XXX) XXX-XX-XX.
    #     # It includes the possibility of spaces or dashes between the number groups.
    #     phone_regex = re.compile(r'[8+7]\\s?\\(\\d{3}\\)\\s?\\d{3}[-\\s]?\\d{2}[-\\s]?\\d{2}')
    #     if not phone_regex.fullmatch(field.data):
    #         raise ValidationError('Not a phone number')

    role_id = QuerySelectField('Role',
                               query_factory=choice_query, allow_blank=False,
                               get_label='name', get_pk=lambda a: a.id,
                               blank_text=u'Select a role')
    # role_id = QuerySelectField(query_factory=choice_query, allow_blank=False, get_label="name", default='admin')
    submit = SubmitField("Submit")
