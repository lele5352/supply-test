import time

from controller.wms_transfer_service_controller import WmsTransferServiceController
from controller.wms_controller import WmsController
from controller.ums_controller import UmsController
from controller.ims_controller import ImsController
from utils.log_handler import logger as log
from utils.barcode_handler import barcode_generate


class WmsTransferDataGenerator:
    def __init__(self, wms, ims, transfer):
        self.wms = wms
        self.transfer = transfer
        self.ims = ims

    def create_transfer_demand(self, delivery_warehouse_id, receive_warehouse_id, sale_sku_code, demand_qty,
                               delivery_target_warehouse_id='', receive_target_warehouse_id='', demand_type=1,
                               customer_type=1, remark=''):
        """
        创建调拨需求

        :param int delivery_warehouse_id: 调出仓库id
        :param int receive_warehouse_id: 调入仓库id
        :param int delivery_target_warehouse_id: 调出仓库的目的仓id，仅调出仓为中转仓时必填
        :param imt receive_target_warehouse_id: 调入仓库的目的仓id，仅调入仓为中转仓时必填
        :param string sale_sku_code: 调拨的商品的销售sku
        :param int demand_qty: 调拨数量
        :param int demand_type: 调拨类型
        :param int customer_type: 客户类型：1-普通客户；2-大客户
        :param string remark: 备注
        """
        central_inventory = self.ims.get_warehouse_central_inventory(sale_sku_code, delivery_target_warehouse_id)
        # 可用库存不足，需要添加库存，分为2种情况：1-查询不到库存；2-查询到库存，block＞stock
        if not central_inventory or central_inventory['central_inventory_sale_block'] >= central_inventory[
            'central_inventory_sale_stock']:
            self.ims.add_stock_by_other_in(
                sale_sku_code,
                'A',
                demand_qty,
                self.wms.db_get_kw(1, 5, demand_qty, delivery_warehouse_id, delivery_target_warehouse_id),
                delivery_warehouse_id,
                delivery_target_warehouse_id)
        # 调用创建调拨需求接口
        res = self.transfer.transfer_out_create_demand(
            self.wms.db_ck_id_to_code(delivery_warehouse_id),
            self.wms.db_ck_id_to_code(receive_warehouse_id),
            sale_sku_code,
            demand_qty,
            self.wms.db_ck_id_to_code(delivery_target_warehouse_id),
            self.wms.db_ck_id_to_code(receive_target_warehouse_id),
            demand_type,
            customer_type,
            remark)
        print('生成调拨需求：%s' % res['data']['demandCode'])
        return res['data']['demandCode']

    def create_transfer_pick_order(self, delivery_warehouse_id, receive_warehouse_id, sale_sku_code, demand_qty,
                                   delivery_target_warehouse_id=None, receive_target_warehouse_id=None, demand_type=1,
                                   customer_type=1, remark=''):
        """
        生成调拨拣货单

        :param int delivery_warehouse_id: 调出仓库id
        :param int receive_warehouse_id: 调入仓库id
        :param int delivery_target_warehouse_id: 调出仓库的目的仓id，仅调出仓为中转仓时必填
        :param int receive_target_warehouse_id: 调入仓库的目的仓id，仅调入仓为中转仓时必填
        :param string sale_sku_code: 调拨的商品的销售sku
        :param int demand_qty: 调拨数量
        :param int demand_type: 调拨类型
        :param int customer_type: 客户类型：1-普通客户；2-大客户
        :param string remark: 备注
        """
        # 先生成调拨需求
        demand_no = self.create_transfer_demand(delivery_warehouse_id, receive_warehouse_id, sale_sku_code, demand_qty,
                                                delivery_target_warehouse_id, receive_target_warehouse_id, demand_type,
                                                customer_type, remark)
        if not demand_no:
            log.error('创建调拨需求失败,流程中断！')
            return
        res = self.wms.transfer_out_create_pick_order([demand_no], 1)
        barcode_generate(res['data'], 'transfer_pick_order')
        print('调拨拣货单号：%s' % res['data'])
        return res['data']


if __name__ == '__main__':
    ums = UmsController()
    transfer = WmsTransferServiceController(ums)
    ims = ImsController()
    transfer_data = WmsTransferDataGenerator()
    demand_qty = 1
    transfer_data.create_transfer_pick_order(511, 514, '63203684930', 1, 513, 514)
    # transfer.create_transfer_demand(511, 514, '63203684930', 1, 513, 514, 1, 1, 'test')
