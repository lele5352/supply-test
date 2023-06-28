import time
from copy import deepcopy
from robots.robot import AppRobot, ServiceRobot
from config.third_party_api_configs.pms_api_config import BaseApiConfig
from dbo.oms_dbo import OMSDBOperator


class PMSAppRobot(AppRobot):
    def __init__(self):
        super().__init__()

    def add_product(self, **kwargs):
        content = deepcopy(BaseApiConfig.AddProduct.get_attributes())
        content["data"].update(**kwargs)
        res = self.call_api(**content)
        return self.formatted_result(res)

    def calculate_product_price(self, spu_id):
        content = deepcopy(BaseApiConfig.CalculateProductPrice.get_attributes())
        content["uri_path"] = content["uri_path"].format(spu_id)
        res = self.call_api(**content)
        return self.formatted_result(res)

    def save_product_price(self, spu_price_list):
        content = deepcopy(BaseApiConfig.SaveProductPrice.get_attributes())
        content["data"] = spu_price_list
        res = self.call_api(**content)
        return self.formatted_result(res)

    def audit_product(self, sku_id):
        content = deepcopy(BaseApiConfig.AuditProduct.get_attributes())
        content["data"] = [
            {
                "auditResult": 1,
                "remark": "",
                "skuId": sku_id
            }
        ]
        res = self.call_api(**content)
        return self.formatted_result(res)


if __name__ == '__main__':
    pass
