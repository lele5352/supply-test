from copy import deepcopy
from typing import Union

from config.third_party_api_configs.rms_api_config import *
from robots.robot import AppRobot
from dbo.wms_dbo import WMSDBOperator
from robots.bpms_robot import BPMSRobot


class RMSRobot(AppRobot):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def transfer_plan_add(self, delivery_warehouse_id, receive_warehouse_id,
                          sku_code, bom_version, qty, remark=None):
        """
        创建调拨需求
        """
        def build_sku_detail(sku_list, qty, bom):
            result = []
            for sku in sku_list:
                result.append({
                    "itemSkuCode": sku['skuCode'],
                    "itemSkuType": 1,
                    "itemSkuName": sku['productName'],
                    "quantity": qty,
                    "itemPicture": sku['mainUrl'],
                    "bomVersion": bom
                })

            return result

        delivery_warehouse = WMSDBOperator.query_warehouse_info_by_id(delivery_warehouse_id)
        receive_warehouse = WMSDBOperator.query_warehouse_info_by_id(receive_warehouse_id)
        sale_sku_list = BPMSRobot().sale_sku_page(sku_code)
        content = deepcopy(RMSApiConfig.TransferPlanAdd.get_attributes())

        content["data"]["details"] = build_sku_detail(sale_sku_list, qty, bom_version)
        content["data"]["deliveryWarehouseId"] = delivery_warehouse_id
        content["data"]["deliveryWarehouseName"] = delivery_warehouse["warehouse_name"]
        content["data"]["deliveryWarehouseCode"] = delivery_warehouse["warehouse_code"]
        content["data"]["receiveWarehouseId"] = receive_warehouse_id
        content["data"]["receiveWarehouseName"] = receive_warehouse["warehouse_name"]
        content["data"]["receiveWarehouseCode"] = receive_warehouse["warehouse_code"]
        content["data"]["remark"] = remark if remark is not None else ''

        return self.call_api(**content)


