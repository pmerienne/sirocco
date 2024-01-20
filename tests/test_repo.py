import pytest

from sirocco.model import Course
from sirocco import repo


@pytest.fixture(autouse=True)
def reset_db():
    yield
    repo.delete_all()


def test_find_all():
    course_1 = Course(name="Course 1")
    repo.save(course_1)

    course_2 = Course(name="Course 2")
    repo.save(course_2)

    courses = repo.find_all()

    assert course_1 in courses
    assert course_2 in courses


def test_get_by_id():
    course = Course(name="Hello")
    repo.save(course)

    assert repo.get_by_id(course.id) == course
    with pytest.raises(RuntimeError):
        repo.get_by_id("42")


def test_save():
    course = Course(name="Hello")
    repo.save(course)

    course.name = 'New course name'
    repo.save(course)

    updated_course = repo.get_by_id(course.id)
    assert updated_course.name == 'New course name'
