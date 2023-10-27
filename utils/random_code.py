# -*- coding: utf-8 -*-
import datetime
import random
import string
from utils.log_handler import logger


class RandomCode(object):
    """随机编码生成规则，后缀的随机字符范围包括数字和大小写字母"""
    RANDOM_RANGE = string.ascii_letters + string.digits

    def __init__(self, prefix, suffix_length, name=None):
        """
        :param str prefix: 前缀，固定
        :param int suffix_length: 后缀长度，程序生成随机值
        :param str name: 编码名称，仅用于日志记录
        """
        self.prefix = prefix
        self.suffix_length = suffix_length
        self.name = name

    def generate(self, count):
        """生成指定数量随机编码

        :param int count: 生成的随机随码数量
        :rtype: list[str]
        """
        code_list = [
            self.prefix + ''.join(
                random.choices(
                    self.RANDOM_RANGE,
                    k=self.suffix_length
                )
            )
            for _ in range(count)
        ]
        if self.name:
            logger.debug(f"生成【{self.name}】编码：{code_list}")
        return code_list

    def generate_one(self):
        """生成1个随机编码

        :rtype: str
        """
        code_list = self.generate(1)
        return code_list[0]


class NumberRandomCode(RandomCode):
    """后缀的随机字符范围只有数字0~9"""
    RANDOM_RANGE = string.digits


class LetterRandomCode(RandomCode):
    """后缀的随机字符范围只有大写字母和小写字母"""
    RANDOM_RANGE = string.ascii_letters


class UpperLetterRandomCode(RandomCode):
    """后缀的随机字符范围只有大写字母"""
    RANDOM_RANGE = string.ascii_uppercase


class LowerLetterRandomCode(RandomCode):
    """后缀的随机字符范围只有小写字母"""
    RANDOM_RANGE = string.ascii_lowercase


def get_random_code(
        prefix, suffix_length,
        count=1, name=None, random_cls=RandomCode
):
    """生成随机编码

    :param str prefix: 前缀，固定
    :param int suffix_length: 后缀长度，程序生成随机值
    :param int count: 生成的随机编码数量
    :param str name: 编码名称，仅用于日志记录
    :param type random_cls: 编码规则类，用于指定后缀随机字符的范围，默认为数字加大小写字符
    :rtype: str | list[str]
    """
    code_list = random_cls(prefix, suffix_length, name).generate(count)
    if len(code_list) == 1:
        return code_list[0]
    else:
        return code_list


def get_number_random_code(prefix, suffix_length, count=1, name=None):
    """生成随机编码，后缀的随机字符范围只有数字0

    :param str prefix: 前缀，固定
    :param int suffix_length: 后缀长度，程序生成随机值
    :param int count: 生成的随机编码数量
    :param str name: 编码名称，仅用于日志记录
    :rtype: str | list[str]
    """
    return get_random_code(
        prefix, suffix_length, count, name,
        random_cls=NumberRandomCode
    )


def get_letter_random_code(prefix, suffix_length, count=1, name=None):
    """生成随机编码，后缀的随机字符范围只有大写字母和小写字母

    :param str prefix: 前缀，固定
    :param int suffix_length: 后缀长度，程序生成随机值
    :param int count: 生成的随机编码数量
    :param str name: 编码名称，仅用于日志记录
    :rtype: str | list[str]
    """
    return get_random_code(
        prefix, suffix_length, count, name,
        random_cls=LetterRandomCode
    )


def get_upper_random_code(prefix, suffix_length, count=1, name=None):
    """生成随机编码，后缀的随机字符范围只有大写字母

    :param str prefix: 前缀，固定
    :param int suffix_length: 后缀长度，程序生成随机值
    :param int count: 生成的随机编码数量
    :param str name: 编码名称，仅用于日志记录
    :rtype: str | list[str]
    """
    return get_random_code(
        prefix, suffix_length, count, name,
        random_cls=UpperLetterRandomCode
    )


def get_lower_random_code(prefix, suffix_length, count=1, name=None):
    """生成随机编码，后缀的随机字符范围只有小写字母

    :param str prefix: 前缀，固定
    :param int suffix_length: 后缀长度，程序生成随机值
    :param int count: 生成的随机编码数量
    :param str name: 编码名称，仅用于日志记录
    :rtype: str | list[str]
    """
    return get_random_code(
        prefix, suffix_length, count, name,
        random_cls=LowerLetterRandomCode
    )


def get_random_times(start, end, frmt="%Y-%m-%d %H:%M:%S"):
    start, end = sorted((start, end))
    stime = datetime.datetime.strptime(start, frmt)
    etime = datetime.datetime.strptime(end, frmt)
    return random.random() * (etime - stime) + stime
