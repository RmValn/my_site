from flask import render_template, request, url_for, flash, redirect
from app import app
from app import db
from app.forms import LoginForm, RegistrationForm, SearchForm
from flask_login import logout_user, current_user, login_user, login_required
from werkzeug.urls import url_parse
from app.models import User
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import responder



@app.route('/')
@app.route('/index')
def index():
    search_form = SearchForm()
    form = RegistrationForm()
    form2 = LoginForm()
    return render_template('index.html', title='Головна', current_user=current_user, form=form, form2=form2, search_form=search_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    form2 = RegistrationForm()
    search_form = SearchForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if str(user) == '<User'+' '+str(request.form['username'])+'>':
            if user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('index')
                return redirect(next_page)
            flash('Невірний логін або пароль!', category='error')
            return redirect(url_for('login'))
            print(User.query.filter_by(email=form.username.data).first())
            users = User.query.filter_by(email=form.username.data).first()
            print(users)
        user = User.query.filter_by(email=form.username.data).first()
        users = User.query.all()
        print(user)
        for u in users:
            if str(user) == '<User'+' '+str(u.username)+'>':
                if u.check_password(form.password.data):
                    login_user(user, remember=form.remember_me.data)
                    next_page = request.args.get('next')
                    if not next_page or url_parse(next_page).netloc != '':
                        next_page = url_for('index')
                    return redirect(next_page)
                flash('Невірний логін або пароль!', category='error')
                return redirect(url_for('login'))

        else:
            flash('Невірний логін або пароль!', category='error')
    return render_template('login.html', title='Вхід', form=form, form2=form2, search_form=search_form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    form2 = LoginForm()
    search_form = SearchForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, firstname=form.firstname.data, secondname=form.secondname.data, username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Реєстрація пройшла успішно', category='info')
        return redirect(url_for('login'))


    return render_template('register.html', title='Реєстрація', form=form, form2=form2, search_form=search_form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    if current_user == user:
        form = RegistrationForm()
        search_form = SearchForm()
        form2 = LoginForm()
        user = User.query.filter_by(username=username).first_or_404()
        return render_template('profile.html', user=user, title="Профіль - " + username, current_user=current_user, form=form, form2=form2, search_form=search_form)
    return redirect(url_for('page_not_found'))

@app.route('/settings/')
@login_required
def settings():
    username = current_user.username
    user = User.query.filter_by(username=username).first_or_404()
    if current_user == user:
        form = RegistrationForm()
        search_form = SearchForm()
        form2 = LoginForm()
        user = User.query.filter_by(username=username).first_or_404()
        return render_template('settings.html', user=user, title="Налаштування - " + username, current_user=current_user, form=form, form2=form2, search_form=search_form)
    return redirect(url_for('page_not_found'))

@login_required
@app.route('/messages')
def messages():
    username = current_user.username
    user = User.query.filter_by(username=username).first_or_404()
    if current_user == user:
        form = RegistrationForm()
        search_form = SearchForm()
        form2 = LoginForm()
        user = User.query.filter_by(username=username).first_or_404()
        return render_template('messages.html', user=user, title="Повідомлення", current_user=current_user, form=form, form2=form2, search_form=search_form)



@app.route('/page_not_found')
def page_not_found():
    form = RegistrationForm()
    search_form = SearchForm()
    form2 = LoginForm()
    return render_template('404.html',  title='Не знайдено', current_user=current_user, form=form, form2=form2, search_form=search_form), 404
    
    
@app.errorhandler(404)
def application(e):
    return redirect(url_for('page_not_found'))