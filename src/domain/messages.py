# pylint: disable=too-few-public-methods
from dataclasses import dataclass
from typing import Union
from fastapi import UploadFile
import typing


class Command:
    pass


class Task:
    pass


@dataclass
class DeleteAnalyse(Task):
    requestId: str


@dataclass
class SaveAnalyse(Command):
    file: UploadFile


class Event:
    pass


@dataclass
class CheckEvent(Event):
    pass


Message = Union[Event, Command, Task]
