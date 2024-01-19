import pytest
from loguru import logger

from sirocco.gen_ai import generator
from sirocco.model import Course, Document, DocumentBlock


@pytest.mark.asyncio
async def test_generate_info_name():
    course = Course(name='', topics=['NoSQL', 'CAP', 'Redis', 'MongoDB', 'Cassandra'])
    name = await generator.generate_info(course, 'name')
    logger.info(f'Name: {name}')
    assert len(name) > 0


@pytest.mark.asyncio
async def test_generate_info_description():
    course = Course(name='Getting started with NoSQL databases')
    description = await generator.generate_info(course, 'description')
    logger.info(f'Description: {description}')
    assert len(description) > 0


@pytest.mark.asyncio
async def test_generate_info_topics():
    course = Course(name='Getting started with NoSQL databases')
    topics = await generator.generate_info(course, 'topics')
    logger.info(f'Topics: {topics}')
    assert len(topics) > 0


@pytest.mark.asyncio
async def test_generate_chapters_titles():
    course = Course(name="Maîtrisez les bases de données NoSQL", topics=['NoSQL', 'DataBase', 'MongoDb', 'Redis', 'Cassandra'])
    titles = await generator.generate_chapters_titles(course)
    logger.info(f'Titles: {titles}')
    assert len(titles) > 0


@pytest.mark.asyncio
async def test_regenerate_chapter():
    course = Course(name="Maîtrisez les bases de données NoSQL", description='', topics=['NoSQL', 'DataBase', 'MongoDb', 'Redis', 'Cassandra'])
    course.chapters.append(Document(title='Introduction aux bases de données NoSQL'))
    course.chapters.append(Document(title='Les grandes familles de base de données NoSQL'))
    course.chapters.append(Document(title='Redis, une base de données "in-memory"'))
    course.chapters.append(Document(title='MongoDb, une base de données orientée document'))
    course.chapters.append(Document(title='Cassandra, une base de données orientée colonne'))

    chapter = await generator.regenerate_chapter(course, 2)
    logger.info(f'Chapter: {chapter}')
    assert len(chapter) > 0


@pytest.mark.asyncio
async def test_generate_chapter_structure():
    course = Course(name="Maîtrisez les bases de données NoSQL", description='', topics=['NoSQL', 'DataBase', 'MongoDb', 'Redis', 'Cassandra'])
    course.chapters.append(Document(title='Introduction aux bases de données NoSQL'))
    course.chapters.append(Document(title='Les grandes familles de base de données NoSQL'))
    course.chapters.append(Document(title='Redis, une base de données "in-memory"'))
    course.chapters.append(Document(title='MongoDb, une base de données orientée document'))
    course.chapters.append(Document(title='Cassandra, une base de données orientée colonne'))

    headers = await generator.generate_chapter_structure(course, 2)  # Redis
    logger.info(f'Headers: {headers}')
    assert isinstance(headers, list)
    assert len(headers) > 0
    assert len(headers[0]) > 0


@pytest.mark.asyncio
async def test_generate_chapter_paragraph():
    course = Course(name="Maîtrisez les bases de données NoSQL", description='', topics=['NoSQL', 'DataBase', 'MongoDb', 'Redis', 'Cassandra'])
    course.chapters.append(Document(title='Introduction aux bases de données NoSQL'))
    course.chapters.append(Document(title='Les grandes familles de base de données NoSQL'))
    course.chapters.append(Document(
        title='Redis, une base de données "in-memory"',
        blocks=[
            DocumentBlock(type='header', data={"text": "Qu'est ce que Redis ?"}),
            DocumentBlock(type='header', data={"text": "Comment fonctionne Redis ?"}),
            DocumentBlock(type='header', data={"text": "Utiliser Redis avec python"}),
            DocumentBlock(type='header', data={"text": "Quand devez-vous utiliser Redis ?"}),
        ]
    ))
    course.chapters.append(Document(title='MongoDb, une base de données orientée document'))
    course.chapters.append(Document(title='Cassandra, une base de données orientée colonne'))

    content = await generator.generate_chapter_paragraph(course, 2, 2)
    logger.info(f'Content: {content}')
    assert len(content) > 0
