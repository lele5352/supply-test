import time

from controller.scm_controller import ScmController
from data_generator import ums
from utils.log_handler import logger as log


class ScmDataGenerator():
    def __init__(self):
        self.scm = ScmController(ums)

    def create_stock_plan(self, sale_sku_list, num, delivery_warehouse, destination_warehouse):
        """生成备货计划数据"""
        stock_plan_res = self.scm.stock_plan_submit(sale_sku_list, num, delivery_warehouse, destination_warehouse)
        if not stock_plan_res or stock_plan_res['code'] != 200:
            log.error('创建备货计划失败：%s' % stock_plan_res)
            return
        stock_plan_id = stock_plan_res['data']['id']
        stock_plan_no = stock_plan_res['data']['stockPlanNumber']
        return stock_plan_id, stock_plan_no

    def create_purchase_demand(self, sale_sku_list, num, delivery_warehouse, destination_warehouse):
        """创建备货计划并执行审核，生成采购需求"""
        # 创建备货计划
        stock_plan_id, stock_plan_no = self.create_stock_plan(
            sale_sku_list,
            num,
            delivery_warehouse,
            destination_warehouse)
        # 执行审核
        audit_res = self.scm.stock_plan_batch_audit(stock_plan_id)
        if not audit_res or audit_res['code'] != 200:
            log.error('备货计划审核失败：%s' % audit_res)
            return
        # 备货计划生成采购需求是异步的，可能存在延迟
        time.sleep(1)
        # 获取生成的采购需求id
        purchase_demand_ids = self.scm.get_stock_plan_purchase_demand_id(stock_plan_no)
        if not purchase_demand_ids:
            log.error('查询不到创建的备货计划的采购需求id')
            return
        return purchase_demand_ids, stock_plan_no

    def create_purchase_order(self, sale_sku_list, num, delivery_warehouse, destination_warehouse):
        """创建备货计划并执行审核，生成采购需求,采购需求确认并生单，生成采购单"""
        # 创建备货计划
        purchase_demand_ids, stock_plan_no = self.create_purchase_demand(sale_sku_list, num, delivery_warehouse,
                                                                         destination_warehouse)
        if not purchase_demand_ids:
            log.error('查询不到创建的备货计划的采购需求id')
            return
        # 根据采购需求id批量确认并生单
        confirm_and_buy_res = self.scm.confirm_and_generate_purchase_order(purchase_demand_ids)
        if not confirm_and_buy_res:
            log.error("采购需求确认并生单失败：%s" % confirm_and_buy_res)
        # 采购需求下单是异步，可能有延迟
        time.sleep(1)
        purchase_order_nos, purchase_order_ids = self.scm.get_purchase_order_page(stock_plan_no)
        if not (purchase_order_ids and purchase_order_nos):
            log.error("根据备货计划单号查询采购单号失败")
        return purchase_order_nos, purchase_order_ids

    def create_distribute_order(self, sale_sku_list, num, delivery_warehouse, destination_warehouse):
        purchase_order_nos, purchase_order_ids = self.create_purchase_order(
            sale_sku_list,
            num,
            delivery_warehouse,
            destination_warehouse)
        # 逐个采购订单编辑并提交审核
        for purchase_order_id in purchase_order_ids:
            purchase_order_detail = self.scm.get_purchase_order_detail(purchase_order_id)
            update_and_submit_to_audit_res = self.scm.update_and_submit_purchase_order_to_audit(purchase_order_detail)
            if not update_and_submit_to_audit_res:
                log.error('采购订单编辑并提交审核失败')
                return
        # 采购订单批量审核
        audit_res = self.scm.purchase_order_audit(purchase_order_ids)
        if not audit_res:
            log.error('采购订单批量审核失败:%s' % audit_res)
            return
        # 采购订单批量下单
        purchase_order_buy_res = self.scm.purchase_order_batch_buy(purchase_order_ids)
        if not purchase_order_buy_res:
            log.error('采购订单批量下单失败:%s' % purchase_order_buy_res)
            return
        # 采购订单批量发货
        for purchase_order_id in purchase_order_ids:
            purchase_order_delivery_detail = self.scm.get_purchase_order_delivery_detail(purchase_order_id)
            if not purchase_order_delivery_detail:
                log.error('获取采购单发货详情失败')
                return
            distribute_order_info = self.scm.generate_distribute_order(purchase_order_delivery_detail,
                                                                       delivery_warehouse)
            if not distribute_order_info:
                log.error('根据采购单发货详情生成分货单信息失败')
                return
            delivery_res = self.scm.purchase_order_delivery(distribute_order_info)
            if not delivery_res:
                log.error("采购订单发货失败：%s" % delivery_res)
                return
        time.sleep(1)
        distribute_order_nos = self.scm.get_distribute_order_page(purchase_order_nos)
        return distribute_order_nos


if __name__ == '__main__':
    data_generator = ScmDataGenerator()
    sale_sku_list = ['63203684930', 'J04MDG000218034']
    sale_sku_num = 2
    destination_warehouse = 'ESFH'
    delivery_warehouse = 'ESZZ'
    res = data_generator.create_distribute_order(sale_sku_list, sale_sku_num, delivery_warehouse,
                                                 destination_warehouse)
    print(res)
