from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    login = StringField("Логин", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")


class AdminForm(FlaskForm):
    email = StringField("Email: ", validators=[Email("Некорректный email")])
    psw = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=4,
                                                                       max=100,
                                                                       message="Пароль должен быть от 4 до 100 символов")])
    submit = SubmitField("Войти")

