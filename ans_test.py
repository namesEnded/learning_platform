from flask import Flask, session
from database import db
from datetime import datetime
from models import Course, Menu, User, Role, Group, Subject, Test, Question, Answer, AssessmentType,QuestionType, DifficultyLevel
from app import app

def search_db():
    with app.app_context():
        with app.app_context():
            q = Test.find_test_by_name("Математический тест").questions
            a = list(filter(lambda p: p.uuid == '0e766fc2-fe1f-4e43-99b6-7f11e2aacf53', q))
            print(q)

if __name__ == '__main__':
    print('Searching in db...')
    search_db()
    print('Successfully!')
