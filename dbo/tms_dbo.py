from models.tms_base import *
from models.tms_order import *
from models.tms_channel import *
from playhouse.shortcuts import model_to_dict


class TMSBaseDBO:
    @classmethod
    def get_base_dict(cls, key_name):
        """
        :params string key_name: 字典键名称
        :return: 查询结果数据，字典格式
        """
        item = BaseDict.get_or_none(BaseDict.label_key == key_name)
        if not item:
            return
        return model_to_dict(item)


class TMSChannelDBO:
    @classmethod
    def get_channel_data(cls, channel_id):
        """
        :params int channel_id: 渠道id
        :return: 查询结果数据，字典格式
        """
        item = LogisticsChannel.get_or_none(LogisticsChannel.id == channel_id)
        if not item:
            return
        return model_to_dict(item)


class LogisticOrderDBO:

    @classmethod
    def express_order_info(cls, express_order_code):
        """
        通过运单号查询运单信息
        """
        data = LogisticsExpressOrder.get_or_none(
            LogisticsExpressOrder.express_order_code == express_order_code
        )
        return model_to_dict(data) if data else None
