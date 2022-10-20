from robots.wms_robot import WMSTransferServiceRobot, WMSAppRobot
from robots.ims_robot import IMSRobot

from utils.log_handler import logger as log
from utils.barcode_handler import barcode_generate
from dbo.ims_dbo import IMSDBOperator


class WmsTransferDataGenerator:
    def __init__(self):
        self.wms_app_robot = WMSAppRobot()
        self.wms_transfer_robot = WMSTransferServiceRobot()
        self.ims_robot = IMSRobot()

    def create_transfer_demand(self, trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id, sale_sku_code,
                               trans_qty, demand_type=1, customer_type=1, remark=''):
        """
        创建调拨需求

        :param int trans_out_id: 调出仓库id
        :param int trans_in_id: 调入仓库id
        :param int trans_out_to_id: 调出仓库的目的仓id
        :param int trans_in_to_id: 调入仓库的目的仓id
        :param string sale_sku_code: 调拨的商品的销售sku
        :param int trans_qty: 调拨数量
        :param int demand_type: 调拨类型
        :param int customer_type: 客户类型：1-普通客户；2-大客户
        :param string remark: 备注
        """
        self.wms_app_robot.switch_default_warehouse(trans_out_id)

        central_inventory = IMSDBOperator.query_central_inventory(sale_sku_code, trans_out_id, trans_out_to_id)
        # print(central_inventory)
        # 可用库存不足，需要添加库存，分为2种情况：1-查询不到库存；2-查询到库存，block＞stock
        if not central_inventory or central_inventory['remain'] <= 0:
            bom_detail = IMSDBOperator.query_bom_detail(sale_sku_code, 'A')
            kw_ids = self.wms_app_robot.get_kw(1, 5, len(bom_detail), trans_out_id, trans_out_to_id)
            add_stock_res = self.ims_robot.add_lp_stock_by_other_in(
                sale_sku_code,
                'A',
                trans_qty,
                kw_ids,
                trans_out_id,
                trans_out_to_id)
            if not add_stock_res:
                log.error('创建调拨需求失败：加库存失败！')
                return
        trans_out_code = self.wms_app_robot.ck_id_to_code(trans_out_id)
        trans_out_to_code = self.wms_app_robot.ck_id_to_code(trans_out_to_id)
        trans_in_code = self.wms_app_robot.ck_id_to_code(trans_in_id)
        trans_in_to_code = self.wms_app_robot.ck_id_to_code(trans_in_to_id)
        # 调用创建调拨需求接口
        create_demand_res = self.wms_transfer_robot.transfer_out_create_demand(
            trans_out_code,
            trans_out_to_code,
            trans_in_code,
            trans_in_to_code,
            sale_sku_code,
            trans_qty,
            demand_type,
            customer_type,
            remark)
        if not create_demand_res or create_demand_res['code'] != 1:
            log.error('创建调拨需求失败！')
            return
        print('生成调拨需求：%s' % create_demand_res['data']['demandCode'])
        return create_demand_res['data']['demandCode']

    def create_transfer_pick_order(self, trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id, sale_sku_code,
                                   demand_qty, demand_type=1, customer_type=1, remark=''):
        """
        生成调拨拣货单

        :param int trans_out_id: 调出仓库id
        :param int trans_in_id: 调入仓库id
        :param int trans_out_to_id: 调出仓库的目的仓id，仅调出仓为中转仓时必填
        :param int trans_in_to_id: 调入仓库的目的仓id，仅调入仓为中转仓时必填
        :param string sale_sku_code: 调拨的商品的销售sku
        :param int demand_qty: 调拨数量
        :param int demand_type: 调拨类型
        :param int customer_type: 客户类型：1-普通客户；2-大客户
        :param string remark: 备注
        """
        self.wms_app_robot.switch_default_warehouse(trans_out_id)
        # 生成调拨需求
        demand_no = self.create_transfer_demand(
            trans_out_id,
            trans_out_to_id,
            trans_in_id,
            trans_in_to_id,
            sale_sku_code,
            demand_qty,
            demand_type,
            customer_type,
            remark
        )
        # 创建调拨拣货单
        pick_order_res = self.wms_app_robot.transfer_out_create_pick_order([demand_no], 1)
        if not pick_order_res or pick_order_res['code'] != 1:
            print('创建调拨拣货单失败！')
            log.error('创建调拨拣货单失败！')
            return
        pick_order_code = pick_order_res['data']
        print('生成调拨拣货单：%s' % pick_order_code)
        return pick_order_code

    def create_transfer_out_order(self, trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id, sale_sku_code,
                                  demand_qty, demand_type=1, customer_type=1, remark=''):
        """
        生成调拨出库单

        :param int trans_out_id: 调出仓库id
        :param int trans_in_id: 调入仓库id
        :param any trans_out_to_id: 调出仓库的目的仓id，仅调出仓为中转仓时必填
        :param any trans_in_to_id: 调入仓库的目的仓id，仅调入仓为中转仓时必填
        :param string sale_sku_code: 调拨的商品的销售sku
        :param int demand_qty: 调拨数量
        :param int demand_type: 调拨类型
        :param int customer_type: 客户类型：1-普通客户；2-大客户
        :param string remark: 备注
        """
        # 生成调拨需求
        demand_no = self.create_transfer_demand(
            trans_out_id,
            trans_out_to_id,
            trans_in_id,
            trans_in_to_id,
            sale_sku_code,
            demand_qty,
            demand_type,
            customer_type,
            remark
        )
        if not demand_no:
            print('创建调拨拣货单失败')
            return
        # 创建调拨拣货单
        create_pick_order_result = self.wms_app_robot.transfer_out_create_pick_order([demand_no], 1)
        if not create_pick_order_result['code']:
            return
        pick_order_code = create_pick_order_result['data']

        # 分配调拨拣货人
        pick_order_assign_result = self.wms_app_robot.transfer_out_pick_order_assign([pick_order_code], 'admin', 1)
        if not pick_order_assign_result['code']:
            return
        # 获取调拨拣货单详情数据
        pick_order_details_result = self.wms_app_robot.transfer_out_pick_order_detail(pick_order_code)
        if not pick_order_details_result['code']:
            return
        pick_order_details = pick_order_details_result['data']['details']

        # 获取拣货单sku详情数据
        pick_sku_list = self.wms_app_robot.get_pick_sku_list(pick_order_details)

        # 调拨拣货单确认拣货-纸质
        confirm_pick_result = self.wms_app_robot.transfer_out_confirm_pick(pick_order_code, pick_order_details)
        if not confirm_pick_result['code']:
            return
        get_trans_out_tp_kw_ids_result = self.wms_app_robot.get_kw(1, 3, len(pick_sku_list), trans_out_id,
                                                                   trans_out_to_id)
        trans_out_tp_kw_ids = get_trans_out_tp_kw_ids_result['data']
        # 调拨拣货单按需装托提交
        submit_tray_result = self.wms_app_robot.transfer_out_submit_tray(pick_order_code, pick_order_details,
                                                                         trans_out_tp_kw_ids)
        if not submit_tray_result['code']:
            return
        # 查看整单获取已装托的托盘
        tray_detail_result = self.wms_app_robot.transfer_out_pick_order_tray_detail(pick_order_code)
        tray_code_list = [tray['storageLocationCode'] for tray in tray_detail_result['data']]

        # 获取生成的调拨出库单号
        finish_result = self.wms_app_robot.transfer_out_finish_packing(pick_order_code, tray_code_list)
        if not finish_result['code']:
            return
        transfer_out_order_no = finish_result['data']

        # 获取调拨出库单明细
        transfer_out_order_detail_result = self.wms_app_robot.transfer_out_order_detail(transfer_out_order_no)
        if not transfer_out_order_detail_result['code']:
            return
        transfer_out_order_detail = transfer_out_order_detail_result['data']['details']

        # 从调拨出库单明细中提取箱单和库位编码对应关系
        details = [(_['boxNo'], _['storageLocationCode']) for _ in transfer_out_order_detail]
        sorted_details = sorted(details, key=lambda a: a[1])
        # 按箱单和托盘对应逐个复核
        for box_no, tray_code in details:
            review_result = self.wms_app_robot.transfer_out_order_review(box_no, tray_code)
            if not review_result['code']:
                return
        for detail in details:
            bind_result = self.wms_app_robot.transfer_out_box_bind(detail[0], '', '')  # 交接单号和收货仓编码实际可以不用传
            handover_no = bind_result['data']['handoverNo']

        delivery_result = self.wms_app_robot.transfer_out_delivery(handover_no)
        if not delivery_result['code']:
            return
        print("创建调拨出库成功,调拨出库单号：%s" % transfer_out_order_no)
        return True


if __name__ == '__main__':
    transfer_data = WmsTransferDataGenerator()
    demand_qty = 1
    # transfer_data.create_transfer_out_order(512, '', 513, 513, '63203684930', 2)
    # transfer_data.create_transfer_demand(512, '', 513, 513, '14093131604', 10)
    transfer_data.create_transfer_out_order(512, 0, 513, 513, '63203684930', 1)
    # transfer_data.create_transfer_pick_order(512, '', 513, 513, '63203684930', 2)
