import logging
import time
from copy import deepcopy

from config.api_config.wms_api_config import wms_api_config
from dbo.wms_dbo import WMSDBOperator


class WmsLogics:
    def __init__(self, wms_app_request):
        self.wms_request = wms_app_request

    @classmethod
    def ck_id_to_code(cls, warehouse_id):
        """
        根据仓库id获取仓库编码

        :param int warehouse_id: 仓库id
        """
        if not warehouse_id:
            return
        data = WMSDBOperator.query_warehouse_info_by_id(warehouse_id)
        return data.get('warehouse_code')

    @classmethod
    def ck_code_to_id(cls, warehouse_code):
        """
        根据仓库编码获取仓库id

        :param string warehouse_code: 仓库编码
        """
        if not warehouse_code:
            return
        data = WMSDBOperator.query_warehouse_info_by_code(warehouse_code)
        return data.get('id')

    @classmethod
    def kw_id_to_code(cls, kw_id):
        """
        根据库位id获取库位编码

        :param int kw_id: 库位id
        """
        data = WMSDBOperator.query_warehouse_location_info_by_id(kw_id)
        return data.get('warehouse_location_code')

    @classmethod
    def kw_code_to_id(cls, kw_code):
        """
        根据库位编码获取库位id

        :param string kw_code: 库位编码
        """
        data = WMSDBOperator.query_warehouse_location_info_by_code(kw_code)
        return data.get('id')

    @classmethod
    def get_ck_area_id(cls, warehouse_id, area_type):
        """
        获取指定区域类型的仓库区域id

        :param int warehouse_id: 仓库id
        :param int area_type: 区域类型
        """
        data = WMSDBOperator.query_warehouse_area_info_by_type(warehouse_id, area_type)
        return str(data.get('id'))

    def mock_express_label_callback(self, delivery_order_code, package_list):
        """
        :param string delivery_order_code: 出库单号
        :param list package_list: 包裹列表

        """
        order_list = list()
        count = 0
        for package in package_list:
            count += 1
            temp_order_info = deepcopy(wms_api_config['label_callback']['data']['orderList'][0])
            temp_order_info.update({
                "deliveryNo": delivery_order_code,
                "packageNoList": [package],
                "logistyNo": "logistyNo" + str(int(time.time() * 1000 + count)),
                "barCode": "barCode" + str(int(time.time() * 1000 + count)),
                "turnOrderNo": str(int(time.time() * 1000)),
                "drawOrderNo": str(int(time.time() * 1000))
            })
            order_list.append(temp_order_info)
        res = self.wms_request.label_callback(delivery_order_code, order_list)
        if res['code'] == 200:
            return True
        else:
            return False

    @classmethod
    def query_delivery_order_package_list(cls, delivery_order_code):
        data = WMSDBOperator.query_delivery_order_package_info(delivery_order_code)
        package_no_list = [package['package_code'] for package in data]
        return package_no_list

    def get_demand_list(self, goods_list, trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id):
        demand_list = list()
        for sku, qty in goods_list:
            demand_res = self.wms_request.transfer_out_create_demand(
                trans_out_id,
                trans_out_to_id,
                trans_in_id,
                trans_in_to_id,
                sku,
                qty)
            demand_no = demand_res['data']['demandCode']
            demand_list.append(demand_no)
        return demand_list

    @classmethod
    def get_pick_sku_list(cls, pick_order_details):
        pick_sku_list = list()
        for detail in pick_order_details:
            pick_sku_list.append(
                (detail['waresSkuCode'], detail['shouldPickQty'], detail['storageLocationId']))
        pick_sku_list = sorted(pick_sku_list, key=lambda pick_sku: pick_sku[2])
        return pick_sku_list

    def transfer_system_flow(self, goods_list, trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id):
        # 切到调出仓
        self.wms_request.switch_default_warehouse(trans_out_id)
        # 生成调拨需求
        demand_list = self.get_demand_list(goods_list, trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id)
        if not demand_list:
            return
        # 创建调拨拣货单
        pick_order_code = self.wms_request.transfer_out_create_pick_order(demand_list, 1)['data']
        # 分配调拨拣货人
        self.wms_request.transfer_out_pick_order_assign([pick_order_code], 'admin', 1)
        # 获取调拨拣货单详情数据
        pick_order_details = self.wms_request.transfer_out_pick_order_detail(pick_order_code)['details']
        # 获取拣货单sku详情数据
        pick_sku_list = self.get_pick_sku_list(pick_order_details)

        # 调拨拣货单确认拣货-纸质
        self.wms_request.transfer_out_confirm_pick(pick_order_code, pick_order_details)
        if len(pick_sku_list) > 1:
            trans_out_tp_kw_ids = self.get_kw(1, 3, len(pick_sku_list), trans_out_id, trans_out_to_id)
        else:
            trans_out_tp_kw_ids = [self.get_kw(1, 3, len(pick_sku_list), trans_out_id, trans_out_to_id)]

        # 调拨拣货单按需装托提交
        self.wms_request.transfer_out_submit_tray(pick_order_code, pick_order_details, trans_out_tp_kw_ids)

        # 查看整单获取已装托的托盘
        tray_detail_res = self.wms_request.transfer_out_pick_order_tray_detail(pick_order_code)
        tray_code_list = [tray['storageLocationCode'] for tray in tray_detail_res['data']]
        # tray_id_list = [tray['storageLocationId'] for tray in tray_detail_res['data']]
        # tray_id_list.sort(reverse=False)
        # tray_sku_list = [tray_detail for tray in tray_detail_res['data'] for tray_detail in tray['trayDetails']]
        # sorted_tray_sku_list = sorted(tray_sku_list, key=lambda x: x['storageLocationCode'], reverse=False)

        # 获取生成的调拨出库单号
        transfer_out_order_no = self.wms_request.transfer_out_finish_packing(pick_order_code, tray_code_list)['data']
        # 获取调拨出库单明细
        transfer_out_order_detail = self.wms_request.transfer_out_order_detail(transfer_out_order_no)['data']['details']
        # 从调拨出库单明细中提取箱单和库位编码对应关系
        details = [(_['boxNo'], _['storageLocationCode']) for _ in transfer_out_order_detail]
        sorted_details = sorted(details, key=lambda a: a[1])
        # 按箱单和托盘对应逐个复核
        for box_no, tray_code in details:
            self.wms_request.transfer_out_order_review(box_no, tray_code)

        # 调拨发货绑定交接单和箱单
        for detail in details:
            bind_res = self.wms_request.transfer_out_box_bind(detail[0], '', '')  # 交接单号和收货仓编码实际可以不用传
            handover_no = bind_res['data']['handoverNo']
        self.wms_request.transfer_out_delivery(handover_no)

        # 切换仓库到调入仓
        self.wms_request.switch_default_warehouse(trans_in_id)
        if len(pick_sku_list) > 1:
            trans_in_sj_kw_ids = self.get_kw(1, 5, len(pick_sku_list), trans_in_id, trans_in_to_id)
        else:
            trans_in_sj_kw_ids = [self.get_kw(1, 5, len(pick_sku_list), trans_in_id, trans_in_to_id)]
        trans_in_sj_kw_codes = [self.kw_id_to_code(kw_id) for kw_id in trans_in_sj_kw_ids]
        # 调拨入库收货
        self.wms_request.transfer_in_received(handover_no)

        # 调拨入库按箱单逐个整箱上架
        for detail, sj_kw_code in zip(sorted_details, trans_in_sj_kw_codes):
            self.wms_request.transfer_in_up_shelf(detail[0], sj_kw_code)

    @classmethod
    def add_bom_stock(cls, sale_sku, bom, count, warehouse_id, to_warehouse_id):
        bom_detail = IMSDBOperator.query_bom_detail(sale_sku, bom)
        location_ids = wms_logics.get_kw(1, 5, len(bom_detail) + 1, warehouse_id, to_warehouse_id)

        res = ims_logics.add_lp_stock_by_other_in(sale_sku, bom, count, location_ids, warehouse_id, to_warehouse_id)
        if res and res['code'] == 200:
            return True
        return

    @classmethod
    def add_ware_stock(cls, ware_qty_list, kw_ids, ck_id, to_ck_id):
        """
        :param list ware_qty_list: 仓库sku个数配置，格式： [('62325087738A01', 4), ('62325087738A01', 5)]
        :param list kw_ids: 仓库库位id数据，与ware_qty_list长度相等
        :param int ck_id: 仓库id
        :param int or None kw_ids: 目的仓id，备货仓时为空
        """
        res = ims_request.lp_other_in(ware_qty_list, kw_ids, ck_id, to_ck_id)
        return res


if __name__ == '__main__':
    wms = WmsLogics()
