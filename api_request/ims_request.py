import time

from utils.request_handler import RequestHandler
from config.api_config.ims_api_config import ims_api_config
from config.sys_config import env_prefix_config
from db_operator.ims_db_operator import IMSDBOperator


class ImsRequest(RequestHandler):
    def __init__(self):
        self.prefix = env_prefix_config.get('ims_service_prefix')
        self.service_headers = {"serviceName": "ec-warehouse-delivery-service"}
        super().__init__(self.prefix, self.service_headers)

    # # 获取仓库商品总库存
    # def get_wares_inventory_by_target_warehouse_id(self, sale_sku_code, to_warehouse_id):
    #     sql = """
    #        SELECT
    #            ware_sku_code,type,storage_location_id,stock,block
    #        FROM
    #            wares_inventory
    #        WHERE
    #            goods_sku_code = "%s"
    #            AND target_warehouse_id = %s
    #        ORDER BY
    #            ware_sku_code;
    #        """ % (sale_sku_code, to_warehouse_id if to_warehouse_id else 0)
    #
    #     ware_inventory = self.db.get_all(sql)
    #     formatted_ware_sku_inventory = dict()
    #     for data in ware_inventory:
    #         # print(data)
    #         if data['ware_sku_code'] not in formatted_ware_sku_inventory:
    #             if data['type'] == 4:
    #                 formatted_ware_sku_inventory.update({
    #                     data['ware_sku_code']: {
    #                         data['storage_location_id']: {'stock': data['stock'], 'block': 0}}
    #                 })
    #             else:
    #                 formatted_ware_sku_inventory.update({
    #                     data['ware_sku_code']: {
    #                         data['type']: {'stock': data['stock'], 'block': 0}}
    #                 })
    #         elif data['type'] not in formatted_ware_sku_inventory[data['ware_sku_code']]:
    #             if data['type'] == 4:
    #                 formatted_ware_sku_inventory[data['ware_sku_code']].update({
    #                     data['storage_location_id']: {'stock': data['stock'], 'block': 0}
    #                 })
    #             else:
    #                 formatted_ware_sku_inventory[data['ware_sku_code']].update({
    #                     data['type']: {'stock': data['stock'], 'block': 0}
    #                 })
    #         else:
    #             formatted_ware_sku_inventory[data['ware_sku_code']][data['type']]['stock'] += data['stock']
    #     return formatted_ware_sku_inventory

    # def get_wares_inventory_by_warehouse_id(self, sale_sku_code, warehouse_id):
    #     sql = """
    #        SELECT
    #            ware_sku_code,type,storage_location_id as location_id,stock,block
    #        FROM
    #            wares_inventory
    #        WHERE
    #            goods_sku_code = "%s"
    #            AND warehouse_id = %s
    #        ORDER BY
    #            ware_sku_code;
    #        """ % (sale_sku_code, warehouse_id)
    #
    #     ware_inventory = self.db.get_all(sql)
    #     formatted_ware_sku_inventory = dict()
    #     for data in ware_inventory:
    #         if formatted_ware_sku_inventory.get(data['ware_sku_code']):
    #             if data['type'] == 0:
    #                 formatted_ware_sku_inventory[data['ware_sku_code']].update(
    #                     {"0": {'stock': data['stock'], 'block': data['block']}}
    #                 )
    #             elif data['type'] == 1:
    #                 formatted_ware_sku_inventory[data['ware_sku_code']].update(
    #                     {"1": {'stock': data['stock'], 'block': data['block']}}
    #                 )
    #             elif data['type'] == 2:
    #                 formatted_ware_sku_inventory[data['ware_sku_code']].update(
    #                     {"2": {'stock': data['stock'], 'block': data['block']}}
    #                 )
    #             elif data['type'] == 3:
    #                 formatted_ware_sku_inventory[data['ware_sku_code']].update(
    #                     {"3": {'stock': data['stock'], 'block': data['block']}}
    #                 )
    #             elif data['type'] == 4:
    #                 formatted_ware_sku_inventory[data['ware_sku_code']].update(
    #                     {str(data['location_id']): {'stock': data['stock'], 'block': data['block']}}
    #                 )
    #         else:
    #             if data['type'] == 0:
    #                 formatted_ware_sku_inventory.update(
    #                     {data['ware_sku_code']: {
    #                         "0": {'stock': data['stock'], 'block': data['block']}}}
    #                 )
    #             elif data['type'] == 1:
    #                 formatted_ware_sku_inventory.update(
    #                     {data['ware_sku_code']: {
    #                         "1": {'stock': data['stock'], 'block': data['block']}}}
    #                 )
    #             elif data['type'] == 2:
    #                 formatted_ware_sku_inventory.update(
    #                     {data['ware_sku_code']: {
    #                         "2": {'stock': data['stock'], 'block': data['block']}}}
    #                 )
    #             elif data['type'] == 3:
    #                 formatted_ware_sku_inventory.update(
    #                     {data['ware_sku_code']: {
    #                         "3": {'stock': data['stock'], 'block': data['block']}}}
    #                 )
    #             elif data['type'] == 4:
    #                 formatted_ware_sku_inventory.update(
    #                     {data['ware_sku_code']: {
    #                         str(data["location_id"]): {'stock': data['stock'], 'block': data['block']}}}
    #                 )
    #     return formatted_ware_sku_inventory

    # OMS下单
    def oms_order_block(self, sale_sku_info, warehouse_id):
        goods_sku_list = list()
        for sale_sku_code, qty in sale_sku_info:
            goods_sku_list.append({
                "goodsSkuCode": sale_sku_code,
                "qty": qty
            })
        ims_api_config['oms_order_block']['data'].update({
            "goodsSkuList": goods_sku_list,
            "sourceNo": "OMS" + str(int(time.time())),
            "warehouseId": warehouse_id
        })
        res = self.send_request(**ims_api_config['oms_order_block'])
        return res

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

        res = self.send_request(**ims_api_config['purchase_create_order'])
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

        res = self.send_request(**ims_api_config['cancel_purchase_order_delivery'])
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
        res = self.send_request(**ims_api_config['purchase_into_warehouse'])
        return res

    # 其他入库-良品
    def lp_other_in(self, ware_sku_qty_list, sj_location_ids, warehouse_id, to_warehouse_id):
        ware_sku_list = list()
        # 构造入库仓库sku明细数据
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
        res = self.send_request(**ims_api_config['qualified_goods_other_into_warehouse'])
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
        res = self.send_request(**ims_api_config['unqualified_goods_other_into_warehouse'])
        return res

    # 销售出库单生成时预占
    def delivery_order_block(self, delivery_order_no, delivery_order_info, warehouse_id, to_warehouse_id):
        goods_sku_list = list()
        for sku, qty in delivery_order_info:
            goods_sku_list.append({
                "goodsSkuCode": sku,
                "qty": qty
            })
        ims_api_config['delivery_order_block']['data'].update({
            "goodsSkuList": goods_sku_list,
            "sourceNo": delivery_order_no,
            "targetWarehouseId": to_warehouse_id,
            "warehouseId": warehouse_id
        })
        res = self.send_request(**ims_api_config['delivery_order_block'])
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
        res = self.send_request(**ims_api_config['assign_location_stock'])
        return res

    # 确认拣货
    def confirm_pick(self, delivery_order_no, pick_ware_sku_list, warehouse_id):
        ims_api_config['confirm_pick']['data'].update({
            "wareSkuList": pick_ware_sku_list,
            "sourceNo": delivery_order_no,
            "warehouseId": warehouse_id
        })
        res = self.send_request(**ims_api_config['confirm_pick'])
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
        res = self.send_request(**ims_api_config['delivery_out'])
        return res

    def cancel_oms_order_block(self, ims_block_book_id, oms_order_code):
        ims_api_config['cancel_oms_order_block']['data'].update({
            "blockBookId": ims_block_book_id,
            "sourceNo": oms_order_code
        })
        res = self.send_request(**ims_api_config['cancel_oms_order_block'])
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
        res = self.send_request(**ims_api_config['cancel_block_before_pick'])
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
        res = self.send_request(**ims_api_config['cancel_block_after_pick'])
        return res

    def only_cancel_location_block(self, block_book_id, source_no):
        ims_api_config['only_cancel_location_block']['data'].update({
            "blockBookId": block_book_id,
            "sourceNo": source_no
        })
        res = self.send_request(**ims_api_config['only_cancel_location_block'])
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
        qualified_goods_other_out_block_res = self.send_request(**ims_api_config['qualified_goods_other_out_block'])
        return qualified_goods_other_out_block_res

    def cancel_lp_other_out_block(self, block_book_id, source_no):
        ims_api_config['cancel_qualified_goods_other_out_block']['data'].update(
            {
                "sourceNo": source_no,
                "blockBookId": block_book_id
            }
        )
        cancel_block_res = self.send_request(**ims_api_config['cancel_qualified_goods_other_out_block'])
        return cancel_block_res

    def cancel_cp_other_out_block(self, block_book_id, source_no):
        ims_api_config['cancel_unqualified_goods_other_out_block']['data'].update(
            {
                "sourceNo": source_no,
                "blockBookId": block_book_id
            }
        )
        cancel_block_res = self.send_request(**ims_api_config['cancel_unqualified_goods_other_out_block'])
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
        unqualified_goods_other_out_block_res = self.send_request(**ims_api_config['unqualified_goods_other_out_block'])
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
        qualified_goods_other_out_block_res = self.send_request(
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
        unqualified_goods_other_out_block_res = self.send_request(
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
        turn_to_unqualified_goods = self.send_request(**ims_api_config['turn_to_unqualified_goods'])
        return turn_to_unqualified_goods

    def get_import_stock_excel_data(self, excel):
        files = {'file': open(excel, 'rb')}
        excel_data = self.send_request(**ims_api_config['get_import_stock_excel_data'], files=files)
        return excel_data

    def import_stock_excel_data(self, excel):
        files = {'file': open(excel, 'rb')}
        res = self.send_request(**ims_api_config['import_stock_excel_data'], files=files)
        return res

    def move_stock(self,source_no, ware_sku_list):
        ims_api_config['move_stock']['data'].update(
            {
                "sourceNo": source_no,
                "wareSkuList": ware_sku_list,
                "idempotentSign": str(int(time.time() * 1000))
            }
        )
        move_stock_res = self.send_request(**ims_api_config['move_stock'])
        return move_stock_res


if __name__ == '__main__':
    pass
