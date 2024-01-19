import pytest

from sirocco.model import Course
from sirocco import repo


@pytest.fixture(autouse=True)
def truncate():
    yield
    repo.truncate()


def test_create():
    course = Course(name="Hello")
    repo.create(course)

    assert course.id is not None
    assert repo.get_by_id(course.id) == course


def test_find_all():
    course_1 = Course(name="Course 1")
    repo.create(course_1)

    course_2 = Course(name="Course 2")
    repo.create(course_2)

    courses = repo.find_all()

    assert course_1 in courses
    assert course_2 in courses


def test_get_by_id():
    course = Course(name="Hello")
    repo.create(course)

    assert repo.get_by_id(course.id) == course
    assert repo.get_by_id(42) is None


def test_save():
    course = Course(name="Hello")
    repo.create(course)

    course.name = 'New course name'
    repo.save(course)

    assert repo.get_by_id(course.id).name == 'New course name'
