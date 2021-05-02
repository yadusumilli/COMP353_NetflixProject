
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, HiddenField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Regexp
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flaskDemo import db
from flaskDemo.models import entertainment, entertainmentgenre, entertainmentcast, producedin, entertainment, entertainmentdirector, entertainmentcountry
from wtforms.fields.html5 import DateField


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = entertainment.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = entertainment.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = entertainment.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = entertainment.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class SearchCast(FlaskForm):
    searchCa = StringField('Search Cast:')
    submitCast = SubmitField('Search')
    
class SearchDirector(FlaskForm):
    searchD = StringField('Search Director:')
    submitDirector = SubmitField('Search')

genreList = entertainmentgenre.query.with_entities(entertainmentgenre.GenreType).distinct()
class SearchGenre(FlaskForm):
    searchG = SelectField('Select Genre:', choices=genreList)
    submitGenre = SubmitField('Search')
    
CountryList = producedin.query.with_entities(producedin.CountryName).distinct()

class SearchCountry(FlaskForm):
    searchCo = SelectField('Select Country:', choices=CountryList)
    submitCountry = SubmitField('Search')
    
LanguageList = entertainmentcountry.query.with_entities(entertainmentcountry.PrimLang).distinct()
class SearchLanguage(FlaskForm):
    searchL = SelectField('Select Language:', choices=LanguageList)
    submitLang = SubmitField('Search')
