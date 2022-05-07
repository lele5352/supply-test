from db_operator.ims_db_operator import IMSDBOperator


class ImsLogics:
    def __init__(self, ims_request):
        self.ims_request = ims_request

    @classmethod
    def query_format_wares_inventory(cls, sale_sku_code, warehouse_id, to_warehouse_id, bom_version=''):
        """
        :param str sale_sku_code: 销售sku编码
        :param int warehouse_id: 仓库id
        :param int to_warehouse_id: 目的仓id
        :param any bom_version: bom版本

        :return dict: 查询结果数据，字典格式
        """
        items = IMSDBOperator.query_wares_inventory(sale_sku_code, warehouse_id, to_warehouse_id, bom_version)
        formatted_ware_sku_inventory = dict()
        for item in items:
            if formatted_ware_sku_inventory.get(item['ware_sku_code']):
                if item['type'] == 0:
                    formatted_ware_sku_inventory[item['ware_sku_code']].update(
                        {"warehouse_total": {'stock': item['stock'], 'block': item['block']}}
                    )
                elif item['type'] == 1:
                    formatted_ware_sku_inventory[item['ware_sku_code']].update(
                        {"purchase_on_way": {'stock': item['stock'], 'block': item['block']}}
                    )
                elif item['type'] == 2:
                    formatted_ware_sku_inventory[item['ware_sku_code']].update(
                        {"transfer_on_way": {'stock': item['stock'], 'block': item['block']}}
                    )
                elif item['type'] == 3:
                    formatted_ware_sku_inventory[item['ware_sku_code']].update(
                        {"location_total": {'stock': item['stock'], 'block': item['block']}}
                    )
                elif item['type'] == 4:
                    formatted_ware_sku_inventory[item['ware_sku_code']].update(
                        {item['storage_location_id']: {'stock': item['stock'], 'block': item['block']}}
                    )
            else:
                if item['type'] == 0:
                    formatted_ware_sku_inventory.update(
                        {item['ware_sku_code']: {"warehouse_total": {'stock': item['stock'], 'block': item['block']}}}
                    )
                elif item['type'] == 1:
                    formatted_ware_sku_inventory.update(
                        {item['ware_sku_code']: {"purchase_on_way": {'stock': item['stock'], 'block': item['block']}}}
                    )
                elif item['type'] == 2:
                    formatted_ware_sku_inventory.update(
                        {item['ware_sku_code']: {"transfer_on_way": {'stock': item['stock'], 'block': item['block']}}}
                    )
                elif item['type'] == 3:
                    formatted_ware_sku_inventory.update(
                        {item['ware_sku_code']: {"location_total": {'stock': item['stock'], 'block': item['block']}}}
                    )
                elif item['type'] == 4:
                    formatted_ware_sku_inventory.update(
                        {item['ware_sku_code']: {
                            item["storage_location_id"]: {'stock': item['stock'], 'block': item['block']}}}
                    )
        return formatted_ware_sku_inventory

    @classmethod
    def query_format_goods_inventory(cls, sale_sku_code, warehouse_id, to_warehouse_id):
        """
        :param str sale_sku_code: 销售sku编码
        :param int warehouse_id: 仓库id
        :param int to_warehouse_id: 目的仓id

        :return dict: 查询结果数据，字典格式
        """
        items = IMSDBOperator.query_goods_inventory(sale_sku_code, warehouse_id, to_warehouse_id)
        goods_inventory_dict = dict()
        for item in items:
            # 销售商品采购在途库存
            if item['type'] == 1:
                goods_inventory_dict.update({
                    'purchase_on_way_stock': item['stock'],
                    'purchase_on_way_remain': item['remain']
                })
            elif item['type'] == 2:
                goods_inventory_dict.update({
                    'transfer_on_way_stock': item['stock'],
                    'transfer_on_way_remain': item['remain']
                })
            elif item['type'] == 3:
                goods_inventory_dict.update({
                    'spot_goods_stock': item['stock'],
                    'spot_goods_remain': item['remain']
                })
        return goods_inventory_dict

    @classmethod
    def query_format_central_inventory(cls, sale_sku_code, warehouse_id, to_warehouse_id):
        """
        :param str sale_sku_code: 销售sku编码
        :param int warehouse_id: 仓库id
        :param int to_warehouse_id: 目的仓id

        :return dict: 查询结果数据，字典格式
        """

        item = IMSDBOperator.query_central_inventory(sale_sku_code, warehouse_id, to_warehouse_id)
        if not item:
            return {}
        else:
            return {
                "central_stock": item['stock'],
                "central_block": item['block'],
                "central_remain": item['remain']
            }

    @classmethod
    def query_lp_inventory(cls, sale_sku_code, warehouse_id, to_warehouse_id, bom='') -> dict:
        """
        :param string sale_sku_code: 销售sku编码
        :param int warehouse_id: 仓库id
        :param int to_warehouse_id: 目的仓库id
        :param string bom: bom版本
        :return: bom版本仓库sku明细字典
        """
        central_inventory = cls.query_format_central_inventory(sale_sku_code, warehouse_id, to_warehouse_id)
        goods_inventory = cls.query_format_goods_inventory(sale_sku_code, warehouse_id, to_warehouse_id)
        wares_inventory = cls.query_format_wares_inventory(sale_sku_code, warehouse_id, to_warehouse_id, bom)

        qualified_inventory = dict()
        if central_inventory:
            qualified_inventory.update(central_inventory)
        if goods_inventory:
            qualified_inventory.update(goods_inventory)
        if wares_inventory:
            qualified_inventory.update(wares_inventory)
        return qualified_inventory

    @classmethod
    def query_format_cp_inventory(cls, sale_sku_code, warehouse_id, bom_version='') -> dict:
        """
        :param string sale_sku_code: 销售sku编码
        :param int warehouse_id: 仓库id
        :param string bom_version: bom版本
        :return: bom版本仓库sku明细字典
        """
        items = IMSDBOperator.query_unqualified_inventory(sale_sku_code, warehouse_id, bom_version)
        temp_ware_sku_inventory = dict()
        for item in items:
            if temp_ware_sku_inventory.get(item['ware_sku_code']):
                if item['storage_location_id'] == 0:
                    temp_ware_sku_inventory[item['ware_sku_code']].update(
                        {"total": {'stock': item['stock'], 'block': item['block']}}
                    )
                elif item['storage_location_id'] > 0:
                    temp_ware_sku_inventory[item['ware_sku_code']].update(
                        {item['storage_location_id']: {'stock': item['stock'], 'block': item['block']}}
                    )
            else:
                if item['storage_location_id'] == 0:
                    temp_ware_sku_inventory.update({
                        item['ware_sku_code']: {"total": {'stock': item['stock'], 'block': item['block']}}
                    })
                elif item['storage_location_id'] > 0:
                    temp_ware_sku_inventory.update({
                        item['ware_sku_code']: {
                            item['storage_location_id']: {'stock': item['stock'], 'block': item['block']}}
                    })
        return temp_ware_sku_inventory

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
    def get_lp_other_in_expect_inventory(cls, ware_sku_qty_list, location_list):
        # 用来存储最终要返回的销售sku的期望库存字典
        result_dict = dict()
        sale_sku_suites_dict = cls.calculate_sets(ware_sku_qty_list)
        for sale_sku in sale_sku_suites_dict:
            expect_lp_inventory = dict()
            # 更新销售商品总库存
            expect_lp_inventory.update({
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
                if expect_lp_inventory.get(ware_sku):
                    if expect_lp_inventory[ware_sku].get(sj_location_id):
                        expect_lp_inventory[ware_sku][sj_location_id]['stock'] += qty
                    else:
                        expect_lp_inventory[ware_sku].update({
                            sj_location_id: {'stock': qty, 'block': 0}
                        })
                    if expect_lp_inventory[ware_sku].get('warehouse_total'):
                        expect_lp_inventory[ware_sku]['warehouse_total']['stock'] += qty
                    else:
                        expect_lp_inventory[ware_sku].update({
                            'warehouse_total': {'stock': qty, 'block': 0}
                        })
                    if expect_lp_inventory[ware_sku].get('location_total'):
                        expect_lp_inventory[ware_sku]['location_total']['stock'] += qty
                    else:
                        expect_lp_inventory[ware_sku].update({
                            'location_total': {'stock': qty, 'block': 0}
                        })
                else:
                    # 更新temp_ware_dict写入库位总库存和仓库总库存
                    expect_lp_inventory.update({
                        ware_sku: {
                            'warehouse_total': {'stock': qty, 'block': 0},
                            'location_total': {'stock': qty, 'block': 0},
                            sj_location_id: {'stock': qty, 'block': 0}
                        }
                    })
            result_dict.update({
                sale_sku: expect_lp_inventory
            })
        return result_dict

    @classmethod
    def get_cp_other_in_expect_inventory(cls, ware_sku_qty_list, location_list):
        result_dict = dict()
        sale_sku_suites_dict = cls.calculate_sets(ware_sku_qty_list)
        for sale_sku in sale_sku_suites_dict:
            # 构造库位期望库存，更新到temp_ware_dict中
            expect_cp_inventory = dict()
            for (ware_sku, qty), cp_location_id in zip(ware_sku_qty_list, location_list):
                if IMSDBOperator.query_bom_detail_by_ware_sku_code(ware_sku)['goods_sku_code'] != sale_sku:
                    continue
                if expect_cp_inventory.get(ware_sku):
                    if expect_cp_inventory[ware_sku].get(cp_location_id):
                        expect_cp_inventory[ware_sku][cp_location_id]['stock'] += qty
                    else:
                        expect_cp_inventory[ware_sku].update({
                            cp_location_id: {'stock': qty, 'block': 0}
                        })
                    if expect_cp_inventory[ware_sku].get('total'):
                        expect_cp_inventory[ware_sku]['total']['stock'] += qty
                    else:
                        expect_cp_inventory[ware_sku].update({
                            'total': {'stock': qty, 'block': 0}
                        })
                else:
                    # 更新temp_ware_dict写入库位总库存和仓库总库存
                    expect_cp_inventory.update({
                        ware_sku: {
                            'total': {'stock': qty, 'block': 0},
                            cp_location_id: {'stock': qty, 'block': 0}
                        }
                    })
            result_dict.update({
                sale_sku: expect_cp_inventory
            })
        return result_dict

    @classmethod
    def get_purchase_in_expect_inventory(cls, ware_sku_qty_list, location_list):
        # 用来存储最终要返回的销售sku的期望库存字典
        result_dict = dict()
        sale_sku_suites_dict = cls.calculate_sets(ware_sku_qty_list)
        for sale_sku in sale_sku_suites_dict:
            expect_lp_inventory = dict()
            # 更新销售商品总库存
            expect_lp_inventory.update({
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
                if expect_lp_inventory.get(ware_sku):
                    if expect_lp_inventory[ware_sku].get(sj_location_id):
                        expect_lp_inventory[ware_sku][sj_location_id]['stock'] += qty
                    else:
                        expect_lp_inventory[ware_sku].update({
                            sj_location_id: {'stock': qty, 'block': 0}
                        })
                    if expect_lp_inventory[ware_sku].get('warehouse_total'):
                        expect_lp_inventory[ware_sku]['warehouse_total']['stock'] += qty
                    else:
                        expect_lp_inventory[ware_sku].update({
                            'warehouse_total': {'stock': qty, 'block': 0}
                        })
                    if expect_lp_inventory[ware_sku].get('location_total'):
                        expect_lp_inventory[ware_sku]['location_total']['stock'] += qty
                    else:
                        expect_lp_inventory[ware_sku].update({
                            'location_total': {'stock': qty, 'block': 0}
                        })
                    if expect_lp_inventory[ware_sku].get('purchase_on_way'):
                        expect_lp_inventory[ware_sku]['purchase_on_way']['stock'] += qty
                    else:
                        expect_lp_inventory[ware_sku].update({
                            'purchase_on_way': {'stock': qty, 'block': 0}
                        })
                else:
                    # 更新temp_ware_dict写入库位总库存和仓库总库存
                    expect_lp_inventory.update({
                        ware_sku: {
                            'warehouse_total': {'stock': qty, 'block': 0},
                            'location_total': {'stock': qty, 'block': 0},
                            'purchase_on_way': {'stock': 0, 'block': 0},
                            sj_location_id: {'stock': qty, 'block': 0}
                        }
                    })
            result_dict.update({
                sale_sku: expect_lp_inventory
            })
        return result_dict

    @classmethod
    def get_purchase_create_order_expect_inventory(cls, ware_sku_qty_list):
        # 用来存储最终要返回的销售sku的期望库存字典
        result_dict = dict()
        sale_sku_suites_dict = cls.calculate_sets(ware_sku_qty_list)
        for sale_sku in sale_sku_suites_dict:
            expect_lp_inventory = dict()
            # 更新销售商品总库存
            expect_lp_inventory.update({
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
                if expect_lp_inventory.get(ware_sku):
                    if expect_lp_inventory[ware_sku].get('warehouse_total'):
                        expect_lp_inventory[ware_sku]['warehouse_total']['stock'] += qty
                    else:
                        expect_lp_inventory[ware_sku].update({'warehouse_total': {'stock': qty, 'block': 0}})
                    if expect_lp_inventory[ware_sku].get('purchase_on_way'):
                        expect_lp_inventory[ware_sku]['purchase_on_way']['stock'] += qty
                    else:
                        expect_lp_inventory[ware_sku].update({'purchase_on_way': {'stock': qty, 'block': 0}})
                else:
                    # 更新temp_ware_dict写入库位总库存和仓库总库存
                    expect_lp_inventory.update({
                        ware_sku: {
                            'warehouse_total': {'stock': qty, 'block': 0},
                            'purchase_on_way': {'stock': qty, 'block': 0},
                        }
                    })
            result_dict.update({
                sale_sku: expect_lp_inventory
            })
        return result_dict

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
        details = IMSDBOperator.query_bom_detail(sale_sku_code, bom_version)
        ware_sku_qty_list = list()
        for ware_sku, qty in details.items():
            ware_sku_qty_list.append((ware_sku, qty * add_stock_count))
        res = self.ims_request.cp_other_in(ware_sku_qty_list, cp_location_ids, warehouse_id, to_warehouse_id)
        return res

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
        details = IMSDBOperator.query_bom_detail(sale_sku_code, bom_version)
        ware_sku_qty_list = list()
        for ware_sku, qty in details.items():
            ware_sku_qty_list.append((ware_sku, qty * add_stock_count))
        res = self.ims_request.lp_other_in(ware_sku_qty_list, location_ids, warehouse_id, to_warehouse_id)
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
        :param str source_no: 来源单号
        :param list sj_kw_ids: 上架库位id列表
        :param list ware_sku_qty_list: 仓库sku及件数关系，格式：[(ware_sku_code，qty),...]
        :param int warehouse_id: 仓库id

        :return dict: 查询结果数据，字典格式
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
        move_res = self.ims_request.move_stock(source_no, ware_sku_list)
        return move_res

    # 确认拣货
    def confirm_all_picked(self, delivery_order_no, block_ware_list, warehouse_id):
        pick_res = self.ims_request.confirm_pick(delivery_order_no, block_ware_list, warehouse_id)
        return pick_res

    # 基于当前wares_inventory计算期望wares_inventory,同个仓，同个销售sku维度
    # def expect_wares_inventory(self, before_wares_inventory, ):
