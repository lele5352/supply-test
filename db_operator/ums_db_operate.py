from models.ums_model import *
from playhouse.shortcuts import model_to_dict


class UMSDBOperator:
    @classmethod
    def query_sys_user(cls, username):
        """
        :param str username: 用户名

        :return dict: 查询结果数据，字典格式
        """

        item = SysUser.get_or_none(SysUser.username == username)
        if not item:
            return
        return model_to_dict(item)
