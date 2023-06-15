# -*- coding: utf-8 -*-
import re
from functools import partial


def str_under2hump(under_str):
    """字符串，下划线转驼峰

    :param str under_str: 要被转换的字符串
    :rtype: str
    """
    return re.sub(r'(_\w)', lambda x: x.group(1)[1].upper(), under_str)


def str_hump2under(hump_str):
    """字符串，驼峰转下划线

    :param str hump_str: 要被转换的字符串
    :rtype: str
    """
    p = re.compile(r'([a-z]|\d)([A-Z])')
    return re.sub(p, r'\1_\2', hump_str).lower()


def dict_under2hump(under_dict):
    """将dict的所有下划线风格key转成驼峰

    :param dict under_dict: 要被转换的字典
    :rtype: dict
    """
    return {str_under2hump(k): v for k, v in under_dict.items()}


def dict_hump2under(hump_dict):
    """将dict的所有驼峰风格key转成下划线

    :param dict hump_dict: 要被转换的字典
    :rtype: dict
    """
    return {str_hump2under(k): v for k, v in hump_dict.items()}


def string_trans(string, maps, hump2under=False, under2hump=False):
    """字符串转换方法

    - 如果string在maps中，则按照maps进行string转换并返回；
    - 如果hump2under为真，则将驼峰风格string转成下划线风格并返回；
    - 如果under2hump为真，则将下划线风格string转驼峰风格并返回；
    - 返回原string；

    :param str string: 要被转换的字符串
    :param dict[str, str] maps: string转换映射
    :param bool hump2under: 驼峰转下划线开关
    :param bool under2hump: 下划线转驼峰开关
    :rtype: str
    """
    return (
        maps.get(string)
        or (hump2under and str_hump2under(string))
        or (under2hump and str_under2hump(string))
        or string
    )


def dict_trans(
        origin_dict, remain_keys=None, pop_keys=None,
        map_keys=None, hump2under=False, under2hump=False,
        default_value_trans=None, value_trans=None,
):
    """字典转换方法，规则执行顺序如下：

    一、key的保留和移除：
        1、remain_keys不为空，则仅保留在remain_keys的key，并跳过pop_keys处理；
        2、pop_keys不为空，则移除origin_dict中在pop_keys中的key；
    二、key名转换：
        1、如果key在map_keys中，则按照map_keys进行key转换，并跳过后续key名转换步骤；否则进行下一步判断；
        2、如果hump2under为真，则将驼峰风格key转成下划线风格，并跳过后续key名转换步骤；否则进行下一步判断；
        3、如果under2hump为真，则将下划线风格key转驼峰风格，并跳过后续key名转换步骤；否则进行下一步判断；
        4、保留原key名；
    三、value转换：
        1、key在value_trans中，则origin_dict[key] = value_trans[key](origin_dict[key])，否则进行下一步判断；
        2、default_value_trans不为空，则origin_dict[key] = default_value_trans(origin_dict[key])，否则进行下一步判断
        3、保留原value

    :param dict origin_dict: 要被转换的字典
    :param list[str] remain_keys: 保留的key列表
    :param list[str] pop_keys: 移除的key列表
    :param dict[str, str] map_keys: key名转换映射
    :param bool hump2under: 驼峰key转下划线key开关
    :param bool under2hump: 下划线key转驼峰key开关
    :param function default_value_trans: 默认value值转换方法
    :param dict[str, function] value_trans: value值转换映射，key为origin_dict的key，value为转换方法
    :rtype: dict
    """
    map_keys = map_keys or {}
    remain_keys = remain_keys or None
    pop_keys = pop_keys or []
    default_trans = default_value_trans or (lambda x: x)
    value_trans = value_trans or {}
    key_trans = {
        "maps": map_keys,
        "hump2under": hump2under,
        "under2hump": under2hump
    }
    if remain_keys and isinstance(remain_keys, list):
        new_dict = {
            string_trans(k, **key_trans): value_trans.get(k, default_trans)(v)
            for k, v in origin_dict.items()
            if k in remain_keys
        }
    else:
        new_dict = {
            string_trans(k, **key_trans): value_trans.get(k, default_trans)(v)
            for k, v in origin_dict.items()
            if not pop_keys or k not in pop_keys
        }
    return new_dict


def list_dict_trans(origin_list, **kwargs):
    """将字典列表中的所有字典进行dict_trans

    :param list[dict] origin_list: 要转换的list，元素为dict
    :param kwargs: 传给dict_trans的参数
    :rtype: list[dict]
    """
    return [dict_trans(_, **kwargs) for _ in origin_list]


def get_dict_transformer(**kwargs):
    return partial(dict_trans, **kwargs)


def get_list_transformer(**kwargs):
    return partial(list_dict_trans, **kwargs)
