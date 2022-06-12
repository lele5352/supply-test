from data_generator import *
from utils.log_handler import logger as log
from utils.barcode_handler import barcode_generate
from db_operator.ims_db_operator import IMSDBOperator


class WmsTransferDataGenerator:
    def __init__(self):
        self.wms_request = wms_request
        self.ims_request = ims_request
        self.wms_logics = wms_logics
        self.ims_logics = ims_logics

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
        self.wms_request.switch_default_warehouse(trans_out_id)

        central_inventory = IMSDBOperator.query_central_inventory(sale_sku_code, trans_out_id, trans_out_to_id)
        # print(central_inventory)
        # 可用库存不足，需要添加库存，分为2种情况：1-查询不到库存；2-查询到库存，block＞stock
        if not central_inventory or central_inventory['remain'] <= 0:
            bom_detail = IMSDBOperator.query_bom_detail(sale_sku_code, 'A')
            add_stock_res = self.ims_logics.add_lp_stock_by_other_in(
                sale_sku_code,
                'A',
                trans_qty,
                self.wms_logics.get_kw(1, 5, len(bom_detail)+1, trans_out_id, trans_out_to_id),
                trans_out_id,
                trans_out_to_id)
            if not add_stock_res:
                log.error('创建调拨需求失败：加库存失败！')
                return
        # 调用创建调拨需求接口
        create_demand_res = self.wms_request.transfer_out_create_demand(
            trans_out_id,
            trans_out_to_id,
            trans_in_id,
            trans_in_to_id,
            sale_sku_code,
            trans_qty,
            demand_type,
            customer_type,
            remark)
        if not create_demand_res or create_demand_res['code'] != 200:
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
        self.wms_request.switch_default_warehouse(trans_out_id)
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
        pick_order_res = self.wms_request.transfer_out_create_pick_order([demand_no], 1)
        if not pick_order_res or pick_order_res['code'] != 200:
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
        # 创建调拨拣货单
        pick_order_res = self.wms_request.transfer_out_create_pick_order([demand_no], 1)
        if not pick_order_res or pick_order_res['code'] != 200:
            print('创建调拨拣货单失败！')
            log.error('创建调拨拣货单失败！')
            return
        pick_order_code = pick_order_res['data']
        print('生成调拨拣货单：%s' % pick_order_code)

        # barcode_generate(pick_order_code, 'transfer/pick_order')

        # 分配调拨拣货人
        assign_pick_user_res = self.wms_request.transfer_out_pick_order_assign([pick_order_code], 'admin', 1)
        if not assign_pick_user_res:
            log.error('创建调拨出库单失败：分配拣货人异常！')
            return
        # 获取调拨拣货单详情数据
        pick_order_details_res = self.wms_request.transfer_out_pick_order_detail(pick_order_code)
        if not pick_order_details_res:
            log.error('创建调拨出库单失败：获取拣货单详情数据异常！')
            return
        pick_order_details = pick_order_details_res['details']
        # 调拨拣货单确认拣货-纸质
        confirm_pick_res = self.wms_request.transfer_out_confirm_pick(pick_order_code, pick_order_details)
        if not confirm_pick_res:
            log.error('创建调拨出库单失败：确认拣货异常！')
            return
        # 调拨拣货单按需装托提交
        trans_out_tp_kw_ids = self.wms_logics.get_kw(1, 3, demand_qty, trans_out_id, trans_out_to_id)
        submit_tray_res = self.wms_request.transfer_out_submit_tray(pick_order_code, pick_order_details,
                                                                    trans_out_tp_kw_ids)
        if not submit_tray_res:
            log.error('创建调拨出库单失败：装托完成异常！')
            return
        # 查看整单获取已装托的托盘
        tray_detail_res = self.wms_request.transfer_out_pick_order_tray_detail(pick_order_code)
        if not tray_detail_res:
            log.error('创建调拨出库单失败：获取已装托的托盘明细数据异常！')
            return
        tray_list = [tray['storageLocationCode'] for tray in tray_detail_res['data']]

        finish_packing_res = self.wms_request.transfer_out_finish_packing(pick_order_code, tray_list)
        if not finish_packing_res:
            log.error('创建调拨出库单失败：创建调拨出库单异常！')
            return
        # 获取生成的调拨出库单号
        transfer_out_order_no = finish_packing_res['data']
        print('生成调拨出库单：%s' % transfer_out_order_no)
        # barcode_generate(transfer_out_order_no, 'transfer/trans_out_order')
        transfer_out_order_detail_res = self.wms_request.transfer_out_order_detail(transfer_out_order_no)
        if not transfer_out_order_detail_res:
            log.error('创建调拨出库单失败：获取调拨出库单详情数据异常！')
            return
        # 提取箱单和库位编码对应关系
        details = [(_['boxNo'], _['storageLocationCode']) for _ in transfer_out_order_detail_res['data']['details']]

        # 按箱单和托盘对应逐个复核
        for box_no, tray_code in details:
            barcode_generate(box_no, 'transfer/box_order')
            print('生成箱单：%s' % box_no)
            review_res = self.wms_request.transfer_out_order_review(box_no, tray_code)
            if not review_res:
                log.error('创建调拨出库单失败：箱单复核异常！')
                return
        # 调拨发货绑定交接单和箱单
        for detail in details:
            bind_res = self.wms_request.transfer_out_box_bind(detail[0], '', '')  # 交接单号和收货仓编码实际可以不用传
            if not bind_res:
                log.error('创建调拨出库单失败：调拨发货交接单绑定箱单失败！')
                return
            handover_no = bind_res['data']['handoverNo']
        print('生成调拨发货交接单：%s' % handover_no)

        delivery_res = self.wms_request.transfer_out_delivery(handover_no)
        if not delivery_res:
            log.error('创建调拨出库单失败：调拨交接单发货失败！')
            return
        assert delivery_res['code'] == 200


if __name__ == '__main__':
    transfer_data = WmsTransferDataGenerator()
    demand_qty = 1
    # transfer_data.create_transfer_out_order(512, '', 513, 513, '63203684930', 2)
    # transfer_data.create_transfer_demand(512, '', 513, 513, '63203684930', 2)
    transfer_data.create_transfer_out_order(511, 513, 540, 540, '62325087738', 2)
    # transfer_data.create_transfer_pick_order(512, '', 513, 513, '63203684930', 2)
