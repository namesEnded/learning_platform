from flask import Flask, session
from database import db
from models import Course, Menu, User, Role, Group
from app import app, page_fs, mongo
import io

def populate_db():
    with app.app_context():
        # uuid = "123"
        # page_number = "page-0"
        # # получаем контент страницы из запроса
        # content ="content"
        # # сохраняем контент страницы в GridFS
        #
        # html_string = "<html><head><title>Example</title></head><body><h1>Hello, world!</h1></body></html>"
        #
        # with io.StringIO(html_string) as f:
        #     file_id = page_fs.put(f.read().encode('utf-8'), filename=page_number, content_type='text/html')
        #
        # # mongo.lectures.update_one({'uuid': uuid},
        # #                           {'$push': {'pages': {'page_number': page_number, 'file_id': file_id}}}, upsert=True)
        # # mongo.lectures.update_one({'uuid': uuid},
        # #                           {'$addToSet': {'pages': {page_number: file_id}}}, upsert=True)
        # mongo.lectures.update_one({'uuid': uuid}, {'$set': {f'pages.{page_number}': file_id}}, upsert=True)
        class Lecture:
            def __init__(self, uuid):
                lecture = mongo.lectures.find_one({'uuid': uuid})
                if lecture:
                    self.uuid = uuid
                else:
                    self.uuid = uuid
                    mongo.lectures.insert_one({'uuid': uuid, 'pages': {}})

            def delete_page(self, page_number: str):
                mongo.lectures.update_one({'uuid': self.uuid}, {'$unset': {f'pages.{page_number}': ''}})

            def update_page_content(self, page_number: str, new_content: str):
                file_id = mongo.lectures.find_one({'uuid': self.uuid}, {'pages': 1})['pages'].get(page_number)
                if file_id:
                    with io.StringIO(new_content) as f:
                        page_fs.delete(file_id)  # удаление старого файла
                        file_id = page_fs.put(f.read().encode('utf-8'), filename=page_number,
                                              content_type='text/html')  # создание нового файла
                    mongo.lectures.update_one({'uuid': self.uuid}, {'$set': {f'pages.{page_number}': file_id}},
                                              upsert=True)  # обновление ссылки на файл в коллекции

            def get_page_content(self, page_number: str) -> str:
                file_id = mongo.lectures.find_one({'uuid': self.uuid}, {'pages': 1})['pages'].get(page_number)
                if file_id:
                    return page_fs.get(file_id).read().decode('utf-8')
                else:
                    return ''

            def create_page(self, page_number: str, content: str):
                with io.StringIO(content) as f:
                    file_id = page_fs.put(f.read().encode('utf-8'), filename=page_number, content_type='text/html')
                mongo.lectures.update_one({'uuid': self.uuid}, {'$set': {f'pages.{page_number}': file_id}}, upsert=True)

        new_lecture = Lecture('123')
        page_number = 'page-1'
        # new_content = '<h1>Новый заголовок</h1><p>Это новый текст на странице 2</p>'
        # new_lecture.create_page(page_number, new_content)
        print(new_lecture.get_page_content(page_number))
        # страница создана, теперь ее содержимое можно обновить так:
        updated_content = '<h1>Обновленный заголовок</h1><p>Это обновленный текст на странице 2</p>'
        new_lecture.update_page_content(page_number, updated_content)
        print(new_lecture .get_page_content(page_number))

if __name__ == '__main__':
    print('Populating db...')
    populate_db()
    print('Successfully populated!')
