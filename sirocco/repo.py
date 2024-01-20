import os
from typing import Mapping

import chromadb
from loguru import logger

from sirocco.model import Course

db_path = os.getenv('DB_PATH')
if db_path:
    logger.info(f'Loading DB from {db_path}')
    client = chromadb.PersistentClient(path=db_path)
else:
    client = chromadb.Client()

courses = client.get_or_create_collection(name="courses")


def find_all(limit: int = 10) -> list[Course]:
    results = courses.peek(limit)
    metadatas = results.get('metadatas') or []

    return [
        _load_from_metadata(metadata)
        for metadata in metadatas
    ]


def _load_from_metadata(metadata: Mapping) -> Course:
    raw = metadata['raw_json']
    course = Course.model_validate_json(raw)
    return course


def get_by_id(course_id: str) -> Course:
    result = courses.get(ids=[course_id])

    metadatas = result['metadatas']
    if not metadatas:
        raise RuntimeError(f'No course found with id {course_id}')

    course = _load_from_metadata(metadatas[0])
    return course


def save(course: Course) -> Course:
    courses.upsert(
        ids=[course.id],
        documents=[course.contents],
        metadatas=[course.metadata]
    )

    return course


def delete_all():
    global courses
    client.reset()
    courses = client.get_or_create_collection(name="courses")
