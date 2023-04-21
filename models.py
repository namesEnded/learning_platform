from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID, REAL, TEXT, JSON
import uuid
from sqlalchemy.orm import backref, declarative_base
from database import db
from werkzeug.security import check_password_hash
from flask_login import UserMixin


user_group = db.Table(
        "user_group",
        db.Column("group_uuid",UUID(as_uuid=True), db.ForeignKey("groups.uuid", ondelete="CASCADE")),
        db.Column("user_uuid",UUID(as_uuid=True), db.ForeignKey("users.uuid", ondelete="CASCADE"))
    )

groups_courses = db.Table('subscribed_groups',
        db.Column('course_uuid', UUID(as_uuid=True), db.ForeignKey('courses.uuid', ondelete="CASCADE")),
        db.Column('group_uuid', UUID(as_uuid=True), db.ForeignKey('groups.uuid', ondelete="CASCADE"))
        )

roles_users = db.Table('roles_users',
        db.Column('user_uuid', UUID(as_uuid=True), db.ForeignKey('users.uuid')),
        db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))

subject_course = db.Table('subject_course',
        db.Column('course_uuid', UUID(as_uuid=True), db.ForeignKey('courses.uuid')),
        db.Column('subject_uuid', UUID(as_uuid=True), db.ForeignKey('subjects.uuid')))

test_questions = db.Table('test_questions',
        db.Column('test_uuid', UUID(as_uuid=True), db.ForeignKey('tests.uuid', ondelete="CASCADE"), primary_key=True),
        db.Column('question_uuid', UUID(as_uuid=True), db.ForeignKey('questions.uuid', ondelete="CASCADE"), primary_key=True))

class Course(db.Model):
    __tablename__ = 'courses'
    uuid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, primary_key=True)

    title = db.Column(db.String(150), nullable=False)
    review = db.Column(db.String(300), nullable=False)
    text_content = db.Column(db.Text, nullable=False)
    creator_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('users.uuid'), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    creator = db.relationship("User", back_populates="courses")
    subjects = db.relationship("Subject", secondary=subject_course, backref="courses",cascade="all, delete")
    subscribed_groups = db.relationship("Course", secondary=groups_courses, backref="subscribed_courses",cascade="all, delete")

    def __init__(self, title, review, text_content, creator_uuid):
        self.creator_uuid = creator_uuid
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

    # User authentication information
    email = db.Column(db.String(255), nullable=False, unique=True)

    # User information
    is_active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    is_verified = db.Column(db.Boolean(),default=False, nullable=False, server_default='0')
    email_confirmed_at = db.Column(db.DateTime())
    first_name = db.Column(db.String(100), nullable=False, server_default='')
    date_str = "2022-01-01 12:00:00"
    date_format = "%Y-%m-%d %H:%M:%S"
    date_of_birth = db.Column(db.Date, nullable=False, server_default='2022-01-01 12:00:00')
    phone_number = db.Column(db.String(20))
    country = db.Column(db.String(50))
    city = db.Column(db.String(50))
    gender = db.Column(db.Boolean(), nullable=False, server_default='1')
    created_datetime = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    last_password_change = db.Column(db.DateTime, default=datetime.utcnow)
    last_name = db.Column(db.String(100), nullable=False, server_default='')
    username = db.Column(db.String(25), nullable=False, server_default='')
    password_hash = db.Column(db.String(300), nullable=False, server_default='')

    # Define the relationship
    roles = db.relationship('Role', secondary=roles_users, backref='roled')
    courses = db.relationship('Course', back_populates="creator")
    lectures = db.relationship('Lecture', back_populates="creator")
    groups = db.relationship('Group', back_populates="owner")
    questions = db.relationship("Question", back_populates="creator", foreign_keys = 'Question.creator_uuid')
    tests = db.relationship("Test", back_populates="creator", )
    moderated_questions = db.relationship("Question", back_populates="moderator", foreign_keys='Question.moderator_uuid')
    answers_tests = db.relationship('AnswersTest', back_populates='user')
    test_results = db.relationship('TestResult', back_populates='user')
    @property
    def id(self):
        return self.uuid

    @id.setter
    def id(self, value):
        self.uuid = value

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, email, password_hash, first_name, last_name, username, date_of_birth, phone_number, country, city,
                 gender, role):
        self.email = email
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.date_of_birth = date_of_birth
        self.phone_number = phone_number
        self.country = country
        self.city = city
        self.gender = gender
        self.roles.append(role)

    def __repr__(self):
        return '< User:email: email {}>'.format(self.email)

    @classmethod
    def find_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_user_by_uuid(cls, user_uuid):
        return cls.query.filter_by(uuid=user_uuid).first()

    def serialize(self):
        return {
            'uuid': self.uuid,
            'username': self.username,
            'email': self.email,
            'first_name' : self.first_name,
            'last_name' : self.last_name
        }

class Group(db.Model):
    __tablename__ = 'groups'
    uuid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, primary_key=True)

    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(300))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    is_virtual = db.Column(db.Boolean, nullable=False, default=False)

    owner_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('users.uuid'), nullable=False)
    documented_group_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('groups.uuid'), nullable=True)

    owner = db.relationship("User", back_populates="groups")
    in_users = db.relationship("User", secondary=user_group, backref="belongs_groups", cascade="all, delete")
    documented_group = db.relationship('Group', remote_side=[uuid], cascade="all, delete")


    def __init__(self, name, description, owner_uuid, is_virtual, documented_group_uuid):
        self.owner_uuid = owner_uuid
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
        return '< Subject: name {}>'.format(self.name)

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

class Test(db.Model):
    __tablename__ = 'tests'
    uuid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, primary_key=True)

    name = db.Column(db.String(150), nullable=False)
    creator_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('users.uuid'), nullable=False)
    assessment_type_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('assessment_type.uuid'), nullable=False)
    description = db.Column(db.String(300))
    duration = db.Column(db.Integer)
    passing_score = db.Column(REAL, default=0.0)
    number_of_questions = db.Column(db.Integer)
    attempts = db.Column(db.Integer)

    randomize_questions = db.Column(db.Boolean, nullable=False, default=False)
    randomize_answers = db.Column(db.Boolean, nullable=False, default=False)
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    show_result = db.Column(db.Boolean, nullable=False, default=False)
    multiply_view = db.Column(db.Boolean, nullable=False, default=False)
    time_expired_questions = db.Column(db.Boolean, nullable=False, default=False)

    start_date = db.Column(db.DateTime())
    end_date = db.Column(db.DateTime())
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.utcnow)

    creator = db.relationship("User", back_populates="tests")
    assessment_type = db.relationship("AssessmentType", back_populates="tests")
    questions = db.relationship("Question", secondary=test_questions, backref="tests",cascade="all, delete")
    answers_users = db.relationship('AnswersTest', back_populates='test')
    users_results = db.relationship('TestResult', back_populates='test')

    def __init__(self, name, description, creator_uuid, assessment_type_uuid, duration, passing_score, number_of_questions,attempts,
                 randomize_questions, randomize_answers, is_active, show_result, multiply_view, time_expired_questions,
                 start_date, end_date):
        self.name = name
        self.description = description
        self.creator_uuid = creator_uuid
        self.assessment_type_uuid = assessment_type_uuid
        self.duration = duration
        self.passing_score = passing_score
        self.number_of_questions = number_of_questions
        self.attempts = attempts
        self.randomize_questions = randomize_questions
        self.randomize_answers = randomize_answers
        self.is_active = is_active
        self.show_result = show_result
        self.multiply_view = multiply_view
        self.time_expired_questions = time_expired_questions
        self.start_date = start_date
        self.end_date = end_date

    def __repr__(self):
        return '< Test: uuid {}>'.format(self.uuid)

    @classmethod
    def find_test_by_name(cls, test_name):
        return cls.query.filter_by(name=test_name).first()


    @classmethod
    def isExist(cls, test_name):
        return True if cls.query.filter_by(name=test_name).first() else False

    def serialize(self):
        return {
            'uuid':self.uuid,
            'name':self.name,
            'description':self.description,
            'creator_uuid':self.creator_uuid,
            'assessment_type_uuid':self.assessment_type_uuid,
            'duration':self.duration,
            'passing_score':self.passing_score,
            'number_of_questions':self.number_of_questions,
            'attempts':self.attempts,
            'randomize_questions':self.randomize_questions,
            'randomize_answers':self.randomize_answers,
            'is_active':self.is_active,
            'show_result':self.show_result,
            'multiply_view':self.multiply_view,
            'time_expired_questions':self.time_expired_questions,
            'start_date':self.start_date,
            'end_date':self.end_date,
            'date_created':self.date_created,
            'date_modified':self.date_modified
        }

class AssessmentType(db.Model):
    __tablename__ = 'assessment_type'
    uuid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(300))
    tests = db.relationship("Test", back_populates="assessment_type")

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return '< AssessmentType: name {}>'.format(self.name)

    @classmethod
    def find_by_name(cls, assessment_type):
        return cls.query.filter_by(name=assessment_type).first()

    @classmethod
    def isExist(cls, assessment_type):
        return True if cls.query.filter_by(name=assessment_type).first() else False

    def serialize(self):
        return {
            'uuid': self.uuid,
            'assessment_type_name': self.name,
            'description': self.description,
        }

class Question(db.Model):
    __tablename__ = 'questions'
    uuid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, primary_key=True)
    content = db.Column(TEXT, nullable=False)
    date_created = db.Column(db.DateTime())
    date_modified = db.Column(db.DateTime())
    weight = db.Column(REAL, default=0.0)
    expiration_time = db.Column(REAL, default=0.0)
    description = db.Column(db.String(300))

    type_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('question_types.uuid'), nullable=False)
    creator_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('users.uuid'), nullable=False)
    moderator_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('users.uuid'), nullable=False)
    difficulty_level_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('difficulty_levels.uuid'), nullable=False)

    type = db.relationship("QuestionType", back_populates="questions")
    creator = db.relationship("User", foreign_keys=[creator_uuid], back_populates="questions")
    moderator = db.relationship("User", foreign_keys=[moderator_uuid], back_populates="moderated_questions")
    difficulty_level = db.relationship("DifficultyLevel", back_populates="questions")
    answers = db.relationship("Answer", back_populates="question", cascade="all, delete",passive_deletes=True)
    tests_users = db.relationship('AnswersTest', back_populates='question')

    def __init__(self, content, weight, expiration_time, description, type_uuid, creator_uuid, moderator_uuid,
                 difficulty_level_uuid):
        self.content = content
        self.weight = weight
        self.expiration_time = expiration_time
        self.description = description
        self.type_uuid = type_uuid
        self.creator_uuid = creator_uuid
        self.moderator_uuid = moderator_uuid
        self.difficulty_level_uuid = difficulty_level_uuid

    def __repr__(self):
        return '< Question: uuid {}>'.format(self.uuid)

    @classmethod
    def find_by_name(cls, question_name):
        return cls.query.filter_by(name=question_name).first()

    @classmethod
    def isExist(cls, question_name):
        return True if cls.query.filter_by(name=question_name).first() else False

    def serialize(self):
        return {
            'uuid': self.uuid,
            'content': self.content,
            'date_created': self.date_created,
            'date_modified': self.date_modified,
            'weight': self.weight,
            'expiration_time': self.expiration_time,
            'description': self.description,
        }

class QuestionType(db.Model):
    __tablename__ = 'question_types'
    uuid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description_template = db.Column(db.String(350), nullable=False)

    questions = db.relationship("Question", back_populates="type")

    def __init__(self, name, description_template):
        self.name = name
        self.description_template = description_template
    def __repr__(self):
        return '< QuestionType: name {}>'.format(self.name)

    @classmethod
    def find_by_name(cls, question_type):
        return cls.query.filter_by(name=question_type).first()

    @classmethod
    def isExist(cls, question_type):
        return True if cls.query.filter_by(name=question_type).first() else False

    def serialize(self):
        return {
            'uuid': self.uuid,
            'name': self.name,
            'description_template': self.description_template
        }

class DifficultyLevel(db.Model):
    __tablename__ = 'difficulty_levels'
    uuid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    
    questions = db.relationship("Question", back_populates="difficulty_level")
    def __init__(self, name, description_template):
        self.name = name
        self.description_template = description_template
    def __repr__(self):
        return '< Difficulty level: name {}>'.format(self.name)

    @classmethod
    def find_by_name(cls, difficulty_level):
        return cls.query.filter_by(name=difficulty_level).first()

    @classmethod
    def isExist(cls, difficulty_level):
        return True if cls.query.filter_by(name=difficulty_level).first() else False

    def serialize(self):
        return {
            'uuid': self.uuid,
            'name': self.name,
        }

class Answer(db.Model):
    __tablename__ = 'answers'
    uuid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, primary_key=True)
    question_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('questions.uuid',ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    content = db.Column(TEXT, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False, default=False)

    question = db.relationship("Question", back_populates="answers")

    def __init__(self, name, content, is_correct):
        self.name = name
        self.content = content
        self.is_correct = is_correct
    def __repr__(self):
        return '< Answer: name {}>'.format(self.name)

    @classmethod
    def find_by_name(cls, question_type):
        return cls.query.filter_by(name=question_type).first()

    @classmethod
    def isExist(cls, question_type):
        return True if cls.query.filter_by(name=question_type).first() else False

    def serialize(self):
        return {
            'uuid': self.uuid,
            'name': self.name,
            'description_template': self.description_template
        }

class AnswersTest(db.Model):
    __tablename__ = 'answers_test'
    uuid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, primary_key=True)
    user_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('users.uuid'), nullable=False)
    test_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('tests.uuid'), nullable=False)
    question_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('questions.uuid'), nullable=False)
    answer = db.Column(db.JSON)
    user = db.relationship('User', back_populates='answers_tests')
    test = db.relationship('Test', back_populates='answers_users')
    question = db.relationship('Question', back_populates='tests_users')
    def __repr__(self):
        return f'{self.uuid} {self.user_uuid} {self.test_uuid} {self.question_uuid} {self.answer}'
    def __init__(self, user_uuid,test_uuid,question_uuid,answer ):
        self.user_uuid = user_uuid
        self.test_uuid = test_uuid
        self.question_uuid = question_uuid
        self.answer = answer

class TestResult(db.Model):
    __tablename__ = 'test_results'
    uuid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, primary_key=True)
    user_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('users.uuid'), nullable=False)
    test_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('tests.uuid'), nullable=False)

    score = db.Column(REAL, default=0.0)
    max_score = db.Column(REAL, default=0.0)
    start_date = db.Column(db.DateTime())
    end_date = db.Column(db.DateTime())
    answered_questions_json =  db.Column(JSON)

    user = db.relationship('User', back_populates='test_results')
    test = db.relationship('Test', back_populates='users_results')

    def __init__(self, name, description_template):
        self.name = name
        self.description_template = description_template

    def __repr__(self):
        return '< QuestionType: name {}>'.format(self.name)

    @classmethod
    def find_by_name(cls, question_type):
        return cls.query.filter_by(name=question_type).first()

    @classmethod
    def isExist(cls, question_type):
        return True if cls.query.filter_by(name=question_type).first() else False

    def serialize(self):
        return {
            'uuid': self.uuid,
            'name': self.name,
            'description_template': self.description_template
        }

# class LectureContent(db.Model):
#     __tablename__ = 'lecture_content'
#     uuid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, primary_key=True)
#     content = db.Column(TEXT, nullable=False)
#
#     def __repr__(self):
#         return f"LectureContent('{self.content}')"

class Lecture(db.Model):
    __tablename__ = 'lectures'
    uuid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    course_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('courses.uuid'), nullable=False)
    course = db.relationship('Course', backref=db.backref('lectures', lazy=True))
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    start_date = db.Column(db.DateTime())
    end_date = db.Column(db.DateTime())
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.utcnow)
    creator = db.relationship("User", back_populates="lectures")
    # content_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('lecture_content.uuid'), nullable=False)
    # content = db.relationship('LectureContent', backref=db.backref('lectures', lazy=True))
    content_url = db.Column(db.String(500))

    def __repr__(self):
        return f"Lecture('{self.name}', '{self.description}')"

# class LectureImage(db.Model):
#     __tablename__ = 'lectures_images'
#     uuid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, primary_key=True)
#     lecture_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('lectures.uuid'), nullable=False)
#     lecture = db.relationship('Lecture', backref=db.backref('images', lazy=True))
#     file_name = db.Column(db.String(100), nullable=False)
#     file_path = db.Column(db.String(100), nullable=False)
#
#     def __repr__(self):
#         return f"LectureImage('{self.file_name}', '{self.file_path}')"