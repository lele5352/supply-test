import json

from redis import Redis
from utils.log_handler import logger

def do_json_load():
    def wrapper(func):
        def inner(is_load=True, *args, **kwargs):
            data = func(*args, **kwargs)
            if is_load and data:
                return json.loads(data)

            return data
        return inner

    return wrapper


class BaseRedisClient(Redis):
    """redis单节点"""

    def __init__(self, *args, **kwargs):
        logger.info(f"BaseRedisClient INIT: {args}  {kwargs}")
        super().__init__(*args, **kwargs)

    def switch_db(self, db_index: int):
        """
        切换db
        """
        logger.info(f"切换db到 {db_index}")
        super().select(db_index)

    def hgetall(self, name: str):
        """
        :param name: redis key name
        """
        return super().hgetall(name)

    @do_json_load
    def hget(self, name: str, key: str, return_dict=True):
        """
        :param name: redis key name
        :param key: hash key name
        :param return_dict: 是否以字典形式返回，默认 True
        """
        data = super().hget(name, key)

        return json.loads(data) if data and return_dict else data

    def get(self, name, return_dict=True):
