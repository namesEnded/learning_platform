from flask import Flask, session
from database import db
from models import Course, Menu, User, Role, Group
from app import app

def populate_db():
    with app.app_context():
        stud_role = Role.get_default()
        admin_role = Role.find_role_by_name("Admin")
        global_user=User(name ="GLOBAL",
                         username="GLOBAL",
                         password_hash="GLOBAL",
                         email="GLOBAL@YANDEX.RU")
        global_user.roles.append(admin_role)
        db.session.add(global_user)

        global_group=Group(name="global_group",
                           description="global_group",
                           user=global_user,
                           is_virtual=0,
                           documented_group_uuid=None)
        db.session.add(global_group)

        local_group=Group(name="global_group",
                           description="global_group",
                           user=global_user,
                           is_virtual=1,
                           documented_group_uuid=global_group.uuid)
        db.session.add(global_group)

        for i in range(10):
            buf_user=User(name ="Gazmanov the " + str(i),
                         username="SPIZDEL_I_USHEL_" + str(i),
                         password_hash="YAEBUSOBAK" + str(i),
                         email="YAEBU@YANDEX.RU"+ str(i))
            buf_user.roles.append(stud_role)
            db.session.add(buf_user)
            local_group.in_users.append(buf_user)

        db.session.commit()
        db.session.close()


if __name__ == '__main__':
    print('Populating db...')
    populate_db()
    print('Successfully populated!')
