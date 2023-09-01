import time
import math
from robots.robot import ServiceRobot
from config.third_party_api_configs.ims_api_config import ims_api_config
from copy import deepcopy
from dbo.ims_dbo import IMSDBOperator
from utils.wait_handler import until


class IMSRobot(ServiceRobot):
    def __init__(self):
        self.dbo = IMSDBOperator
        super().__init__("ims")

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
        return self.formatted_result(res)

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
        return self.formatted_result(res)

    # 采购入库上架
    def purchase_into_warehouse(self, ware_sku_qty_list, sj_location_ids, warehouse_id, to_warehouse_id):
        # 构造 销售sku+bom的唯一键，用来下面聚合同个销售sku同个bom的仓库sku
        temp_list = list()
        for i in ware_sku_qty_list:
            bom_info = self.dbo.query_bom_detail_by_ware_sku_code(i[0])
            if bom_info not in temp_list:
                temp_list.append(bom_info)

        goods_sku_list = list()
        for temp in temp_list:
            ware_sku_list = list()
            for (ware_sku, qty), location_id in zip(ware_sku_qty_list, sj_location_ids):
                sale_sku_bom = self.dbo.query_bom_detail_by_ware_sku_code(ware_sku)
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
        return self.formatted_result(res)

    # 其他入库-良品
    def lp_other_in(self, ware_sku_qty_list, sj_location_ids, warehouse_id, to_warehouse_id):
        ware_sku_list = list()
        # 构造入库仓库sku明细数据
        kw_diff_num = len(ware_sku_qty_list) - len(sj_location_ids)
        temp = list()
        if kw_diff_num > 0:
            sj_location_ids.extend([sj_location_ids[-1]] * kw_diff_num)
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
        return self.formatted_result(res)

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
        return self.formatted_result(res)

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
        return self.formatted_result(res)

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
        return self.formatted_result(res)

    # 确认拣货
    def confirm_pick(self, delivery_order_no, pick_ware_sku_list, warehouse_id):
        ims_api_config['confirm_pick']['data'].update({
            "wareSkuList": pick_ware_sku_list,
            "sourceNo": delivery_order_no,
            "warehouseId": warehouse_id
        })
        res = self.call_api(**ims_api_config['confirm_pick'])
        return self.formatted_result(res)

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
        return self.formatted_result(res)

    def cancel_oms_order_block(self, ims_block_book_id, oms_order_code):
        ims_api_config['cancel_oms_order_block']['data'].update({
            "blockBookId": ims_block_book_id,
            "sourceNo": oms_order_code
        })
        res = self.call_api(**ims_api_config['cancel_oms_order_block'])
        return self.formatted_result(res)

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
        return self.formatted_result(res)

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
        return self.formatted_result(res)

    def only_cancel_location_block(self, block_book_id, source_no):
        ims_api_config['only_cancel_location_block']['data'].update({
            "blockBookId": block_book_id,
            "sourceNo": source_no
        })
        res = self.call_api(**ims_api_config['only_cancel_location_block'])
        return self.formatted_result(res)

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
        return self.formatted_result(purchase_into_warehouse_res)

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
        return self.formatted_result(cancel_block_res)

    def cancel_cp_other_out_block(self, block_book_id, source_no):
        ims_api_config['cancel_unqualified_goods_other_out_block']['data'].update(
            {
                "sourceNo": source_no,
                "blockBookId": block_book_id
            }
        )
        cancel_block_res = self.call_api(**ims_api_config['cancel_unqualified_goods_other_out_block'])
        return self.formatted_result(cancel_block_res)

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
        return self.formatted_result(unqualified_goods_other_out_block_res)

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
        return self.formatted_result(qualified_goods_other_out_block_res)

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
        return self.formatted_result(unqualified_goods_other_out_block_res)

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
        return self.formatted_result(turn_to_unqualified_goods)

    def get_import_stock_excel_data(self, excel):
        files = {'file': open(excel, 'rb')}
        excel_data = self.call_api(**ims_api_config['get_import_stock_excel_data'], files=files)
        return excel_data

    def import_stock_excel_data(self, excel):
        files = {'file': open(excel, 'rb')}
        res = self.call_api(**ims_api_config['import_stock_excel_data'], files=files)
        return self.formatted_result(res)

    def move_stock(self, source_no, ware_sku_list):
        ims_api_config['move_stock']['data'].update(
            {
                "sourceNo": source_no,
                "wareSkuList": ware_sku_list,
                "idempotentSign": str(int(time.time() * 1000))
            }
        )
        move_stock_res = self.call_api(**ims_api_config['move_stock'])
        return self.formatted_result(move_stock_res)

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
        return res

    def add_ware_stock(self, ware_qty_list, kw_ids, ck_id, to_ck_id):
        """
        :param ck_id: 仓库id
        :param kw_ids: 仓库库位id数据，与ware_qty_list长度相等
        :param ware_qty_list: 仓库sku个数配置，格式： [('62325087738A01', 4), ('62325087738A01', 5)]
        :param to_ck_id: 目的仓id，备货仓时为空
        """
        res = self.lp_other_in(ware_qty_list, kw_ids, ck_id, to_ck_id)
        return res

    def del_stock(self, sale_skus):
        self.dbo.delete_qualified_inventory(sale_skus)

    #
    def is_stock_enough(self, order_sku_info_list) -> dict:
        """
        判断发货仓库存是否满足oms库存数量
        :param order_sku_info_list:格式[{"sku_code": "JJH3C94287", "bom_version": "A", "qty": 2, "warehouse_id": '513'}]
        :return:
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

    @classmethod
    def format_wares_inventory(cls, wares_inventory) -> dict:
        """
        把查库获取到的wares_inventory数据格式化为库存统一数据结构
        :param list wares_inventory: wares_inventory库存数据
        :return dict: 查询结果数据，字典格式
        """
        formatted_inventory = dict()
        if not wares_inventory:
            return {}
        for item in wares_inventory:
            sale_sku, ware_sku, bom = item['goods_sku_code'], item['ware_sku_code'], item['bom_version']
            stock, block, kw_id, wares_type = item['stock'], item['block'], item['storage_location_id'], item['type']
            if bom not in formatted_inventory:
                if wares_type == 0:
                    formatted_inventory.update(
                        {bom: {ware_sku: {"warehouse_total": {'stock': stock, 'block': block}}}}
                    )
                elif wares_type == 1:
                    formatted_inventory.update(
                        {bom: {ware_sku: {"purchase_on_way": {'stock': stock, 'block': block}}}}
                    )
                elif wares_type == 2:
                    formatted_inventory.update(
                        {bom: {ware_sku: {"transfer_on_way": {'stock': stock, 'block': block}}}}
                    )
                elif wares_type == 3:
                    formatted_inventory.update(
                        {bom: {ware_sku: {"location_total": {'stock': stock, 'block': block}}}}
                    )
                elif wares_type == 4:
                    formatted_inventory.update(
                        {bom: {ware_sku: {kw_id: {'stock': stock, 'block': block}}}}
                    )
            elif ware_sku not in formatted_inventory[bom]:
                if wares_type == 0:
                    formatted_inventory[bom].update(
                        {ware_sku: {"warehouse_total": {'stock': stock, 'block': block}}}
                    )
                elif wares_type == 1:
                    formatted_inventory[bom].update(
                        {ware_sku: {"purchase_on_way": {'stock': stock, 'block': block}}}
                    )
                elif wares_type == 2:
                    formatted_inventory[bom].update(
                        {ware_sku: {"transfer_on_way": {'stock': stock, 'block': block}}}
                    )
                elif wares_type == 3:
                    formatted_inventory[bom].update(
                        {ware_sku: {"location_total": {'stock': stock, 'block': block}}}
                    )
                elif wares_type == 4:
                    formatted_inventory[bom].update(
                        {ware_sku: {kw_id: {'stock': stock, 'block': block}}}
                    )
            else:
                if wares_type == 0:
                    if formatted_inventory.get(bom).get(ware_sku).get('warehouse_total'):
                        formatted_inventory[bom][ware_sku]['warehouse_total']['stock'] += stock
                        formatted_inventory[bom][ware_sku]['warehouse_total']['block'] += block
                    else:
                        formatted_inventory[bom][ware_sku].update(
                            {"warehouse_total": {'stock': stock, 'block': block}}
                        )
                elif wares_type == 1:
                    if formatted_inventory.get(bom).get(ware_sku).get('purchase_on_way'):
                        formatted_inventory[bom][ware_sku]['purchase_on_way']['stock'] += stock
                        formatted_inventory[bom][ware_sku]['purchase_on_way']['block'] += block
                    else:
                        formatted_inventory[bom][ware_sku].update(
                            {"purchase_on_way": {'stock': stock, 'block': block}}
                        )
                elif wares_type == 2:
                    if formatted_inventory.get(bom).get(ware_sku).get('transfer_on_way'):
                        formatted_inventory[bom][ware_sku]['transfer_on_way']['stock'] += stock
                        formatted_inventory[bom][ware_sku]['transfer_on_way']['block'] += block
                    else:
                        formatted_inventory[bom][ware_sku].update(
                            {"transfer_on_way": {'stock': stock, 'block': block}}
                        )
                elif wares_type == 3:
                    if formatted_inventory.get(bom).get(ware_sku).get('location_total'):
                        formatted_inventory[bom][ware_sku]['location_total']['stock'] += stock
                        formatted_inventory[bom][ware_sku]['location_total']['block'] += block
                    else:
                        formatted_inventory[bom][ware_sku].update(
                            {"location_total": {'stock': stock, 'block': block}}
                        )
                elif wares_type == 4:
                    if formatted_inventory.get(bom).get(ware_sku).get(kw_id):
                        formatted_inventory[bom][ware_sku][kw_id]['stock'] += stock
                        formatted_inventory[bom][ware_sku][kw_id]['block'] += block
                    else:
                        formatted_inventory[bom][ware_sku].update(
                            {kw_id: {'stock': stock, 'block': block}}
                        )
        return formatted_inventory

    def get_format_wares_inventory_self(self, sale_sku_code, ck_id, to_ck_id):
        """
        仅查询指定销售sku在指定所属仓+目的仓的单个仓库数据,并格式化为统一库存结构进行返回
        :param str sale_sku_code: 销售sku编码
        :param int ck_id: 仓库id
        :param int to_ck_id: 目的仓id
        :return: 查询结果数据，字典格式
        """
        wares_inventory = self.dbo.query_wares_inventory(sale_sku_code, ck_id, to_ck_id)
        return self.format_wares_inventory(wares_inventory)

    def get_format_wares_inventory_all(self, sale_sku_code, ck_id, to_ck_id):
        """
        查询指定销售sku在全部相关仓库的数据,并格式化为统一库存结构进行返回
        :param str sale_sku_code: 销售sku编码
        :param int ck_id: 仓库id
        :param int to_ck_id: 目的仓id
        :return: 查询结果数据，字典格式
        """
        wares_inventory = self.dbo.query_wares_inventory(sale_sku_code, ck_id, to_ck_id, 2)
        return self.format_wares_inventory(wares_inventory)

    def get_format_goods_inventory(self, sale_sku_code, warehouse_id, to_warehouse_id):
        """
        查询指定销售sku的goods_inventory数据，并格式化为库存统一结构进行返回

        :param str sale_sku_code: 销售sku编码
        :param int warehouse_id: 仓库id
        :param int to_warehouse_id: 目的仓id
        :return: 查询结果数据，字典格式
        """
        goods_inventory = self.dbo.query_goods_inventory(sale_sku_code, warehouse_id, to_warehouse_id)
        formatted_goods_inventory = dict()
        for item in goods_inventory:
            # 销售商品采购在途库存
            if item['type'] == 1:
                formatted_goods_inventory.update({
                    'purchase_on_way_stock': item['stock'],
                    'purchase_on_way_remain': item['remain']
                })
            elif item['type'] == 2:
                formatted_goods_inventory.update({
                    'transfer_on_way_stock': item['stock'],
                    'transfer_on_way_remain': item['remain']
                })
            elif item['type'] == 3:
                formatted_goods_inventory.update({
                    'spot_goods_stock': item['stock'],
                    'spot_goods_remain': item['remain']
                })
        return formatted_goods_inventory

    def get_format_central_inventory(self, sale_sku_code, warehouse_id, to_warehouse_id):
        """
        查询指定销售sku的central_inventory数据，并格式化为库存统一结构进行返回
        :param str sale_sku_code: 销售sku编码
        :param int warehouse_id: 仓库id
        :param int to_warehouse_id: 目的仓id
        :return dict: 查询结果数据，字典格式
        """
        central_inventory = self.dbo.query_central_inventory(sale_sku_code, warehouse_id, to_warehouse_id)
        if not central_inventory:
            return {}
        else:
            return {
                "central_stock": central_inventory['stock'],
                # "central_block": central_inventory['block'],
                "central_remain": central_inventory['remain']
            }

    def get_lp_inventories(self, sale_sku_list, warehouse_id, to_warehouse_id) -> dict:
        """
        查询销售sku列表中各销售sku的库存数据，并全部格式化为库存统一格式进行返回
        :param list sale_sku_list: 销售sku编码列表
        :param int warehouse_id: 仓库id
        :param int to_warehouse_id: 目的仓库id
        :return: 格式化后的良品库存数据
        """
        result = dict()
        for sale_sku in sale_sku_list:
            result.update({sale_sku: self.get_lp_inventory(sale_sku, warehouse_id, to_warehouse_id)})
        return result

    def get_lp_inventory(self, sale_sku, warehouse_id, to_warehouse_id) -> dict:
        """
        查询销售sku的库存数据，并格式化为库存统一格式进行返回
        :param string sale_sku: 销售sku编码
        :param int warehouse_id: 仓库id
        :param int to_warehouse_id: 目的仓库id
        :return: 格式化后的良品库存数据
        """
        qualified_inventory = dict()
        central_inventory = self.get_format_central_inventory(sale_sku, warehouse_id, to_warehouse_id)
        goods_inventory = self.get_format_goods_inventory(sale_sku, warehouse_id, to_warehouse_id)
        wares_inventory = self.get_format_wares_inventory_self(sale_sku, warehouse_id, to_warehouse_id)
        if central_inventory:
            qualified_inventory.update(central_inventory)
        if goods_inventory:
            qualified_inventory.update(goods_inventory)
        if wares_inventory:
            qualified_inventory.update(wares_inventory)
        return qualified_inventory

    def get_sale_skus(self, ware_sku_qty_list) -> list:
        """
        根据ware_sku_qty_list计算出对应的销售sku列表
        :param list ware_sku_qty_list: 变更的仓库sku及数量列表，格式[(ware_sku,qty),...]
        """
        sale_sku_list = list()
        ware_sku_list = [_[0] for _ in self.combine_ware_sku_qty_list(ware_sku_qty_list)]
        for ware_sku in ware_sku_list:
            sale_sku = self.dbo.query_bom_detail_by_ware_sku_code(ware_sku)['goods_sku_code']
            if sale_sku not in sale_sku_list:
                sale_sku_list.append(sale_sku)
        return sale_sku_list

    def get_format_cp_inventory(self, sale_sku_code, warehouse_id, bom_version='') -> dict:
        """
        :param string sale_sku_code: 销售sku编码
        :param int warehouse_id: 仓库id
        :param string bom_version: bom版本
        :return: bom版本仓库sku明细字典
        """
        items = self.dbo.query_unqualified_inventory(sale_sku_code, warehouse_id, bom_version)
        ware_sku_inventory = dict()
        for item in items:
            if ware_sku_inventory.get(item['ware_sku_code']):
                if item['storage_location_id'] == 0:
                    ware_sku_inventory[item['ware_sku_code']].update(
                        {"total": {'stock': item['stock'], 'block': item['block']}}
                    )
                elif item['storage_location_id'] > 0:
                    ware_sku_inventory[item['ware_sku_code']].update(
                        {item['storage_location_id']: {'stock': item['stock'], 'block': item['block']}}
                    )
            else:
                if item['storage_location_id'] == 0:
                    ware_sku_inventory.update({
                        item['ware_sku_code']: {"total": {'stock': item['stock'], 'block': item['block']}}
                    })
                elif item['storage_location_id'] > 0:
                    ware_sku_inventory.update({
                        item['ware_sku_code']: {
                            item['storage_location_id']: {'stock': item['stock'], 'block': item['block']}}
                    })
        return ware_sku_inventory

    def calculate_sets(self, ware_sku_qty_list):
        sale_sku_dict = dict()
        result_sku_suites = dict()
        for ware_sku, qty in ware_sku_qty_list:
            sale_sku_info = self.dbo.query_bom_detail_by_ware_sku_code(ware_sku)
            if sale_sku_info['goods_sku_code'] not in sale_sku_dict:
                sale_sku_dict.update({
                    sale_sku_info['goods_sku_code']: {
                        sale_sku_info['bom_version']: {
                            ware_sku: qty
                        }
                    }
                })
            elif sale_sku_info['bom_version'] not in sale_sku_dict[sale_sku_info['goods_sku_code']]:
                sale_sku_dict[sale_sku_info['goods_sku_code']].update({
                    sale_sku_info['bom_version']: {
                        ware_sku: qty
                    }
                })
            elif ware_sku not in sale_sku_dict[sale_sku_info['goods_sku_code']][sale_sku_info['bom_version']]:
                sale_sku_dict[sale_sku_info['goods_sku_code']][sale_sku_info['bom_version']].update({
                    ware_sku: qty
                })
            else:
                sale_sku_dict[sale_sku_info['goods_sku_code']][sale_sku_info['bom_version']][ware_sku] += qty
        for sale_sku in sale_sku_dict:
            for bom in sale_sku_dict[sale_sku]:
                bom_detail = self.dbo.query_bom_detail(sale_sku, bom)
                if len(sale_sku_dict[sale_sku][bom]) < len(bom_detail):
                    result_sku_suites.update(
                        {sale_sku: 0}
                    )
                else:
                    result_suites = list()
                    for ware_sku, qty in sale_sku_dict[sale_sku][bom].items():
                        suites = qty // self.dbo.query_bom_detail(sale_sku, bom)[ware_sku]
                        result_suites.append(suites)
                    min_suites = min(result_suites)
                    if result_sku_suites.get(sale_sku):
                        result_sku_suites[sale_sku] += min_suites
                    else:
                        result_sku_suites.update(
                            {sale_sku: min(result_suites)}
                        )
        return result_sku_suites

    def calc_suites(self, sale_sku, bom, wares_inventory, inventory_type):
        """
        根据格式化好的期望wares_inventory库存数据，匹配bom版本明细计算各销售成套数
        :param string sale_sku: 销售sku编码
        :param string bom: bom版本
        :param dict wares_inventory: 销售sku对应bom的wares_inventory库存数据
        :param string inventory_type: purchase_on_way，transfer_on_way，warehouse_total，location_total
        :return: min_stock:成套库存数, max_block:成套预占数, remain:剩余数（库存-预占)
        """
        result_stock = list()
        result_block = list()
        bom_detail = self.dbo.query_bom_detail(sale_sku, bom)
        if len(wares_inventory) < len(bom_detail):
            return 0, 0
        else:
            for ware_sku in wares_inventory:
                if inventory_type not in wares_inventory[ware_sku]:
                    stock = 0
                    block = 0
                else:
                    stock = wares_inventory[ware_sku].get(inventory_type).get('stock')
                    block = wares_inventory[ware_sku].get(inventory_type).get('block')
                # 库存整除、向下取整
                goods_stock = stock // bom_detail[ware_sku]
                # 预占向上取整
                goods_block = math.ceil(block / bom_detail[ware_sku])
                result_stock.append(goods_stock)
                result_block.append(goods_block)
            # 整套算时预占取最大，库存取最小
            min_stock = min(result_stock)
            max_block = max(result_block)
            remain = min_stock - max_block
        return min_stock, remain

    @classmethod
    def combine_ware_sku_qty_list(cls, ware_sku_qty_list) -> list:
        """
        把ware_sku_qty_list去重合且累加数量
        :param list ware_sku_qty_list: 变动的ware_sku、qty列表，格式[(ware_sku,qty),...]
        """
        ware_sku_list = list()
        temp_dict = dict()
        for ware_sku, qty in ware_sku_qty_list:
            if ware_sku in temp_dict:
                temp_dict[ware_sku] += qty
            else:
                temp_dict.update({ware_sku: qty})
        for ware_sku, total_qty in temp_dict.items():
            ware_sku_list.append((ware_sku, total_qty))
        return sorted(ware_sku_list, key=lambda s: s[0])

    def get_add_stock_change_inventory(self, ware_sku_qty_list, kw_ids_list=None) -> dict:
        """
        把ware_sku_qty_list格式化库存统一格式
        :param list ware_sku_qty_list: 变动的ware_sku、qty列表，格式[(ware_sku,qty),...]
        :param list optional kw_ids_list: 库位id列表
        """
        result_dict = dict()
        if kw_ids_list:
            for (ware_sku, qty), kw_id in zip(ware_sku_qty_list, kw_ids_list):
                bom_detail_info = self.dbo.query_bom_detail_by_ware_sku_code(ware_sku)
                sale_sku, bom = bom_detail_info['goods_sku_code'], bom_detail_info['bom_version']
                if sale_sku not in result_dict:
                    result_dict.update({
                        sale_sku: {bom: {ware_sku: {kw_id: qty}}}
                    })
                elif bom not in result_dict[sale_sku]:
                    result_dict[sale_sku].update({
                        bom: {ware_sku: {kw_id: qty}}
                    })
                elif ware_sku not in result_dict[sale_sku][bom]:
                    result_dict[sale_sku][bom].update(
                        {ware_sku: {kw_id: qty}}
                    )
                elif kw_id not in result_dict[sale_sku][bom][ware_sku]:
                    result_dict[sale_sku][bom][ware_sku].update(
                        {kw_id: qty}
                    )
                else:
                    result_dict[sale_sku][bom][ware_sku][kw_id] += qty
        else:
            for ware_sku, qty in ware_sku_qty_list:
                bom_detail_info = self.dbo.query_bom_detail_by_ware_sku_code(ware_sku)
                sale_sku, bom = bom_detail_info['goods_sku_code'], bom_detail_info['bom_version']
                if sale_sku not in result_dict:
                    result_dict.update({
                        sale_sku: {bom: {ware_sku: qty}}
                    })
                elif bom not in result_dict[sale_sku]:
                    result_dict[sale_sku][bom].update(
                        {ware_sku: qty}
                    )
                elif ware_sku not in result_dict[bom]:
                    result_dict[sale_sku][bom].update(
                        {ware_sku: qty}
                    )
                else:
                    result_dict[sale_sku][bom][ware_sku] += qty
        return result_dict

    def get_deduct_kw_stock_change_inventory(self, ware_sku_kw_qty_list) -> dict:
        """
        把ware_sku_qty_list格式化库存统一格式
        :param list ware_sku_kw_qty_list: 变动的ware_sku、qty列表，格式[(ware_sku,qty),...]
        """
        result_dict = dict()

        for ware_sku, qty, kw_id in ware_sku_kw_qty_list:
            bom_detail_info = self.dbo.query_bom_detail_by_ware_sku_code(ware_sku)
            sale_sku, bom = bom_detail_info['goods_sku_code'], bom_detail_info['bom_version']
            if sale_sku not in result_dict:
                result_dict.update({
                    sale_sku: {bom: {ware_sku: {kw_id: qty}}}
                })
            elif bom not in result_dict[sale_sku]:
                result_dict[sale_sku].update({
                    bom: {ware_sku: {kw_id: qty}}
                })
            elif ware_sku not in result_dict[sale_sku][bom]:
                result_dict[sale_sku][bom].update(
                    {ware_sku: {kw_id: qty}}
                )
            elif kw_id not in result_dict[sale_sku][bom][ware_sku]:
                result_dict[sale_sku][bom][ware_sku].update(
                    {kw_id: qty}
                )
            else:
                result_dict[sale_sku][bom][ware_sku][kw_id] += qty
        return result_dict

    def get_format_expect_wares_inventory(self, ware_sku_qty_list, ck_id, to_ck_id, data_type,
                                          inventory_type='warehouse_total'):
        """
        根据变更的仓库sku及数量列表计算加库存后期望wares_inventory库存数据，按库存数据统一结构返回
        :param list ware_sku_qty_list: 变动的ware_sku、qty列表，格式[(ware_sku,qty),...]
        :param int ck_id: 所属仓库id
        :param int to_ck_id: 目的仓库id
        :param int data_type: 数据范围，1:仅查询本仓数据；2:查询全部相关数据
        :param inventory_type: 加的库存类型，枚举：transfer_on_way,purchase_on_way,warehouse_total
        """
        result_dict = dict()

        change_inventory = self.get_add_stock_change_inventory(ware_sku_qty_list)
        for sale_sku in change_inventory:
            if data_type == 1:
                wares_inventory = self.get_format_wares_inventory_self(sale_sku, ck_id, to_ck_id)
            else:
                wares_inventory = self.get_format_wares_inventory_all(sale_sku, ck_id, to_ck_id)
            temp_dict = dict()
            for bom in change_inventory[sale_sku]:
                for ware_sku, qty in change_inventory[sale_sku][bom].items():
                    # 如果查到库存数据，根据仓库sku是否在库存数据中存在处理库存数据
                    if wares_inventory:
                        if inventory_type == 'warehouse_total':
                            if bom not in wares_inventory:
                                wares_inventory.update(
                                    {bom: {ware_sku: {inventory_type: {'stock': qty, 'block': 0}}}}
                                )
                            elif ware_sku not in wares_inventory[bom]:
                                wares_inventory[bom].update(
                                    {ware_sku: {inventory_type: {'stock': qty, 'block': 0}}}
                                )
                            elif inventory_type not in wares_inventory[bom][ware_sku]:
                                wares_inventory[bom][ware_sku].update(
                                    {inventory_type: {'stock': qty, 'block': 0}}
                                )
                            else:
                                wares_inventory[bom][ware_sku][inventory_type]['stock'] += qty
                            temp_dict.update(wares_inventory)
                        else:
                            if bom not in wares_inventory:
                                wares_inventory.update(
                                    {bom: {ware_sku: {inventory_type: {'stock': qty, 'block': 0},
                                                      'warehouse_total': {'stock': qty, 'block': 0}}}}
                                )
                            elif ware_sku not in wares_inventory[bom]:
                                wares_inventory[bom].update(
                                    {ware_sku: {inventory_type: {'stock': qty, 'block': 0},
                                                'warehouse_total': {'stock': qty, 'block': 0}}}
                                )
                            elif inventory_type not in wares_inventory[bom][ware_sku]:
                                wares_inventory[bom][ware_sku].update(
                                    {inventory_type: {'stock': qty, 'block': 0},
                                     'warehouse_total': {'stock': qty, 'block': 0}}
                                )
                            else:
                                wares_inventory[bom][ware_sku][inventory_type]['stock'] += qty
                                wares_inventory[bom][ware_sku]['warehouse_total']['stock'] += qty
                            temp_dict.update(wares_inventory)

                    else:
                        if inventory_type == 'warehouse_total':
                            if bom not in temp_dict:
                                temp_dict.update(
                                    {bom: {ware_sku: {inventory_type: {'stock': qty, 'block': 0}}}}
                                )
                            elif ware_sku not in temp_dict[bom]:
                                temp_dict[bom].update(
                                    {ware_sku: {inventory_type: {'stock': qty, 'block': 0}}}
                                )
                            elif inventory_type not in temp_dict[bom][ware_sku]:
                                wares_inventory[bom][ware_sku].update(
                                    {inventory_type: {'stock': qty, 'block': 0}}
                                )
                            else:
                                temp_dict[bom][ware_sku][inventory_type]['stock'] += qty
                        else:
                            if bom not in temp_dict:
                                temp_dict.update(
                                    {bom: {ware_sku: {inventory_type: {'stock': qty, 'block': 0},
                                                      'warehouse_total': {'stock': qty, 'block': 0}}}}
                                )
                            elif ware_sku not in temp_dict[bom]:
                                temp_dict[bom].update(
                                    {ware_sku: {inventory_type: {'stock': qty, 'block': 0},
                                                'warehouse_total': {'stock': qty, 'block': 0}}}
                                )
                            elif inventory_type not in temp_dict[bom][ware_sku]:
                                wares_inventory[bom][ware_sku].update(
                                    {inventory_type: {'stock': qty, 'block': 0},
                                     'warehouse_total': {'stock': qty, 'block': 0}}
                                )
                            else:
                                temp_dict[bom][ware_sku][inventory_type]['stock'] += qty
                                temp_dict[bom][ware_sku]['warehouse_total']['stock'] += qty
            result_dict.update({sale_sku: temp_dict})
        return result_dict

    def get_format_expect_wares_inventory_with_kw(self, ware_sku_qty_list, kw_ids_list, ck_id, to_ck_id,
                                                  data_type):
        """
        根据变更的仓库sku及数量列表计算加库位库存后期望wares_inventory库存数据，按库存数据统一结构返回
        :param list ware_sku_qty_list: 变动的ware_sku、qty列表，格式[(ware_sku,qty),...]
        :param list kw_ids_list: 库位id列表
        :param int ck_id: 所属仓库id
        :param int to_ck_id: 目的仓库id
        :param int data_type: 数据范围，1:仅查询本仓数据；2:查询全部相关数据
        """
        result_dict = dict()

        change_inventory = self.get_add_stock_change_inventory(ware_sku_qty_list, kw_ids_list)
        for sale_sku in change_inventory:
            if data_type == 1:
                wares_inventory = self.get_format_wares_inventory_self(sale_sku, ck_id, to_ck_id)
            else:
                wares_inventory = self.get_format_wares_inventory_all(sale_sku, ck_id, to_ck_id)
            temp_dict = dict()
            for bom in change_inventory[sale_sku]:
                for ware_sku in change_inventory[sale_sku][bom]:
                    for kw_id, qty in change_inventory[sale_sku][bom][ware_sku].items():
                        # 如果查到库存数据，根据仓库sku是否在库存数据中存在处理库存数据
                        if wares_inventory:
                            if bom not in wares_inventory:
                                wares_inventory.update(
                                    {bom: {
                                        ware_sku: {
                                            kw_id: {'stock': qty, 'block': 0},
                                            'warehouse_total': {'stock': qty, 'block': 0},
                                            'location_total': {'stock': qty, 'block': 0}}}}
                                )
                            elif ware_sku not in wares_inventory[bom]:
                                wares_inventory[bom].update({
                                    ware_sku: {
                                        kw_id: {'stock': qty, 'block': 0},
                                        'warehouse_total': {'stock': qty, 'block': 0},
                                        'location_total': {'stock': qty, 'block': 0}
                                    }
                                })
                            elif kw_id not in wares_inventory[bom][ware_sku]:
                                wares_inventory[bom][ware_sku].update({
                                    kw_id: {'stock': qty, 'block': 0}
                                })
                                wares_inventory[bom][ware_sku]['warehouse_total']['stock'] += qty
                                if wares_inventory[bom][ware_sku].get('location_total'):
                                    wares_inventory[bom][ware_sku]['location_total']['stock'] += qty
                                else:
                                    wares_inventory[bom][ware_sku].update({
                                        'location_total': {'stock': qty, 'block': 0}
                                    })
                            else:
                                wares_inventory[bom][ware_sku][kw_id]['stock'] += qty
                                wares_inventory[bom][ware_sku]['warehouse_total']['stock'] += qty
                                wares_inventory[bom][ware_sku]['location_total']['stock'] += qty
                            temp_dict.update(wares_inventory)
                        else:
                            if bom not in temp_dict:
                                temp_dict.update({
                                    bom: {
                                        ware_sku: {kw_id: {'stock': qty, 'block': 0},
                                                   'warehouse_total': {'stock': qty, 'block': 0},
                                                   'location_total': {'stock': qty, 'block': 0}}}
                                })
                            elif ware_sku not in temp_dict[bom]:
                                temp_dict[bom].update({
                                    ware_sku: {
                                        kw_id: {'stock': qty, 'block': 0},
                                        'warehouse_total': {'stock': qty, 'block': 0},
                                        'location_total': {'stock': qty, 'block': 0}}
                                })
                            elif kw_id not in temp_dict[bom][ware_sku]:
                                temp_dict[bom][ware_sku].update({
                                    kw_id: {'stock': qty, 'block': 0}
                                })
                                temp_dict[bom][ware_sku]['warehouse_total']['stock'] += qty
                                temp_dict[bom][ware_sku]['location_total']['stock'] += qty
                            else:
                                temp_dict[bom][ware_sku][kw_id]['stock'] += qty
                                temp_dict[bom][ware_sku]['warehouse_total']['stock'] += qty
                                temp_dict[bom][ware_sku]['location_total']['stock'] += qty
            result_dict.update({
                sale_sku: temp_dict
            })
        return result_dict

    def get_expect_goods_inventory(self, wares_inventory, ck_id, to_ck_id):
        """
        根据wares_inventory生成goods_inventory期望库存，并格式化为统一库存格式返回
        :param dict wares_inventory: 格式化为统一库存结构的wares_inventory数据
        :param int ck_id: 所属仓库id
        :param int to_ck_id: 目的仓库id
        """
        result_dict = dict()
        for sale_sku in wares_inventory:
            total_spot_stock = 0
            total_spot_remain = 0
            total_transfer_stock = 0
            total_transfer_remain = 0
            total_purchase_stock = 0
            total_purchase_remain = 0

            temp_inventory = dict()

            for bom in wares_inventory[sale_sku]:
                inventory = wares_inventory[sale_sku][bom]
                spot_stock, spot_remain = self.calc_suites(sale_sku, bom, inventory, 'location_total')
                total_spot_stock += spot_stock
                total_spot_remain += spot_remain
                if total_spot_stock >= 0:
                    temp_inventory.update({
                        'spot_goods_stock': total_spot_stock,
                        'spot_goods_remain': total_spot_remain
                    })
                transfer_stock, transfer_remain = self.calc_suites(sale_sku, bom, inventory, 'transfer_on_way')
                total_transfer_stock += transfer_stock
                total_transfer_remain += transfer_remain
                if total_transfer_stock > 0:
                    temp_inventory.update({
                        'transfer_on_way_stock': total_transfer_stock,
                        'transfer_on_way_remain': total_transfer_remain
                    })
                purchase_stock, purchase_remain = self.calc_suites(sale_sku, bom, inventory, 'purchase_on_way')
                total_purchase_stock += purchase_stock
                total_purchase_remain += purchase_remain
                if total_purchase_stock > 0:
                    temp_inventory.update({
                        'purchase_on_way_stock': total_purchase_stock,
                        'purchase_on_way_remain': total_purchase_remain
                    })
            goods_inventory = self.get_format_goods_inventory(sale_sku, ck_id, to_ck_id)
            goods_inventory.update(temp_inventory)
            result_dict.update({
                sale_sku: goods_inventory
            })
        return result_dict

    def get_expect_central_inventory(self, wares_inventory, ck_id, to_ck_id):
        """
        根据wares_inventory生成central_inventory期望库存，并格式化为统一库存格式返回
        :param dict wares_inventory: 格式化为统一库存结构的wares_inventory数据
        :param int ck_id: 所属仓库id
        :param int to_ck_id: 目的仓库id
        """
        result_dict = dict()
        for sale_sku in wares_inventory:
            total_stock = 0
            total_remain = 0
            for bom in wares_inventory[sale_sku]:
                inventory = wares_inventory[sale_sku][bom]
                stock, remain = self.calc_suites(sale_sku, bom, inventory, 'warehouse_total')
                total_stock += stock
                total_remain += remain
            central_inventory = self.get_format_central_inventory(sale_sku, ck_id, to_ck_id)
            if central_inventory:
                central_inventory['central_stock'] = total_stock
                central_inventory['central_remain'] = total_remain
            else:
                central_inventory.update({
                    'central_stock': total_stock,
                    'central_remain': total_remain
                })
            result_dict.update({
                sale_sku: central_inventory
            })
        return result_dict

    def get_add_kw_stock_expect_inventory(self, ware_sku_qty_list, kw_ids_list, ck_id, to_ck_id):
        """
        计算带库位的库存变动后的期望库存
        :param list ware_sku_qty_list: 变动的ware_sku、qty列表，格式[(ware_sku,qty),...]
        :param list kw_ids_list: 库位id列表
        :param int ck_id: 所属仓库id
        :param int to_ck_id: 目的仓库id
        """
        wares_inventory_for_goods = self.get_format_expect_wares_inventory_with_kw(ware_sku_qty_list,
                                                                                   kw_ids_list, ck_id,
                                                                                   to_ck_id, 1)
        wares_inventory_for_central = self.get_format_expect_wares_inventory_with_kw(ware_sku_qty_list,
                                                                                     kw_ids_list,
                                                                                     ck_id, to_ck_id, 2)
        wares_inventory = self.get_format_expect_wares_inventory_with_kw(ware_sku_qty_list, kw_ids_list, ck_id,
                                                                         to_ck_id,
                                                                         1)

        expect_goods_inventory = self.get_expect_goods_inventory(wares_inventory_for_goods, ck_id, to_ck_id)
        expect_central_inventory = self.get_expect_central_inventory(wares_inventory_for_central, ck_id, to_ck_id)

        for sale_sku in wares_inventory:
            wares_inventory[sale_sku].update(expect_goods_inventory[sale_sku])
            wares_inventory[sale_sku].update(expect_central_inventory[sale_sku])
        return wares_inventory

    def get_cp_other_in_expect_inventory(self, origin_cp_inventory, ware_sku_qty_list, location_list):
        result_dict = dict()
        sale_sku_list = self.get_sale_skus(ware_sku_qty_list)
        for sale_sku in sale_sku_list:
            # 构造库位期望库存，更新到temp_ware_dict中
            for (ware_sku, qty), cp_location_id in zip(ware_sku_qty_list, location_list):
                if self.dbo.query_bom_detail_by_ware_sku_code(ware_sku)['goods_sku_code'] != sale_sku:
                    continue
                if origin_cp_inventory.get(ware_sku):
                    if origin_cp_inventory[ware_sku].get(cp_location_id):
                        origin_cp_inventory[ware_sku][cp_location_id]['stock'] += qty
                    else:
                        origin_cp_inventory[ware_sku].update({
                            cp_location_id: {'stock': qty, 'block': 0}
                        })
                    if origin_cp_inventory[ware_sku].get('total'):
                        origin_cp_inventory[ware_sku]['total']['stock'] += qty
                    else:
                        origin_cp_inventory[ware_sku].update({
                            'total': {'stock': qty, 'block': 0}
                        })
                else:
                    # 更新temp_ware_dict写入库位总库存和仓库总库存
                    origin_cp_inventory.update({
                        ware_sku: {
                            'total': {'stock': qty, 'block': 0},
                            cp_location_id: {'stock': qty, 'block': 0}
                        }
                    })
            result_dict.update({
                sale_sku: origin_cp_inventory
            })
        return result_dict

    def get_purchase_in_expect_inventory(self, ware_sku_qty_list, kw_ids_list, ck_id, to_ck_id):
        """
        计算带库位的库存变动后的期望库存
        :param list ware_sku_qty_list: 变动的ware_sku、qty列表，格式[(ware_sku,qty),...]
        :param list kw_ids_list: 库位id列表
        :param int ck_id: 所属仓库id
        :param int to_ck_id: 目的仓库id
        """
        wares_inventory_for_goods = self.get_format_expect_wares_inventory_with_kw(ware_sku_qty_list, kw_ids_list,
                                                                                   ck_id, to_ck_id, 1)
        wares_inventory_for_central = self.get_format_expect_wares_inventory_with_kw(ware_sku_qty_list,
                                                                                     kw_ids_list, ck_id, to_ck_id, 2)
        wares_inventory = self.get_format_expect_wares_inventory_with_kw(ware_sku_qty_list, kw_ids_list, ck_id,
                                                                         to_ck_id, 1)

        expect_goods_inventory = self.get_expect_goods_inventory(wares_inventory_for_goods, ck_id, to_ck_id)
        expect_central_inventory = self.get_expect_central_inventory(wares_inventory_for_central, ck_id, to_ck_id)

        for sale_sku in wares_inventory:
            wares_inventory[sale_sku].update(expect_goods_inventory[sale_sku])
            wares_inventory[sale_sku].update(expect_central_inventory[sale_sku])
        return wares_inventory
        # # 用来存储最终要返回的销售sku的期望库存字典
        # result_dict = dict()
        # sale_sku_suites_dict = self.calculate_sets(ware_sku_qty_list)
        # for sale_sku in sale_sku_suites_dict:
        #     expect_lp_inventory = dict()
        #     # 更新销售商品总库存
        #     expect_lp_inventory.update({
        #         'central_stock': sale_sku_suites_dict[sale_sku],
        #         'central_block': 0,
        #         'central_remain': sale_sku_suites_dict[sale_sku],
        #         'purchase_on_way_stock': 0,
        #         'purchase_on_way_remain': 0,
        #         'spot_goods_stock': sale_sku_suites_dict[sale_sku],
        #         'spot_goods_remain': sale_sku_suites_dict[sale_sku]
        #     })
        #     # 构造库位期望库存，更新到temp_ware_dict中
        #     for (ware_sku, qty), sj_location_id in zip(ware_sku_qty_list, location_list):
        #         if self.dbo.query_bom_detail_by_ware_sku_code(ware_sku)['goods_sku_code'] != sale_sku:
        #             continue
        #         if expect_lp_inventory.get(ware_sku):
        #             if expect_lp_inventory[ware_sku].get(sj_location_id):
        #                 expect_lp_inventory[ware_sku][sj_location_id]['stock'] += qty
        #             else:
        #                 expect_lp_inventory[ware_sku].update({
        #                     sj_location_id: {'stock': qty, 'block': 0}
        #                 })
        #             if expect_lp_inventory[ware_sku].get('warehouse_total'):
        #                 expect_lp_inventory[ware_sku]['warehouse_total']['stock'] += qty
        #             else:
        #                 expect_lp_inventory[ware_sku].update({
        #                     'warehouse_total': {'stock': qty, 'block': 0}
        #                 })
        #             if expect_lp_inventory[ware_sku].get('location_total'):
        #                 expect_lp_inventory[ware_sku]['location_total']['stock'] += qty
        #             else:
        #                 expect_lp_inventory[ware_sku].update({
        #                     'location_total': {'stock': qty, 'block': 0}
        #                 })
        #             if expect_lp_inventory[ware_sku].get('purchase_on_way'):
        #                 expect_lp_inventory[ware_sku]['purchase_on_way']['stock'] += qty
        #             else:
        #                 expect_lp_inventory[ware_sku].update({
        #                     'purchase_on_way': {'stock': qty, 'block': 0}
        #                 })
        #         else:
        #             # 更新temp_ware_dict写入库位总库存和仓库总库存
        #             expect_lp_inventory.update({
        #                 ware_sku: {
        #                     'warehouse_total': {'stock': qty, 'block': 0},
        #                     'location_total': {'stock': qty, 'block': 0},
        #                     'purchase_on_way': {'stock': 0, 'block': 0},
        #                     sj_location_id: {'stock': qty, 'block': 0}
        #                 }
        #             })
        #     result_dict.update({
        #         sale_sku: expect_lp_inventory
        #     })
        # return result_dict

    def get_purchase_create_order_expect_inventory(self, ware_sku_qty_list, ck_id, to_ck_id):
        # 用来存储最终要返回的销售sku的期望库存字典
        wares_inventory_for_goods = self.get_format_expect_wares_inventory(ware_sku_qty_list, ck_id,
                                                                           to_ck_id, 1, 'purchase_on_way')
        wares_inventory_for_central = self.get_format_expect_wares_inventory(ware_sku_qty_list, ck_id,
                                                                             to_ck_id, 2, 'warehouse_total')
        wares_inventory = self.get_format_expect_wares_inventory(ware_sku_qty_list, ck_id, to_ck_id, 1,
                                                                 'purchase_on_way')

        expect_goods_inventory = self.get_expect_goods_inventory(wares_inventory_for_goods, ck_id, to_ck_id)
        expect_central_inventory = self.get_expect_central_inventory(wares_inventory_for_central, ck_id, to_ck_id)

        for sale_sku in wares_inventory:
            wares_inventory[sale_sku].update(expect_goods_inventory[sale_sku])
            wares_inventory[sale_sku].update(expect_central_inventory[sale_sku])
        return wares_inventory

    def add_cp_stock_by_other_in(self, sale_sku_code, bom_version, add_stock_count, cp_location_ids,
                                 warehouse_id, to_warehouse_id):
        """
        :param str sale_sku_code: 销售sku编码
        :param str bom_version: bom版本
        :param int add_stock_count: 销售sku件数
        :param list cp_location_ids: 次品库位列表
        :param int warehouse_id: 仓库id
        :param int to_warehouse_id: 目的仓库id
        """
        details = self.dbo.query_bom_detail(sale_sku_code, bom_version)
        ware_sku_qty_list = list()
        for ware_sku, qty in details.items():
            ware_sku_qty_list.append((ware_sku, qty * add_stock_count))
        res = self.cp_other_in(ware_sku_qty_list, cp_location_ids, warehouse_id, to_warehouse_id)
        return res

    @classmethod
    def get_combined_block_result_list(cls, block_result_list):
        ware_sku_list = list()
        temp_dict = dict()
        for result in block_result_list:
            ware_sku = result["wareSkuCode"]
            qty = result["qty"]
            if ware_sku in temp_dict:
                temp_dict[ware_sku] += qty
            else:
                temp_dict.update({
                    ware_sku: qty
                })
        for ware_sku, total_qty in temp_dict.items():
            ware_sku_list.append(
                (ware_sku, total_qty)
            )
        return sorted(ware_sku_list, key=lambda s: s[0])

    def move_dock_to_sj_kw(self, warehouse_id, source_no, ware_sku_qty_list, sj_kw_ids):
        """
        从dock库位转移库存到上架库位

        :param warehouse_id:
        :param source_no:
        :param ware_sku_qty_list:
        :param sj_kw_ids:
        :return:
        """
        ware_sku_list = list()
        for (ware_sku, qty), sj_kw_id in zip(ware_sku_qty_list, sj_kw_ids):
            ware_sku_list.append({
                "fromStorageLocationId": -warehouse_id,
                "qty": qty,
                "toStorageLocationId": sj_kw_id,
                "toStorageLocationType": "5",
                "toTargetWarehouseId": warehouse_id,
                "wareSkuCode": ware_sku
            })
        move_res = self.move_stock(source_no, ware_sku_list)
        return move_res

    # 确认拣货
    def confirm_all_picked(self, delivery_order_no, block_ware_list, warehouse_id):
        pick_res = self.confirm_pick(delivery_order_no, block_ware_list, warehouse_id)
        return pick_res

    def is_stock_satisfy(self, sale_sku_list, warehouse_id, to_warehouse_id) -> bool:
        """
        是否有可用库存

        :param list sale_sku_list: 销售sku编码列表
        :param int warehouse_id: 所属仓库id
        :param any to_warehouse_id: 目的仓库id
        """
        for sale_sku in sale_sku_list:
            inventory = self.get_format_goods_inventory(sale_sku, warehouse_id, to_warehouse_id)
            # try:
            remain = inventory.get("spot_goods_remain")
            if remain > 0:
                continue
            else:
                return False
        return True
        # except :
        #     return False

    @until(50, 0.2)
    def is_bom_stock_enough(self, sale_sku, bom, qty, warehouse_id, to_warehouse_id):
        """
        是否有指定数量库存
        :param sale_sku: 销售sku编码
        :param bom: bom版本
        :param qty: 数量
        :param warehouse_id: 仓库id
        :param to_warehouse_id: 目的id
        """
        inventory = self.get_format_wares_inventory_self(sale_sku, warehouse_id, to_warehouse_id)
        try:
            bom_inventory = inventory[bom]
            stock, remain = self.calc_suites(sale_sku, bom, bom_inventory, "location_total")
            if remain >= qty:
                return True
            else:
                return False
        except KeyError:
            return False


if __name__ == '__main__':
    ims = IMSRobot()
    # ims.del_stock(["16338527895"])
    # ims.del_stock(["63203684930"])
    # self.add_bom_stock("JF2KB93311", "C", 1, [1496], 513, 513)
    # self.add_bom_stock("JF2KB93311", "D", 1, [1544], 512, '')
    # ware_inventory = [["16338527895A01", 1]]
    # print(ims.get_format_expect_wares_inventory_with_kw(ware_inventory, [1496, 1505], 513, 513, 1))
    print(ims.stock_enough_required("63203684930", "C", 999999, 511, 513))
