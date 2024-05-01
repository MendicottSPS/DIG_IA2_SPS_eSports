from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, GameSearchForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Games
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
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    else:
        flash('something went wrong')
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
        flash('Something went wrong')
        print(form.errors)
    return render_template('game_search.html', title='Game Search', form=form)


'''
@app.route('/user_search', methods=['GET', 'POST'])
@login_required
'''