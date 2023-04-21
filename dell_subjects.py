from flask import Flask, session
from database import db
from models import Course, Menu, User, Role, Group, Subject
from app import app

def populate_db():
    with app.app_context():
        BUFF=Course.query.get("88353120-4dde-42c7-a6c2-44d0cd187056")
        BUFF2 = Course.query.get("794d12bc-60d4-4049-b141-fed25f2fb881")
        print(BUFF)

        db.session.delete(BUFF)
        db.session.delete(BUFF2)
        db.session.commit()

if __name__ == '__main__':
    print('Populating db...')
    populate_db()
    print('Successfully populated!')
