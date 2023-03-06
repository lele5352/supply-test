from cases import *

from utils.log_handler import logger as log


class WmsReceiptDataGenerator:
    def __init__(self):
        self.wms_app = wms_app
        self.ims = ims_robot

    def create_other_in_order(self, sale_sku_code, bom, qty, warehouse_id):
        """
        创建其他其他入库单
        :param warehouse_id:仓库id
        :param bom: bom版本
        :param sale_sku_code: 销售sku编码
        :param qty: 套数
        :return:
        """
        # 切换仓库
        switch_res = self.wms_app.common_switch_warehouse(warehouse_id)
        if not self.wms_app.is_success(switch_res):
            print("切换仓库失败")
            return

        bom_detail = self.ims.dbo.query_bom_detail(sale_sku_code, bom)
        if not bom_detail:
            print("查询销售sku bom版本失败")
            return
        ware_sku_codes = list(bom_detail.keys())
        get_sku_info_res = self.wms_app.other_in_get_sku_info(ware_sku_codes)
        if not self.wms_app.is_success(get_sku_info_res):
            print("查询销售sku对应仓库sku信息失败")
            return

        sku_info_list = get_sku_info_res["data"]["records"]

        result_sku_list = [
            {"warehouseSkuCode": sku["skuCode"],
             "planSkuQty": bom_detail[sku["skuCode"]] * qty,
             "warehouseSkuName": sku["skuName"],
             "warehouseSkuWeight": sku["weight"],
             "saleSkuCode": sku["saleSku"],
             "saleSkuName": sku["skuZhName"],
             "bomVersion": sku["bomVersion"],
             "saleSkuImg": sku["skuImageUrl"],
             "warehouseSkuHeight": sku["warehouseSkuHeight"],
             "warehouseSkuLength": sku["warehouseSkuLength"],
             "warehouseSkuWidth": sku["warehouseSkuWidth"]
             } for sku in sku_info_list
        ]

        create_other_in_order_res = self.wms_app.other_in_create_order(result_sku_list)

        return create_other_in_order_res

    def create_other_in_order_and_up_shelf(self, sale_sku_code, bom, qty, warehouse_id, to_warehouse_id):
        """
        创建其他入库单并执行提交和上架
        :param to_warehouse_id: 目的仓id
        :param warehouse_id: 仓库id
        :param sale_sku_code: 销售sku编码
        :param bom: bom版本
        :param qty: 套数
        :return:
        """
        create_order_res = self.create_other_in_order(sale_sku_code, bom, qty, warehouse_id)
        if not wms_app.is_success(create_order_res):
            print("创建其他入库单失败")
            return
        entry_order_code = create_order_res["data"]["entryOrderCode"]
        entry_order_id = create_order_res["data"]["entryOrderId"]

        # 提交其他入库单
        submit_res = wms_app.other_in_submit_order(entry_order_code, entry_order_id)
        if not submit_res["code"]:
            print("提交其他入库单失败")
            return
        up_shelf_res = wms_app.other_in_order_up_shelf(entry_order_code, entry_order_id, warehouse_id, to_warehouse_id)
        return up_shelf_res


if __name__ == '__main__':
    receipt_data = WmsReceiptDataGenerator()
    print(receipt_data.create_other_in_order_and_up_shelf("JJ306J84G7", "A", 2, 543, 543))
