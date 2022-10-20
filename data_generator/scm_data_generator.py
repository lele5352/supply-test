import time

from robots.scm_robot import SCMRobot
from utils.log_handler import logger as log
from utils.barcode_handler import barcode_generate


class ScmDataGenerator:
    def __init__(self):
        self.scm_robot = SCMRobot()

    def create_stock_plan(self, sale_sku_list, num, delivery_warehouse_code, target_warehouse_code):
        """
        生成备货计划数据

        :param list sale_sku_list: 销售sku编码的数组
        :param int num: 采购的套数
        :param string delivery_warehouse_code: 收货仓库编码
        :param string target_warehouse_code: 目的仓库编码
        :return: 备货计划id、备货计划单号
        """
        plan_res = self.scm_robot.stock_plan_submit(sale_sku_list, num, delivery_warehouse_code,
                                                    target_warehouse_code)
        if not plan_res or plan_res['code'] != 200:
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
        audit_res = self.scm_robot.stock_plan_batch_audit(plan_id)
        if not audit_res or audit_res['code'] != 200:
            log.error('备货计划审核失败：%s' % audit_res)
            return
        # 备货计划生成采购需求是异步的，可能存在延迟
        time.sleep(1)
        # 获取生成的采购需求id
        demand_ids = self.scm_robot.get_stock_plan_purchase_demand_id(plan_no)
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
        confirm_and_buy_res = self.scm_robot.confirm_and_generate_purchase_order(demand_ids)
        if not confirm_and_buy_res:
            log.error("采购需求确认并生单失败：%s" % confirm_and_buy_res)
        # 采购需求下单是异步，可能有延迟
        time.sleep(1)
        purchase_order_nos, purchase_order_ids = self.scm_robot.get_purchase_order_page(plan_no)
        if not (purchase_order_ids and purchase_order_nos):
            log.error("根据备货计划单号查询采购单号失败")
        print('采购订单单号：%s' % purchase_order_nos)
        print('采购订单id：%s' % purchase_order_ids)
        return purchase_order_nos, purchase_order_ids

    def create_wait_delivery_purchase_order(self, sale_sku_list, num, delivery_warehouse_code, target_warehouse_code):
        """
        生成采购订单，并批量发货生成分货单,最终推送WMS生成采购入库单

        :param list sale_sku_list: 销售sku编码的数组
        :param int num: 采购的套数
        :param string delivery_warehouse_code: 收货仓库编码
        :param string target_warehouse_code: 目的仓库编码
        :return: list 分货单列表
        """
        purchase_order_nos, purchase_order_ids = self.create_purchase_order(
            sale_sku_list,
            num,
            delivery_warehouse_code,
            target_warehouse_code)
        # 逐个采购订单编辑并提交审核
        for purchase_order_id in purchase_order_ids:
            purchase_order_detail = self.scm_robot.get_purchase_order_detail(purchase_order_id)
            update_and_submit_to_audit_res = self.scm_robot.update_and_submit_purchase_order_to_audit(
                purchase_order_detail)
            if not update_and_submit_to_audit_res:
                log.error('采购订单编辑并提交审核失败')
                return
        # 采购订单批量审核
        audit_res = self.scm_robot.purchase_order_audit(purchase_order_ids)
        if not audit_res:
            log.error('采购订单批量审核失败:%s' % audit_res)
            return
        # 采购订单批量下单
        purchase_order_buy_res = self.scm_robot.purchase_order_batch_buy(purchase_order_ids)
        if not purchase_order_buy_res:
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
        purchase_order_nos, purchase_order_ids = self.create_purchase_order(
            sale_sku_list,
            num,
            delivery_warehouse_code,
            target_warehouse_code)
        # 逐个采购订单编辑并提交审核
        for purchase_order_id in purchase_order_ids:
            purchase_order_detail = self.scm_robot.get_purchase_order_detail(purchase_order_id)
            update_and_submit_to_audit_res = self.scm_robot.update_and_submit_purchase_order_to_audit(
                purchase_order_detail)
            if not update_and_submit_to_audit_res:
                log.error('采购订单编辑并提交审核失败')
                return
        # 采购订单批量审核
        audit_res = self.scm_robot.purchase_order_audit(purchase_order_ids)
        if not audit_res:
            log.error('采购订单批量审核失败:%s' % audit_res)
            return
        # 采购订单批量下单
        purchase_order_buy_res = self.scm_robot.purchase_order_batch_buy(purchase_order_ids)
        if not purchase_order_buy_res:
            log.error('采购订单批量下单失败:%s' % purchase_order_buy_res)
            return
        # 采购订单批量发货
        for purchase_order_id in purchase_order_ids:
            # 获取采购订单发货明细
            purchase_order_delivery_detail = self.scm_robot.get_purchase_order_delivery_detail(purchase_order_id)
            if not purchase_order_delivery_detail:
                log.error('获取采购单发货详情失败')
                return
            # 根据采购订单发货明细生成分货单信息
            distribute_order_info = self.scm_robot.generate_distribute_order(purchase_order_delivery_detail,
                                                                             delivery_warehouse_code)
            if not distribute_order_info:
                log.error('根据采购单发货详情生成分货单信息失败')
                return
            # 采购订单发货
            delivery_res = self.scm_robot.purchase_order_delivery(distribute_order_info)
            if not delivery_res:
                log.error("采购订单发货失败：%s" % delivery_res)
                return
        time.sleep(1)
        # 获取分货单号
        distribute_order_nos = self.scm_robot.get_distribute_order_page(purchase_order_nos)
        # for code in distribute_order_nos:
        # barcode_generate(code, 'entry_order')
        print('分货单号：%s' % distribute_order_nos)
        return distribute_order_nos


if __name__ == '__main__':
    scm = ScmDataGenerator()

    # scm.create_distribute_order(["14093131604"], 10, 'ESBH', '')
    # scm.create_stock_plan(['14093131604'], 10 ,'ESBH', '')
    # scm.create_purchase_demand(['14093131604'], 10, 'ESBH', '')
    scm.create_distribute_order(["63203684930"], 1, 'ESZZ', 'ESFH')
