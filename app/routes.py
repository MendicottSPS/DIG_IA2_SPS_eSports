from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, GameSearchForm, UserSearchForm, EditProfileForm, \
    CreateTeamForm, SearchTeamForm, CreateTournamentForm, SearchTournamentForm, CreatePractiseForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Games, Team, FavouriteGames, Tournaments, TournamentUsers, Practises, TeamUsers
from werkzeug.urls import url_parse
import datetime
import csv

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        nextpage = request.args.get('next')
        if not nextpage or url_parse(nextpage).netloc != '':
            nextpage = url_for('index')
        return redirect(nextpage)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()

    if form.validate_on_submit():

        if form.admin_code.data == 'staff1234':
            role = 'Staff'
        elif form.admin_code.data == 'sponsor1234':
            role = 'Sponsor'
        else:
            role = 'User'
        user = User(username=form.username.data, email=form.email.data, grade=form.grade.data, skill_level=form.skill_level.data, role=role)
        user.set_password(form.password.data)


        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    else:
        #flash('something went wrong')
        print(form.errors)

    return render_template('register.html', title='Register', form=form)


@app.route('/game_search', methods=['GET', 'POST'])
@login_required
def game_search():
    form = GameSearchForm()
    if form.validate_on_submit():
        game_title = form.game_title.data
        games = Games.query.filter(Games.game_title.contains(game_title)).all()
        print(games)
        for game in games:
            print(game.game_title)
        return render_template('game_results.html', title='Game Results', form=form, games=games)
    else:
        #flash('Something went wrong')
        print(form.errors)
    return render_template('game_search.html', title='Game Search', form=form)


@app.route('/game/<int:game_id>')
@login_required
def game(game_id):
    game = Games.query.filter_by(game_id=game_id).first_or_404()
    is_favourite = FavouriteGames.query.filter_by(user_id=current_user.id, game_id=game.game_id).count()
    return render_template('game_details.html', game=game, is_favourite=is_favourite)


@app.route('/favourite_game/<game_id>', methods=['GET', 'POST'])
@login_required
def favourite_game(game_id):
    game = Games.query.filter_by(game_id=game_id).first_or_404()
    user = current_user


    # Check if the game is already in the user's favourites
    favourite = FavouriteGames.query.filter_by(user_id=user.id, game_id=game.game_id).first()

    # Toggle the game's favourite status
    if favourite:
        # Remove the game from favourites
        db.session.delete(favourite)
        db.session.commit()

        flash('Game removed from favourites')
    else:
        # Add the game to favourites
        favourite = FavouriteGames(user_id=user.id, game_id=game.game_id)
        db.session.add(favourite)
        db.session.commit()
        flash('Game added to favourites')

        print(favourite)

    return redirect(url_for('game', game_id=game.game_id))


@app.route('/user_search', methods=['GET', 'POST'])
@login_required
def user_search():
    form = UserSearchForm()
    if form.validate_on_submit():
        username = form.username.data
        users = User.query.filter(User.username.contains(username)).all()
        print(users)
        for user in users:
            print(user.username)
        return render_template('user_results.html', title='User Results', form=form, users=users)
    else:
        #flash('Something went wrong')
        print(form.errors)
    return render_template('user_search.html', title='User Search', form=form)


@app.route ('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    favourites = db.session.query(FavouriteGames, Games).filter(
        FavouriteGames.user_id == user.id,
        FavouriteGames.game_id == Games.game_id
    ).all()
    return render_template('user.html', user=user, favourites=favourites)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@app.route('/create_team', methods=['GET', 'POST'])
@login_required
def create_team():
    form = CreateTeamForm()
    user = current_user

    if user.role != 'Staff':
        return redirect(url_for('index'))


    if form.validate_on_submit():
        team = Team(team_name=form.team_name.data, team_description=form.team_description.data)
        db.session.add(team)
        db.session.commit()
        flash('Congratulations, you have created a team!')
        return redirect(url_for('index'))
    else:
        #flash('something went wrong')
        print(form.errors)
    return render_template('create_team.html', title='Create Team', form=form)


@app.route('/team_search', methods=['GET', 'POST'])
@login_required
def team_search():
    form = SearchTeamForm()
    if form.validate_on_submit():
        team_name = form.team_name.data
        teams = Team.query.filter(Team.team_name.contains(team_name)).all()
        print(teams)
        for team in teams:
            print(team.team_name)
        return render_template('team_results.html', title='Team Results', form=form, teams=teams)
    else:
        #flash('Something went wrong')
        print(form.errors)
    return render_template('team_search.html', title='Search Team', form=form)

@app.route('/team/<team_id>', methods=['GET', 'POST'])
@login_required
def team(team_id):
    team = Team.query.filter_by(team_id=team_id).first_or_404()

    team_users = TeamUsers.query.filter_by(team_id=team.team_id).all()
    user_list = []
    for team_user in team_users:
        user = User.query.filter_by(id=team_user.user_id).first()
        user_list.append(user)

    practises = Practises.query.filter_by(team_id=team.team_id).all()
    # filter by date
    practises = Practises.query.filter(Practises.practise_date >= datetime.date.today()).all()

    return render_template('team.html', title='Team', team=team, team_users=team_users, user_list=user_list, practises=practises)

## tournaments ##
@app.route('/create_tournament', methods=['GET', 'POST'])
@login_required
def create_tournament():
    form = CreateTournamentForm()
    user = current_user

    if user.role != 'Staff':
        return redirect(url_for('index'))

    if form.validate_on_submit():
        tournament = Tournaments(tournament_name=form.tournament_name.data, tournament_description=form.tournament_description.data, tournament_date=form.tournament_date.data)
        db.session.add(tournament)
        db.session.commit()
        flash('Congratulations, you have created a tournament!')
        return redirect(url_for('index'))
    else:
        #flash('something went wrong')
        print(form.errors)
    return render_template('create_tournament.html', title='Create Tournament', form=form)


@app.route('/tournament/<tournament_id>' , methods=['GET', 'POST'])
@login_required
def tournament(tournament_id):
    tournament = Tournaments.query.filter_by(tournament_id=tournament_id).first_or_404()
    in_tournament = TournamentUsers.query.filter_by(tournament_id=tournament.tournament_id, user_id=current_user.id).count()

    participants = TournamentUsers.query.filter_by(tournament_id=tournament.tournament_id).all()
    participant_list = []
    for participant in participants:
        user = User.query.filter_by(id=participant.user_id).first()
        participant_list.append(user)


    return render_template('tournament.html', title='Tournaments', tournament=tournament, in_tournament=in_tournament, participants=participants, participant_list=participant_list)

@app.route('/join_tournament/<tournament_id>', methods=['GET', 'POST'])
@login_required
def join_tournament(tournament_id):
    tournament = Tournaments.query.filter_by(tournament_id=tournament_id).first_or_404()
    user = current_user

    # check if in tournament
    in_tournament = TournamentUsers.query.filter_by(tournament_id=tournament.tournament_id, user_id=user.id).count()
    if in_tournament:
        tournament_user = TournamentUsers.query.filter_by(tournament_id=tournament.tournament_id, user_id=user.id).first()
        db.session.delete(tournament_user)
        db.session.commit()
        flash('You have left the tournament')
    else:
        tournament_user = TournamentUsers(tournament_id=tournament.tournament_id, user_id=user.id)
        db.session.add(tournament_user)
        db.session.commit()
        flash('Congratulations, you have joined a tournament!')
    return redirect(url_for('tournament', tournament_id=tournament.tournament_id))


@app.route('/tournament_search', methods=['GET', 'POST'])
@login_required
def tournament_search():
    form = SearchTournamentForm()
    if form.validate_on_submit():
        tournament_name = form.tournament_name.data
        tournaments = Tournaments.query.filter(Tournaments.tournament_name.contains(tournament_name)).all()
        print(tournaments)
        for tournament in tournaments:
            print(tournament.tournament_name)
        return render_template('tournament_results.html', title='Tournament Results', form=form, tournaments=tournaments)
    else:
        #flash('Something went wrong')
        print(form.errors)
    return render_template('tournament_search.html', title='Search Tournament', form=form)

## practises ##

@app.route('/create_practise/<team_id>',  methods=['GET', 'POST'])
@login_required
def create_practise(team_id):
    form = CreatePractiseForm()
    user = current_user

    if form.validate_on_submit():
        practise = Practises(practise_name=form.practise_name.data, practise_description=form.practise_description.data, practise_date=form.practise_date.data, team_id=team_id)
        db.session.add(practise)
        db.session.commit()
        flash('Congratulations, you have created a practise!')
        return redirect(url_for('team', team_id=team_id))
    else:
        #flash('something went wrong')
        print(form.errors)
        return render_template('create_practise.html', title='Create Practise', team_id=team_id, form=form)
    return render_template('create_practise.html', title='Create Practise', team_id=team_id, form=form)

