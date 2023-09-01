from abc import ABC
from redis import Redis
from utils.log_handler import logger
from utils.custom_wrapper import deserialize


class BaseRedisClient(Redis, ABC):
    """redis单节点"""

    def __init__(self, *args, **kwargs):
        logger.info(f"BaseRedisClient INIT: {args}  {kwargs}")
        super().__init__(*args, **kwargs)

    def switch_db(self, db_index: int):
        """
        切换db
        """
        logger.info(f"redis切换db > {db_index}")
        super().select(db_index)

    def hgetall(self, name: str):
        """
        :param name: redis key name
        """
        return super().hgetall(name)

    @deserialize
    def hget(self, name: str, key: str):
        """
        :param name: redis key name
        :param key: hash key name
        """
        return super().hget(name, key)

    @deserialize
    def get(self, name):
        """
        :param name: redis key name
        """
        return super().get(name)

