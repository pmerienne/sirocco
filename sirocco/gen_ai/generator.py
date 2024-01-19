from typing import Literal

from sirocco.model import Course
from sirocco.gen_ai import llm
from sirocco.gen_ai.parser import JSONArrayOutputParser


async def generate_info(course: Course, field_name: Literal["name", "description", "topics"]) -> list | str:
    course_description = "\n".join([
        f"- {available_field_name}: {getattr(course, available_field_name)}"
        for available_field_name in ['name', 'description', 'topics']
        if available_field_name != field_name and getattr(course, available_field_name)
    ])

    output_parser = None
    format_instructions = ''
    if field_name == 'topics':
        output_parser = JSONArrayOutputParser(example='["topic1", "topic2", "topic3", "topic4"]')
        format_instructions = output_parser.get_format_instructions()

    task = {
        'name': 'Generate a concise and engaging name',
        'description': 'Generate an engaging description for this course (500-1000 characters)',
        'topics': 'Generate a list of 5-10 tags for this course',  # (should be single word key topics)
    }[field_name]

    prompt = f"""
    [INST]
    Act as an assistant to kickstart the creation of a new online course.
    Your task : {task}
    
    Use the following information:
    {course_description}
    
    Use language: french
    {format_instructions}
    [/INST]
    """

    response = await llm.instruct(prompt)
    if output_parser:
        response = output_parser.parse(response)  # type: ignore
    else:
        response = response.strip().strip('"')

    return response


async def generate_chapters_titles(course: Course) -> list[str]:
    course_info = "\n".join([
        f"- {available_field_name}: {getattr(course, available_field_name)}"
        for available_field_name in ['name', 'description', 'topics']
    ])

    output_parser = JSONArrayOutputParser(example='["Header title 1", "Header title 2", "Header title 3"]')
    format_instructions = output_parser.get_format_instructions()

    prompt = f"""
    [INST]
    Act as an assistant to kickstart the creation of a new online course.
    Generate 5-7 chapter titles for the new course.
    
    Use the following course information:
    {course_info}
    
    Use language: french
    {format_instructions}
    [/INST]
    """

    response = await llm.instruct(prompt)
    titles = output_parser.parse(response)

    return titles


async def regenerate_chapter(course: Course, chapter_index: int):
    course_info = "\n".join([
        f"- {available_field_name}: {getattr(course, available_field_name)}"
        for available_field_name in ['name', 'description', 'topics']
    ])

    chapter_titles = "\n".join([
        f"{index}. {chapter.title}" if index != chapter_index else f"{index}. ???"
        for index, chapter in enumerate(course.chapters)
    ])

    prompt = f"""
    [INST]
    Act as an assistant to kickstart the creation of a new online course.
    Generate a title for the chapter no. {chapter_index}
    
    Use the following course information:
    {course_info}
    
    The existing chapters:
    {chapter_titles}
    
    Use language: french
    Don't prefix the title with the chapter index
    [/INST]
    """

    title = await llm.instruct(prompt)
    title = title.strip().strip('"')

    return title


async def generate_chapter_structure(course: Course, chapter_index: int, nb_headers: int = 7):
    chapter = course.chapters[chapter_index]
    chapter_title = chapter.title
    course_info = f"-name: {course.name}"
    course_chapters = "\n".join([
        f"{index}. {chapter.title}"
        for index, chapter in enumerate(course.chapters)
    ])

    output_parser = JSONArrayOutputParser(example='["header 1", "header 2", "header 3"]')
    format_instructions = output_parser.get_format_instructions()

    prompt = f"""
    [INST]
    Act as an assistant to help writing an online course chapter.
    Generate {nb_headers} headers for the chapter no. {chapter_index} named "{chapter_title}".
    
    Course information:    
    {course_info}
    
    Course chapters:
    {course_chapters}
    
    Current chapter:
    {chapter_title}
    
    Use language: french
    Don't prefix the header with the header index
    {format_instructions}
    [/INST]
    """

    response = await llm.instruct(prompt)
    headers = output_parser.parse(response)

    return headers


async def generate_chapter_paragraph(course: Course, chapter_index: int, header_index: int):
    chapter = course.chapters[chapter_index]
    header = chapter.blocks[header_index]

    chapter_headers = '\n'.join([
        f"- {header}"
        for index, header in enumerate(chapter.headers)
    ])

    prompt = f"""
    [INST]
    Act as an assistant to help writing an online course.
    Task: Write down the content of a new paragraph.
    
    Information:
    - Course: {course.name}
    - Chapter: {chapter.title}
    
    Chapter headers:
    {chapter_headers}
    
    Output format:
    - Use language: french
    - Write only a single paragraph for the header named "{header.text}"
    [/INST]
    """

    content = await llm.instruct(prompt)
    content = content.strip().strip('"')

    return content
