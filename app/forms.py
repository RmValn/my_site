from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, Length, ValidationError
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Логін', validators=[DataRequired(message="Поле обов'язкове для заповнення")])
    password = PasswordField('Пароль', validators=[DataRequired(message="Поле обов'язкове для заповнення")])
    remember_me = BooleanField('Запам\'ятати мене')
    submit = SubmitField('Вхід')

    
class RegistrationForm(FlaskForm):
    firstname = StringField('Ім\'я', validators=[DataRequired(message="Поле обов'язкове для заповнення")])
    secondname = StringField('Прізвище', validators=[DataRequired(message="Поле обов'язкове для заповнення")])
    username = StringField('Логін', validators=[DataRequired(message="Поле обов'язкове для заповнення")])
    email = StringField('Електронна адреса', validators=[DataRequired(message="Поле обов'язкове для заповнення"), Email(message="Невірна електронна адреса!")])
    password = PasswordField('Пароль', validators=[DataRequired(message="Поле обов'язкове для заповнення"), Length(min=8, message='Пароль має містити мінімум 8 символів')])
    repeat_password = PasswordField('Повторіть пароль', validators=[DataRequired(message="Поле обов'язкове для заповнення"), EqualTo('password', message='Паролі не збігаються!')])
    submit = SubmitField('Реєстрація')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Це ім\'я користувача вже використовується!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Електронна адреса вже використовується!')
class SearchForm(FlaskForm):
     search_form = StringField(label='', validators=[DataRequired()])
     submit = SubmitField('Пошук')