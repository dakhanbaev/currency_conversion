# pylint: disable=too-few-public-methods
from dataclasses import dataclass
from typing import Union


class Command:
    pass


class Task:
    pass


@dataclass
class DeleteAnalyse(Command):
    request_id: str


@dataclass
class SaveAnalyse(Task):
    request_id: str
    file_path: str
    file_content_type: str


class Event:
    pass


@dataclass
class CheckEvent(Event):
    pass


Message = Union[Event, Command, Task]
