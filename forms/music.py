from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class MusForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    link = StringField('Ссылка', validators=[DataRequired()])
    genre = StringField('Жанр', validators=[DataRequired()])
    submit = SubmitField('Применить')