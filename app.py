import json
import os
import uuid
from datetime import datetime
# from flask_ckeditor import CKEditor, CKEditorField, upload_fail, upload_success
from flask_wtf import csrf, CSRFProtect
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
import database
import gridfs
from dotenv import load_dotenv
from sqlalchemy import exc
from database import db
from mongo_conn import mongo, img_fs, page_fs
from flask import Flask, render_template, url_for, request, redirect, flash, session, abort, jsonify, send_file, \
    Response
import commands
from models import Course, Menu, User, Role, Group, Subject, Test, AnswersTest, Lecture
from flask_migrate import Migrate
from forms import LoginForm, SignupForm, LectureForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_uploads import UploadSet, IMAGES, configure_uploads, UploadNotAllowed
from DAO.lectures_mongo_model import LectureMongo

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from config import *

app = Flask(__name__)
# setup with thew configurations by user
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
# app.config['UPLOAD_FOLDER'] = '/upload'

# Need for flask-pymongo
# app.config['MONGO_URI'] = 'mongodb://localhost:27017/'

database.init_app(app)
commands.start_app(app)
migrate = Migrate(app, db)

# menuItems = [{"name": "Main", "url": "/"},
#              {"name": "About", "url": "/about"},
#              {"name": "Create course", "url": "/create_course"},
#              {"name": "Courses", "url": "/courses"}]

# Need for login-flask
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Need for upload-flask
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img/'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

csrf = CSRFProtect(app)

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
        return render_template('courses.html', title="Courses", all_courses=all_courses, menuItems=menu_items(),subjects=subjects,
                               course_subject=course_subject)

    elif request.method == "POST":
        user = current_user
        title = request.form['title']
        if Course.isExist(title):
            flash('Course with this title already exist', category='success')
            return render_template('create_course.html', title="Create course", menuItems=menu_items())
        else:
            review = request.form['intro']
            text_content = request.form['text']
            course = Course(title=title, review=review, text_content=text_content, creator_uuid=user.uuid)
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
                session['kek'] = 'kek' + str(user.uuid)
                return redirect(url_for('dashboard'),)
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
        kek = session.get('kek')
        print(kek)
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
            password_hash = generate_password_hash(signup_form.password_hash.data, "sha256")
            role = Role.query.get(signup_form.role_id.data.id)
            signup_user = User(
                email = signup_form.email.data,
                password_hash = password_hash,
                first_name = signup_form.first_name.data,
                last_name = signup_form.last_name.data,
                username = signup_form.username.data,
                date_of_birth = signup_form.date_of_birth.data,
                phone_number = signup_form.phone_number.data,
                country = signup_form.country.data,
                city = signup_form.city.data,
                gender = bool(int(signup_form.gender.data)),
                role = role)
            is_successful = True
            now = datetime.now()
            date_str = now.strftime("%Y-%m-%d %H:%M:%S")
            signup_user.last_login = date_str
            db.session.add(signup_user)
            db.session.commit()
            # signup_form = SignupForm(formdata=None)
            flash("User Added Successfully!")
        else:
            flash("Error! Email already in use")
    return render_template('signup.html', title="Signup", menuItems=menu_items(), signup_form=signup_form,
                           is_successful=is_successful, signup_user=signup_user, is_submitted=is_submitted)


@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/api/<uuid:test_uuid>/<uuid:question_uuid>/answer', methods=['POST'])
@login_required
def save_answer(test_uuid, question_uuid):
        #TODO: Check mb answer is already exist
        answers_test = AnswersTest(
            user_uuid = current_user.uuid,
            test_uuid = test_uuid,
            question_uuid = question_uuid,
            answer = json.dumps(dict(request.form))
        )
        db.session.add(answers_test)
        try:
            db.session.commit()
            flash('Successfully save!', category='danger')
        except exc.SQLAlchemyError as ex:
            flash('ERROR: error while sending data!', category='danger')

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


# LECTURES TRY PART---------TINYMCE, Files upload.
@app.route('/lectures', methods=['GET', 'POST'])
def create_lecture():
    form = LectureForm()
    if form.validate_on_submit() and request.method == 'POST':
        course = Course.query.get_or_404("5a060858-607c-4333-b39a-810233c1e3a8")
        # db.session.add(content)
        # db.session.commit()
        # lecture = Lecture(name=form.name.data, description=form.description.data, course_uuid=course.uuid)
        # db.session.add(lecture)
        # db.session.commit()
    return render_template('create_lecture.html', form=form)

@csrf.exempt
@app.route('/img', methods=['POST'])
@login_required
def img_load():
    response = {
        'uploaded': False,
        'url': '/'
    }
    if request.method == 'POST' and 'upload' in request.files:
        fileobj = request.files['upload']
        suffix = fileobj.filename.rsplit('.', 1)[1]
        if suffix not in ('jpeg', 'jpg', 'png', 'gif'):
            return jsonify(response)
        try:
            filename = secure_filename(fileobj.filename)
            photos.save(fileobj, name=filename)
            file_path = photos.path(filename)
            response = {
                'uploaded': True,
                'url': file_path
            }
            return jsonify(response)
        except UploadNotAllowed:
            response = {
                'uploaded': False,
                'url': '/'
            }
            return jsonify(response)
    else:
        flash("Invalid file.")
        return jsonify(response)

@app.route("/upload/img", methods=["POST"])
def upload_image():
    response = {
        'uploaded': False,
        'url': '/'
    }
    if request.method == 'POST' and 'upload' in request.files:
        file_obj = request.files['upload']
        suffix = file_obj.filename.rsplit('.', 1)[1]
        if suffix not in ('jpeg', 'jpg', 'png', 'gif'):
            return jsonify(response)
        try:
            filename = secure_filename(file_obj.filename)
            #TODO: EX FOR GRIDFS PUT

            file_id = img_fs.put(file_obj,
                            filename=filename,
                            content_type=file_obj.content_type
                            )
            file_path = url_for("get_image", file_id=file_id)
            response = {
                'uploaded': True,
                'url': file_path
            }
            return jsonify(response)
        except UploadNotAllowed:
            response = {
                'uploaded': False,
                'url': '/'
            }
            return jsonify(response)
    else:
        flash("Invalid file.")
        return jsonify(response)


@app.route("/get/img/<file_id>")
def get_image(file_id):
    try:
        query = {"_id": ObjectId(file_id)}
        image = img_fs.find_one(query)
        response = Response(image.read(), image.content_type)
        return response
    except Exception as e:
        return str(e)

@app.route('/lecture/<uuid:uuid>')
def lecture_get(uuid):
    lecture = Lecture.query.get_or_404(uuid)
    # images = lecture.images
    return render_template('lecture.html', lecture=lecture_get)

@app.route('/api/pages', methods=['POST'])
def save_pages():
    new_lecture = LectureMongo('123')
    pages_data = request.get_json()
    for page_number, page_content in pages_data.items():
        prew_page_content = new_lecture.get_page_content(page_number)
        if prew_page_content is None:
            new_lecture.create_page(page_number, page_content)
        else:
            new_lecture.update_page_content(page_number, page_content)
    return jsonify({'message': 'All pages saved successfully!'})

@app.route('/api/pages/<int:lecture_uuid>', methods=['GET'])
def get_pages(lecture_uuid):
    lecture = LectureMongo.find_by_uuid(str(lecture_uuid))
    if lecture is None:
        return 'Lecture not found', 404
    try:
        pages = lecture.get_all_pages()
        return jsonify(pages)
    except Exception as e:
        return {'error': str(e)}, 500


if __name__ == '__main__':
    app.run(debug=True)
