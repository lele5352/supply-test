from copy import deepcopy

from config.third_party_api_configs.bpms_api_config import *
from robots.robot import AppRobot
from utils.custom_wrapper import extract_json


class BPMSRobot(AppRobot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @extract_json("$.data.records")
    def plat_product_page(self, sku_code, store_code=None, fn_sku_code=None, page_no=1):
        """
        查询平台sku列表
        :param sku_code: 销售sku编码
        :param store_code: 店铺sku编码
        :param fn_sku_code: fn sku 编码
        :param page_no: 页码

        return list
        """
        content = deepcopy(ProductInfo.PlatProductPage.get_attributes())
        content["data"]["param"]["productSkuCodeList"] = [sku_code]
        content["data"]["param"]["pageNo"] = page_no

        if store_code:
            content["data"]["param"]["storeSkuCodeList"] = [store_code]
        if fn_sku_code:
            content["data"]["param"]["fnSkuCodeList"] = [fn_sku_code]

        return self.call_api(**content)
