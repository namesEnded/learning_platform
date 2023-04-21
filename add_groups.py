from flask import Flask, session
from database import db
from models import Course, Menu, User, Role, Group, Subject
from app import app

def populate_db():
    with app.app_context():
        # bufUser = User.find_user_by_username("GLOBAL")
        # fake1 = Group.find_group_by_name("WITH_UUID")
        # print(fake1)
        # bufGroup = Group(name="WITH_UUID3",description="WITH_UUID3",owner=bufUser,is_virtual=True,documented_group=fake1.uuid)
        # db.session.add(bufGroup)
        # db.session.commit()
        # db.session.close()

        WITH_OBJ = Group.find_group_by_name("WITH_UUID3")
        print(WITH_OBJ.uuid)
        print("?-?")
        print(WITH_OBJ.documented_group.uuid)

if __name__ == '__main__':
    print('Populating db...')
    populate_db()
    print('Successfully populated!')

