import time

from utils.log_handler import logger as log
from cases import *
from data_generator.transfer_data_generator import WmsTransferDataGenerator
from data_generator.receipt_data_generator import WmsReceiptDataGenerator
from data_generator.scm_data_generator import ScmDataGenerator


class DataTemplate:
    @classmethod
    def spot_data_template(cls, sale_sku, bom, count, warehouse_id, to_warehouse_id):
        """
        现货参数模板
        :param to_warehouse_id: 目的仓id
        :param warehouse_id: 所属仓id
        :param count:数量
        :param bom:bom版本
        :param sale_sku:销售sku编码
        """
        return [sale_sku, bom, count, warehouse_id, to_warehouse_id]

    @classmethod
    def scm_data_template(cls, sale_sku_list, num, delivery_warehouse_code, to_warehouse_code):
        """
        申购计划、采购在途参数模板
        :param sale_sku_list: 需要采购的销售sku的列表，格式["sku1","sku2"]
        :param num: 采购的件数
        :param delivery_warehouse_code: 发货仓编码
        :param to_warehouse_code: 收货仓编码
        """
        return [sale_sku_list, num, delivery_warehouse_code, to_warehouse_code]

    @classmethod
    def transfer_data_template(cls, trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id, trans_sku, bom,
                               trans_num):
        """
        调拨参数模板
        :param bom: bom版本
        :param trans_out_id: 调出仓id
        :param trans_out_to_id: 调出仓目的仓id
        :param trans_in_id: 调入仓id
        :param trans_in_to_id:调入仓目的仓id
        :param trans_num:调拨件数
        :param trans_sku:销售sku编码
        """
        return [trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id, trans_sku, bom, trans_num]


class AddInventory:
    """
    库存生成器，用于生成各种类型库存数据，具体库存类型定义如下：
    1, "现货"
    2, "调拨在途": 已调拨出库
    3, "采购在途": 目的仓跟发货仓一样，且目的仓为直发仓的采购在途
    4, "申购库存": 发货仓申购库存，有目的仓的缺货需求（待处理）、采购需求（待确认+已确认+确认中）、采购单（草稿+待审核+待下单+已下单(未发数量)）
    5, "调拨计划": 调拨需求(未分配状态)
    6, "采购下单库存": 有目的仓的采购单(已下单未发货)
    7, "中转现货"
    8, "备货现货"
    9, "中转在途": 目的仓跟发货仓不一样，目的仓为海外仓的采购在途
    10, "备货在途": 没有目的仓的采购在途
    11, "缺货"
    12, "备货申购": 备货仓(没有目的仓)的缺货需求（待处理）、采购需求（+待确认+已确认+确认中）、采购单（草稿+待审核+待下单+审核不通过）
    13, "备货下单库存":  没有目的仓的采购单(已下单未发货)
    """

    def __init__(self):
        self.scm_data = ScmDataGenerator()
        self.transfer_data = WmsTransferDataGenerator()
        self.receipt_data = WmsReceiptDataGenerator()

    def add_in_stock_inventory(self, sale_sku, bom, count, warehouse_id, to_warehouse_id):
        """
        添加1发货仓现货库存/7中转现货/8备货现货,通过其他入库方式

        :param to_warehouse_id: 目的仓id
        :param warehouse_id: 所属仓id
        :param count:数量
        :param bom:bom版本
        :param sale_sku:销售sku编码
        """
        wms_app.common_switch_warehouse(warehouse_id)
        add_res = self.receipt_data.create_other_in_order_and_up_shelf(sale_sku, bom, count, warehouse_id,
                                                                       to_warehouse_id)
        return add_res

    def add_transfer_on_way_inventory(self, trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id, sale_sku_code,
                                      bom, demand_qty):
        """
        添加2 调拨在途库存,通过调用wms调拨出库流程

        :param bom: bom版本
        :param trans_out_id: 调出仓id
        :param trans_out_to_id: 调出仓目的仓id
        :param trans_in_id: 调入仓id
        :param trans_in_to_id:调入仓目的仓id
        :param demand_qty:调拨件数
        :param sale_sku_code:销售sku编码
        """
        add_res = self.transfer_data.create_handover_order(trans_out_id, trans_out_to_id, trans_in_id,
                                                           trans_in_to_id, sale_sku_code, bom, demand_qty)

        return add_res

    def add_purchase_on_way_inventory(self, sale_sku_list, num, delivery_warehouse_code, to_warehouse_code):
        """
        添加3采购在途/9中转在途/10备货在途库存,通过调用scm采购发货流程

        :param sale_sku_list: 需要采购的销售sku的列表，格式["sku1","sku2"]
        :param num: 采购的件数
        :param delivery_warehouse_code: 发货仓编码
        :param to_warehouse_code: 收货仓编码

        """
        add_res = self.scm_data.create_distribute_order(sale_sku_list, num, delivery_warehouse_code, to_warehouse_code)
        return add_res

    def add_purchase_wait_buy_inventory(self, sale_sku_list, num, delivery_warehouse_code, to_warehouse_code):
        """
        添加4采购申购/12备货仓申购库存,通过调用scm采购入库发货流程

        :param sale_sku_list: 需要采购的销售sku的列表，格式["sku1","sku2"]
        :param num: 采购的件数
        :param delivery_warehouse_code: 发货仓编码
        :param to_warehouse_code: 收货仓编码

        """
        add_res = self.scm_data.create_purchase_order(sale_sku_list, num, delivery_warehouse_code, to_warehouse_code)
        return add_res

    def add_transfer_plan_inventory(self, trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id, sale_sku_code,
                                    bom, demand_qty):
        """
        添加5调拨计划库存,通过调用wms调拨出库流程

        :param bom: bom版本
        :param trans_out_id: 调出仓id
        :param trans_out_to_id: 调出仓目的仓id
        :param trans_in_id: 调入仓id
        :param trans_in_to_id:调入仓目的仓id
        :param demand_qty:调拨件数
        :param sale_sku_code:销售sku编码
        """
        add_res = self.transfer_data.create_transfer_demand(trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id,
                                                            sale_sku_code, bom, demand_qty)
        return add_res

    def add_purchase_wait_delivery_inventory(self, sale_sku_list, num, delivery_warehouse_code, to_warehouse_code):
        """
        添加6采购下单/13备货仓采购下单库存,通过调用scm采购入库发货流程

        :param sale_sku_list: 需要采购的销售sku的列表，格式["sku1","sku2"]
        :param num: 采购的件数
        :param delivery_warehouse_code: 发货仓编码
        :param to_warehouse_code: 收货仓编码
        """
        add_res = self.scm_data.create_wait_delivery_purchase_order(sale_sku_list, num, delivery_warehouse_code,
                                                                    to_warehouse_code)
        return add_res


if __name__ == '__main__':
    data = AddInventory()

    # -------------------现货相关------------------------------------------------------------------------------------
    # 通过参数模板组装参数
    # params = DataTemplate.spot_data_template("KK931075TA", "A", 799, 540, 540)
    # params = DataTemplate.spot_data_template("COCOM974W132", "A", 1, 532, 532)
    # params = DataTemplate.spot_data_template("COCOZE527222", "A", 177, 650, 650)

    # # 添加1发货仓现货库存，7中转仓现货库存、8备货仓现货库存，都用这个，控制warehouse_id和to_warehouse_id即可，没有
    # data.add_in_stock_inventory(*params)

    # -------------------采购相关------------------------------------------------------------------------------------
    # 通过参数模板组装参数
    # params = DataTemplate.scm_data_template(["COCOZE527222"], 13, "ESZF", "ESZF")
    # # 采购在途库存:3直发仓仓采购在途/9中转在途/10备货在途都用这个
    # data.add_purchase_on_way_inventory(*params)
    #
    # # 采购申购库存:4采购申购/12备货仓申购都用这个
    # data.add_purchase_wait_buy_inventory(*params)
    #
    # # 采购下单库存:6采购下单/13备货仓采购下单都用这个
    # data.add_purchase_wait_delivery_inventory(*params)

    #
    # # -------------------------------------------------------------------------------------------------------
    # 通过参数模板组装参数
    in_wid = 542
    out_wid = 543
    sku_code = "COCOZE527222"
    params = DataTemplate.transfer_data_template(in_wid, 0, out_wid, out_wid, sku_code, "A", 150)
    # 调拨在途库存:2调拨在途
    #data.add_transfer_on_way_inventory(*params)

    #
    # # 调拨计划库存: 5调拨计划
    # data.add_transfer_plan_inventory(*params)
    transfer_data = WmsTransferDataGenerator()
    handover_order_no_list = transfer_data.generate_cds_cabin_order(sku_list=[sku_code], step=8, trans_in_id=in_wid,
                                                                    trans_out_id=out_wid)
