"""
校验工具
"""
# -*- coding: utf-8 -*-
import inspect
from utils.log_handler import logger
from utils import transformer


def check_isinstance(arg, expected_type, arg_desc):
    """
    校验类型
    :param arg: 校验的参数
    :param expected_type: 预期类型
    :param arg_desc: 参数名称
    """
    if not isinstance(arg, expected_type):
        raise TypeError(f"Expected argument '{arg_desc}' of type {expected_type}, but got {type(arg)}")


class KeyNotFound(object):
    pass


def get_func_ident(func):
    """获取函数的标识

    :param function|Callable func: 函数
    :rtype str
    """
    if func.__name__ == '<lambda>':
        src = inspect.getsource(func)
        return src.replace(' ', '').replace('\n', '')
    else:
        return func.__name__


def simple_check(actual_value, expect_value, prefix=''):
    """两个值的比对校验

    :param dict actual_value: 实际值
    :param dict expect_value: 预期值
    :param str prefix: 错误提示前缀
    :return: 错误信息列表，为空表示校验通过
    :rtype: list[str]
    """
    wrong_list = []
    if not expect_value:
        if actual_value:
            wrong_list.append(f"字段{prefix}校验不通过，预期值为空，实际值为{actual_value}；")

    elif type(expect_value) != type(actual_value):
        wrong_list.append(
            f"字段{prefix}校验不通过，预期值类型={type(expect_value)}，"
            f"实际值类型={type(actual_value)}；")

    elif isinstance(expect_value, dict):
        wrong_list.extend(_check_dict(
            actual_value, expect_value, prefix=prefix
        ))

    elif isinstance(expect_value, list):
        expect_length, actual_length = len(expect_value), len(actual_value)
        if expect_length != actual_length:
            wrong_list.append(
                f"字段{prefix}校验不通过，预期值列表长度={expect_length}，"
                f"实际值列表长度={actual_length}；")
        else:
            for i in range(expect_length):
                wrong_list.extend(simple_check(
                    actual_value[i], expect_value[i], prefix + '.' + str(i)
                ))

    elif actual_value != expect_value:
        wrong_list.append(
            f"字段{prefix}校验不通过，预期值{expect_value}，实际值{actual_value}；")
    else:
        pass

    return wrong_list


def _check_dict(actual, expect, rule_map=None, prefix=''):
    """两个字典的比对校验

    :param dict actual: 实际值
    :param dict expect: 预期值
    :param dict[str, function|dict] rule_map: 校验方法
    :param str prefix: 错误提示前缀
    :return: 错误信息列表，为空表示校验通过
    :rtype: list[str]
    """
    wrong_list = []

    for key, expect_value in expect.items():
        actual_value = actual.get(key, KeyNotFound())
        log_key = prefix + '.' + key if prefix else key

        if rule_map and key in rule_map:
            # 按照传入的校验方法校验实际值和预期值
            check_rule = rule_map[key]
            if callable(check_rule):
                # 校验方法
                if not check_rule(actual_value, expect_value):
                    wrong_list.append(
                        f"字段{log_key}校验不通过，预期值{expect_value}，"
                        f"实际值{actual_value}，校验方法{get_func_ident(check_rule)}；"
                    )
            elif isinstance(check_rule, dict):
                # 校验方法字典，要求预期和实际值为list或dict
                if isinstance(expect_value, dict):
                    if isinstance(actual_value, dict):
                        wrong_list.extend(_check_dict(
                            actual_value, expect_value, check_rule, log_key
                        ))
                    else:
                        wrong_list.append(
                            f"字段{log_key}校验不通过，预期值类型=dict，"
                            f"实际值类型={type(actual_value)}，校验规则{check_rule}；")
                elif isinstance(expect_value, list):
                    if isinstance(actual_value, list):
                        e_length, a_length = len(expect_value), len(actual_value)
                        if e_length != a_length:
                            wrong_list.append(
                                f"字段{log_key}校验不通过，预期值列表长度={e_length}，"
                                f"实际值列表长度={a_length}；")
                        else:
                            try:
                                wrong_list.extend(check_list_of_dict(
                                    actual_value, expect_value,
                                    prefix=log_key,
                                    **check_rule
                                ))
                            except TypeError:
                                wrong_list.extend(check_list_of_dict(
                                    actual_value, expect_value,
                                    prefix=log_key,
                                    rule_map=check_rule
                                ))
                    else:
                        wrong_list.append(
                            f"字段{log_key}校验不通过，预期值类型=list，"
                            f"实际值类型={type(actual_value)}，校验规则{check_rule}；")
                else:
                    raise TypeError(
                        "check_rule is dict, expect_value must be list|dict")
            else:
                raise TypeError("check_rule must be function|dict")

        elif key not in actual:
            wrong_list.append(f"字段{log_key}校验不通过，实际值中没有这个字段；")

        else:
            wrong_list.extend(simple_check(actual_value, expect_value, log_key))

    return wrong_list


def check_dict(
        actual_dict, expect_dict, rule_map=None,
        actual_trans_rule=None, expect_trans_rule=None,
        prefix=''
):
    """两个字典的比对校验

    :param dict actual_dict: 实际值
    :param dict expect_dict: 预期值
    :param dict[str, function|dict] rule_map: 校验方法
    :param dict actual_trans_rule: 转换规则，将实际值转换后再进行校验
    :param dict expect_trans_rule: 转换规则，将预期值转换后再进行校验
    :param str prefix: 错误提示前缀
    :return: 错误信息列表，为空表示校验通过
    :rtype: list[str]
    """
    logger.debug("实际值：" + str(actual_dict))
    logger.debug("预期：" + str(expect_dict))
    if actual_trans_rule:
        actual_dict = transformer.dict_trans(actual_dict, **actual_trans_rule)
        logger.debug("实际值转换后：" + str(actual_dict))
    if expect_trans_rule:
        expect_dict = transformer.dict_trans(expect_dict, **expect_trans_rule)
        logger.debug("预期值转换后：" + str(expect_dict))
    return _check_dict(actual_dict, expect_dict, rule_map, prefix)


def check_list_of_dict(
        actual_list, expect_list, keys=None, order_check=False, rule_map=None,
        actual_trans_rule=None, expect_trans_rule=None, prefix=''
):
    """字典列表list[dict]的比对校验

    :param list[dict] actual_list: 实际值
    :param list[dict] expect_list: 预期值
    :param list[str] keys: 字典唯一标识key列表
    :param bool order_check: 是否进行顺序检查
    :param dict[str, function|dict] rule_map: 校验方法
    :param dict actual_trans_rule: 转换规则，将实际值转换后再进行校验
    :param dict expect_trans_rule: 转换规则，将预期值转换后再进行校验
    :param str prefix: 错误提示前缀
    :return: 错误信息列表，为空表示校验通过
    :rtype: list[str]
    :return: list[str] 错误标记，错误信息
    """
    prefix = prefix + '.' if prefix else prefix

    logger.debug(f"{prefix}实际值：" + str(actual_list))
    logger.debug(f"{prefix}预期：" + str(expect_list))
    if actual_trans_rule:
        actual_list = transformer.list_dict_trans(actual_list, **actual_trans_rule)
        logger.debug(f"{prefix}实际值转换后：" + str(actual_list))
    if expect_trans_rule:
        expect_list = transformer.list_dict_trans(expect_list, **expect_trans_rule)
        logger.debug("预期值转换后：" + str(expect_list))

    # 一、keys为空

    if not keys:
        expect_length, actual_length = len(expect_list), len(actual_list)
        if expect_length != actual_length:
            return [
                f"字段{prefix}校验不通过，预期值列表长度={expect_length}，"
                f"实际值列表长度={actual_length}；"]
        wrong_list = []
        for i in range(expect_length):
            wrong_list.extend(_check_dict(
                actual_list[i], expect_list[i], rule_map, prefix + str(i)
            ))
        return wrong_list

    # 二、keys不为空

    actual_keys = [':'.join([str(_[k]) for k in keys]) for _ in actual_list]
    expect_keys = [':'.join([str(_[k]) for k in keys]) for _ in expect_list]
    # 1、记录检查
    expect_not_in_actual = [_ for _ in expect_keys if _ not in actual_keys]
    actual_not_in_expect = [_ for _ in actual_keys if _ not in expect_keys]
    if expect_not_in_actual or actual_not_in_expect:
        return [
            f"记录校验不通过，在预期值而不在实际值：{expect_not_in_actual}，"
            f"在实际值而不在预期值：{actual_not_in_expect};"]
    # 2、顺序检查
    if order_check:
        for i in range(len(actual_keys)):
            if actual_keys[i] != expect_keys[i]:
                return [f"顺序校验不通过，预期值顺序{actual_keys}，实际值顺序{expect_keys};"]
    # 3、记录详细校验
    wrong_list = []
    actual_dicts = {':'.join([str(_[k]) for k in keys]): _ for _ in actual_list}
    expect_dicts = {':'.join([str(_[k]) for k in keys]): _ for _ in expect_list}
    for i, key in enumerate(actual_keys):
        wrong_list.extend(_check_dict(
            actual_dicts[key], expect_dicts[key], rule_map, prefix + str(i)
        ))
    return wrong_list
