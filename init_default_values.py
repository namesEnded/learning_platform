from flask import Flask, session
from database import db
from models import Course, Menu, User, Role, Group, Subject
from app import app

def populate_db():
    with app.app_context():
        admin = Role(name="Admin")
        db.session.add(admin)
        menuItem1 = Menu(item_name="Курсы", item_url="/courses")
        menuItem2 = Menu(item_name="Группы", item_url="/groups")
        menuItem3 = Menu(item_name="Создать курс", item_url="/courses/new")
        menuItem4 = Menu(item_name="О платформе", item_url="/about")
        menuItem5 = Menu(item_name="Профиль", item_url="/dashboard")
        db.session.add(menuItem1)
        db.session.add(menuItem2)
        db.session.add(menuItem3)
        db.session.add(menuItem4)
        db.session.add(menuItem5)

        IT = Subject(name="Информатика", description="Информатика топ")
        MATH = Subject(name="Математика", description="Математика не очень топ")
        SU = Subject(name="Информационная безопасность", description="Информационная безопасность - это страшно")
        db.session.add(IT)
        db.session.add(MATH)
        db.session.add(SU)
        db.session.commit()
        db.session.close()


if __name__ == '__main__':
    print('Populating db...')
    populate_db()
    print('Successfully populated!')
