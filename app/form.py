from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,  BooleanField, SubmitField, RadioField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

class FictionForm(FlaskForm):
    name = StringField('Fiction Name', validators=[DataRequired()])
    cover = StringField('Cover', validators=[DataRequired()])
    desc = StringField('Description', validators=[DataRequired()])
    submit =  SubmitField('Save')



class AuthorForm(FlaskForm):
    author_name = StringField('Author Name', validators=[DataRequired()])
    img = StringField('img link', validators=[DataRequired()])
    about = StringField('About', validators=[DataRequired()])
    submit =  SubmitField('Save')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit =  SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('REG NOW')
    
    def validate_username(self, username):
        user = User.query.filter_by(user_name=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username!!!')
        
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email is already used')
class Quiz_answer(FlaskForm):
    answer = RadioField('Label', choices=[('A','Answer 1'),('B','Answer 2')])
    submit = SubmitField('Answer')
    