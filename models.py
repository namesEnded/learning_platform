from datetime import datetime

from database import db


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    review = db.Column(db.String(300), nullable=False)
    text_content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, title, review, text_content, author):
        self.title = title
        self.review = review
        self.text_content = text_content
        self.author = author

    def __repr__(self):
        return '< Course saved: id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'review': self.review,
            'text_content': self.text_content,
            'date_added': self.date_added,
            'author': self.author
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


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=True)
    password = db.Column(db.String(300), nullable=False)
    e_mail = db.Column(db.String(300), unique=True, nullable=False)
    courses = db.relationship('Course', backref='author', lazy='dynamic')

    def __init__(self, name, role, password, e_mail):
        self.name = name
        self.role = role
        self.password = password
        self.e_mail = e_mail

    def __repr__(self):
        return '< Saved user:e_mail: e_mail {}>'.format(self.e_mail)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'role': self.role,
            'password': self.password,
            'e_mail': self.e_mail,
        }


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    users = db.relationship('User', backref='users', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '< Saved role: name {}>'.format(self.name)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }
