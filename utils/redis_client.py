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
        操作string类型，获取值
        :param name: redis key name
        """
        return super().get(name)

    def set(self, name, value, **kwargs):
        """
        操作string类型，写入值
        :param name: redis key name
        :param value: 值
        """
        return super().set(name, value, **kwargs)

    def smembers(self, name: str):
        """
        获取set类型数据
        :param name: redis key name
        """
        return super().smembers(name)

    def sismember(self, name: str, value: str):
        """
        判断某个值是否存在set
        :param name: redis key name
        :param value: redis key value
        """
        return super().sismember(name, value)

    def sadd(self, name: str, *values):
        """
        add to a set
        :param name: redis key name
        :param values: value
        """
        return super().sadd(name, *values)

    def srem(self, name:str, *values):
        """
        remove from a set
        :param name: redis key name
        :param values: value
        """
        return super().srem(name, *values)

    def delete(self, name):
        """
        删除 key
        :param name: redis key name
        """
        return super().delete(name)

    def hdel(self, name, *keys):
        """
        删除 hash key
        :param name: redis key name
        :param keys: hash key
        """
        return super().hdel(name, *keys)



