from db_operator.ims_db_operate import IMSDBOperator
from logics import  ims_request

class ImsLogics:
    def __init__(self):
        self.ims_request = ims_request

    @classmethod
    def calculate_sets(cls, ware_sku_qty_list):
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

    @classmethod
    def get_other_in_expect_inventory(cls, ware_sku_qty_list, location_list):
        # 用来存储最终要返回的销售sku的期望库存字典
        result_dict = dict()
        sale_sku_suites_dict = cls.calculate_sets(ware_sku_qty_list)
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

    @classmethod
    def get_unqualified_goods_other_in_expect_inventory(cls, ware_sku_qty_list, location_list):
        result_dict = dict()
        sale_sku_suites_dict = cls.calculate_sets(ware_sku_qty_list)
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

    @classmethod
    def get_purchase_in_expect_inventory(cls, ware_sku_qty_list, location_list):
        # 用来存储最终要返回的销售sku的期望库存字典
        result_dict = dict()
        sale_sku_suites_dict = cls.calculate_sets(ware_sku_qty_list)
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

    @classmethod
    def get_purchase_create_order_expect_inventory(cls, ware_sku_qty_list):
        # 用来存储最终要返回的销售sku的期望库存字典
        result_dict = dict()
        sale_sku_suites_dict = cls.calculate_sets(ware_sku_qty_list)
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

    def add_unqualified_stock_by_other_in(self, sale_sku_code, bom_version, add_stock_count, cp_location_ids,
                                          warehouse_id, to_warehouse_id):
        details = IMSDBOperator.query_bom_detail(sale_sku_code, bom_version)
        ware_sku_qty_list = list()
        for ware_sku, qty in details.items():
            ware_sku_qty_list.append((ware_sku, qty * add_stock_count))
        res = self.ims_request.unqualified_goods_other_in(ware_sku_qty_list, cp_location_ids, warehouse_id,
                                                          to_warehouse_id)
        return res

    def add_qualified_stock_by_other_in(self, sale_sku_code, bom_version, add_stock_count, location_ids, warehouse_id,
                                        to_warehouse_id):
        details = IMSDBOperator.query_bom_detail(sale_sku_code, bom_version)
        ware_sku_qty_list = list()
        for ware_sku, qty in details.items():
            ware_sku_qty_list.append((ware_sku, qty * add_stock_count))
        res = self.ims_request.qualified_goods_other_in(ware_sku_qty_list, location_ids, warehouse_id, to_warehouse_id)
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
