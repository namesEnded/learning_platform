from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///learningPlatform.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Course %r>' % self.id

menuItems = [{"name": "Main", "url": "/"},
             {"name": "About", "url": "/about"},
             {"name": "Create course", "url": "/create_course"},
             {"name": "Courses", "url": "/courses"},
             {"name": "Profile", "url": "/profile"}]


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html", menuItems=menuItems)


@app.route('/create_course', methods=['POST', 'GET'])
def create_course():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        course = Course(title=title, intro=intro, text=text)

        try:
            db.session.add(course)
            db.session.commit()
            return redirect('/courses')
        except:
            return "ERROR: error while sending data"
    else:
        return render_template("create_course.html", menuItems=menuItems)


@app.route('/about')
def about():
    return render_template("about.html", menuItems=menuItems)


@app.route('/courses')
def courses():
    all_courses = Course.query.order_by(Course.date.desc()).all()
    return render_template("courses.html", all_courses=all_courses, menuItems=menuItems)

@app.route('/profile')
def profile():
    return render_template("profile.html", menuItems=menuItems)

@app.route('/editpage')
def editpage():
    return render_template("editpage.html", menuItems=menuItems)

@app.route('/language')
def language():
    return render_template("language.html")

@app.route('/changepass')
def changepass():
    return render_template("changepass.html")


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
        return redirect('/courses', menuItems=menuItems)

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
