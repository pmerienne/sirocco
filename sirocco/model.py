from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from sirocco.utils.common import uuid


class DocumentBlock(BaseModel):
    id: str = Field(default_factory=uuid)
    type: str
    data: dict = Field(default_factory=dict)

    @property
    def text(self):
        return self.data.get('text', '')

    @text.setter
    def text(self, value):
        self.data['text'] = value


class Document(BaseModel):
    id: str = Field(default_factory=uuid)
    title: str
    description: str = ''
    color: str = 'blue'
    icon: str = 'mdi-clipboard-text'
    blocks: list[DocumentBlock] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)

    @property
    def headers(self) -> list[str]:
        return [
            block.data.get('text', '')
            for block in self.blocks
            if block.type == 'header'
        ]

    def add_header(self, header: str):
        self.blocks.append(DocumentBlock(type='header', data={"text": header}))

    def insert_paragraph(self, index: int, content: str = '') -> DocumentBlock:
        block = DocumentBlock(type='paragraph', data={"text": content})
        self.blocks.insert(index, block)
        return block

    def clear_blocks(self):
        self.blocks = []


class Course(BaseModel):
    id: Optional[int] = None
    # TODO: document <- Syllabus
    name: str = "Maîtriser les bases de données NoSQL"
    description: str = ""
    topics: list[str] = ["Base de données", "NoSQL", "CAP", "MongoDB", "Cassandra", "Redis"]
    # requirements: list[str] = Field(default_factory=list)  # Requirements
    # learning_objectives: list[str] = Field(default_factory=list)  # What you'll learn ?
    # target_audience: str = ""  # Who this course is for?
    chapters: list[Document] = Field(default_factory=list)

    created_at: datetime = Field(default_factory=datetime.now)


