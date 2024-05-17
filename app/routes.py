from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, GameSearchForm, UserSearchForm, EditProfileForm, CreateTeamForm, SearchTeamForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Games, Team
from werkzeug.urls import url_parse
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
        user = User(username=form.username.data, email=form.email.data, grade=form.grade.data)
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
    return render_template('user.html', user=user)


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

