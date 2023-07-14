from random import randint
from copy import deepcopy
from robots.robot import AppRobot
from config.third_party_api_configs.pms_api_config import BaseApiConfig


class PMSAppRobot(AppRobot):
    def __init__(self):
        super().__init__()

    def add_product(self, **kwargs):
        content = deepcopy(BaseApiConfig.AddProduct.get_attributes())
        if 'package_num' in kwargs.keys() and 'single_package_num' in kwargs.keys():
            single_package_num = kwargs.pop('single_package_num')
            content["data"]["skuList"][0]['packageInfoList'] = [
                {
                    "height": randint(1, 10), "length": randint(1, 10), "width": randint(1, 10),
                    "weight": randint(1, 10), "packageName": f"package{index}",
                    "packageNum": single_package_num
                } for index in range(0, kwargs.pop('package_num'))
            ]
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

    def approve_sku_attribution(self, sku_id):
        # 获取sku信息并填充提交表单数据
        content = deepcopy(BaseApiConfig.GetSkuAttribution.get_attributes())
        content['uri_path'] = content['uri_path'].format(sku_id)
        sku_detail = self.call_api(**content).get('data')
        content_edit = deepcopy(BaseApiConfig.EditSkuAttribution.get_attributes())
        sku_detail.pop('installDescs')
        sku_detail.pop('skuSuitRelationInfoVoList')
        sku_detail['operateFlag'] = 2
        sku_detail['pmsSkuModityInfoVoList'] = [
            {
                "attrId": 4,
                "usaAttrName": "sink material"
            },
            {
                "attrId": 979,
                "usaAttrName": "image filter test"
            }
        ]
        sku_detail['pmsSkuAttrVoSellList'][0].update(
            {"zharr": [
                {
                    "attrValueId": "",
                    "propertiesValue": "one",
                    "propertiesValueEn": "one",
                    "propertiesValueZh": "1"
                }
            ], "attrDetailNameUk": "one", "attrDetailNameUs": "one"})
        sku_detail['pmsSkuAttrVoBaseList'][0]['attrValueVoList'].append(
            {"attrDetailId": 1206, "attrDetailNameUs": "Glass", "attrDetailName": "玻璃", "attrDetailNameUk": "Glass"})
        sku_detail['pmsSkuAttrVoSellList'][0]['attrValueVoList'][0].update(
            {"attrDetailId": 0, "attrDetailType": 2, "moreLanguageId": None})
        # 修改提交的表单数据后提交审核
        content_edit['data'].update(sku_detail)
        self.call_api(**content_edit)
        # 审核通过sku修改，上架商品
        content_approve = deepcopy(BaseApiConfig.ApproveSkuAttribution.get_attributes())
        content_approve['data'].update({'skuIds': [sku_id]})
        self.call_api(**content_approve)


if __name__ == '__main__':
    pass
