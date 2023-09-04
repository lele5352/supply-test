# -*- coding: utf-8 -*-
import time
from functools import wraps
import jsonpath_rw_ext as jsre
from utils.log_handler import logger as log
from threading import Thread
import json


def until(try_times: int, gap: [int, float]):
    """等待装饰器，运行等待时间，func返回值为真或超过重试次数时退出

    :param int try_times: 运行次数
    :param int,float gap: 每次等待时间，单位秒，可以是整数或浮点数
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


def until_false(try_times: int, gap: [int, float]):
    """等待装饰器，运行等待时间，func返回值为假时退出

    :param int try_times: 运行次数
    :param int,flaat gap: 每次等待时间，单位秒，可以是整数或浮点数
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


def deserialize(func):

    """装饰器，反序列化字符串"""

    @wraps(func)
    def wrapper(*args, **kwargs):

        data = func(*args, **kwargs)
        log.debug(f"{func.__name__} returned: {data}")

        if data:
            try:
                # 去除转义字符
                data = json.loads(data)
                # 二次转换
                if isinstance(data, str):
                    data = json.loads(data)

            except json.JSONDecodeError:
                log.error("JSON decoding failed")

        return data

    return wrapper


def async_call(func):
    """装饰器，异步线程执行"""
    def wrapper(*args, **kwargs):
        Thread(target=func, args=args, kwargs=kwargs).start()

    return wrapper


def extract_json(json_path):
    """
    装饰器，接收一个 json path 字符串，提取指定的值
    可用于通用的接口返回，提取结果
    被装饰的函数必须保证返回结果是可以被 json.loads() 解析的有效 JSON 数据类型
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 执行被装饰的函数
            result = func(*args, **kwargs)
            log.debug(f"{func.__name__} returned: {result}")

            try:
                # 使用 jsonpath_rw_ext 解析 JSON path
                jsonpath_expr = jsre.parse(json_path)
                matches = [match.value for match in jsonpath_expr.find(result)]

                if not matches:
                    log.debug(f"No match found for JSON path: {json_path}")

                return matches[0] if len(matches) == 1 else matches

            except Exception as e:
                raise ValueError(f"Failed to extract JSON path '{json_path}': {str(e)}")

        return wrapper

    return decorator







