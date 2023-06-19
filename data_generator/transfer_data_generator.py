import random
import time

from cases import *

from utils.log_handler import logger as log
from utils.code_handler import GenerateCode
from utils.wait_handler import until

from data_generator.receipt_data_generator import WmsReceiptDataGenerator
from robot_run.run_transfer import run_transfer


class WmsTransferDataGenerator:
    def __init__(self):
        self.wms_app = wms_app
        self.wms_transfer = wms_transfer
        self.ims = ims_robot
        self.wms_data = WmsReceiptDataGenerator()

    def create_transfer_demand(self, trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id, sale_sku_code, bom,
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
        :param bom: bom版本
        """
        self.wms_app.common_switch_warehouse(trans_out_id)

        # 判断bom版本库存是否足够
        is_stock_enough = self.ims.is_bom_stock_enough(sale_sku_code, bom, trans_qty, trans_out_id, trans_out_to_id)

        if not is_stock_enough:
            add_stock_res = self.wms_data.create_other_in_order_and_up_shelf(
                sale_sku_code, bom, trans_qty, trans_out_id, trans_out_to_id
            )
            if not add_stock_res or add_stock_res.get("code") != 1:
                log.error('创建调拨需求失败：加库存失败！')
                return

        # 用户检查库存是否加成功了，加库存需要时间
        until(120, 0.1)(
            lambda: trans_qty <= self.ims.dbo.query_central_inventory(
                sale_sku_code, trans_out_id, trans_out_to_id).get("remain", 0)
        )()

        # 仓库id转换为code
        trans_out_code = self.wms_app.db_ck_id_to_code(trans_out_id)
        trans_out_to_code = self.wms_app.db_ck_id_to_code(trans_out_to_id)
        trans_in_code = self.wms_app.db_ck_id_to_code(trans_in_id)
        trans_in_to_code = self.wms_app.db_ck_id_to_code(trans_in_to_id)
        # 调用创建调拨需求接口
        create_demand_res = self.wms_transfer.transfer_out_create_demand(
            trans_out_code, trans_out_to_code, trans_in_code, trans_in_to_code, sale_sku_code, bom, trans_qty,
            demand_type, customer_type, remark)
        if not create_demand_res or create_demand_res['code'] != 1:
            log.error('创建调拨需求失败！')
            return
        print('生成调拨需求：%s' % create_demand_res['data']['demandCode'])
        return create_demand_res['data']['demandCode']

    def create_transfer_pick_order(self, trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id, sale_sku_code, bom,
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
        :param bom: bom版本
        """
        self.wms_app.common_switch_warehouse(trans_out_id)
        # 生成调拨需求
        demand_no = self.create_transfer_demand(
            trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id, sale_sku_code, bom, demand_qty, demand_type,
            customer_type, remark
        )
        if not demand_no:
            print('创建调拨拣货单失败：需求创建失败！')
            return
        # 创建调拨拣货单
        result, order_no = run_transfer(demand_no, "create_pick_order")
        if not result:
            print('创建调拨拣货单失败！')
            log.error('创建调拨拣货单失败！')
            return
        pick_order_code = order_no

        GenerateCode("barcode", "transfer_pick_order", pick_order_code)
        print('生成调拨拣货单：%s' % pick_order_code)
        return pick_order_code

    def create_handover_order(self, trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id, sale_sku_code, bom,
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
        :param bom: bom版本
        """
        # 生成调拨需求
        demand_no = self.create_transfer_demand(
            trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id, sale_sku_code, bom, demand_qty, demand_type,
            customer_type, remark
        )
        if not demand_no:
            print('创建调拨拣货单失败')
            return
        # 执行调拨流程到发货交接节点
        result, order_no = run_transfer(demand_no, "handover")
        print("创建调拨出库成功,调拨交接单号：%s" % order_no)
        return order_no

    def create_cabinet_order(self, trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id, sale_sku_code, bom,
                             demand_qty, demand_type=1, customer_type=1, remark=''):
        """
        生成海柜单

        :param int trans_out_id: 调出仓库id
        :param int trans_in_id: 调入仓库id
        :param any trans_out_to_id: 调出仓库的目的仓id，仅调出仓为中转仓时必填
        :param any trans_in_to_id: 调入仓库的目的仓id，仅调入仓为中转仓时必填
        :param string sale_sku_code: 调拨的商品的销售sku
        :param int demand_qty: 调拨数量
        :param int demand_type: 调拨类型
        :param int customer_type: 客户类型：1-普通客户；2-大客户
        :param string remark: 备注
        :param bom: bom版本
        """
        # 生成调拨需求
        demand_no = self.create_transfer_demand(
            trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id, sale_sku_code, bom, demand_qty, demand_type,
            customer_type, remark
        )

        if not demand_no:
            print('创建调拨拣货单失败')
            return
        # 执行调拨流程到复核完成
        result, order_no = run_transfer(demand_no, "bind")
        # print("复核成功,交接单号：%s" % order_no)
        # 获取交接货单id
        order_detail = self.wms_app.transfer_handover_order(handover_ids=[order_no]).get('data').get('records')[0]
        handover_id = order_detail.get('id')
        # 获取海运柜号信息并更新
        cabinet_info = random.choice(self.wms_app.transfer_cabinet_list().get('data'))
        container_no = cabinet_info.get('cabinetNumber')
        so_number = cabinet_info.get('soNumber')
        # print("更新海运柜号，{}".format(cabinet_info))
        self.wms_app.transfer_out_update_delivery_config(handover_id, container_no, so_number)
        # print("完成调拨发货")
        self.wms_app.transfer_out_delivery(order_no)
        print('交接单号:{},交接单id:{},海柜信息:{}'.format(order_no, handover_id, cabinet_info))
        return order_no


if __name__ == '__main__':
    transfer_data = WmsTransferDataGenerator()
    demand_qty = 10
    # transfer_data.create_transfer_demand(512, '', 513, 513, '63203684930', "B", 2)
    # transfer_data.create_transfer_demand(511, 513, 513, 513, '63203684930', "B", 1)
    # transfer_data.create_handover_order(512, '', 513, 513, '63203684930', "B", 1)
    # transfer_data.create_transfer_pick_order(512, '', 513, 513, '63203684930',"B", 2)
    import threading

    # sku_list = ['JF067T801S', 'JF31665XD8', 'JF954856UJ', 'JF389G7H75', 'P31559628', 'BPJF067T801SB01']
    sku_list = ['JF067T801S', 'JF31665XD8']
    # sku_list = ['JF067T801S']
    th_list = []
    for sku in sku_list:
        th = threading.Thread(target=transfer_data.create_cabinet_order, args=(
            515, 515, 542, 542, sku, "A", 1))
        th.start()
        th_list.append(th)
    for th in th_list:
        th.join()
