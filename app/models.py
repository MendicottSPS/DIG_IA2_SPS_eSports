from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login



#creating the user class - i.e the user table in the database and associated columns
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    role = db.Column(db.String(64), index=True)
    skill_level = db.Column(db.String(64), index=True)
    grade = db.Column(db.Integer, index=True)
    favourite_games = db.relationship('FavouriteGames', back_populates='user')

    tournament_users = db.relationship('TournamentUsers', back_populates='user')
    team_users = db.relationship('TeamUsers', back_populates='user')

    def __repr__(self):
        return '<User {}>'.format(self.username)
#creating a password hash for secuity purposes
#this was where the first errors occured with the actual method of hashing the password
#the final method to be used was pbkdf2:sha256 - rather than the default sha256

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

#creating the game class - i.e the game table in the database and associated columns
#the data from this table was accessed from the provided data, csv file and then added to the database for use through SQL queries
class Games(db.Model):
    game_id = db.Column(db.Integer, primary_key=True)
    game_title = db.Column(db.String(64), index=True, nullable=False)
    game_genre = db.Column(db.String(64), index=True)
    game_platform = db.Column(db.String(64), index=True)
    game_publisher = db.Column(db.String(64), index=True)
    game_year = db.Column(db.Integer, index=True)
    game_sales_global = db.Column(db.Float, index=True)
    game_sales_ranking = db.Column(db.Integer, index=True)
    favourite_games = db.relationship('FavouriteGames', back_populates='game')

    def __repr__(self):
        return '<Game {}>'.format(self.game_title)

    def get_id(self):
        return str(self.game_id)


class Team(db.Model):
    team_id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(64), index=True, nullable=False)
    team_description = db.Column(db.String(140), index=True)

    team_users = db.relationship('TeamUsers', back_populates='team')
    practises = db.relationship('Practises', back_populates='team')

    def __repr__(self):
        return '<Team {}>'.format(self.team_name)

    def get_id(self):
        return str(self.team_id)

class TeamUsers(db.Model):
    team_user_id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    team = db.relationship('Team', back_populates='team_users')
    user = db.relationship('User', back_populates='team_users')

    def __repr__(self):
        return '<TeamUsers {}>'.format(self.team_user_id)

    def get_id(self):
        return str(self.team_user_id)

class FavouriteGames(db.Model):
    favourite_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'))

    user = db.relationship('User', back_populates='favourite_games')
    game = db.relationship('Games', back_populates='favourite_games')

    def __repr__(self):
        return '<FavouriteGames {}>'.format(self.favourite_id)

    def get_id(self):
        return str(self.favourite_id)

class Tournaments(db.Model):
    tournament_id = db.Column(db.Integer, primary_key=True)
    tournament_name = db.Column(db.String(64), index=True, nullable=False, unique=True)
    tournament_description = db.Column(db.String(140), index=True)
    tournament_date = db.Column(db.Date, index=True)

    tournament_users = db.relationship('TournamentUsers', back_populates='tournament')

    def __repr__(self):
        return '<Tournament {}>'.format(self.tournament_name)

    def get_id(self):
        return str(self.tournament_id)

class TournamentUsers(db.Model):
    tournament_user_id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.tournament_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    tournament = db.relationship('Tournaments', back_populates='tournament_users')
    user = db.relationship('User', back_populates='tournament_users')

    def __repr__(self):
        return '<TournamentUsers {}>'.format(self.tournament_user_id)

    def get_id(self):
        return str(self.tournament_user_id)

class Practises(db.Model):
    practise_id = db.Column(db.Integer, primary_key=True)
    practise_name = db.Column(db.String(64), index=True, nullable=False)
    practise_description = db.Column(db.String(140), index=True)
    practise_date = db.Column(db.Date, index=True)

    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'))

    team = db.relationship('Team', back_populates='practises')

    def __repr__(self):
        return '<Practise {}>'.format(self.practise_name)

    def get_id(self):
        return str(self.practise_id)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))