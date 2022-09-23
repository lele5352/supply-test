import copy

from config.api_config.scm_api_config import scm_api_config
from robots.robot import AppRobot
from utils.log_handler import logger as log


class SCMRobot(AppRobot):
    def __init__(self):
        super().__init__()

    def get_sku_info(self, sale_sku_code):
        """获取供应商产品信息"""
        scm_api_config['get_product_info']['data'].update({'skuCode': sale_sku_code})
        res = self.robot_call_api(**scm_api_config['get_product_info'])
        return res['data']['list'] if res else None

    def stock_plan_submit(self, sale_sku_list, num, delivery_warehouse_code, destination_warehouse_code):
        """备货计划提交"""
        if not destination_warehouse_code:
            destination_warehouse_code = '无'
        sale_sku_info_list = list()
        for sale_sku in sale_sku_list:
            sku_info = self.get_sku_info(sale_sku)
            if not sku_info:
                log.error('获取销售sku%s信息失败' % sale_sku)
                continue
            sku_info[0].update({"minOrderQuantity": 1, "purchaseQuantity": num})
            sale_sku_info_list.append(sku_info[0])
        # 销售sku不存在，直接返回
        if not sale_sku_info_list or len(sale_sku_info_list) < 1:
            log.error('获取不到销售SKU信息！')
            return
        scm_api_config['stock_plan_submit']['data'].update({
            'productInfos': sale_sku_info_list,
            "baseInfo": {
                "destinationWarehouse": destination_warehouse_code,
                "deliveryWarehouse": delivery_warehouse_code
            }
        })
        res = self.robot_call_api(**scm_api_config['stock_plan_submit'])
        return res

    def stock_plan_batch_audit(self, stock_plan_id):
        """备货计划批量审核"""
        scm_api_config['stock_plan_batch_audit']['data'].update({"ids": [stock_plan_id]})
        audit_res = self.robot_call_api(**scm_api_config['stock_plan_batch_audit'])
        if not audit_res or audit_res['code'] != 200:
            return
        return audit_res

    def get_stock_plan_purchase_demand_id(self, stock_plan_no):
        """获取备货计划生成的采购需求id列表"""
        scm_api_config['get_purchase_demand_page']['data'].update(
            {"orderNos": [stock_plan_no]}
        )
        res = self.robot_call_api(**scm_api_config['get_purchase_demand_page'])
        if not res:
            return
        purchase_demand_id_list = [demand['id'] for demand in res['data']['list']]
        return purchase_demand_id_list

    def get_purchase_demand_detail(self, purchase_demand_id):
        """获取采购需求详情"""
        scm_api_config['get_purchase_demand_detail']['uri_path'] += str(purchase_demand_id)
        res = self.robot_call_api(**scm_api_config['get_purchase_demand_detail'])
        return res['data'] if res else None

    def batch_get_purchase_demand_detail(self, purchase_demand_id_list):
        """获取采购需求详情"""
        scm_api_config['batch_get_purchase_demand_detail'].update({'data': purchase_demand_id_list})
        res = self.robot_call_api(**scm_api_config['batch_get_purchase_demand_detail'])
        return res['data'] if res else None

    def confirm_and_generate_purchase_order(self, purchase_demand_id_list):
        """采购需求确认并生单"""
        # 详情获取到的数据和确认并生单要提交的数据格式不一致，主要是product info有差异。
        # 用详情获取到的构建提交的，目标格式："productInfo"：{"details":xxx,"totalPrice": xxx]}
        purchase_demand_detail_list = self.batch_get_purchase_demand_detail(purchase_demand_id_list)
        for purchase_demand_detail in purchase_demand_detail_list:
            temp_product_info = purchase_demand_detail['productInfos']
            product_infos = {
                "details": temp_product_info,
                "totalPrice": purchase_demand_detail["totalAmount"]
            }
            purchase_demand_detail.update({"productInfo": product_infos})
            del purchase_demand_detail["productInfos"]
        scm_api_config['confirm_and_generate_purchase_order'].update({
            'data': purchase_demand_detail_list
        })
        res = self.robot_call_api(**scm_api_config['confirm_and_generate_purchase_order'])
        if not res or res['code'] != 200:
            return
        return True

    def get_purchase_order_page(self, stock_plan_no):
        scm_api_config['get_purchase_order_page']['data'].update({
            "stockOrderNos": [stock_plan_no]
        })
        res = self.robot_call_api(**scm_api_config['get_purchase_order_page'])
        purchase_order_ids = [purchase_order['id'] for purchase_order in res['data']['list']]
        purchase_order_nos = [purchase_order['purchaseOrderNo'] for purchase_order in res['data']['list']]
        return purchase_order_nos, purchase_order_ids

    def get_purchase_order_detail(self, purchase_order_id):
        """获取采购订单详情"""
        body = copy.deepcopy(scm_api_config['get_purchase_order_detail'])
        body.update({
            'uri_path': body['uri_path'] % purchase_order_id
        })

        res = self.robot_call_api(**body)
        return res['data'] if res else None

    def update_and_submit_purchase_order_to_audit(self, purchase_order_detail):
        """采购订单更新并提交审核"""
        purchase_order_detail.update({"operation": 2})
        scm_api_config['purchase_order_update'].update({'data': purchase_order_detail})
        res = self.robot_call_api(**scm_api_config['purchase_order_update'])
        if not res or res['code'] != 200:
            return
        return True

    def purchase_order_audit(self, purchase_order_id_list):
        """采购订单批量审核"""
        scm_api_config['purchase_order_batch_audit']['data'].update({
            "ids": purchase_order_id_list
        })
        audit_res = self.robot_call_api(**scm_api_config['purchase_order_batch_audit'])
        if not audit_res or audit_res['code'] != 200:
            return
        return True

    def purchase_order_batch_buy(self, purchase_order_id_list):
        """采购订单下单"""
        scm_api_config['purchase_order_batch_buy'].update({
            "data": purchase_order_id_list
        })
        audit_res = self.robot_call_api(**scm_api_config['purchase_order_batch_buy'])
        if not audit_res or audit_res['code'] != 200:
            return
        return True

    def get_purchase_order_delivery_detail(self, purchase_order_id):
        """获取采购订单详情"""
        scm_api_config['get_purchase_order_delivery_detail']['data'].update({
            'ids': [purchase_order_id]
        })
        res = self.robot_call_api(**scm_api_config['get_purchase_order_delivery_detail'])
        return res['data']['list'] if res else None

    def generate_distribute_order(self, purchase_order_delivery_detail, delivery_warehouse_code):
        """生成分货单"""
        for detail in purchase_order_delivery_detail:
            detail.update({
                "fix": True,
                "currentSentQuantity": detail['unsentQuantity'],
                "deliveryWarehouse": delivery_warehouse_code
            })
        scm_api_config['generate_distribute_order'].update({
            'data': purchase_order_delivery_detail
        })
        res = self.robot_call_api(**scm_api_config['generate_distribute_order'])
        return res['data'] if res else None

    def purchase_order_delivery(self, distribute_order_info):
        """采购单发货"""
        distribute_order_info.update(
            {'logisticsInfos': []}
        )
        scm_api_config['purchase_order_delivery']['data'].update(distribute_order_info)
        res = self.robot_call_api(**scm_api_config['purchase_order_delivery'])
        if not res or res['code'] != 200:
            return
        return True

    def get_distribute_order_page(self, purchase_order_nos):
        """分货单查询"""
        scm_api_config['get_distribute_order_page']['data'].update({
            "purchaseOrderNos": purchase_order_nos
        })
        res = self.robot_call_api(**scm_api_config['get_distribute_order_page'])
        if not res:
            return
        distribute_order_nos = [distribute_order['shippingOrderNo'] for distribute_order in res['data']['list']]
        return distribute_order_nos
