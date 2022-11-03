from copy import deepcopy
from config.third_party_api_configs.eta_api_config import ETAApiConfig
from robots.robot import ServiceRobot


class ETARobot(ServiceRobot):
    def __init__(self):
        super().__init__("eta")

    def get_available_stock(self, ck_code_list=None):
        """获取可用库存（商城用）
        :param list ck_code_list : 发货仓编码数组
        """
        content = deepcopy(ETAApiConfig.GetAvailableStock.get_attributes())
        content.get('data').update(
            {
                'deliveryWarehouseCodes': ck_code_list
            }
        )
        res = self.call_api(**content)
        return res

    def get_goods_eta(self, country_code, site_code, sku_codes, zip_code):
        """获取商品非自提ETA（商城用）
        :param list sku_codes : 销售sku编码数组
        :param string country_code : 国家编码
        :param string site_code : 站点编码，如US
        :param string zip_code : 邮编
        """
        content = deepcopy(ETAApiConfig.GetGoodsETA.get_attributes())
        content.get('data').update(
            {
                "countryCode": country_code,
                "siteCode": site_code,
                "skuCodes": sku_codes,
                "zipCode": zip_code
            }
        )
        res = self.call_api(**content)
        return res

    def get_all_country_warehouses(self):
        """获取全部国家发货仓（商城用）"""
        content = deepcopy(ETAApiConfig.CountryDeliveryWarehouses.get_attributes())
        res = self.call_api(**content)
        return res

    def get_trade_self_goods_eta(self, country_code, site_code, sku_infos, zip_code):
        """获取商品非自提ETA（商城用）
        @param zip_code: 邮编
        @param sku_infos: 销售sku和仓库编码数组，格式[{"skuCode": "","warehouseCode": ""}]
        @param country_code: 国家编码
        @param site_code: 站点编码
        """
        content = deepcopy(ETAApiConfig.GetTradeSelfGoodsEtA.get_attributes())
        content.get('data').update(
            {
                "countryCode": country_code,
                "skuInfos": sku_infos,
                "zipCode": zip_code,
                "siteCode": site_code
            }
        )
        res = self.call_api(**content)
        return res

    def get_all_warehouses(self, country_code):
        """获取全部发货仓（商城用）"""
        content = deepcopy(ETAApiConfig.GetCountryList.get_attributes())
        content.get('data').update({"countryCode": country_code})
        res = self.call_api(**content)
        return res

    def get_inventory(self, abroad_flag, country_code):
        """获取全部发货仓（商城用）"""
        content = deepcopy(ETAApiConfig.GetInventory.get_attributes())
        content.get('data').update({"abroadFlag": abroad_flag, "countryCode": country_code})
        res = self.call_api(**content)
        return res

    def get_distribute_warehouses_info_by_country_and_zipcode(self, country_code, zip_code):
        """根据国家和邮编信息获取分仓信息（商城用）"""
        content = deepcopy(ETAApiConfig.GetDistributeWarehousesByCountryAndZipcode.get_attributes())
        content.get('data').append(
            {"countryCode": country_code, "zipCode": zip_code}
        )
        res = self.call_api(**content)
        return res

    def get_distribute_warehouses_info_by_four_params(self, inputs):
        """根据sku、站点、国家和邮编获取分仓信息（商城用）"""
        content = deepcopy(ETAApiConfig.GetDistributeWarehousesByFourParams.get_attributes())
        content.update({
            "data": inputs
        })
        res = self.call_api(**content)
        return res


if __name__ == '__main__':
    eta_robot = ETARobot()
    site = 'US'
    country_code = 'MX'
    sku_code_list = ['14093131604']
    zip_code = '1234'
    sku_info = [{"skuCode": "14093131604", "warehouseCode": ""}]
    inputs = [
        {
            "countryCode": country_code,
            "siteCode": site,
            "skuCode": "14093131604",
            "zipCode": zip_code
        }
    ]
    print(eta_robot.get_available_stock([]))
    print(eta_robot.get_goods_eta(country_code, site, sku_code_list, zip_code))
    print(eta_robot.get_all_country_warehouses())
    print(eta_robot.get_trade_self_goods_eta(country_code, site, sku_info, zip_code))
    print(eta_robot.get_all_warehouses(country_code))
    print(eta_robot.get_inventory(1, country_code))
    print(eta_robot.get_distribute_warehouses_info_by_country_and_zipcode(country_code, zip_code))
    print(eta_robot.get_distribute_warehouses_info_by_four_params(inputs))
