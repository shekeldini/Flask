from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[Email("Некорректный email")])
    psw = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=4,
                                                                       max=100,
                                                                       message="Пароль должен быть от 4 до 100 символов")])
    remember = BooleanField("Запомнить", default=False)
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    name = StringField("Имя: ", validators=[Length(min=4, max=20, message="Имя должно быть от 4 до 20 символов")])
    email = StringField("Email: ", validators=[Email("Некорректный email")])
    psw = PasswordField("Придумайте пароль: ", validators=[DataRequired(), Length(min=4,
                                                                       max=100,
                                                                       message="Пароль должен быть от 4 до 100 символов")])
    repeat_psw = PasswordField("Повторите пароль: ", validators=[DataRequired(), EqualTo('psw', message="Пароли не совпадают")])
    submit = SubmitField("Регистрация")


class AdminForm(FlaskForm):
    email = StringField("Email: ", validators=[Email("Некорректный email")])
    psw = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=4,
                                                                       max=100,
                                                                       message="Пароль должен быть от 4 до 100 символов")])
    submit = SubmitField("Войти")


class VPRAnalysisForm(FlaskForm):
    name_of_the_settlement = SelectField('Муниципалитет', choices=[])
    oo = SelectField('Образовательная организация', choices=[])
    parallel = SelectField('Параллель', choices=[])
    subject = SelectField('Дисциплина', choices=[])
    report = SelectField('Отчет', choices=[])
    submit = SubmitField("Показать")
