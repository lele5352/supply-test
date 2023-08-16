import time
from copy import deepcopy
from robots.robot import AppRobot, ServiceRobot
from config.third_party_api_configs.oms_api_config import oms_api_config, OMSApiConfig
from dbo.oms_dbo import OMSDBOperator


class OMSAppRobot(AppRobot):
    def __init__(self):
        self.dbo = OMSDBOperator
        super().__init__()

    def get_product_info(self, sku_code, sku_type=1, site="US"):
        """
        根据sku编码、sku类型、站点获取sku信息
        :param str sku_code : 销售sku编码，
        :param int sku_type: sku类型:1:销售sku;2:部件sku
        :param str site: 站点
        :return : sku的信息
        """
        content = deepcopy(OMSApiConfig.GetProductInfo.get_attributes())
        content['data'].update(
            {
                "type": sku_type,
                "skuCode": sku_code,
                "siteCode": site,
                "t": int(time.time() * 1000)
            }
        )
        res_data = self.call_api(**content)
        try:
            res_data.update({
                "data": res_data["data"]["records"][0]
            })
        except TypeError:
            res_data.update({
                "data": []
            })
        return self.formatted_result(res_data)

    def get_follow_order_page(self, oms_no):
        """
        根据oms单号查询跟单列表数据
        :return : oms的跟单信息
        """
        content = deepcopy(OMSApiConfig.GetFollowOrderPage.get_attributes())
        content['data'].update(
            {
                "orderNo": oms_no
            }
        )
        res_data = self.call_api(**content)
        return self.formatted_result(res_data)

    def get_warehouse_info(self, warehouse_id):
        """
        根据仓库id获取仓库信息
        :param warehouse_id: 仓库id
        :return:
        """
        oms_api_config["get_warehouse_info"]["data"].update({"t": int(time.time() * 1000)})
        res_data = self.call_api(**oms_api_config["get_warehouse_info"])

        for warehouse in res_data['data']:
            if warehouse['warehouseId'] == warehouse_id:
                res_data.update({
                    "data": warehouse
                })
                return self.formatted_result(res_data)
        return None

    def create_sale_order(self, order_sku_info_list):
        """
        创建销售单
        :param list order_sku_info_list: 销售sku及数量的数组，格式：[{"sku_code":"","qty":1,"bom":"A","warehouse_id":""}]
        :return:创建结果
        """

        temp_items_data_list = []
        for order_sku_info in order_sku_info_list:
            temp_items_data = deepcopy(oms_api_config['create_sale_order']['data']['items'][0])
            product_info_result = self.get_product_info(order_sku_info["sku_code"])
            if not product_info_result["code"]:
                return self.formatted_result(product_info_result)
            product_info = product_info_result["data"]
            if order_sku_info["warehouse_id"]:
                warehouse_info_result = self.get_warehouse_info(order_sku_info["warehouse_id"])
                product_info.update({
                    "warehouseCode": warehouse_info_result["data"]["warehouseCode"],
                    "warehouseId": warehouse_info_result["data"]["warehouseId"],
                    "warehouseName": warehouse_info_result["data"]["warehouseName"]
                })
            if order_sku_info["bom"]:
                product_info.update({
                    "bomVersion": order_sku_info["bom"]
                })
            product_info.update({
                "itemQty": order_sku_info["qty"],
                "itemSkuCode": order_sku_info["sku_code"]
            })

            temp_items_data.update(product_info)
            temp_items_data_list.append(temp_items_data)
        oms_api_config["create_sale_order"]["data"].update({"items": temp_items_data_list})
        res_data = self.call_api(**oms_api_config["create_sale_order"])
        return self.formatted_result(res_data)

    def query_oms_order_by_oms_no(self, oms_order_no):
        """
        :param oms_order_no: oms单号
        :return: list
        """
        oms_api_config["query_oms_order"]["data"].update({"orderNos": oms_order_no})
        res_data = self.call_api(**oms_api_config["query_oms_order"])
        res_data.update({
            "data": res_data['data']['records']
        })
        return self.formatted_result(res_data)

    def query_oms_order_by_sale_no(self, sale_order_no):
        """
        :param sale_order_no: 销售单号
        :return: list
        """
        oms_api_config["query_oms_order"]["data"].update({"salesOrderNos": sale_order_no})
        res_data = self.call_api(**oms_api_config["query_oms_order"])
        res_data.update({
            "data": res_data['data']['records']
        })
        return self.formatted_result(res_data)

    def query_oms_order_detail(self, oms_order_id):
        """
        :param oms_order_id: oms单id
        :return: list
        """
        temp = deepcopy(oms_api_config["query_oms_order_detail"])
        temp.update({
            "uri_path": temp["uri_path"] % oms_order_id,
            "data": {'t': int(time.time() * 1000)}
        })

        res_data = self.call_api(**temp)
        return self.formatted_result(res_data)

    def query_oms_order_sku_items(self, oms_order_id):
        """
        :param oms_order_id: oms单id
        :return: list
        """
        temp = deepcopy(oms_api_config["query_oms_order_sku_items"])
        temp.update({
            "uri_path": temp["uri_path"] % oms_order_id,
            "data": {'t': int(time.time() * 1000)}
        })
        res_data = self.call_api(**temp)
        return self.formatted_result(res_data)

    def query_common_warehouse(self, common_warehouse_code):
        """
        查询共享仓信息
        :param common_warehouse_code: 共享仓编码
        :return: list
        """
        oms_api_config["query_common_warehouse"]["data"].update({
            "virtualWarehouseCodes": [common_warehouse_code]
        })

        res_data = self.call_api(**oms_api_config["query_common_warehouse"])
        return self.formatted_result(res_data)

    def query_sku_stock_detail(self, sku_code, site_code='US', country='US', postal_code='10001'):
        """
        查询sku的可用库存信息
        :param sku_code: 共享仓编码
        :param site_code: 站点编码
        :param country: 国家编码
        :param postal_code: 邮编
        :return: list
        """
        oms_api_config["product_detail"]["uri"] %= (sku_code, site_code, country, postal_code)
        res_data = self.call_api(**oms_api_config["query_common_warehouse"])
        return self.formatted_result(res_data)

    def query_divide_warehouse(self, country='US',  postal_code='10001', transport_type=3):
        """
        查询分仓规则
        :param str country: 国家编码
        :param str postal_code: 邮编
        :param int transport_type: 物流方式（1.卡车 2.快递（可跨仓） 3.快读（不可跨仓） 4.快递（可跨仓-LA） 5.国内直发）
        :return: list
        """
        oms_api_config["query_common_warehouse"]["data"].update({
            "countryCode": [country], "postCodes": [postal_code], "logisticsType": [transport_type]
        })
        res_data = self.call_api(**oms_api_config["warehouse_allocation_rule"])
        return self.formatted_result(res_data)


class OMSAppIpRobot(ServiceRobot):
    def __init__(self):
        self.dbo = OMSDBOperator
        super().__init__("oms_app")

    def dispatch_oms_order(self, oms_order_list):
        oms_api_config["dispatch_oms_order"].update({
            "data": oms_order_list
        })
        res_data = self.call_api(**oms_api_config["dispatch_oms_order"])
        return self.formatted_result(res_data)

    def oms_order_follow(self, follow_list):
        """
        执行跟单
        :param follow_list: [{"skuCode": "demoData", "bomVersion": "demoData"}]
        :return:
        """
        oms_api_config["oms_order_follow"].update({
            "data": follow_list
        })
        res_data = self.call_api(**oms_api_config["oms_order_follow"])
        return self.formatted_result(res_data)

    def push_order_to_wms(self):
        """
        下发订单
        :return:
        """
        res_data = self.call_api(**oms_api_config["push_order_to_wms"])
        return self.formatted_result(res_data)


if __name__ == '__main__':
    oms = OMSAppRobot()
    print(oms.get_follow_order_page("OMS2209270111"))