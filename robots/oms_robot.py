import time
from copy import deepcopy
from math import ceil

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

    def create_sale_order(self, order_sku_info_list, **kwargs):
        """
        创建销售单
        :param list order_sku_info_list: 销售sku及数量的数组，格式：[{"sku_code":"","qty":1,"bom":"A","warehouse_id":""}]
        :param kwargs: 其他参数
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
            else:
                product_info.update({
                    "warehouseCode": '',
                    "warehouseId": '',
                    "warehouseName": ''
                })
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
        for key in kwargs:
            if key in oms_api_config["create_sale_order"]["data"]:
                oms_api_config["create_sale_order"]["data"].update({key: kwargs[key]})
        res_data = self.call_api(**oms_api_config["create_sale_order"])
        return self.formatted_result(res_data)

    def query_oms_order_by_oms_no(self, oms_order_no):
        """
        :param oms_order_no: oms单号
        :return: list
        """
        temp = deepcopy(oms_api_config["query_oms_order"])
        temp["data"].update({"orderNos": oms_order_no})
        res_data = self.call_api(**temp)
        res_data.update({
            "data": res_data['data']['records']
        })
        return self.formatted_result(res_data)

    def query_oms_order_by_sale_no(self, sale_order_no, **kwargs):
        """
        :param sale_order_no: 销售单号
        :return: list
        """
        temp = deepcopy(oms_api_config["query_oms_order"])
        temp["data"].update({"salesOrderNos": sale_order_no})
        if kwargs and set(kwargs.keys()).issubset(set(temp['data'].keys())):
            temp["data"].update(kwargs)
        res_data = self.call_api(**temp)
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

    def query_common_warehouse(self, common_warehouse_code=None, **kwargs):
        """
        查询共享仓信息
        :param common_warehouse_code: 共享仓编码
        :return: list
        """
        temp = deepcopy(oms_api_config["query_common_warehouse"])
        temp["data"].update({
            "virtualWarehouseCodes": [common_warehouse_code] if common_warehouse_code else []
        })
        for k in kwargs:
            if k in temp['data']:
                temp["data"].update({
                    k: kwargs[k]
                })
        res_data = self.call_api(**temp)
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
        temp = deepcopy(oms_api_config["product_detail"])
        temp["uri_path"] %= (sku_code, site_code, country, postal_code)
        res_data = self.call_api(**temp)
        return self.formatted_result(res_data)

    def query_divide_warehouse(self, country, postal_code, transport_type):
        """
        查询分仓规则
        :param list(str) country: 国家编码 ['US']
        :param list(str) postal_code: 邮编 ['10001']
        :param list(int) transport_type: 物流方式（1.卡车 2.快递（可跨仓） 3.快读（不可跨仓） 4.快递（可跨仓-LA） 5.国内直发） [1,2]
        :return: list
        """
        temp = deepcopy(oms_api_config["warehouse_allocation_rule"])
        temp["data"].update({
            "countryCode": country, "postCodes": postal_code, "logisticsType": transport_type
        })
        res_data = self.call_api(**temp)
        return self.formatted_result(res_data)

    def apply_modify(self, order_id):
        """
        申请修改订单
        :param str order_id: oms订单id
        :return: dict
        """
        temp = deepcopy(oms_api_config["apply_modify"])
        oms_api_config['check_lock']['data'] = [order_id]
        self.call_api(**oms_api_config['check_lock'])
        temp['uri_path'] %= (order_id, int(time.time() * 1000))
        res_data = self.call_api(**temp)
        oms_api_config['release_lock']['data'] = [order_id]
        self.call_api(**oms_api_config['release_lock'])
        return self.formatted_result(res_data)

    def update_buyer(self, order_id, order_detail):
        """
        修改订单
        :param str order_id: oms订单id
        :param list(dict) order_detail: 修改明细
        :return: dict
        """
        temp = deepcopy(oms_api_config["update_buyer"])
        oms_api_config['check_lock']['data'] = [order_id]
        self.call_api(**oms_api_config['check_lock'])
        temp["data"].update({
            "orderId": order_id, "details": order_detail
        })
        res_data = self.call_api(**temp)
        oms_api_config['release_lock']['data'] = [order_id]
        self.call_api(**oms_api_config['release_lock'])
        return self.formatted_result(res_data)

    def labor_update(self, order_id, order_detail):
        """
        修改订单
        :param str order_id: oms订单id
        :param list(dict) order_detail: 修改明细
        :return: dict
        """
        temp = deepcopy(oms_api_config["labor_update"])
        oms_api_config['check_lock']['data'] = [order_id]
        self.call_api(**oms_api_config['check_lock'])
        temp["data"].update({
            "orderId": order_id, "details": order_detail
        })
        res_data = self.call_api(**temp)
        oms_api_config['release_lock']['data'] = [order_id]
        self.call_api(**oms_api_config['release_lock'])
        return self.formatted_result(res_data)

    def get_invalid_order(self, so_order_nos='', oms_no=''):
        """
        查询作废订单列表
        :param str so_order_nos: so订单号
        :param str oms_no: oms订单号
        :return: dict
        """
        temp = deepcopy(oms_api_config["order_invalid_page"])
        temp["data"].update({
            "salesOrderNos": so_order_nos,
            "orderNos": oms_no
        })
        res_data = self.call_api(**temp)
        res_data.update({
            "data": res_data['data']['records']
        })
        return self.formatted_result(res_data)

    def get_province_list(self, country_code="US"):
        """
        查询sku的可用库存信息
        :param country_code: 国家编码
        :return: list
        """
        temp = deepcopy(oms_api_config["get_province_list"])
        temp["uri_path"] %= (country_code, int(time.time() * 1000))
        res_data = self.call_api(**temp)
        return self.formatted_result(res_data)

    def get_oms_warehouse_eta_page(self, oms_warehouse_code="", warehouse_type=1):
        """
        查询oms共享仓eta配置列表
        :param str oms_warehouse_code: oms共享仓编码
        :param int warehouse_type: oms共享仓类型 1发货 2备货 3中转
        :return: dict
        """
        temp_page = deepcopy(oms_api_config["eta_warehouse_rule_page"])
        temp_page["data"].update({
            "warehouseCode": oms_warehouse_code,
            "warehouseType": warehouse_type
        })
        res_data = self.call_api(**temp_page)
        res_data.update({
            "data": res_data['data']['records']
        })
        return self.formatted_result(res_data)

    def get_shipping_eta_rule(self):
        """
        查询oms海运时长
        :return: dict
        """
        temp_page = deepcopy(oms_api_config["get_shipping_eta_rule"])
        res_data = self.call_api(**temp_page)
        return self.formatted_result(res_data)

    def get_salesorder_item_detail(self, sale_order_no):
        """
        查询销售订单审单情况
        :return: dict
        """
        temp_page = deepcopy(oms_api_config["salesorder_item_detail"])
        temp_page['uri_path'] %= (sale_order_no, int(time.time() * 1000))
        res_data = self.call_api(**temp_page)
        return self.formatted_result(res_data)

    def get_omsorder_item_detail(self, sale_order_no):
        temp = deepcopy(oms_api_config['get_order_item'])
        temp['uri_path'] %= (sale_order_no, int(time.time() * 1000))
        res_data = self.call_api(**temp)
        return self.formatted_result(res_data)

    def get_oms_warehouse_eta_rule(self, oms_warehouse_code=""):
        """
        查询oms共享仓eta配置
        :param str oms_warehouse_code: oms共享仓编码
        :return: dict
        """
        per_page = 10
        temp_page = deepcopy(oms_api_config["eta_warehouse_rule_page"])
        temp_page["data"].update({
            "warehouseCode": oms_warehouse_code
        })
        warehouse_rule_id = self.call_api(**temp_page)['data']['records'][0]['id']

        temp_info = deepcopy(oms_api_config["eta_warehouse_rule_info"])
        temp_info["data"].update({
            "id": warehouse_rule_id,
            "size": per_page
        })
        res_data = self.call_api(**temp_info)
        total = res_data['data']['ruleLogisticsPage']['total']
        if total > per_page:
            for page in range(2, ceil(total / per_page) + 1):
                temp_info["data"].update({
                    "current": page
                })
                res_data['data']['ruleLogisticsPage']['records'] += self.call_api(**temp_info)[
                    'data']['ruleLogisticsPage']['records']
        return self.formatted_result(res_data)

    def get_order_follow_trace_page(self, so_no_list):
        temp = deepcopy((oms_api_config['order_follow_trace_page']))
        temp["data"].update({
            "salesOrderNoList": so_no_list
        })
        res = self.call_api(**temp)
        return self.formatted_result(res)

    def get_order_follow_trace_detail(self, trace_id, latest=True):
        temp = deepcopy((oms_api_config['order_follow_trace_detail']))
        temp["data"].update({
            "id": trace_id, 'size': 1 if latest else 100
        })
        res = self.call_api(**temp)
        return self.formatted_result(res)


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

    def push_order_to_wms(self, order_no_list=None):
        """
        下发订单,默认全部下发，可指定oms单号
        :return:
        """
        oms_api_config["push_order_to_wms"]['data'].update({
            "orderNos": order_no_list or []
        })
        res_data = self.call_api(**oms_api_config["push_order_to_wms"])
        return self.formatted_result(res_data)


if __name__ == '__main__':
    oms = OMSAppRobot()
    print(oms.get_follow_order_page("OMS2209270111"))