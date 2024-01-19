from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sirocco import repo
from sirocco.gen_ai import generator
from sirocco.model import Course, Document
from sirocco.utils.common import require

api = FastAPI()
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.post("/courses/")
async def create() -> Course:
    course = Course()
    repo.create(course)
    return course


@api.get("/courses/")
async def find_all() -> list[Course]:
    courses = repo.find_all()
    return courses


@api.get("/courses/{course_id}")
async def get_by_id(course_id: int) -> Course:
    course = repo.get_by_id(course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@api.put("/courses/{course_id}")
async def update(course_id: str, course: Course) -> Course:
    repo.save(course)
    return course


@api.put("/courses/{course_id}/info/{field_name}")
async def update_info(course_id: int, field_name: Literal["name", "description", "topics"]) -> Course:
    course = repo.get_by_id(course_id)

    info = await generator.generate_info(course, field_name)
    setattr(course, field_name, info)

    repo.save(course)
    return course


@api.post("//courses{course_id}/chapters")
async def create_chapter(course_id: int) -> Course:
    course = repo.get_by_id(course_id)

    chapter = Document(title=f"Chapter {len(course.chapters) + 1}")
    course.chapters.append(chapter)

    repo.save(course)
    return course


@api.put("/courses/{course_id}/chapters")
async def generate_chapters(course_id: int) -> Course:
    course = repo.get_by_id(course_id)

    titles = await generator.generate_chapters_titles(course)
    for title in titles:
        chapter = Document(title=title)
        course.chapters.append(chapter)

    repo.save(course)
    return course


@api.put("/courses/{course_id}/chapters/{chapter_index}")
async def regenerate_chapter(course_id: int, chapter_index: int) -> Course:
    course = repo.get_by_id(course_id)

    title = await generator.regenerate_chapter(course, chapter_index)
    chapter = Document(title=title)
    course.chapters[chapter_index] = chapter

    repo.save(course)
    return course


@api.put("/courses/{course_id}/chapters/{chapter_index}/structure")
async def generate_chapter_structure(course_id: int, chapter_index: int) -> Course:
    course = repo.get_by_id(course_id)
    chapter = course.chapters[chapter_index]

    headers = await generator.generate_chapter_structure(course, chapter_index)
    chapter.clear_blocks()
    for header in headers:
        chapter.add_header(header)

    repo.save(course)
    return course


@api.put("/courses/{course_id}/chapters/{chapter_index}/paragraph/{header_index}")
async def generate_chapter_paragraph(course_id: int, chapter_index: int, header_index: int) -> Course:
    course = repo.get_by_id(course_id)
    chapter = course.chapters[chapter_index]

    content = await generator.generate_chapter_paragraph(course, chapter_index, header_index)
    chapter.insert_paragraph(header_index + 1, content)

    repo.save(course)
    return course
