import os
from typing import Optional

from fastapi.encoders import jsonable_encoder
from loguru import logger
from tinydb import TinyDB

from sirocco.model import Course

tiny_db_path = os.getenv('TINY_DB_PATH')
logger.info(f'Loading TinyDB from {tiny_db_path}')

db = TinyDB(tiny_db_path)
courses = db.table('courses')


def find_all() -> list[Course]:
    return [
        Course(**raw)
        for raw in courses.all()
    ]


def get_by_id(course_id: int) -> Course:
    raw = courses.get(doc_id=course_id)
    if raw is None:
        raise RuntimeError(f'No course found with id {course_id}')
    return Course(**raw)  # type: ignore


def create(course: Course) -> Course:
    raw = jsonable_encoder(course)
    doc_id = courses.insert(raw)
    course.id = doc_id
    save(course)  # TODO: I need this in order to properly save the "id" field !
    return course


def save(course: Course) -> Course:
    raw: dict = jsonable_encoder(course)
    courses.update(raw, doc_ids=[course.id])  # type: ignore
    return course


def truncate():
    courses.truncate()
