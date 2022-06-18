import time

from config.sys_config import env_prefix_config
from config.api_config.eta_api_config import eta_api_config
from utils.request_handler import RequestHandler
from logics.ums_logics import UmsLogics
from api_request.ums_request import UmsRequest


class ETARequest(RequestHandler):
    def __init__(self, service_header):
        self.prefix = env_prefix_config.get('eta_prefix')
        super().__init__(self.prefix, service_header)

    def mall_get_available_stock(self, ck_code_list):
        """获取可用库存（商城用）
        :param list ck_code_list : 发货仓编码数组
        """
        eta_api_config['mall_get_available_stock']['data'].update(
            {
                'deliveryWarehouseCodes': ck_code_list,
                'version': int(time.time() * 1000)
            }
        )
        res = self.send_request(**eta_api_config['mall_get_available_stock'])
        return res

    def mall_get_not_trade_self_goods_eta(self, country_code, site_code, sku_codes, zip_code):
        """获取商品非自提ETA（商城用）
        :param list sku_codes : 销售sku编码数组
        :param string country_code : 国家编码
        :param string site_code : 站点编码，如US
        :param string zip_code : 邮编
        """
        eta_api_config['mall_get_not_trade_self_goods_eta']['data'].update(
            {
                "countryCode": country_code,
                "siteCode": site_code,
                "skuCodes": sku_codes,
                "zipCode": zip_code
            }
        )
        res = self.send_request(**eta_api_config['mall_get_not_trade_self_goods_eta'])
        return res

    def mall_get_all_country_warehouses(self):
        """获取全部国家发货仓（商城用）"""
        res = self.send_request(**eta_api_config['mall_country_delivery_warehouses'])
        return res

    def mall_get_trade_self_goods_eta(self, country_code, sku_infos, zip_code):
        """获取商品非自提ETA（商城用）
        :param list sku_infos : 销售sku和仓库编码数组，格式[{"skuCode": "","warehouseCode": ""}]
        :param string country_code : 国家编码
        :param string zip_code : 邮编
        """
        eta_api_config['mall_get_trade_self_goods_eta']['data'].update(
            {
                "countryCode": country_code,
                "skuInfos": sku_infos,
                "zipCode": zip_code
            }
        )
        res = self.send_request(**eta_api_config['mall_get_trade_self_goods_eta'])
        return res

    def mall_get_all_warehouses(self, country_code):
        """获取全部发货仓（商城用）"""
        eta_api_config['mall_get_country_list']['data'].update(
            {"countryCode": country_code}
        )
        res = self.send_request(**eta_api_config['mall_get_country_list'])
        return res

    def mall_get_inventory(self, abroad_flag, country_code):
        """获取全部发货仓（商城用）"""
        eta_api_config['mall_get_inventory']['data'].update(
            {"abroadFlag": abroad_flag, "countryCode": country_code}
        )
        res = self.send_request(**eta_api_config['mall_get_inventory'])
        return res

    def mall_get_distribute_warehouses_info_by_country_and_zipcode(self, country_code, abroad_flag):
        """根据国家和邮编信息获取分仓信息（商城用）"""
        eta_api_config['mall_get_distribute_warehouses_info_by_country_and_zipcode']['data'].update(
            {"countryCode": country_code, "abroadFlag": abroad_flag}
        )
        res = self.send_request(**eta_api_config['mall_get_distribute_warehouses_info_by_country_and_zipcode'])
        return res

    def mall_get_distribute_warehouses_info_by_four_params(self, inputs):
        """根据sku、站点、国家和邮编获取分仓信息（商城用）"""
        eta_api_config['mall_get_distribute_warehouses_info_by_four_params'].update(
            {"data": inputs}
        )
        res = self.send_request(**eta_api_config['mall_get_distribute_warehouses_info_by_four_params'])
        return res


if __name__ == '__main__':
    ums_request = UmsRequest()
    ums_logics = UmsLogics(ums_request)
    service_headers = ums_logics.get_service_headers()
    eta = ETARequest(service_headers)

    site = 'US'
    country_code = 'MX'
    sku_code_list = ['14093131604']
    zip_code = '1234'
    print(eta.mall_get_not_trade_self_goods_eta(country_code, site, sku_code_list, zip_code))
