import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import RegistrationForm, LoginForm, SearchCast, SearchGenre, SearchCountry, SearchDirector, SearchLanguage
from flaskDemo.models import entertainmentcast, entertainmentgenre, entertainmentcountry, entertainment, entertainmentdirector, producedin
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy, BaseQuery


@app.route("/")
@app.route("/netflix")
def about():
    return render_template('netflix.html', title='Profiles')
    
@app.route("/Movies_TVShows", methods=['GET', 'POST'])
def Movies_TVShows():
    formCast = SearchCast()
    formGenre = SearchGenre()
    formCountry = SearchCountry()
    formDirector = SearchDirector()
    formLang = SearchLanguage()
    
    #all= entertainment.query.join(producedin, entertainment.ShowID== producedin.ShowID) \
    #.add_columns(entertainment.Title, entertainment.Type, entertainment.Description) \
    #.join(entertainmentdirector, producedin.ShowID == entertainmentdirector.ShowID)
    all = entertainment.query.all()
    
    if formCast.validate_on_submit():
        castSearch = formCast.searchCa.data #cast name we are looking for
        castQ = entertainment.query.join(entertainmentcast, entertainment.ShowID == entertainmentcast.ShowID).where(entertainmentcast.CastName.contains(castSearch))
        return render_template('entertainment_list.html', joined_m_n= castQ, title = 'Movies_TVShows', form=formCast, form1=formGenre, form2=formCountry, form3=formDirector, form4=formLang)
        
    if formDirector.validate_on_submit():
        directorSearch = formDirector.searchD.data
        print(directorSearch)
        directorQ = entertainment.query.join(entertainmentdirector, entertainment.ShowID == entertainmentdirector.ShowID).where(entertainmentdirector.DirectorName.contains(directorSearch))
        print(directorQ)
        return render_template('entertainment_list.html', joined_m_n= directorQ, title = 'Movies_TVShows', form=fromCast, form1=formGenre, form2=formCountry, form3=formDirector, form4=formLang)
        
    if formGenre.validate_on_submit():
        genreSearch = formGenre.searchG.data
        print(genreSearch)
        genreQ = all
        return render_template('entertainment_list.html', joined_m_n= genreQ, title = 'Movies_TVShows', form=formCast, form1=formGenre, form2=formCountry, form3=formDirector, form4=formLang)
        
    if formCountry.validate_on_submit():
        countrySearch = formCountry.searchCo.data
        countryQ =all
        return render_template('entertainment_list.html', joined_m_n= countryQ, title = 'Movies_TVShows', form=fromCast, form1=formGenre, form2=formCountry, form3=formDirector, form4=formLang)
        
    if formLang.validate_on_submit():
        langSearch = formLang.searchL.data
        langQ = all
        return render_template('entertainment_list.html', joined_m_n= langQ, title = 'Movies_TVShows', form=fromCast, form1=formGenre, form2=formCountry, form3=formDirector, form4=formLang)
    
    return render_template('entertainment_list.html', joined_m_n= all, title = 'Movies_TVShows', form=formCast, form1=formGenre, form2=formCountry, form3=formDirector, form4=formLang)

  
@app.route("/about")
def netflix():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = entertainment(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
    
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('Movies_TVShows'))
    form = LoginForm()
    if form.validate_on_submit():
        user = entertainment.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('Movies_TVShows'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('Movies_TVShows'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


