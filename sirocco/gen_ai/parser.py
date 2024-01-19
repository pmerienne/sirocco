import json
import logging
from json import JSONDecodeError
from typing import Optional

from pydantic import BaseModel


class GenAIOutputParser(BaseModel):
    def parse(self, raw_json: str):
        raise NotImplementedError()

    def get_format_instructions(self) -> str:
        raise NotImplementedError()


class JSONArrayOutputParser(GenAIOutputParser):
    example: Optional[str] = None

    def parse(self, raw_json: str) -> list[str]:
        try:
            result = json.loads(raw_json)
            return result
        except JSONDecodeError as e:
            logging.error(f'Could not load json:\n{raw_json}')
            raise e

    def get_format_instructions(self) -> str:
        example = f"e.g. {self.example}" if self.example else ""
        return f"Format your response as a JSON array\n{example}"

    @property
    def _type(self) -> str:
        return "json_array_output_parser"
