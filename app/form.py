from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,  BooleanField, SubmitField, RadioField, TextAreaField,DateField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo


class ParserForm(FlaskForm):
    link = StringField('Enter Fiction Book', validators=[DataRequired()])
    submit =  SubmitField('Show result')