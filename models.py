from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
import uuid
from sqlalchemy.orm import backref
from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    review = db.Column(db.String(300), nullable=False)
    text_content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship("User", back_populates="courses")
    uuid =  db.Column(UUID(as_uuid=True), default=uuid.uuid4,unique=True)

    def __init__(self, title, review, text_content, user):
        self.user = user
        self.title = title
        self.review = review
        self.text_content = text_content

    def __repr__(self):
        return '< Course saved: id {}>'.format(self.id)

    @classmethod
    def find_course_by_title(cls, course_title):
        return cls.query.filter_by(title=course_title).first()

    @classmethod
    def isExist(cls, course_title):
        return True if cls.query.filter_by(title=course_title).first() else False

    def serialize(self):
        return {
            'id': self.id,
            'course_name': self.title,
            'review': self.review,
            'text_content': self.text_content,
            'date_added': self.date_added,
            'author': self.user_id,
            'uuid': str(self.uuid)
        }


class Menu(db.Model):
    __tablename__ = 'menu_items'

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    item_url = db.Column(db.String(300), nullable=False)

    def __init__(self, item_name, item_url):
        self.item_name = item_name
        self.item_url = item_url

    def __repr__(self):
        return '< Saved Item:URL: id {}>'.format(self.item_url)

    def serialize(self):
        return {
            'id': self.id,
            'item_name': self.item_name,
            'item_url': self.item_url
        }


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(25), nullable=False)

    #Kind of differents way to make one to one relationship
    #------------------------------------------------------
    #role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), unique=True)
    # ------------------------------------------------------
    #role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    #role = db.relationship("Role", backref=backref("user", uselist=False))
    # ------------------------------------------------------

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship("Role", back_populates="user")

    global_group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    global_group = db.relationship("Group", back_populates="users")

    password_hash = db.Column(db.String(300), nullable=False)
    e_mail = db.Column(db.String(300), unique=True, nullable=False)
    courses = db.relationship('Course', back_populates="user")
    groups = db.relationship('Group', back_populates="user")
    uuid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, name,username, role, password_hash, e_mail):
        self.name = name
        self.username = username
        self.role = role
        self.password_hash = password_hash
        self.e_mail = e_mail

    def __repr__(self):
        return '< Saved user:e_mail: e_mail {}>'.format(self.e_mail)

    @classmethod
    def find_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_user_by_uuid(cls, username):
        return cls.query.filter_by(uuid=uuid).first()

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'role': self.role,
            'password': self.password_hash,
            'e_mail': self.e_mail,
            'uuid': str(self.uuid)
        }


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    #user = db.relationship('User', backref='role', uselist=False)
    user = db.relationship("User", back_populates="role")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '< Saved role id: {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }

class Group(db.Model):
    __tablename__ = 'groups'

    uuid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship("User", back_populates="groups")
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.String(300))
    is_global = db.Column(db.Boolean, nullable=False, default=False)
    users = db.relationship("User", back_populates="global_group_id")

    def __init__(self, name, description, user, is_global):
        self.user = user
        self.name = name
        self.description = description
        self.is_global = is_global

    def __repr__(self):
        return '< Course saved: id {}>'.format(self.id)

    @classmethod
    def find_group_by_name(cls, group_name):
        return cls.query.filter_by(name=group_name).first()

    @classmethod
    def isExist(cls, group_name):
        return True if cls.query.filter_by(name=group_name).first() else False

    def serialize(self):
        return {
            'uuid': str(self.uuid),
            'group_name': self.title,
            'description': self.review,
            'date_added': self.date_added,
            'owner_id': self.user_id,
        }