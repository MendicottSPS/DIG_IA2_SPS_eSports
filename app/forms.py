#importing necessary libraries
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Email
from app.models import User

#creating the login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()]) #username field - with data required validation
    password = PasswordField('Password', validators=[DataRequired()]) #password field - with data required validation
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


#creating the registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')]) #used to check that the user enters the same password twice
    grade = StringField('Grade', validators=[DataRequired()])
    skill_level = SelectField('Skill Level', choices=[
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced')
    ]) #a set of options the user is able to pick from for their skill level - limits error and ensures consistency
    submit = SubmitField('Register')

    #validation to ensure that the username and email are unique - if not, the user is prompted to enter a different username or email
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

#creating the game search form
class GameSearchForm(FlaskForm):
    game_title = StringField('Game Title', validators=[DataRequired()]) #data is required to make a search
    submit = SubmitField('Search')

#form for users to search for other users
class UserSearchForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Search')

#form for users to edit their profile
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    #while data is required, an error would only be raised if the user removed what was already there and tried to submit the form
    about_me = StringField('About me', validators=[DataRequired()])
    skill_level = StringField('Skill Level', validators=[DataRequired()])
    submit = SubmitField('Submit')

#form for users to create a team (should be changed in the future to only allow team creation from admin users
class CreateTeamForm(FlaskForm):
    team_name = StringField('Team Name', validators=[DataRequired()])
    team_description = StringField('Team Description', validators=[DataRequired()])
    submit = SubmitField('Create Team')

#form for users to search for a team
class SearchTeamForm(FlaskForm):
    team_name = StringField('Team Name', validators=[DataRequired()])
    submit = SubmitField('Search Team')

