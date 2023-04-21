from flask import Flask, session
from database import db
from models import Course, Menu, User, Role, Group, Subject
from app import app

def populate_db():
    with app.app_context():
        # IT = Subject(name="Информатика", description="Информатика топ")
        # MATH = Subject(name="Математика", description="Математика не очень топ")
        # SU = Subject(name="Информационная безопасность", description="Информационная безопасность - это страшно")
        # db.session.add(IT)
        # db.session.add(MATH)
        # db.session.add(SU)

        bufUser = User.find_user_by_username("GLOBAL")
        db.session.add(bufUser)

        IT = Subject.find_subject_by_name(subject_name="Информатика")
        MATH = Subject.find_subject_by_name(subject_name="Математика")
        SU = Subject.find_subject_by_name(subject_name="Безопасность")

        it_course = Course(title = "IT",
             review = "Any",
             text_content = "Any",
             creator_uuid=bufUser.uuid)
        it_course.subjects.append(IT)
        db.session.add(it_course)

        math_course = Course(title="MATH",
                           review="Any",
                           text_content="Any",
                           creator_uuid=bufUser.uuid)
        math_course.subjects.append(MATH)
        db.session.add(math_course)

        su_course = Course(title="SU",
                           review="Any",
                           text_content="Any",
                           creator_uuid=bufUser.uuid)
        su_course.subjects.append(SU)
        db.session.add(su_course)

        db.session.commit()
        db.session.close()


if __name__ == '__main__':
    print('Populating db...')
    populate_db()
    print('Successfully populated!')
