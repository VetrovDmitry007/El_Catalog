from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class LoginForm(FlaskForm):
    """
    Класс формы авторизации пользователя
    """
    username = StringField(label='Имя пользователя', validators= [DataRequired()])
    password = PasswordField(label='Пароль', validators=[DataRequired()])
    remember_me = BooleanField(label='Запомнить меня')
    submit = SubmitField('Вход')


class FindForm(FlaskForm):
    """
    Класс формы поиска
    """
    edit_1 = StringField()
    edit_2 = StringField()
    edit_3 = StringField()
    edit_4 = StringField()
    select_1 = SelectField(choices=[('245a', 'Заглавие'), ('100a', 'Автор'), ('260b', 'Издательство'), ('SUJET', 'Рубрика'), ('THESAURUS', 'Название тезауруса'), ('010a', 'ISBN') ])
    select_2 = SelectField(choices=[('245a', 'Заглавие'), ('100a', 'Автор'), ('260b', 'Издательство'), ('SUJET', 'Рубрика'), ('THESAURUS', 'Название тезауруса'), ('010a', 'ISBN') ])
    select_3 = SelectField(choices=[('245a', 'Заглавие'), ('100a', 'Автор'), ('260b', 'Издательство'), ('SUJET', 'Рубрика'), ('THESAURUS', 'Название тезауруса'), ('010a', 'ISBN') ])
    select_4 = SelectField(choices=[('245a', 'Заглавие'), ('100a', 'Автор'), ('260b', 'Издательство'), ('SUJET', 'Рубрика'), ('THESAURUS', 'Название тезауруса'), ('010a', 'ISBN') ])
    submit = SubmitField('Поиск')

class HideForm(FlaskForm):
    """
    Класс скрытой формы для хранения
    json списка найденной литературы
    """
    # json_txt = StringField(u'Text', widget=TextArea())
    json_txt = HiddenField(u'Text')