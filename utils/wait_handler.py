# -*- coding: utf-8 -*-
import time
from utils.log_handler import logger as log


def until(try_times, gap):
    """等待装饰器，运行等待时间，func返回值为真或超过重试次数时退出

    :param int try_times: 运行次数
    :param int gap: 每次等待时间
    """

    def wrapper(func):
        def inner(*args, **kwargs):
            result = False
            for i in range(try_times):
                result = func(*args, **kwargs)
                log.info(f"{func.__name__}执行了:{i + 1}")
                if result:
                    return result
                else:
                    time.sleep(gap)
            return result
        return inner
    return wrapper


def until_false(try_times, gap):
    """等待装饰器，运行等待时间，func返回值为假时退出

    :param int try_times: 运行次数
    :param int gap: 每次等待时间
    """

    def wrapper(func):
        def inner(*args, **kwargs):
            result = True
            for i in range(try_times):
                result = func(*args, **kwargs)
                log.info(f"{func.__name__}执行了:{i + 1}")
                if result:
                    time.sleep(gap)
                else:
                    return result
            return result
        return inner
    return wrapper
