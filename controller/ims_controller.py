import time

from utils.request_handler import RequestHandler
from config.api_config.ims_api_config import ims_api_config
from config.sys_config import env_config
from db_operator.ims_db_operate import IMSDBOperator


class ImsController(RequestHandler):
    def __init__(self):
        self.prefix = env_config.get('ims_service_prefix')
        self.service_headers = {"serviceName": "ec-warehouse-delivery-service"}
        super().__init__(self.prefix, self.service_headers)

    # 获取仓库商品总库存
    def get_wares_inventory_by_target_warehouse_id(self, sale_sku_code, to_warehouse_id):
        sql = """
           SELECT
               ware_sku_code,type,storage_location_id,stock,block 
           FROM
               wares_inventory 
           WHERE
               goods_sku_code = "%s"
               AND target_warehouse_id = %s
           ORDER BY
               ware_sku_code;
           """ % (sale_sku_code, to_warehouse_id if to_warehouse_id else 0)

        ware_inventory = self.db.get_all(sql)
        formatted_ware_sku_inventory = dict()
        for data in ware_inventory:
            # print(data)
            if data['ware_sku_code'] not in formatted_ware_sku_inventory:
                if data['type'] == 4:
                    formatted_ware_sku_inventory.update({
                        data['ware_sku_code']: {
                            data['storage_location_id']: {'stock': data['stock'], 'block': 0}}
                    })
                else:
                    formatted_ware_sku_inventory.update({
                        data['ware_sku_code']: {
                            data['type']: {'stock': data['stock'], 'block': 0}}
                    })
            elif data['type'] not in formatted_ware_sku_inventory[data['ware_sku_code']]:
                if data['type'] == 4:
                    formatted_ware_sku_inventory[data['ware_sku_code']].update({
                        data['storage_location_id']: {'stock': data['stock'], 'block': 0}
                    })
                else:
                    formatted_ware_sku_inventory[data['ware_sku_code']].update({
                        data['type']: {'stock': data['stock'], 'block': 0}
                    })
            else:
                formatted_ware_sku_inventory[data['ware_sku_code']][data['type']]['stock'] += data['stock']
        return formatted_ware_sku_inventory

    def get_wares_inventory_by_warehouse_id(self, sale_sku_code, warehouse_id):
        sql = """
           SELECT
               ware_sku_code,type,storage_location_id as location_id,stock,block 
           FROM
               wares_inventory 
           WHERE
               goods_sku_code = "%s"
               AND warehouse_id = %s
           ORDER BY
               ware_sku_code;
           """ % (sale_sku_code, warehouse_id)

        ware_inventory = self.db.get_all(sql)
        formatted_ware_sku_inventory = dict()
        for data in ware_inventory:
            if formatted_ware_sku_inventory.get(data['ware_sku_code']):
                if data['type'] == 0:
                    formatted_ware_sku_inventory[data['ware_sku_code']].update(
                        {"0": {'stock': data['stock'], 'block': data['block']}}
                    )
                elif data['type'] == 1:
                    formatted_ware_sku_inventory[data['ware_sku_code']].update(
                        {"1": {'stock': data['stock'], 'block': data['block']}}
                    )
                elif data['type'] == 2:
                    formatted_ware_sku_inventory[data['ware_sku_code']].update(
                        {"2": {'stock': data['stock'], 'block': data['block']}}
                    )
                elif data['type'] == 3:
                    formatted_ware_sku_inventory[data['ware_sku_code']].update(
                        {"3": {'stock': data['stock'], 'block': data['block']}}
                    )
                elif data['type'] == 4:
                    formatted_ware_sku_inventory[data['ware_sku_code']].update(
                        {str(data['location_id']): {'stock': data['stock'], 'block': data['block']}}
                    )
            else:
                if data['type'] == 0:
                    formatted_ware_sku_inventory.update(
                        {data['ware_sku_code']: {
                            "0": {'stock': data['stock'], 'block': data['block']}}}
                    )
                elif data['type'] == 1:
                    formatted_ware_sku_inventory.update(
                        {data['ware_sku_code']: {
                            "1": {'stock': data['stock'], 'block': data['block']}}}
                    )
                elif data['type'] == 2:
                    formatted_ware_sku_inventory.update(
                        {data['ware_sku_code']: {
                            "2": {'stock': data['stock'], 'block': data['block']}}}
                    )
                elif data['type'] == 3:
                    formatted_ware_sku_inventory.update(
                        {data['ware_sku_code']: {
                            "3": {'stock': data['stock'], 'block': data['block']}}}
                    )
                elif data['type'] == 4:
                    formatted_ware_sku_inventory.update(
                        {data['ware_sku_code']: {
                            str(data["location_id"]): {'stock': data['stock'], 'block': data['block']}}}
                    )
        return formatted_ware_sku_inventory

    def calculate_sets(self, ware_sku_qty_list):
        sale_sku_dict = dict()
        result_sku_suites = dict()
        for ware_sku, qty in ware_sku_qty_list:
            sale_sku_info = IMSDBOperator.query_bom_detail_by_ware_sku_code(ware_sku)
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
                bom_detail = IMSDBOperator.query_bom_detail(sale_sku, bom)
                if len(sale_sku_dict[sale_sku][bom]) < len(bom_detail):
                    result_sku_suites.update(
                        {sale_sku: 0}
                    )
                else:
                    result_suites = list()
                    for ware_sku, qty in sale_sku_dict[sale_sku][bom].items():
                        suites = qty // IMSDBOperator.query_bom_detail(sale_sku, bom)[ware_sku]
                        result_suites.append(suites)
                    min_suites = min(result_suites)
                    if result_sku_suites.get(sale_sku):
                        result_sku_suites[sale_sku] += min_suites
                    else:
                        result_sku_suites.update(
                            {sale_sku: min(result_suites)}
                        )
        return result_sku_suites

    def get_other_in_expect_inventory(self, ware_sku_qty_list, location_list):
        # 用来存储最终要返回的销售sku的期望库存字典
        result_dict = dict()
        sale_sku_suites_dict = self.calculate_sets(ware_sku_qty_list)
        for sale_sku in sale_sku_suites_dict:
            expect_qualified_inventory = dict()
            # 更新销售商品总库存
            expect_qualified_inventory.update({
                'central_stock': sale_sku_suites_dict[sale_sku],
                'central_block': 0,
                'central_remain': sale_sku_suites_dict[sale_sku],
                'spot_goods_stock': sale_sku_suites_dict[sale_sku],
                'spot_goods_remain': sale_sku_suites_dict[sale_sku]
            })
            # 构造库位期望库存，更新到temp_ware_dict中
            for (ware_sku, qty), sj_location_id in zip(ware_sku_qty_list, location_list):
                if IMSDBOperator.query_bom_detail_by_ware_sku_code(ware_sku)['goods_sku_code'] != sale_sku:
                    continue
                if expect_qualified_inventory.get(ware_sku):
                    if expect_qualified_inventory[ware_sku].get(sj_location_id):
                        expect_qualified_inventory[ware_sku][sj_location_id]['stock'] += qty
                    else:
                        expect_qualified_inventory[ware_sku].update({
                            sj_location_id: {'stock': qty, 'block': 0}
                        })
                    if expect_qualified_inventory[ware_sku].get('warehouse_total'):
                        expect_qualified_inventory[ware_sku]['warehouse_total']['stock'] += qty
                    else:
                        expect_qualified_inventory[ware_sku].update({
                            'warehouse_total': {'stock': qty, 'block': 0}
                        })
                    if expect_qualified_inventory[ware_sku].get('location_total'):
                        expect_qualified_inventory[ware_sku]['location_total']['stock'] += qty
                    else:
                        expect_qualified_inventory[ware_sku].update({
                            'location_total': {'stock': qty, 'block': 0}
                        })
                else:
                    # 更新temp_ware_dict写入库位总库存和仓库总库存
                    expect_qualified_inventory.update({
                        ware_sku: {
                            'warehouse_total': {'stock': qty, 'block': 0},
                            'location_total': {'stock': qty, 'block': 0},
                            sj_location_id: {'stock': qty, 'block': 0}
                        }
                    })
            result_dict.update({
                sale_sku: expect_qualified_inventory
            })
        return result_dict

    def get_unqualified_goods_other_in_expect_inventory(self, ware_sku_qty_list, location_list):
        result_dict = dict()
        sale_sku_suites_dict = self.calculate_sets(ware_sku_qty_list)
        for sale_sku in sale_sku_suites_dict:
            # 构造库位期望库存，更新到temp_ware_dict中
            expect_unqualified_inventory = dict()
            for (ware_sku, qty), cp_location_id in zip(ware_sku_qty_list, location_list):
                if IMSDBOperator.query_bom_detail_by_ware_sku_code(ware_sku)['goods_sku_code'] != sale_sku:
                    continue
                if expect_unqualified_inventory.get(ware_sku):
                    if expect_unqualified_inventory[ware_sku].get(cp_location_id):
                        expect_unqualified_inventory[ware_sku][cp_location_id]['stock'] += qty
                    else:
                        expect_unqualified_inventory[ware_sku].update({
                            cp_location_id: {'stock': qty, 'block': 0}
                        })
                    if expect_unqualified_inventory[ware_sku].get('total'):
                        expect_unqualified_inventory[ware_sku]['total']['stock'] += qty
                    else:
                        expect_unqualified_inventory[ware_sku].update({
                            'total': {'stock': qty, 'block': 0}
                        })
                else:
                    # 更新temp_ware_dict写入库位总库存和仓库总库存
                    expect_unqualified_inventory.update({
                        ware_sku: {
                            'total': {'stock': qty, 'block': 0},
                            cp_location_id: {'stock': qty, 'block': 0}
                        }
                    })
            result_dict.update({
                sale_sku: expect_unqualified_inventory
            })
        return result_dict

    def get_purchase_in_expect_inventory(self, ware_sku_qty_list, location_list):
        # 用来存储最终要返回的销售sku的期望库存字典
        result_dict = dict()
        sale_sku_suites_dict = self.calculate_sets(ware_sku_qty_list)
        for sale_sku in sale_sku_suites_dict:
            expect_qualified_inventory = dict()
            # 更新销售商品总库存
            expect_qualified_inventory.update({
                'central_stock': sale_sku_suites_dict[sale_sku],
                'central_block': 0,
                'central_remain': sale_sku_suites_dict[sale_sku],
                'purchase_on_way_stock': 0,
                'purchase_on_way_remain': 0,
                'spot_goods_stock': sale_sku_suites_dict[sale_sku],
                'spot_goods_remain': sale_sku_suites_dict[sale_sku]
            })
            # 构造库位期望库存，更新到temp_ware_dict中
            for (ware_sku, qty), sj_location_id in zip(ware_sku_qty_list, location_list):
                if IMSDBOperator.query_bom_detail_by_ware_sku_code(ware_sku)['goods_sku_code'] != sale_sku:
                    continue
                if expect_qualified_inventory.get(ware_sku):
                    if expect_qualified_inventory[ware_sku].get(sj_location_id):
                        expect_qualified_inventory[ware_sku][sj_location_id]['stock'] += qty
                    else:
                        expect_qualified_inventory[ware_sku].update({
                            sj_location_id: {'stock': qty, 'block': 0}
                        })
                    if expect_qualified_inventory[ware_sku].get('warehouse_total'):
                        expect_qualified_inventory[ware_sku]['warehouse_total']['stock'] += qty
                    else:
                        expect_qualified_inventory[ware_sku].update({
                            'warehouse_total': {'stock': qty, 'block': 0}
                        })
                    if expect_qualified_inventory[ware_sku].get('location_total'):
                        expect_qualified_inventory[ware_sku]['location_total']['stock'] += qty
                    else:
                        expect_qualified_inventory[ware_sku].update({
                            'location_total': {'stock': qty, 'block': 0}
                        })
                    if expect_qualified_inventory[ware_sku].get('purchase_on_way'):
                        expect_qualified_inventory[ware_sku]['purchase_on_way']['stock'] += qty
                    else:
                        expect_qualified_inventory[ware_sku].update({
                            'purchase_on_way': {'stock': qty, 'block': 0}
                        })
                else:
                    # 更新temp_ware_dict写入库位总库存和仓库总库存
                    expect_qualified_inventory.update({
                        ware_sku: {
                            'warehouse_total': {'stock': qty, 'block': 0},
                            'location_total': {'stock': qty, 'block': 0},
                            'purchase_on_way': {'stock': 0, 'block': 0},
                            sj_location_id: {'stock': qty, 'block': 0}
                        }
                    })
            result_dict.update({
                sale_sku: expect_qualified_inventory
            })
        return result_dict

    def get_purchase_create_order_expect_inventory(self, ware_sku_qty_list):
        # 用来存储最终要返回的销售sku的期望库存字典
        result_dict = dict()
        sale_sku_suites_dict = self.calculate_sets(ware_sku_qty_list)
        for sale_sku in sale_sku_suites_dict:
            expect_qualified_inventory = dict()
            # 更新销售商品总库存
            expect_qualified_inventory.update({
                'central_stock': sale_sku_suites_dict[sale_sku],
                'central_remain': sale_sku_suites_dict[sale_sku],
                'central_block': 0,
                'purchase_on_way_stock': sale_sku_suites_dict[sale_sku],
                'purchase_on_way_remain': sale_sku_suites_dict[sale_sku]

            })
            # 构造库位期望库存，更新到temp_ware_dict中
            for ware_sku, qty in ware_sku_qty_list:
                if IMSDBOperator.query_bom_detail_by_ware_sku_code(ware_sku)['goods_sku_code'] != sale_sku:
                    continue
                if expect_qualified_inventory.get(ware_sku):
                    if expect_qualified_inventory[ware_sku].get('warehouse_total'):
                        expect_qualified_inventory[ware_sku]['warehouse_total']['stock'] += qty
                    else:
                        expect_qualified_inventory[ware_sku].update({
                            'warehouse_total': {'stock': qty, 'block': 0}
                        })
                    if expect_qualified_inventory[ware_sku].get('purchase_on_way'):
                        expect_qualified_inventory[ware_sku]['purchase_on_way']['stock'] += qty
                    else:
                        expect_qualified_inventory[ware_sku].update({
                            'purchase_on_way': {'stock': qty, 'block': 0}
                        })
                else:
                    # 更新temp_ware_dict写入库位总库存和仓库总库存
                    expect_qualified_inventory.update({
                        ware_sku: {
                            'warehouse_total': {'stock': qty, 'block': 0},
                            'purchase_on_way': {'stock': qty, 'block': 0},
                        }
                    })
            result_dict.update({
                sale_sku: expect_qualified_inventory
            })
        return result_dict

    # OMS下单预占中央库存、销售商品总库存
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
    def qualified_goods_other_in(self, ware_sku_qty_list, sj_location_ids, warehouse_id, to_warehouse_id):
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
    def unqualified_goods_other_in(self, ware_sku_qty_list, cp_location_ids, warehouse_id, to_warehouse_id):
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
    def assign_location_stock(self, delivery_order_no, ware_sku_list, warehouse_id):
        temp_list = list()
        for ware_sku, qty in ware_sku_list:
            temp_list.append({
                'qty': qty,
                'wareSkuCode': ware_sku
            })
        ims_api_config['assign_location_stock']['data'][0].update({
            "wareSkuList": temp_list,
            "sourceNo": delivery_order_no,
            "warehouseId": warehouse_id
        })
        res = self.send_request(**ims_api_config['assign_location_stock'])
        return res

    # 确认拣货
    def confirm_pick(self, delivery_order_no, pick_ware_sku_list, warehouse_id):
        for pick_item in pick_ware_sku_list:
            pick_item.update({
                "storageLocationType": 5,
            })
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

    def qualified_goods_other_out_block(self, ware_sku_list, warehouse_id, to_warehouse_id):
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

    def cancel_qualified_goods_other_out_block(self, block_book_id, source_no):
        ims_api_config['cancel_qualified_goods_other_out_block']['data'].update(
            {
                "sourceNo": source_no,
                "blockBookId": block_book_id
            }
        )
        cancel_block_res = self.send_request(**ims_api_config['cancel_qualified_goods_other_out_block'])
        return cancel_block_res

    def cancel_unqualified_goods_other_out_block(self, block_book_id, source_no):
        ims_api_config['cancel_unqualified_goods_other_out_block']['data'].update(
            {
                "sourceNo": source_no,
                "blockBookId": block_book_id
            }
        )
        cancel_block_res = self.send_request(**ims_api_config['cancel_unqualified_goods_other_out_block'])
        return cancel_block_res

    def unqualified_goods_other_out_block(self, ware_sku_qty_list, cp_location_ids, warehouse_id):
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

    def qualified_goods_other_out_delivered(self, ware_sku_list, warehouse_id, to_warehouse_id):
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

    def unqualified_goods_other_out_delivered(self, ware_sku_qty_list, cp_location_ids, warehouse_id):
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

    def turn_to_unqualified_goods(self, ware_sku, from_location_id, to_location_id, qty, warehouse_id, to_warehouse_id):
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

    def add_unqualified_stock_by_other_in(self, sale_sku_code, bom_version, add_stock_count, cp_location_ids,
                                          warehouse_id, to_warehouse_id):
        details = IMSDBOperator.query_bom_detail(sale_sku_code, bom_version)
        ware_sku_qty_list = list()
        for ware_sku, qty in details.items():
            ware_sku_qty_list.append((ware_sku, qty * add_stock_count))
        res = self.unqualified_goods_other_in(ware_sku_qty_list, cp_location_ids, warehouse_id,
                                              to_warehouse_id)
        return res

    def add_qualified_stock_by_other_in(self, sale_sku_code, bom_version, add_stock_count, location_ids, warehouse_id,
                                        to_warehouse_id):
        details = IMSDBOperator.query_bom_detail(sale_sku_code, bom_version)
        ware_sku_qty_list = list()
        for ware_sku, qty in details.items():
            ware_sku_qty_list.append((ware_sku, qty * add_stock_count))
        res = self.qualified_goods_other_in(ware_sku_qty_list, location_ids, warehouse_id, to_warehouse_id)
        return res

    def get_combined_block_result_list(self, block_result_list):
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

    def get_import_stock_excel_data(self, excel):
        files = {'file': open(excel, 'rb')}
        excel_data = self.send_request(**ims_api_config['get_import_stock_excel_data'], files=files)
        return excel_data

    def import_stock_excel_data(self, excel):
        files = {'file': open(excel, 'rb')}
        res = self.send_request(**ims_api_config['import_stock_excel_data'], files=files)
        return res


if __name__ == '__main__':
    ims = ImsController()
    IMSDBOperator.delete_qualified_inventory(['63203684930'])
    ims.add_qualified_stock_by_other_in('63203684930', 'A', 10, [1496, 1505], 513, 513)
    # ims.qualified_goods_other_in([('J06ZWJ000252WG', 1)], [2451], 539, 539)
    # data = ims.get_central_inventory('63203684930', 520, 520)
    # data2 = ims.get_goods_inventory('63203684930', 520, 520)
    # data3 = ims.get_wares_inventory('63203684930', 'A', 520, 520)
    # print(data)
    # print(data2)
    # print(data3)
    # print(IMSDBOperator.query_unqualified_inventory('63203684930', 520, 520))
    # print(ims.get_expect_inventory([('63203684930A01', 1), ('63203684930A02', 4), ('63203684930A02', 1)]))
    # print(IMSDBOperator.query_qualified_inventory('63203684930', 513, 513))
    # print(IMSDBOperator.query_unqualified_inventory('16338527895', 513, 513))
