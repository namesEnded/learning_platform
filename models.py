from datetime import datetime

from sqlalchemy import MetaData
from sqlalchemy.dialects.postgresql import UUID, REAL
from flask_sqlalchemy import SQLAlchemy
import uuid
from sqlalchemy.orm import backref, declarative_base
from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


user_group = db.Table(
        "user_group",
        db.Column("group_uuid",UUID(as_uuid=True), db.ForeignKey("groups.uuid")),
        db.Column("user_uuid",UUID(as_uuid=True), db.ForeignKey("users.uuid")),
    )

groups_courses = db.Table('subscribed_groups',
        db.Column('course_uuid', UUID(as_uuid=True), db.ForeignKey('courses.uuid')),
        db.Column('group_uuid', UUID(as_uuid=True), db.ForeignKey('groups.uuid'))
        )

roles_users = db.Table('roles_users',
        db.Column('user_uuid', UUID(as_uuid=True), db.ForeignKey('users.uuid')),
        db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))

subject_course = db.Table('subject_course',
        db.Column('course_uuid', UUID(as_uuid=True), db.ForeignKey('courses.uuid')),
        db.Column('subject_uuid', UUID(as_uuid=True), db.ForeignKey('subjects.uuid')))

class Course(db.Model):
    __tablename__ = 'courses'
    uuid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, primary_key=True)

    title = db.Column(db.String(150), nullable=False)
    review = db.Column(db.String(300), nullable=False)
    text_content = db.Column(db.Text, nullable=False)
    user_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('users.uuid'), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship("User", back_populates="courses")
    subscribed_groups = db.relationship("Course", secondary=groups_courses, backref="subscribed_courses")
    subjects = db.relationship("Subject", secondary=subject_course, backref="courses")
    def __init__(self, title, review, text_content, user):
        self.user = user
        self.title = title
        self.review = review
        self.text_content = text_content

    def __repr__(self):
        return '< Course uuid: {}>'.format(self.uuid)

    @classmethod
    def find_course_by_title(cls, course_title):
        return cls.query.filter_by(title=course_title).first()

    @classmethod
    def isExist(cls, course_title):
        return True if cls.query.filter_by(title=course_title).first() else False

    def serialize(self):
        return {
            'uuid': str(self.uuid),
            'course_name': self.title,
            'review': self.review,
            'text_content': self.text_content,
            'date_added': self.date_added,
            'author': str(self.uuid),
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
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    @classmethod
    def find_role_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_default(cls):
        return cls.query.filter_by(name="Student").first()

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '< Role id: {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    uuid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    email = db.Column(db.String(255), nullable=False, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')

    # User information
    first_name = db.Column(db.String(100), nullable=False, server_default='')
    last_name = db.Column(db.String(100), nullable=False, server_default='')
    username = db.Column(db.String(25), nullable=False)
    password_hash = db.Column(db.String(300), nullable=False)

    # Define the relationship
    roles = db.relationship('Role', secondary=roles_users, backref='roled')
    courses = db.relationship('Course', back_populates="user")
    groups = db.relationship('Group', back_populates="owner")
    # tests = db.relationship("Test", back_populates="creator")
    @property
    def id(self):
        return self.uuid
    # Map: user.id=id to: user.uuid=id

    @id.setter
    def id(self, value):
        self.uuid = value

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, name,username, password_hash, email):
        self.name = name
        self.username = username
        self.password_hash = password_hash
        self.email = email

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

class Group(db.Model):
    __tablename__ = 'groups'
    uuid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, primary_key=True)

    name = db.Column(db.String(150), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    owner = db.relationship("User", back_populates="groups")
    in_users = db.relationship("User", secondary=user_group, backref="in_users")
    owner_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('users.uuid'), nullable=False)
    documented_group_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('groups.uuid'), nullable=True)
    documented_group = db.relationship('Group', remote_side=[uuid], backref='document_source')
    description = db.Column(db.String(300))
    is_virtual = db.Column(db.Boolean, nullable=False, default=False)


    def __init__(self, name, description, user, is_virtual, documented_group_uuid):
        self.owner = user
        self.name = name
        self.documented_group_uuid = documented_group_uuid
        self.description = description
        self.is_virtual = is_virtual

    def __repr__(self):
        return '< Group saved: uuid {}>'.format(self.uuid)

    @classmethod
    def find_group_by_name(cls, group_name):
        return cls.query.filter_by(name=group_name).first()

    @classmethod
    def isExist(cls, group_name):
        return True if cls.query.filter_by(name=group_name).first() else False

    def serialize(self):
        return {
            'uuid': str(self.uuid),
            'group_name': self.name,
            'description': self.description,
            'date_added': self.date_added,
        }

class Subject(db.Model):
    __tablename__ = 'subjects'
    uuid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(300))

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return '< Subject saved: uuid {}>'.format(self.id)

    @classmethod
    def find_subject_by_name(cls, subject_name):
        return cls.query.filter_by(name=subject_name).first()

    @classmethod
    def isExist(cls, subject_name):
        return True if cls.query.filter_by(name=subject_name).first() else False

    def serialize(self):
        return {
            'uuid': str(self.uuid),
            'subject_name': self.name,
            'description': self.description,
        }

# class Test(db.Model):
#     __tablename__ = 'tests'
#     uuid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, primary_key=True)
#     name = db.Column(db.String(150), nullable=False)
#
#     creator_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('users.uuid'), nullable=False)
#     creator = db.relationship("User", back_populates="tests")
#
#     assessment_type_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('assessment_type.uuid'), nullable=False)
#     assessment_type = db.relationship("AssessmentType", back_populates="tests")
#
#
#     description = db.Column(db.String(300))
#     duration = db.Column(db.Integer)
#     passing_score = db.Column(REAL, default=0.0)
#     number_of_questions = db.Column(db.Integer)
#     attempts = db.Column(db.Integer)
#
#     randomize_questions = db.Column(db.Boolean, nullable=False, default=False)
#     randomize_answers = db.Column(db.Boolean, nullable=False, default=False)
#     is_active = db.Column(db.Boolean, nullable=False, default=False)
#     show_result = db.Column(db.Boolean, nullable=False, default=False)
#     multiply_view = db.Column(db.Boolean, nullable=False, default=False)
#     time_expired_questions = db.Column(db.Boolean, nullable=False, default=False)
#
#     start_date = db.Column(db.DateTime())
#     end_date = db.Column(db.DateTime())
#     date_created = db.Column(db.DateTime())
#     date_modified = db.Column(db.DateTime())
#
#
#     def __init__(self, name, description):
#         self.name = name
#         self.description = description
#
#     def __repr__(self):
#         return '< Subject saved: uuid {}>'.format(self.id)
#
#     @classmethod
#     def find_subject_by_name(cls, subject_name):
#         return cls.query.filter_by(name=subject_name).first()
#
#     @classmethod
#     def isExist(cls, subject_name):
#         return True if cls.query.filter_by(name=subject_name).first() else False
#
#     def serialize(self):
#         return {
#             'uuid': str(self.uuid),
#             'subject_name': self.name,
#             'description': self.description,
#         }