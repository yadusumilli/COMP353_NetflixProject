import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, DeptForm,DeptUpdateForm, AssignForm, AssignUpdateForm
from flaskDemo.models import User, Post,Department, Dept_Locations, Employee, Project, Works_On
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime


@app.route("/")
@app.route("/home")
def home():
 
    
    testing= Employee.query.join(Works_On, Employee.ssn== Works_On.essn) \
    .add_columns(Employee.fname, Employee.lname, Project.pname, Employee.ssn, Works_On.pno, Works_On.essn) \
    .join(Project, Works_On.pno == Project.pnumber)
    return render_template('assign.html', joined_m_n= testing)
    
   
    
    posts = Post.query.all()
    return render_template('home.html', posts=posts)
    results2 = Faculty.query.join(Qualified,Faculty.facultyID == Qualified.facultyID) \
               .add_columns(Faculty.facultyID, Faculty.facultyName, Qualified.Datequalified, Qualified.courseID) \
               .join(Course, Course.courseID == Qualified.courseID).add_columns(Course.courseName)
    results = Faculty.query.join(Qualified,Faculty.facultyID == Qualified.facultyID) \
              .add_columns(Faculty.facultyID, Faculty.facultyName, Qualified.Datequalified, Qualified.courseID)
    return render_template('join.html', title='Join',joined_1_n=results, joined_m_n=results2)

   


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


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


@app.route("/dept/new", methods=['GET', 'POST'])
@login_required
def new_dept():
    form = DeptForm()
    if form.validate_on_submit():
        dept = Department(dname=form.dname.data, pno=form.pno.data,mgr_ssn=form.mgr_ssn.data,mgr_start=form.mgr_start.data)
        db.session.add(dept)
        db.session.commit()
        flash('You have added a new department!', 'success')
        return redirect(url_for('home'))
    return render_template('create_dept.html', title='New Department',
                           form=form, legend='New Department')

@app.route("/assign/new", methods=['GET', 'POST'])
@login_required
def new_assign():
    form = AssignUpdateForm()
    if form.validate_on_submit():
        assign = Works_On(pno=form.pno.data, essn=form.essn.data, hours=form.hours.data)
        db.session.add(assign)
        db.session.commit()
        flash('You have added a new Assignment!', 'success')
        return redirect(url_for('home'))
    return render_template('create_ass.html', title='New Assignment',
                           form=form, legend='New Assignment')


@app.route("/dept/<pno>")
@login_required
def dept(pno):
    dept = Department.query.get_or_404(pno)
    return render_template('dept.html', title=dept.dname, dept=dept, now=datetime.utcnow())


@app.route("/assign/<int:pno>/<int:essn>")
@login_required
def assign(pno,essn): 
    
    #return( "page under Const" ) 

    assign= Works_On.query.get_or_404([essn,pno])
   
    
    print ("I got here")
    return render_template('assignment.html', title=str(assign.pno)+ "_" +str(assign.essn),assign=assign, now=datetime.utcnow())

@app.route("/assign/<pno>/<essn>update", methods=['GET', 'POST'])
@login_required
def update_assign(essn,pno):
  #  return "update page under construction" 
    assign=Works_On.query.get_or_404([essn,pno])
    currentass = assign.pno, assign.essn

    form = AssignUpdateForm()
    if form.validate_on_submit():          # notice we are are not passing the dnumber from the form
        if currentass !=form.pno.data:
            assign.pno=form.pno.data
        assign.essn=form.essn.data
       # assign.mgr_start=form.mgr_start.data
        db.session.commit()
        flash('Your Assignment has been updated!', 'success')
        return redirect(url_for('dept', pno=pno))
    elif request.method == 'GET':              # notice we are not passing the dnumber to the form

        form.pno.data = assign.pno
        form.essn.data = assign.essn
        #form.hours.data = dept.mgr_ssn
 
    return render_template('create_ass.html', title='Update Assignment',
                           form=form, legend='New Assignment')


@app.route("/assign/<pno>/<essn>delete", methods=['POST'])
@login_required
def delete_assign(essn,pno):
    assign=Works_On.query.get_or_404([essn,pno])
    db.session.delete(assign)
    db.session.commit()
    flash('The Assignment has been deleted!', 'success')
    return redirect(url_for('home'))