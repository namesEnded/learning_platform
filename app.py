import os
import database
from dotenv import load_dotenv
from database import db
from flask import Flask, render_template, url_for, request, redirect, flash, session, abort
import commands
from models import Course, Menu
from flask_migrate import Migrate
from forms import LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

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


@app.route('/create_course', methods=['POST', 'GET'])
def create_course():
    # TODO: Make a normal request success handler
    if request.method == "POST":
        title = request.form['title']
        review = request.form['intro']
        text_content = request.form['text']
        course = Course(title=title, review=review, text_content=text_content, author="default author")
        try:
            if len(title) == 0:
                flash('ERROR: error while sending data!', category='danger')
                return render_template('create_course.html', title="Create course", menuItems=menu_items())
            else:
                db.session.add(course)
                db.session.commit()
                flash('Data sent successfully!', category='success')
                return render_template('create_course.html', title="Create course", menuItems=menu_items())

        except:
            flash('ERROR: error while sending data!', category='danger')
            return
    else:
        return render_template('create_course.html', title="Create course", menuItems=menu_items())


@app.route('/about')
def about():
    return render_template('about.html', title="About learning platform", menuItems=menu_items())


@app.route('/courses')
def courses():
    all_courses = Course.query.order_by(Course.date_added.desc()).all()
    return render_template('courses.html', title="Courses", all_courses=all_courses, menuItems=menu_items())


@app.route('/courses/<int:id>')
def course_detail(id):
    course = Course.query.get(id)
    if not course:
        return render_template('page404.html', title="Page not found", menuItems=menu_items()), 404
    else:
        return render_template('course_detail.html', title="Course detail", course=course, menuItems=menu_items())


@app.route('/courses/<int:id>/delete')
def course_delete(id):
    course = Course.query.get_or_404(id)

    try:
        db.session.delete(course)
        db.session.commit()
        return redirect('/courses')

    except:
        return "ERROR: error while deleting course"


@app.route('/courses/<int:id>/update', methods=['POST', 'GET'])
def course_update(id):
    course = Course.query.get(id)

    if request.method == "POST":

        course.title = request.form['title']
        course.review = request.form['intro']
        course.text_content = request.form['text']

        try:
            db.session.commit()
            return redirect('/courses')
        except:
            return "ERROR: error while updating data"
    else:
        return render_template('course_update.html', title="Update course", course=course, menuItems=menu_items())


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title="Page not found", menuItems=menu_items()), 404


@app.route('/login', methods=['POST', 'GET'])
def login():
    name = None
    form = LoginForm()

    if form.validate_on_submit():
        name = form.email.data
        form.email.data = ""




    # # TODO: When tables with user login data appear - fix authorization
    # if 'userLogged' in session:
    #     return redirect(url_for('profile', email=session['userLogged']))
    # elif request.method == 'POST' and request.form['email'] == "defaultUser@d.ru" and request.form['password'] == "123":
    #     session['userLogged'] = request.form['email']
    #     return redirect(url_for('profile', email=session['userLogged']))

    return render_template('login.html', title="Authorization", menuItems=menu_items(),name=name, form=form)


@app.route('/profile/<email>')
def profile(email):
    if 'userLogged' not in session or session['userLogged'] != email:
        abort(401)
    return f"Welcome: {email}"


if __name__ == '__main__':
    app.run(debug=True)
