import inspect
from enum import Enum


class ApiConfig:
    @classmethod
    def get_attributes(cls):
        attributes = inspect.getmembers(cls, predicate=lambda a: not (inspect.isroutine(a)))
        return {d[0]: d[1] for d in attributes if not (d[0].startswith('__') and d[0].endswith('__'))}


class BizEnum(Enum):
    def __new__(cls, value, description):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.description = description
        return obj