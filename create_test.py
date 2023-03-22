from flask import Flask, session
from database import db
from datetime import datetime
from models import Course, Menu, User, Role, Group, Subject, Test, Question, Answer, AssessmentType,QuestionType, DifficultyLevel
from app import app

def populate_db():
    with app.app_context():
        bufUser = User.find_user_by_username("GLOBAL")
        db.session.add(bufUser)

        # Создание AssessmentType
        assessment_type1 = AssessmentType(name='Лучшая оценка', description='Лучшая оценка')
        assessment_type2 = AssessmentType(name='Средняя оценка ', description='Средняя оценка')
        db.session.add(assessment_type1)
        db.session.add(assessment_type2)

        # Создание типа вопроса
        question_type1 = QuestionType(name='Одиночный выбор', description_template='Выберите правильный ответ')
        question_type2 = QuestionType(name='Множественный выбор', description_template='Выберите все правильные ответы')
        question_type3 = QuestionType(name='Ответ в свободной форме', description_template='Введите ответ в свободной форме')
        db.session.add(question_type1)
        db.session.add(question_type2)
        db.session.add(question_type3)

        # Создание уровней сложности
        difficulty_level1 = DifficultyLevel(name='Легкий', description_template='')
        difficulty_level2 = DifficultyLevel(name='Средний', description_template='')
        difficulty_level3 = DifficultyLevel(name='Тяжелый', description_template='')
        db.session.add(difficulty_level1)
        db.session.add(difficulty_level2)
        db.session.add(difficulty_level3)
        db.session.commit()

        # Создание теста
        test = Test(name='Математический тест',
                    description='Тест на знание математики',
                    creator_uuid=bufUser.uuid,
                    assessment_type_uuid=assessment_type1.uuid,
                    duration=60,
                    passing_score=70,
                    number_of_questions=10,
                    attempts=3,
                    randomize_questions=False,
                    randomize_answers=True,
                    is_active=True,
                    show_result=True,
                    multiply_view=False,
                    time_expired_questions=False,
                    start_date=datetime.now(),
                    end_date=datetime.now()
                    )
        db.session.add(test)

        # Создание вопросов для теста
        question1 = Question(content='Какое число является простым?',
                             weight=1.0,
                             description="1",
                             expiration_time=0.0,
                             type_uuid=question_type1.uuid,
                             creator_uuid=bufUser.uuid,
                             moderator_uuid=bufUser.uuid,
                             difficulty_level_uuid=difficulty_level1.uuid )

        question2 = Question(content='Решите уравнение 2x + 5 = 13',
                             weight=2.0,
                             description="2",
                             expiration_time=0.0,
                             type_uuid=question_type2.uuid,
                             creator_uuid=bufUser.uuid,
                             moderator_uuid=bufUser.uuid,
                             difficulty_level_uuid=difficulty_level2.uuid)
        question3 = Question(content='Найдите площадь треугольника со сторонами 3, 4 и 5',
                             weight=3.0,
                             expiration_time=0.0,
                             description="3",
                             type_uuid=question_type3.uuid,
                             creator_uuid=bufUser.uuid,
                             moderator_uuid=bufUser.uuid,
                             difficulty_level_uuid=difficulty_level3.uuid)

        # Добавление вопросов в тест
        test.questions.append(question1)
        test.questions.append(question2)
        test.questions.append(question3)

        # Создание ответов для вопросов
        answer1_q1 = Answer(name='17',
                            content='17',
                            is_correct=True)
        answer2_q1 = Answer(name='23',
                            content='23',
                            is_correct=False)
        answer3_q1 = Answer(name='31',
                            content='31',
                            is_correct=False)
        answer1_q2 = Answer(name='4',
                            content='4',
                            is_correct=True)
        answer2_q2 = Answer(name='5',
                            content='5',
                            is_correct=False)
        answer3_q2 = Answer(name='6',
                            content='6',
                            is_correct=False)
        answer1_q3 = Answer(name='6',
                            content='6',
                            is_correct=True)
        answer2_q3 = Answer(name='8',
                            content='8',
                            is_correct=False)
        answer3_q3 = Answer(name='10',
                            content='10',
                            is_correct=False)

        # Добавление ответов к вопросам
        question1.answers.append(answer1_q1)
        question1.answers.append(answer2_q1)
        question1.answers.append(answer3_q1)
        question2.answers.append(answer1_q2)
        question2.answers.append(answer2_q2)
        question2.answers.append(answer3_q2)
        question3.answers.append(answer1_q3)
        question3.answers.append(answer2_q3)
        question3.answers.append(answer3_q3)

        # Сохранение изменений
        db.session.commit()
        db.session.close()


if __name__ == '__main__':
    print('Populating db...')
    populate_db()
    print('Successfully populated!')