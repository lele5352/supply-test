from models.tms_base import *
from playhouse.shortcuts import model_to_dict


class TMSBaseDBOperator:
    @classmethod
    def get_base_dict(cls,key_name):
        """
        :params string key_name: 字典键名称
        :return: 查询结果数据，字典格式
        """

        item = BaseDict.get_or_none(BaseDict.label_key == key_name)
        if not item:
            return
        return model_to_dict(item)
