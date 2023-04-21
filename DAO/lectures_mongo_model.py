import json
from typing import Any, Optional

from mongo_conn import mongo, img_fs, page_fs
import io

class LectureMongo:
    def __init__(self, uuid):
        lecture = mongo.lectures.find_one({'uuid': uuid})
        if lecture:
            self.uuid = uuid
        else:
            self.uuid = uuid
            mongo.lectures.insert_one({'uuid': uuid, 'pages': {}})

    @staticmethod
    def find_by_uuid(uuid) -> Optional['LectureMongo']:
        if mongo.lectures.find_one({'uuid': uuid}):
            return LectureMongo(uuid)
        return None

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

    def get_page_content(self, page_number: str) -> Optional[str]:
        file_id = mongo.lectures.find_one({'uuid': self.uuid}, {'pages': 1})['pages'].get(page_number)
        if file_id:
            return page_fs.get(file_id).read().decode('utf-8')
        else:
            return None

    def create_page(self, page_number: str, content: str):
        with io.StringIO(content) as f:
            file_id = page_fs.put(f.read().encode('utf-8'), filename=page_number, content_type='text/html')
        mongo.lectures.update_one({'uuid': self.uuid}, {'$set': {f'pages.{page_number}': file_id}}, upsert=True)

    def get_all_pages(self):
        pages = mongo.lectures.find_one({'uuid': self.uuid}, {'pages': 1})['pages']
        result = {}
        for page_number, file_id in pages.items():
            content = page_fs.get(file_id).read().decode('utf-8')
            result[page_number] = content
        return result
