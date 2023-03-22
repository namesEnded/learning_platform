import os
import database
from dotenv import load_dotenv
from sqlalchemy import exc
from database import db
from flask import Flask, render_template, url_for, request, redirect, flash, session, abort
import commands
from models import Course, Menu, User, Role, Group, Subject
from flask_migrate import Migrate
from forms import LoginForm, SignupForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from config import *

app = Flask(__name__)
# setup with thew configurations by user
app.config.from_object(os.environ['APP_SETTINGS'])

database.init_app(app)
commands.start_app(app)
migrate = Migrate(app, db)

# menuItems = [{"name": "Main", "url": "/"},
#              {"name": "About", "url": "/about"},
#              {"name": "Create course", "url": "/create_course"},
#              {"name": "Courses", "url": "/courses"}]



# Need to login-flask
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_uuid):
    return User.query.get(user_uuid)

def menu_items():
    try:
        items = Menu.query.all()
        if items:
            return items
    except:
        print("!!! Error while getting menu items! !!!")
    return []


@app.route('/')
@app.route('/home')
def index():
    print(menu_items())
    return render_template('index.html', menuItems=menu_items())


# @app.route('/create_course', methods=['POST', 'GET'])
# def create_course():
#     # TODO: Make a normal request success handler
#     if request.method == "POST":
#         user = current_user
#         title = request.form['title']
#         review = request.form['intro']
#         text_content = request.form['text']
#         course = Course(title=title, review=review, text_content=text_content, user=user)
#         try:
#             if len(title) == 0:
#                 flash('ERROR: error while sending data!', category='danger')
#                 return render_template('create_course.html', title="Create course", menuItems=menu_items())
#             else:
#                 db.session.add(course)
#                 db.session.commit()
#                 flash('Data sent successfully!', category='success')
#                 return render_template('create_course.html', title="Create course", menuItems=menu_items())
#
#         except:
#             flash('ERROR: error while sending data!', category='danger')
#             return
#     else:
#         return render_template('create_course.html', title="Create course", menuItems=menu_items())


@app.route('/about')
def about():
    return render_template('about.html', title="About learning platform", menuItems=menu_items())


@app.route('/courses', methods=['POST', 'GET'])
@login_required
def courses():

    if request.method == "GET":
        try:
            all_courses = Course.query.order_by(Course.date_added.desc()).all()
        except exc.SQLAlchemyError as ex:
            flash('ERROR: error while getting date', category='danger')
            return render_template('error.html', ex=ex.code)
        # course_subject = { 'Subjects': { },
        #                    'Courses' : { }}
        # course_subject = {'Subjects': {}, 'Courses': {}}
        # course_subject = {0 : {0: 'course'}}
        course_subject = {}      
        # subjects = {0 : 'subject'}
        subjects = {}
        tab_id=0
        item_id=0
        for subject in Subject.query.all():
            tab_id=tab_id+1
            subjects[tab_id]=subject.name
            for course in subject.courses:
                item_id=item_id+1
                course_subject[tab_id]={}
                course_subject[tab_id][item_id] = course
        return render_template('courses.html', title="Courses", all_courses=all_courses, menuItems=menu_items(),subjects=subjects,course_subject=course_subject )

    elif request.method == "POST":
        user = current_user
        title = request.form['title']
        if Course.isExist(title):
            flash('Course with this title already exist', category='success')
            return render_template('create_course.html', title="Create course", menuItems=menu_items())
        else:
            review = request.form['intro']
            text_content = request.form['text']
            course = Course(title=title, review=review, text_content=text_content, user=user)
            try:

                if len(title) == 0:
                    flash('ERROR: error while sending data!', category='danger')
                    return render_template('create_course.html', title="Create course", menuItems=menu_items())
                else:
                    db.session.add(course)
                    db.session.commit()
                    flash('Data sent successfully!', category='success')
                    return redirect('/courses')

            except exc.SQLAlchemyError as ex:
                flash('ERROR: error while sending data!', category='danger')
                return render_template('error.html', ex=ex.code)
    else:
        return render_template('page405.html', title="Method Not Allowed", menuItems=menu_items()), 405



@app.route('/courses/new', methods=['GET'])
@login_required
def course_new():
    return render_template('create_course.html', title="Create course", menuItems=menu_items())

@app.route('/courses/<uuid:course_uuid>/delete', methods=['POST'])
@login_required
def course_delete(course_uuid):
    course = Course.query.get_or_404(course_uuid)
    try:
        db.session.delete(course)
        db.session.commit()
        flash('Course delete successfully!', category='success')
        return redirect('/courses')
    except exc.SQLAlchemyError as ex:
        return "ERROR: error while deleting course"

@app.route('/courses/<uuid:course_uuid>/edit', methods=['POST','GET'])
@login_required
def course_update(course_uuid):
    if request.method == "GET":
        course = Course.query.get(course_uuid)
        if not course:
            return render_template('page404.html', title="Page not found", menuItems=menu_items()), 404
        return render_template('course_update.html', title="Update course", course=course, menuItems=menu_items())
    elif request.method == "POST":
        course = Course.query.get(course_uuid)
        course.title = request.form['title']
        course.review = request.form['intro']
        course.text_content = request.form['text']
        try:
            db.session.commit()
            return redirect('/courses')
        except exc.SQLAlchemyError as ex:
            flash('ERROR: error while sending data!', category='danger')
    else:
        return render_template('page405.html', title="Method Not Allowed", menuItems=menu_items()), 405

@app.get('/courses/<uuid:course_uuid>')
@login_required
def course_detail(course_uuid):
    course = Course.query.get(course_uuid)
    if not course:
        return render_template('page404.html', title="Page not found", menuItems=menu_items()), 404
    else:
        return render_template('course_detail.html', title="Course detail", course=course, menuItems=menu_items())




# _____________________________________________________________
#                 TRYING TO WRITE NORMAL API
# _____________________________________________________________
# @app.delete('/courses/<int:course_id>')
# def course_delete(course_id):
#     course = Course.query.get_or_404(course_id)
#     try:
#         db.session.delete(course)
#         db.session.commit()
#         flash('Course delete successfully!', category='success')
#         return redirect('/courses')
#     except exc.SQLAlchemyError as ex:
#         return "ERROR: error while deleting course"
#
# @app.patch('/courses/<int:course_id>')
# def course_update(course_id):
#     course = Course.query.get(course_id)
#     course.title = request.form['title']
#     course.review = request.form['intro']
#     course.text_content = request.form['text']
#     try:
#         db.session.commit()
#         return redirect('/courses')
#     except exc.SQLAlchemyError as ex:
#         flash('ERROR: error while sending data!', category='danger')
#
# @app.get('/courses/<int:course_id>/edit')
# def edit(course_id):
#     course = Course.query.get(course_id)
#     return render_template('course_update.html', title="Update course", course=course, menuItems=menu_items())
#
#
# @app.get('/courses/<int:course_id>')
# def course_detail(course_id):
#     course = Course.query.get(course_id)
#     if not course:
#         return render_template('page404.html', title="Page not found", menuItems=menu_items()), 404
#     else:
#         return render_template('course_detail.html', title="Course detail", course=course, menuItems=menu_items())
# _____________________________________________________________


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title="Page not found", menuItems=menu_items()), 404


@app.route('/login', methods=['POST', 'GET'])
def login():
    name = None
    login_form = LoginForm()

    is_submitted = False
    if login_form.is_submitted():
        is_submitted = True

    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user:
            password = login_form.password.data
            if check_password_hash(user.password_hash, password):
                login_user(user)
                flash("Login successful!")
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong password!")
        else:
            flash("User doesnt exist")
    return render_template('login.html', title="Authorization", menuItems=menu_items(), name=name, form=login_form,
                           is_submitted=is_submitted)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash("You have been log out!")
    return redirect(url_for('index'))


@app.route('/dashboard', methods=['POST', 'GET'])
@login_required
def dashboard():
    user_courses = None
    if current_user.is_authenticated:
        user_courses = current_user.courses
    return render_template('user_dashboard.html', title="Authorization", menuItems=menu_items(), user_courses=user_courses)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    default_role = Role.get_default()
    signup_form = SignupForm(role_id=default_role)
    is_submitted = False
    is_validate = False
    is_successful = False
    user_name = ''
    signup_user = None

    if signup_form.is_submitted():
        is_submitted = True

    if signup_form.validate():
        is_validate = True

    if not signup_form.errors:
        signup_form_errors = "all is fine"
    else:
        signup_form_errors = signup_form.errors

    print("Sign up form: submitted = {}, validate = {}.".format(is_submitted, is_validate))
    print("Sign up form errors: {}".format(signup_form_errors))
    print("signup_form.validate_on_submit(): {}".format(signup_form.validate_on_submit()))

    if signup_form.validate_on_submit():
        user = User.query.filter_by(email=signup_form.email.data).first()
        if user is None:
            role = Role.query.get(signup_form.role_id.data.id)
            password_hash = generate_password_hash(signup_form.password_hash.data, "sha256")
            signup_user = User(first_name=signup_form.name.data, last_name=signup_form.name.data, username=signup_form.username.data,
                               password_hash=password_hash, email=signup_form.email.data, is_active=True)
            signup_user.roles.append(Role(name=role.name))
            is_successful = True
            db.session.add(signup_user)
            db.session.commit()
            signup_form.name.data = ''
            signup_form.username.data = ''
            signup_form.email.data = ''
            signup_form.password_hash.data = ''
            flash("User Added Successfully!")
        else:
            flash("Error! Email already in use")
    return render_template('signup.html', title="Signup", menuItems=menu_items(), signup_form=signup_form,
                           is_successful=is_successful, signup_user=signup_user, is_submitted=is_submitted)


@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/groups')
@login_required
def groups():
    group_name_user_name = {}
    for g in Group.query.all():
        for u in g.in_users:
            group_name_user_name[u.username] = g.name
    return render_template('group.html', group_name_user_name=group_name_user_name)


@app.route('/profile/<email>')
@login_required
def profile(email):
    if 'userLogged' not in session or session['userLogged'] != email:
        abort(401)
    return f"Welcome: {email}"


if __name__ == '__main__':
    app.run(debug=True)
