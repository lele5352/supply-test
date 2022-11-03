import inspect


class ApiConfig:
    @classmethod
    def get_attributes(cls):
        attributes = inspect.getmembers(cls, predicate=lambda a: not (inspect.isroutine(a)))
        return {d[0]: d[1] for d in attributes if not (d[0].startswith('__') and d[0].endswith('__'))}
