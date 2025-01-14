import json
import time

from utils.log_handler import logger as log
from utils.code_handler import GenerateCode
from cases import scm_app


class ScmDataGenerator:
    def __init__(self):
        self.scm_app = scm_app

    def create_stock_plan(self, sale_sku_list, num, delivery_warehouse_code, target_warehouse_code):
        """
        生成备货计划数据

        :param list sale_sku_list: 销售sku编码的数组
        :param int num: 采购的套数
        :param string delivery_warehouse_code: 收货仓库编码
        :param string target_warehouse_code: 目的仓库编码
        :return: 备货计划id、备货计划单号
        """
        plan_res = self.scm_app.stock_plan_submit(sale_sku_list, num, delivery_warehouse_code, target_warehouse_code)
        if not plan_res['code']:
            log.error('创建备货计划失败：%s' % plan_res)
            return
        stock_plan_id = plan_res['data']['id']
        plan_no = plan_res['data']['stockPlanNumber']
        print('备货计划单号：%s' % plan_no)
        print('备货计划id：%s' % stock_plan_id)
        return stock_plan_id, plan_no

    def create_purchase_demand(self, sale_sku_list, num, delivery_warehouse_code, target_warehouse_code):
        """
        创建备货计划并执行审核，生成采购需求

        :param list sale_sku_list: 销售sku编码的数组
        :param int num: 采购的套数
        :param string delivery_warehouse_code: 收货仓库编码
        :param string target_warehouse_code: 目的仓库编码
        :return: 采购需求id列表，备货计划单号
        """
        # 创建备货计划
        plan_id, plan_no = self.create_stock_plan(sale_sku_list, num, delivery_warehouse_code, target_warehouse_code)
        # 执行审核
        audit_result = self.scm_app.stock_plan_batch_audit(plan_id)
        if not audit_result['code']:
            log.error('备货计划审核失败：%s' % audit_result)
            return
        # 备货计划生成采购需求是异步的，可能存在延迟
        time.sleep(1)
        # 获取生成的采购需求id
        demand_ids = self.scm_app.get_purchase_demand_id(plan_no)
        if not demand_ids:
            log.error('查询不到创建的备货计划的采购需求id')
            return
        print('备货计划单号：%s' % plan_no)
        print('采购需求id：%s' % demand_ids)
        return demand_ids, plan_no

    def create_purchase_order(self, sale_sku_list, num, delivery_warehouse_code, target_warehouse_code):
        """
        创建备货计划并执行审核，生成采购需求,采购需求确认并生单，生成采购单

        :param list sale_sku_list: 销售sku编码的数组
        :param int num: 采购的套数
        :param string delivery_warehouse_code: 收货仓库编码
        :param string target_warehouse_code: 目的仓库编码
        :return: 采购单号列表、采购单id列表
        """
        # 创建备货计划
        demand_ids, plan_no = self.create_purchase_demand(sale_sku_list, num, delivery_warehouse_code,
                                                          target_warehouse_code)
        if not demand_ids:
            log.error('查询不到创建的备货计划的采购需求id')
            return
        # 根据采购需求id批量确认并生单
        confirm_and_buy_res = self.scm_app.confirm_and_generate_purchase_order(demand_ids)
        if not confirm_and_buy_res["code"]:
            log.error("采购需求确认并生单失败：%s" % confirm_and_buy_res)
        # 采购需求下单是异步，可能有延迟
        time.sleep(3)
        purchase_order_page_result = self.scm_app.get_purchase_order_page(order_no=plan_no)
        if not purchase_order_page_result["code"]:
            log.error("根据备货计划单号查询采购单号失败")
            return
        purchase_order_list = [(
            purchase_order["id"],
            purchase_order["purchaseOrderNo"]
        ) for purchase_order in purchase_order_page_result["data"]["list"]]
        print('采购订单id、采购订单号：%s' % purchase_order_list)
        return purchase_order_list

    def create_wait_delivery_purchase_order(self, sale_sku_list, num, delivery_warehouse_code, target_warehouse_code):
        """
        生成采购订单，并批量发货生成分货单,最终推送WMS生成采购入库单

        :param list sale_sku_list: 销售sku编码的数组
        :param int num: 采购的套数
        :param string delivery_warehouse_code: 收货仓库编码
        :param string target_warehouse_code: 目的仓库编码
        :return: list 分货单列表
        """
        purchase_order_list = self.create_purchase_order(
            sale_sku_list,
            num,
            delivery_warehouse_code,
            target_warehouse_code)

        purchase_order_ids = [_[0] for _ in purchase_order_list]
        purchase_order_nos = [_[1] for _ in purchase_order_list]
        # 逐个采购订单编辑并提交审核
        for purchase_order_id in purchase_order_ids:
            purchase_order_detail_result = self.scm_app.get_purchase_order_detail(purchase_order_id)
            if not purchase_order_detail_result["code"]:
                return
            purchase_order_detail = purchase_order_detail_result["data"]
            purchase_way = json.loads(purchase_order_detail.get("supplierInfo").get("purchaseWay")).get("code")
            purchase_order_detail["supplierInfo"]["purchaseWay"] = purchase_way
            update_and_submit_to_audit_res = self.scm_app.update_and_submit_purchase_order_to_audit(
                purchase_order_detail)
            if not update_and_submit_to_audit_res["code"]:
                log.error('采购订单编辑并提交审核失败')
                return
        # 采购订单批量审核
        audit_res = self.scm_app.purchase_order_audit(purchase_order_ids)
        if not audit_res["code"]:
            log.error('采购订单批量审核失败:%s' % audit_res)
            return
        # 采购订单批量下单
        purchase_order_buy_res = self.scm_app.purchase_order_batch_buy(purchase_order_ids)
        if not purchase_order_buy_res["code"]:
            log.error('采购订单批量下单失败:%s' % purchase_order_buy_res)
            return
        return purchase_order_nos, purchase_order_ids

    def create_distribute_order(self, sale_sku_list, num, delivery_warehouse_code, target_warehouse_code):
        """
        生成采购订单，并批量发货生成分货单,最终推送WMS生成采购入库单

        :param list sale_sku_list: 销售sku编码的数组
        :param int num: 采购的套数
        :param string delivery_warehouse_code: 收货仓库编码
        :param string target_warehouse_code: 目的仓库编码
        :return: list 分货单列表
        """
        # 调用创建待发货采购单
        purchase_order_nos, purchase_order_ids = self.create_wait_delivery_purchase_order(sale_sku_list, num,
                                                                                          delivery_warehouse_code,
                                                                                          target_warehouse_code)
        # 采购订单批量发货
        for purchase_order_id in purchase_order_ids:
            # 获取采购订单发货明细
            delivery_detail_result = self.scm_app.get_purchase_order_delivery_detail(purchase_order_id)
            if not delivery_detail_result["code"]:
                log.error('获取采购单发货详情失败')
                return
            purchase_order_delivery_detail = delivery_detail_result["data"]["list"]
            # 根据采购订单发货明细生成分货单信息
            generate_result = self.scm_app.generate_distribute_order(purchase_order_delivery_detail,
                                                                     delivery_warehouse_code)
            if not generate_result["code"]:
                log.error('根据采购单发货详情生成分货单信息失败')
                return
            distribute_order_info = generate_result["data"]

            # 采购订单发货
            delivery_res = self.scm_app.purchase_order_delivery(distribute_order_info)
            if not delivery_res["code"]:
                log.error("采购订单发货失败：%s" % delivery_res)
                return
        time.sleep(1)
        # 获取分货单号
        distribute_order_result = self.scm_app.get_distribute_order_page(purchase_order_nos)
        if not distribute_order_result["code"]:
            log.error("获取分货单列表失败：%s" % distribute_order_result)
            return
        distribute_order_list = distribute_order_result["data"]["list"]

        result_distribute_order_list = [
            (
                _["shippingOrderNo"],
                _["deliveryWarehouse"],
                _["destinationWarehouse"]
            ) for _ in distribute_order_list]

        for distribute_order in distribute_order_list:
            distribute_order_detail = self.scm_app.get_distribute_order_detail(distribute_order["id"])
            distribute_order_code = distribute_order_detail["data"]["shippingOrderNo"]
            GenerateCode("barcode", "distribute_order", distribute_order_code)
            if not self.scm_app.is_success(distribute_order_detail):
                continue
            sku_list = distribute_order_detail.get("data").get("skuInfos").get("list")
            for sku_info in sku_list:
                bom_detail = json.loads(sku_info["bomDetail"])
                for bom_detail_item in bom_detail:
                    ware_sku_code = bom_detail_item["waresSku"]
                    sku_label_info = {"SKU_CODE": ware_sku_code, "SOURCE_ORDER_CODE": distribute_order_code}
                    GenerateCode("qrcode", "distribute_order", json.dumps(sku_label_info))
        print('分货单列表：%s' % result_distribute_order_list)
        return result_distribute_order_list


if __name__ == '__main__':
    scm = ScmDataGenerator()

    # scm.create_purchase_order(["14093131604"], 10, 'ESBH', '')
    # scm.create_stock_plan(['14093131604'], 10 ,'ESBH', '')
    # scm.create_purchase_demand(['14093131604'], 10, 'ESBH', '')
    # scm.create_wait_delivery_purchase_order(["14093131604"], 10, 'ESBH', '')

    scm.create_distribute_order(["HW929O38V1"], 20, 'HWBH', '')
