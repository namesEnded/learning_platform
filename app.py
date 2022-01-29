import secrets
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///learningPlatform.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
db = SQLAlchemy(app)

menuItems = [{"name": "Main", "url": "/"},
             {"name": "About", "url": "/about"},
             {"name": "Create course", "url": "/create_course"},
             {"name": "Courses", "url": "/courses"}]


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Course %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html", menuItems=menuItems)


@app.route('/create_course', methods=['POST', 'GET'])
def create_course():
    # TODO: Make a normal request success handler
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        course = Course(title=title, intro=intro, text=text)
        try:
            if len(title) == 0:
                flash('ERROR: error while sending data!', category='danger')
                return render_template("create_course.html", menuItems=menuItems)
            else:
                db.session.add(course)
                db.session.commit()
                flash('Data sent successfully!', category='success')
                return render_template("create_course.html", menuItems=menuItems)

        except:
            flash('ERROR: error while sending data!', category='danger')
            return
    else:
        return render_template("create_course.html", menuItems=menuItems)


@app.route('/about')
def about():
    return render_template("about.html", menuItems=menuItems)


@app.route('/courses')
def courses():
    all_courses = Course.query.order_by(Course.date.desc()).all()
    return render_template("courses.html", all_courses=all_courses, menuItems=menuItems)


@app.route('/courses/<int:id>')
def course_detail(id):
    course = Course.query.get(id)
    return render_template("course_detail.html", course=course, menuItems=menuItems)


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
        course.intro = request.form['intro']
        course.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/courses')
        except:
            return "ERROR: error while updating data"
    else:
        return render_template("course_update.html", course=course, menuItems=menuItems)


if __name__ == '__main__':
    app.run(debug=True)
