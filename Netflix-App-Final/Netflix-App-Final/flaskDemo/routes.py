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
    
    db.session.query(entertainment).filter(entertainment.ShowID == 9).\
    update({"ReleaseYear": (entertainment.ReleaseYear+1)})
    db.session.commit()
    
    db.session.query(entertainmentcast).filter(entertainmentcast.ShowID == 13).delete()
    db.session.query(entertainmentdirector).filter(entertainmentdirector.ShowID == 13).delete()
    db.session.query(entertainmentgenre).filter(entertainmentgenre.ShowID == 13).delete()
    db.session.query(producedin).filter(producedin.ShowID == 13).delete()
    db.session.query(entertainment).filter(entertainment.ShowID == 13).delete()
    db.session.commit()
    
    db.session.query(entertainment).filter(entertainment.Rating == 'TV-Y', 
    entertainment.ReleaseYear == 2019, entertainment.Type=='TV Show', entertainment.Duration == '1 Season').\
    update({"ReleaseYear": (entertainment.ReleaseYear+1)})
    db.session.commit()
    
    if formCast.validate_on_submit() and formCast.submitCast.data:
        castSearch = formCast.searchCa.data #cast name we are looking for
        castQ = entertainment.query.join(entertainmentcast, entertainment.ShowID == entertainmentcast.ShowID).filter(entertainmentcast.CastName.contains(castSearch))
        return render_template('entertainment_list.html', joined_m_n= castQ, title = 'Movies_TVShows', form=formCast, form1=formGenre, form2=formCountry, form3=formDirector, form4=formLang)
        
    elif formDirector.validate_on_submit() and formDirector.submitDirector.data:
        directorSearch = formDirector.searchD.data
        directorQ = entertainment.query.join(entertainmentdirector, entertainment.ShowID == entertainmentdirector.ShowID).filter(entertainmentdirector.DirectorName.contains(directorSearch))
        #.where(entertainmentdirector.DirectorName.contains(directorSearch))
        return render_template('entertainment_list.html', joined_m_n= directorQ, title = 'Movies_TVShows', form=formCast, form1=formGenre, form2=formCountry, form3=formDirector, form4=formLang)
        
    elif formGenre.validate_on_submit() and formGenre.submitGenre.data:
        genreSearch = formGenre.searchG.data
        genreQ = entertainment.query.join(entertainmentgenre, entertainment.ShowID == entertainmentgenre.ShowID).filter(entertainmentgenre.GenreType.ilike(genreSearch))
        #.where(entertainmentgenre.GenreType.contains(genreSearch))
        return render_template('entertainment_list.html', joined_m_n= genreQ, title = 'Movies_TVShows', form=formCast, form1=formGenre, form2=formCountry, form3=formDirector, form4=formLang)
        
    elif formCountry.validate_on_submit() and formCountry.submitCountry.data:
        countrySearch = formCountry.searchCo.data
        countryQ = entertainment.query.join(producedin, entertainment.ShowID == producedin.ShowID).filter(producedin.CountryName.ilike(countrySearch))
        #.where(producedin.CountryName.contains(countrySearch))
        return render_template('entertainment_list.html', joined_m_n= countryQ, title = 'Movies_TVShows', form=formCast, form1=formGenre, form2=formCountry, form3=formDirector, form4=formLang)
        
    elif formLang.validate_on_submit():
        langSearch = formLang.searchL.data
        langQ = all
        return render_template('entertainment_list.html', joined_m_n= langQ, title = 'Movies_TVShows', form=formCast, form1=formGenre, form2=formCountry, form3=formDirector, form4=formLang)
    else:
        return render_template('entertainment_list.html', joined_m_n= all, title = 'Movies_TVShows', form=formCast, form1=formGenre, form2=formCountry, form3=formDirector, form4=formLang)

  
@app.route("/about")
def netflix():
    return render_template('about.html', title='About')
    
@app.route("/trendingnow")
def trendingnow():
    return render_template('trendingnow.html', title='Trending Now')
    
@app.route("/comingsoon")
def comingsoon():
    return render_template('comingsoon.html', title='Coming Soon')

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


