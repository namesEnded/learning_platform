
from datetime import datetime

from database import db


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    review = db.Column(db.String(300), nullable=False)
    text_content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(150), nullable=True)
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
            'author' : self.author
        }