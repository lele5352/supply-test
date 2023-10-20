"""
校验工具
"""


def check_isinstance(arg, expected_type, arg_desc):
    """
    校验类型
    :param arg: 校验的参数
    :param expected_type: 预期类型
    :param arg_desc: 参数名称
    """
    if not isinstance(arg, expected_type):
        raise TypeError(f"Expected argument '{arg_desc}' of type {expected_type}, but got {type(arg)}")
