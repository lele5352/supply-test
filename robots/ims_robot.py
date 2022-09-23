import time

from robots.robot import ServiceRobot
from config.api_config.ims_api_config import ims_api_config
from copy import deepcopy
from db_operator.ims_db_operator import IMSDBOperator


class IMSRobot(ServiceRobot):
    def __init__(self):
        super().__init__("ims", IMSDBOperator)

    # 采购下单
    def purchase_create_order(self, ware_sku_qty_list, warehouse_id, to_warehouse_id):
        temp_list = list()
        for ware_sku, qty in ware_sku_qty_list:
            temp_list.append({
                "wareSkuCode": ware_sku,
                "qty": qty
            })
        ims_api_config['purchase_create_order']['data'][0].update({
            "wareSkuRequestBOS": temp_list,
            "sourceNo": "CG" + str(int(time.time() * 1000)),
            "warehouseId": warehouse_id,
            "targetWarehouseId": to_warehouse_id
        })

        res = self.call_api(**ims_api_config['purchase_create_order'])
        return res

    # 采购下单发货后终止来货
    def cancel_purchase_order_delivery(self, ware_sku_qty_list, warehouse_id, to_warehouse_id):
        temp_list = list()
        for ware_sku, qty in ware_sku_qty_list:
            temp_list.append({
                "functionType": "26",
                "operateType": "1",
                "wareSkuCode": ware_sku,
                "qty": qty,
                "sourceNo": "CG" + str(int(time.time() * 1000)),
                "warehouseId": warehouse_id,
                "targetWarehouseId": to_warehouse_id
            })
        ims_api_config['cancel_purchase_order_delivery'].update(
            {'data': temp_list}
        )

        res = self.call_api(**ims_api_config['cancel_purchase_order_delivery'])
        return res

    # 采购入库上架
    def purchase_into_warehouse(self, ware_sku_qty_list, sj_location_ids, warehouse_id, to_warehouse_id):
        # 构造 销售sku+bom的唯一键，用来下面聚合同个销售sku同个bom的仓库sku
        temp_list = list()
        for i in ware_sku_qty_list:
            bom_info = IMSDBOperator.query_bom_detail_by_ware_sku_code(i[0])
            if bom_info not in temp_list:
                temp_list.append(bom_info)

        goods_sku_list = list()
        for temp in temp_list:
            ware_sku_list = list()
            for (ware_sku, qty), location_id in zip(ware_sku_qty_list, sj_location_ids):
                sale_sku_bom = IMSDBOperator.query_bom_detail_by_ware_sku_code(ware_sku)
                if temp == sale_sku_bom:
                    ware_sku_list.append(
                        {
                            "bomQty": sale_sku_bom['bom_qty'],
                            "qty": qty,
                            "storageLocationId": location_id,
                            "storageLocationType": 5,
                            "wareSkuCode": ware_sku
                        }
                    )

            goods_sku_list.append({
                "bomVersion": temp['bom_version'],
                "goodsSkuCode": temp['goods_sku_code'],
                "wareSkuList": ware_sku_list
            })

        temp_data = {
            "goodsSkuList": goods_sku_list,
            "sourceNo": "CG" + str(int(time.time() * 1000)),
            "targetWarehouseId": to_warehouse_id,
            "warehouseId": warehouse_id
        }
        ims_api_config['purchase_into_warehouse']['data'].update(temp_data)
        res = self.call_api(**ims_api_config['purchase_into_warehouse'])
        return res

    # 其他入库-良品
    def lp_other_in(self, ware_sku_qty_list, sj_location_ids, warehouse_id, to_warehouse_id):
        ware_sku_list = list()
        # 构造入库仓库sku明细数据
        kw_diff_num = len(ware_sku_qty_list) - len(sj_location_ids)
        temp = list()
        if kw_diff_num > 0:
            for i in range(kw_diff_num):
                temp.append(sj_location_ids[-1])
            sj_location_ids.extend(temp)
        for (ware_sku, qty), sj_location_id in zip(ware_sku_qty_list, sj_location_ids):
            temp_dict = {
                "qty": qty,
                "storageLocationId": sj_location_id,
                "storageLocationType": 5,
                "wareSkuCode": ware_sku
            }
            ware_sku_list.append(temp_dict)
        ims_api_config['qualified_goods_other_into_warehouse']['data'][0].update(
            {
                "sourceNo": "QRKL" + str(int(time.time() * 1000)),
                "targetWarehouseId": to_warehouse_id,
                "warehouseId": warehouse_id,
                "wareSkuList": ware_sku_list
            })
        res = self.call_api(**ims_api_config['qualified_goods_other_into_warehouse'])
        return res

    # 其他入库-良品
    def cp_other_in(self, ware_sku_qty_list, cp_location_ids, warehouse_id, to_warehouse_id):
        ware_sku_list = list()
        # 构造入库仓库sku明细数据
        for (ware_sku, qty), cp_location_id in zip(ware_sku_qty_list, cp_location_ids):
            temp_dict = {
                "qty": qty,
                "storageLocationId": cp_location_id,
                "storageLocationType": 6,
                "wareSkuCode": ware_sku
            }
            ware_sku_list.append(temp_dict)
        ims_api_config['unqualified_goods_other_into_warehouse']['data'][0].update(
            {
                "sourceNo": "QRKC" + str(int(time.time() * 1000)),
                "targetWarehouseId": to_warehouse_id,
                "warehouseId": warehouse_id,
                "wareSkuList": ware_sku_list
            })
        res = self.call_api(**ims_api_config['unqualified_goods_other_into_warehouse'])
        return res

    def delivery_order_block(self, oms_order_no, oms_order_sku_info_list, warehouse_id, to_warehouse_id):
        """
        销售出库单生成时预占

        :param oms_order_sku_info_list: oms订单内的sku信息列表，格式:[(sku,bom,qty)),..]
        :param oms_order_no: oms单号
        :param warehouse_id: 所属仓库id
        :param to_warehouse_id: 目的仓库id
        :return: dict，响应内容
        """
        sku_list = list()
        for sku, bom, qty in oms_order_sku_info_list:
            base_data = deepcopy(ims_api_config['delivery_order_block']['data'])
            base_data.update({
                "bomVersion": bom,
                "goodsSkuCode": sku,
                "idempotentSign": oms_order_no,
                "qty": qty,
                "sourceNo": oms_order_no,
                "targetWarehouseId": to_warehouse_id,
                "warehouseId": warehouse_id
            })
            sku_list.append(base_data)
        ims_api_config['delivery_order_block'].update({
            "data": sku_list
        })
        res = self.call_api(**ims_api_config['delivery_order_block'])
        return res

    # 分配库位库存
    def assign_stock(self, delivery_order_no, ware_sku_list, warehouse_id):
        temp_list = list()
        for ware_sku, qty in ware_sku_list:
            temp_list.append({
                'qty': qty,
                'wareSkuCode': ware_sku
            })
        ims_api_config['assign_location_stock']['data'][0].update({
            "wareSkuList": temp_list,
            'idempotentSign': str(int(time.time() * 1000)),
            "sourceNo": delivery_order_no,
            "warehouseId": warehouse_id,
        })
        res = self.call_api(**ims_api_config['assign_location_stock'])
        return res

    # 确认拣货
    def confirm_pick(self, delivery_order_no, pick_ware_sku_list, warehouse_id):
        ims_api_config['confirm_pick']['data'].update({
            "wareSkuList": pick_ware_sku_list,
            "sourceNo": delivery_order_no,
            "warehouseId": warehouse_id
        })
        res = self.call_api(**ims_api_config['confirm_pick'])
        return res

    # 发货
    def delivery_out(self, delivery_order_no, delivery_order_goods, warehouse_id, to_warehouse_id):
        ware_sku_list = list()
        for ware_sku, qty in delivery_order_goods:
            temp_ware_sku_dict = {
                "qty": qty,
                "wareSkuCode": ware_sku,
                "storageLocationId": -warehouse_id
            }
            ware_sku_list.append(temp_ware_sku_dict)
        ims_api_config['delivery_out']['data'][0].update({
            "wareSkuList": ware_sku_list,
            "sourceNo": delivery_order_no,
            "warehouseId": warehouse_id,
            "targetWarehouseId": to_warehouse_id
        })
        res = self.call_api(**ims_api_config['delivery_out'])
        return res

    def cancel_oms_order_block(self, ims_block_book_id, oms_order_code):
        ims_api_config['cancel_oms_order_block']['data'].update({
            "blockBookId": ims_block_book_id,
            "sourceNo": oms_order_code
        })
        res = self.call_api(**ims_api_config['cancel_oms_order_block'])
        return res

    def cancel_block_before_pick(self, delivery_order_no, roll_back_type):
        """
        :param string delivery_order_no: 出库单号
        :param int roll_back_type: 回滚类型：1，当前已分配库位库存；2，当前未分配库位库存
        """
        ims_api_config['cancel_block_before_pick']['data'].update({
            "sourceNo": delivery_order_no,
            "rollBackBlockType": roll_back_type

        })
        res = self.call_api(**ims_api_config['cancel_block_before_pick'])
        return res

    def cancel_block_after_pick(self, delivery_order_no, pick_order_goods_list, location_id, warehouse_id):
        ware_sku_list = list()
        for ware_sku, qty in pick_order_goods_list:
            temp_ware_sku_dict = {
                "fromStorageLocationId": -warehouse_id,
                "qty": qty,
                "toStorageLocationId": location_id,
                "toStorageLocationType": "4",
                "toTargetWarehouseId": warehouse_id,
                "wareSkuCode": ware_sku
            }
            ware_sku_list.append(temp_ware_sku_dict)
        ims_api_config['cancel_block_after_pick']['data'].update(
            {
                "wareSkuList": ware_sku_list,
                "sourceNo": delivery_order_no
            })
        res = self.call_api(**ims_api_config['cancel_block_after_pick'])
        return res

    def only_cancel_location_block(self, block_book_id, source_no):
        ims_api_config['only_cancel_location_block']['data'].update({
            "blockBookId": block_book_id,
            "sourceNo": source_no
        })
        res = self.call_api(**ims_api_config['only_cancel_location_block'])
        return res

    def add_stock_by_purchase_in(self, ware_sku_qty_list, sj_location_ids, warehouse_id,
                                 to_warehouse_id):
        purchase_create_order_res = self.purchase_create_order(
            ware_sku_qty_list,
            warehouse_id,
            to_warehouse_id)
        if not purchase_create_order_res or purchase_create_order_res['code'] != 200:
            return
        purchase_into_warehouse_res = self.purchase_into_warehouse(
            ware_sku_qty_list,
            sj_location_ids,
            warehouse_id,
            to_warehouse_id)
        return purchase_into_warehouse_res

    def lp_other_out_block(self, ware_sku_list, warehouse_id, to_warehouse_id):
        ims_api_config['qualified_goods_other_out_block']['data'][0].update(
            {
                "sourceNo": "CK" + str(int(time.time() * 1000)),
                "targetWarehouseId": to_warehouse_id,
                "wareSkuList": ware_sku_list,
                "warehouseId": warehouse_id
            }
        )
        qualified_goods_other_out_block_res = self.call_api(**ims_api_config['qualified_goods_other_out_block'])
        return qualified_goods_other_out_block_res

    def cancel_lp_other_out_block(self, block_book_id, source_no):
        ims_api_config['cancel_qualified_goods_other_out_block']['data'].update(
            {
                "sourceNo": source_no,
                "blockBookId": block_book_id
            }
        )
        cancel_block_res = self.call_api(**ims_api_config['cancel_qualified_goods_other_out_block'])
        return cancel_block_res

    def cancel_cp_other_out_block(self, block_book_id, source_no):
        ims_api_config['cancel_unqualified_goods_other_out_block']['data'].update(
            {
                "sourceNo": source_no,
                "blockBookId": block_book_id
            }
        )
        cancel_block_res = self.call_api(**ims_api_config['cancel_unqualified_goods_other_out_block'])
        return cancel_block_res

    def cp_other_out_block(self, ware_sku_qty_list, cp_location_ids, warehouse_id):
        temp_list = list()
        for (ware_sku, qty), cp_location_id in zip(ware_sku_qty_list, cp_location_ids):
            temp_list.append({
                "qty": qty,
                "storageLocationId": cp_location_id,
                "wareSkuCode": ware_sku
            })
        ims_api_config['unqualified_goods_other_out_block']['data'][0].update(
            {
                "sourceNo": "QCKC" + str(int(time.time() * 1000)),
                "wareSkuList": temp_list,
                "warehouseId": warehouse_id
            }
        )
        unqualified_goods_other_out_block_res = self.call_api(**ims_api_config['unqualified_goods_other_out_block'])
        return unqualified_goods_other_out_block_res

    def lp_other_out_delivered(self, ware_sku_list, warehouse_id, to_warehouse_id):
        ims_api_config['qualified_goods_other_out_delivery_goods']['data'][0].update(
            {
                "sourceNo": "CK" + str(int(time.time() * 1000)),
                "targetWarehouseId": to_warehouse_id,
                "wareSkuList": ware_sku_list,
                "warehouseId": warehouse_id
            }
        )
        qualified_goods_other_out_block_res = self.call_api(
            **ims_api_config['qualified_goods_other_out_delivery_goods'])
        return qualified_goods_other_out_block_res

    def cp_other_out_delivered(self, ware_sku_qty_list, cp_location_ids, warehouse_id):
        temp_list = list()
        for (ware_sku, qty), cp_location_id in zip(ware_sku_qty_list, cp_location_ids):
            temp_list.append({
                "qty": qty,
                "storageLocationId": cp_location_id,
                "wareSkuCode": ware_sku
            })
        ims_api_config['unqualified_goods_other_out_delivery_goods']['data'][0].update(
            {
                "sourceNo": "QCKC" + str(int(time.time() * 1000)),
                "wareSkuList": temp_list,
                "warehouseId": warehouse_id
            }
        )
        unqualified_goods_other_out_block_res = self.call_api(
            **ims_api_config['unqualified_goods_other_out_delivery_goods'])
        return unqualified_goods_other_out_block_res

    def turn_to_cp(self, ware_sku, from_location_id, to_location_id, qty, warehouse_id, to_warehouse_id):
        ims_api_config['turn_to_unqualified_goods']['data'].update(
            {
                "sourceNo": "LZC" + str(int(time.time() * 1000)),
                "qty": qty,
                "fromStorageLocationId": from_location_id,
                "toStorageLocationId": to_location_id,
                "warehouseId": warehouse_id,
                "targetWarehouseId": to_warehouse_id,
                "wareSkuCode": ware_sku
            }
        )
        turn_to_unqualified_goods = self.call_api(**ims_api_config['turn_to_unqualified_goods'])
        return turn_to_unqualified_goods

    def get_import_stock_excel_data(self, excel):
        files = {'file': open(excel, 'rb')}
        excel_data = self.call_api(**ims_api_config['get_import_stock_excel_data'], files=files)
        return excel_data

    def import_stock_excel_data(self, excel):
        files = {'file': open(excel, 'rb')}
        res = self.call_api(**ims_api_config['import_stock_excel_data'], files=files)
        return res

    def move_stock(self, source_no, ware_sku_list):
        ims_api_config['move_stock']['data'].update(
            {
                "sourceNo": source_no,
                "wareSkuList": ware_sku_list,
                "idempotentSign": str(int(time.time() * 1000))
            }
        )
        move_stock_res = self.call_api(**ims_api_config['move_stock'])
        return move_stock_res

    def add_lp_stock_by_other_in(self, sale_sku_code, bom_version, add_stock_count, location_ids, warehouse_id,
                                 to_warehouse_id):
        """
        :param str sale_sku_code: 销售sku编码
        :param str bom_version: bom版本
        :param int add_stock_count: 销售sku件数
        :param list location_ids: 库位列表
        :param int warehouse_id: 仓库id
        :param int to_warehouse_id: 目的仓库id
        """
        details = self.dbo.query_bom_detail(sale_sku_code, bom_version)
        ware_sku_qty_list = list()
        for ware_sku, qty in details.items():
            ware_sku_qty_list.append((ware_sku, qty * add_stock_count))
        res = self.lp_other_in(ware_sku_qty_list, location_ids, warehouse_id, to_warehouse_id)
        return res

    def add_bom_stock(self, sale_sku, bom, count, location_ids, warehouse_id, to_warehouse_id):
        res = self.add_lp_stock_by_other_in(sale_sku, bom, count, location_ids, warehouse_id, to_warehouse_id)
        if res and res['code'] == 200:
            return self.report(1, True, {})
        return self.report(0, False, {})

    def add_ware_stock(self, ware_qty_list, kw_ids, ck_id, to_ck_id):
        """
        @param ck_id: 仓库id
        @param kw_ids: 仓库库位id数据，与ware_qty_list长度相等
        @param ware_qty_list: 仓库sku个数配置，格式： [('62325087738A01', 4), ('62325087738A01', 5)]
        @param to_ck_id: 目的仓id，备货仓时为空
        """
        res = self.lp_other_in(ware_qty_list, kw_ids, ck_id, to_ck_id)
        return res

    def del_stock(self, sale_skus):
        self.dbo.delete_qualified_inventory(sale_skus)

    #
    def is_stock_enough(self, order_sku_info_list) -> dict:
        """
        判断发货仓库存是否满足oms库存数量
        @param order_sku_info_list:格式[{"sku_code": "JJH3C94287", "bom_version": "A", "qty": 2, "warehouse_id": '513'}]
        @return:
        """
        for order_sku in order_sku_info_list:
            sku_code, bom, qty, warehouse_id = order_sku.values()
            bom_detail = self.dbo.query_bom_detail(sku_code, bom)

            ware_sku_data = self.dbo.query_stock_with_bom(sku_code, bom, warehouse_id, warehouse_id)
            if not ware_sku_data:
                return self.report(0, False, {})
            stock_less_sku_list = []
            for data in ware_sku_data:
                if (data['stock'] - data['block']) / bom_detail.get(data['ware_sku_code']) < qty:
                    stock_less_sku_list.append([sku_code, bom, qty, warehouse_id])
                return self.report(0, False, stock_less_sku_list)
            return self.report(1, True, {})


if __name__ == '__main__':
    ims_robot = IMSRobot()
    ims_robot.del_stock(["67330337129"])
    # ims_robot.add_bom_stock("JF2KB93311", "C", 1, [1496], 513, 513)
    # ims_robot.add_bom_stock("JF2KB93311", "D", 1, [1544], 512, '')
