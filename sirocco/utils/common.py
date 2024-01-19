from typing import Optional
from uuid import uuid4


def uuid() -> str:
    return str(uuid4())


def require(condition: bool, message: Optional[str] = None, exception: Optional[BaseException] = None):
    if not condition:
        exception = exception or RequirementError(message)
        raise exception


class RequirementError(Exception):
    pass
