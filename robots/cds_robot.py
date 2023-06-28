import time
from dbo.cds_dbo import CDSDBOperator
from copy import deepcopy
from robots.robot import AppRobot
from config.third_party_api_configs.cds_api_config import *


class CDSAppRobot(AppRobot):
    def __init__(self):
        self.dbo = CDSDBOperator()
        super().__init__()

    def get_cabinet_order(self, **kwargs):
        """海柜单: 获取海列表
        :param kwargs: 查询条件
        :return:
        """
        content = deepcopy(SeaCabinetApiConfig.GetCabinetOrder.get_attributes())
        content["data"].update(**kwargs)
        res = self.call_api(**content)
        return self.formatted_result(res)

    def cabinet_order_detail(self, sea_cabinet_order_id):
        """海柜单: 获取详情和商品明细
        :param str sea_cabinet_order_id: 海柜单id
        :return:
        """
        content = deepcopy(SeaCabinetApiConfig.CabinetOrderDetail.get_attributes())
        content["uri_path"] = content["uri_path"].format(sea_cabinet_order_id, int(time.time() * 1000))
        res = self.call_api(**content)
        return self.formatted_result(res)

    def cabinet_order_sku_detail(self, sea_cabinet_order_id):
        """海柜单: 获取sku明细
        :param str sea_cabinet_order_id: 海柜单id
        :return:
        """
        content = deepcopy(SeaCabinetApiConfig.CabinetOrderSkuDetail.get_attributes())
        content["data"].update({'seaCabinetOrderId': sea_cabinet_order_id})
        res = self.call_api(**content)
        return self.formatted_result(res)

    def confirm_cabinet_order(self, sea_cabinet_order_id):
        """海柜单: 确认发柜
        :param str sea_cabinet_order_id: 海柜单id
        :return:
        """
        content = deepcopy(SeaCabinetApiConfig.ConfirmCabinetOrder.get_attributes())
        content["uri_path"] = content["uri_path"].format(sea_cabinet_order_id, int(time.time() * 1000))
        res = self.call_api(**content)
        return self.formatted_result(res)

    def edit_cabinet_order(self, sea_cabinet_order_id, goods_list, operate_type=2):
        """海柜单: 保存/保存并生单/重新生单
        :param str sea_cabinet_order_id: 海柜单id
        :param list goods_list: 商品明细列表
        :param int operate_type: 操作类型：1、保存；2、保存并生单；3、重新生单
        :return:
        """
        content = deepcopy(SeaCabinetApiConfig.EditCabinetOrder.get_attributes())
        content["data"].update({
            'seaCabinetOrderId': sea_cabinet_order_id,
            'seaCabinetGoodsEditDTOList': goods_list,
            'operateType': operate_type
        })
        res = self.call_api(**content)
        return self.formatted_result(res)


if __name__ == '__main__':
    app = CDSAppRobot()
    print(app.get_cabinet_order())
