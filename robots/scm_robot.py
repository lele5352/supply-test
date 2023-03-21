from copy import deepcopy
from config.third_party_api_configs.scm_api_config import SCMApiConfig
from robots.robot import AppRobot
from utils.log_handler import logger as log
from dbo.scm_dbo import SCMDBOperator


class SCMRobot(AppRobot):
    def __init__(self):
        self.dbo = SCMDBOperator
        super().__init__()

    def get_sku_info(self, sale_sku_code):
        """获取供应商产品信息
        :param string sale_sku_code:销售出库单编码
        :return:
        """
        content = deepcopy(SCMApiConfig.GetProductInfo.get_attributes())
        content["data"].update({"skuCode": sale_sku_code})
        res = self.call_api(**content)
        return self.formatted_result(res)

    def shortage_demand_batch_confirm(self, shortage_demand_id_list):
        """
        缺货需求批量确认
        :param list shortage_demand_id_list:缺货需求id列表
        :return:
        """
        content = deepcopy(SCMApiConfig.ShortageDemandBatchConfirm.get_attributes())
        content.update({"data": shortage_demand_id_list})
        res = self.call_api(**content)
        return self.formatted_result(res)

    def stock_plan_submit(self, sale_sku_list, num, delivery_warehouse_code, destination_warehouse_code):
        """备货计划提交"""
        if not destination_warehouse_code:
            destination_warehouse_code = "无"
        sale_sku_info_list = list()
        for sale_sku in sale_sku_list:
            sku_info_result = self.get_sku_info(sale_sku)
            if self.is_data_empty(sku_info_result):
                log.error("获取销售sku%s信息失败" % sale_sku)
                continue
            sku_info = sku_info_result['data']["list"][0]
            sku_info.update({"minOrderQuantity": 1, "purchaseQuantity": num})
            sale_sku_info_list.append(sku_info)
        # 销售sku不存在，直接返回
        if not sale_sku_info_list or len(sale_sku_info_list) < 1:
            log.error("获取不到销售SKU信息！")
            return
        content = deepcopy(SCMApiConfig.StockPlanSubmit.get_attributes())
        content["data"].update({
            "productInfos": sale_sku_info_list,
            "baseInfo": {
                "destinationWarehouse": destination_warehouse_code,
                "deliveryWarehouse": delivery_warehouse_code}
        })
        res = self.call_api(**content)
        return self.formatted_result(res)

    def stock_plan_batch_audit(self, stock_plan_id):
        """备货计划批量审核"""
        content = deepcopy(SCMApiConfig.StockPlanAudit.get_attributes())
        content["data"].update({"ids": [stock_plan_id]})
        res = self.call_api(**content)
        if not res or res["code"] != 200:
            return
        return self.formatted_result(res)

    def get_purchase_demand_id(self, order_no, status=None):
        """获取生成的采购需求id列表
        :param status: 采购需求状态
        :param list order_no: 备货计划单号或缺货需求编码
        :return:采购需求id列表
        """
        content = deepcopy(SCMApiConfig.GetPurchaseDemandPage.get_attributes())
        content["data"].update({
            "orderNos": [order_no],
            "status": status
        })
        res = self.call_api(**content)
        result = self.formatted_result(res)
        if not result["code"]:
            return
        purchase_demand_id_list = [demand["id"] for demand in res["data"]["list"]]
        return purchase_demand_id_list

    def get_purchase_demand_detail(self, purchase_demand_id):
        """获取采购需求详情"""
        content = deepcopy(SCMApiConfig.GetPurchaseDemandDetail.get_attributes())
        content["uri_path"] += str(purchase_demand_id)
        res = self.call_api(**content)
        return self.formatted_result(res)

    def batch_get_purchase_demand_detail(self, purchase_demand_id_list):
        """获取采购需求详情"""
        content = deepcopy(SCMApiConfig.BatchGetPurchaseDemandDetail.get_attributes())
        content.update({"data": purchase_demand_id_list})
        res = self.call_api(**content)
        return self.formatted_result(res)

    def confirm_and_generate_purchase_order(self, purchase_demand_id_list):
        """采购需求确认并生单"""
        # 详情获取到的数据和确认并生单要提交的数据格式不一致，主要是product info有差异。
        # 用详情获取到的构建提交的，目标格式："productInfo"：{"details":xxx,"totalPrice": xxx]}
        purchase_demand_detail_result = self.batch_get_purchase_demand_detail(purchase_demand_id_list)
        if not purchase_demand_detail_result["code"]:
            return {"code": 0, "msg": "获取采购需求明细失败！", "data": ""}
        purchase_demand_detail_list = purchase_demand_detail_result["data"]
        for purchase_demand_detail in purchase_demand_detail_list:
            temp_product_info = purchase_demand_detail["productInfos"]
            product_infos = {
                "details": temp_product_info,
                "totalPrice": purchase_demand_detail["totalAmount"]
            }
            purchase_demand_detail.update({"productInfo": product_infos})
            del purchase_demand_detail["productInfos"]
        content = deepcopy(SCMApiConfig.ConfirmAndGeneratePurchaseOrder.get_attributes())
        content.update({"data": purchase_demand_detail_list})
        res = self.call_api(**content)
        return self.formatted_result(res)

    def get_purchase_order_page(self, order_no="", purchase_order_no=""):
        content = deepcopy(SCMApiConfig.GetPurchaseOrderPage.get_attributes())
        if order_no:
            content["data"].update({
                "stockOrderNos": [order_no]
            })
        if purchase_order_no:
            content["data"].update({
                "purchaseOrderNos": [purchase_order_no]
            })
        res = self.call_api(**content)
        return self.formatted_result(res)

    def get_purchase_order_detail(self, purchase_order_id):
        """获取采购订单详情"""
        content = deepcopy(SCMApiConfig.GetPurchaseOrderDetail.get_attributes())
        content.update({"uri_path": content["uri_path"] % purchase_order_id})

        res = self.call_api(**content)
        return self.formatted_result(res)

    def update_and_submit_purchase_order_to_audit(self, purchase_order_detail):
        """采购订单更新并提交审核"""
        purchase_order_detail.update({"operation": 2})

        content = deepcopy(SCMApiConfig.PurchaseOrderUpdate.get_attributes())
        content.update({"data": purchase_order_detail})
        res = self.call_api(**content)
        return self.formatted_result(res)

    def purchase_order_audit(self, purchase_order_id_list):
        """采购订单批量审核"""
        content = deepcopy(SCMApiConfig.PurchaseOrderBatchAudit.get_attributes())
        content["data"].update({
            "ids": purchase_order_id_list
        })
        res = self.call_api(**content)
        return self.formatted_result(res)

    def purchase_order_batch_buy(self, purchase_order_id_list):
        """采购订单下单"""
        content = deepcopy(SCMApiConfig.PurchaseOrderBatchBuy.get_attributes())
        content.update({
            "data": purchase_order_id_list
        })
        res = self.call_api(**content)
        return self.formatted_result(res)

    def get_purchase_order_delivery_detail(self, purchase_order_id):
        """获取采购订单详情"""
        content = deepcopy(SCMApiConfig.GetPurchaseOrderDeliveryDetail.get_attributes())
        content["data"].update({
            "ids": [purchase_order_id]
        })
        res = self.call_api(**content)
        return self.formatted_result(res)

    def generate_distribute_order(self, purchase_order_delivery_detail, delivery_warehouse_code):
        """生成分货单"""
        for detail in purchase_order_delivery_detail:
            detail.update({
                "fix": True,
                "currentSentQuantity": detail["unsentQuantity"],
                "currentSentExternalQuantity": detail["unsentQuantity"],
                "deliveryWarehouse": delivery_warehouse_code
            })
        content = deepcopy(SCMApiConfig.GenerateDistributeOrder.get_attributes())
        content.update({
            "data": purchase_order_delivery_detail
        })
        res = self.call_api(**content)
        return self.formatted_result(res)

    def purchase_order_delivery(self, distribute_order_info):
        """采购单发货"""
        distribute_order_info.update(
            {"logisticsInfos": []}
        )
        content = deepcopy(SCMApiConfig.PurchaseOrderDelivery.get_attributes())
        content["data"].update(distribute_order_info)
        res = self.call_api(**content)
        return self.formatted_result(res)

    def get_distribute_order_page(self, purchase_order_nos):
        """分货单查询"""
        content = deepcopy(SCMApiConfig.GetDistributeOrderPage.get_attributes())
        content["data"].update({
            "purchaseOrderNos": purchase_order_nos
        })
        res = self.call_api(**content)
        # distribute_order_nos = [distribute_order["shippingOrderNo"] for distribute_order in res["data"]["list"]]
        return self.formatted_result(res)

    def get_distribute_order_detail(self, purchase_order_id):
        """分货单明细查询"""
        content = deepcopy(SCMApiConfig.GetDistributeOrderDetail.get_attributes())
        content["data"].update({
            "id": purchase_order_id
        })
        res = self.call_api(**content)
        # distribute_order_nos = [distribute_order["shippingOrderNo"] for distribute_order in res["data"]["list"]]
        return self.formatted_result(res)
