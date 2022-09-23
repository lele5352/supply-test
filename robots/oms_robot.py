import time
from copy import deepcopy
from robots.robot import AppRobot, ServiceRobot
from config.api_config.oms_api_config import oms_api_config
from db_operator.oms_db_operator import OMSDBOperator


class OMSAppRobot(AppRobot):
    def __init__(self):
        super().__init__(OMSDBOperator)

    def get_product_info(self, sku_code, sku_type=1, site="US"):
        """
        根据sku编码、sku类型、站点获取sku信息
        @param str sku_code : 销售sku编码，
        @param int sku_type: sku类型:1:销售sku;2:部件sku
        @param str site: 站点
        @return : sku的信息
        """
        oms_api_config['get_product_info']['data'].update(
            {
                "type": sku_type,
                "skuCode": sku_code,
                "siteCode": site,
                "t": int(time.time() * 1000)
            }
        )
        res_data = self.call_api(**oms_api_config['get_product_info'])
        res_data.update({
            "data": res_data["data"]["records"][0]
        })
        return self.formatted_result(res_data)

    def get_warehouse_info(self, warehouse_id):
        """
        根据仓库id获取仓库信息
        @param warehouse_id: 仓库id
        @return:
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
        @param list order_sku_info_list: 销售sku及数量的数组，格式：[{"sku_code":"","qty":1,"bom":"A","warehouse_id":""}]
        @return:创建结果
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

    def query_oms_order(self, sale_order_no):
        """
        @param sale_order_no: 销售单号
        @return: list
        """
        oms_api_config["query_oms_order"]["data"].update({"salesOrderNos": sale_order_no})
        res_data = self.call_api(**oms_api_config["query_oms_order"])
        res_data.update({
            "data": res_data['data']['records']
        })
        return self.formatted_result(res_data)

    def query_oms_order_detail(self, oms_order_id):
        """
        @param oms_order_id: oms单id
        @return: list
        """
        oms_api_config["query_oms_order_detail"].update({
            "uri_path": oms_api_config["query_oms_order_detail"]["uri_path"] % oms_order_id,
            "data": {'t': int(time.time() * 1000)}
        })

        res_data = self.call_api(**oms_api_config["query_oms_order_detail"])
        return self.formatted_result(res_data)

    def query_oms_order_sku_items(self, oms_order_id):
        """
        @param oms_order_id: oms单id
        @return: list
        """
        oms_api_config["query_oms_order_sku_items"].update({
            "uri_path": oms_api_config["query_oms_order_sku_items"]["uri_path"] % oms_order_id,
            "data": {'t': int(time.time() * 1000)}
        })

        res_data = self.call_api(**oms_api_config["query_oms_order_sku_items"])
        return self.formatted_result(res_data)

    def query_common_warehouse(self, common_warehouse_code):
        """
        查询共享仓信息
        @param common_warehouse_code: 共享仓编码
        @return: list
        """
        oms_api_config["query_common_warehouse"]["data"].update({
            "virtualWarehouseCodes": [common_warehouse_code]
        })

        res_data = self.call_api(**oms_api_config["query_common_warehouse"])
        return self.formatted_result(res_data)


class OMSAppIpRobot(ServiceRobot):
    def __init__(self):
        super().__init__("oms_app", OMSDBOperator)

    def dispatch_oms_order(self, oms_order_list):
        oms_api_config["dispatch_oms_order"]["data"].extend(oms_order_list)
        aaa = oms_api_config["dispatch_oms_order"]
        res_data = self.call_api(**oms_api_config["dispatch_oms_order"])
        return self.formatted_result(res_data)

    def oms_order_follow(self, follow_list):
        """
        执行跟单
        @param follow_list: [{"skuCode": "demoData", "bomVersion": "demoData"}]
        @return:
        """
        oms_api_config["oms_order_follow"].update({
            "data": follow_list
        })
        res_data = self.call_api(**oms_api_config["oms_order_follow"])
        return self.formatted_result(res_data)

    def push_order_to_wms(self):
        """
        下发订单
        @return:
        """
        res_data = self.call_api(**oms_api_config["push_order_to_wms"])
        return self.formatted_result(res_data)
