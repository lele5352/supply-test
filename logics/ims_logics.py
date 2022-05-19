import math

from db_operator.ims_db_operator import IMSDBOperator as IMSDBO


class ImsLogics:
    def __init__(self, ims_request):
        self.ims_request = ims_request

    @classmethod
    def format_wares_inventory(cls, wares_inventory):
        """
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

    @classmethod
    def query_format_wares_inventory_self(cls, sale_sku_code, ck_id, to_ck_id):
        """
        仅返回指定销售sku在指定所属仓+目的仓的单个仓库数据

        :param str sale_sku_code: 销售sku编码
        :param int ck_id: 仓库id
        :param int to_ck_id: 目的仓id
        :return: 查询结果数据，字典格式
        """
        wares_inventory = IMSDBO.query_wares_inventory(sale_sku_code, ck_id, to_ck_id)
        return cls.format_wares_inventory(wares_inventory)

    @classmethod
    def query_format_wares_inventory_all(cls, sale_sku_code, ck_id, to_ck_id):
        """
        返回指定销售sku在全部相关仓库的数据

        :param str sale_sku_code: 销售sku编码
        :param int ck_id: 仓库id
        :param int to_ck_id: 目的仓id
        :return: 查询结果数据，字典格式
        """
        wares_inventory = IMSDBO.query_wares_inventory(sale_sku_code, ck_id, to_ck_id, 2)
        return cls.format_wares_inventory(wares_inventory)

    @classmethod
    def query_format_goods_inventory(cls, sale_sku_code, warehouse_id, to_warehouse_id):
        """
        :param str sale_sku_code: 销售sku编码
        :param int warehouse_id: 仓库id
        :param int to_warehouse_id: 目的仓id
        :return: 查询结果数据，字典格式
        """
        goods_inventory = IMSDBO.query_goods_inventory(sale_sku_code, warehouse_id, to_warehouse_id)
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

    @classmethod
    def query_format_central_inventory(cls, sale_sku_code, warehouse_id, to_warehouse_id):
        """
        :param str sale_sku_code: 销售sku编码
        :param int warehouse_id: 仓库id
        :param int to_warehouse_id: 目的仓id

        :return dict: 查询结果数据，字典格式
        """
        central_inventory = IMSDBO.query_central_inventory(sale_sku_code, warehouse_id, to_warehouse_id)
        if not central_inventory:
            return {}
        else:
            return {
                "central_stock": central_inventory['stock'],
                "central_block": central_inventory['block'],
                "central_remain": central_inventory['remain']
            }

    @classmethod
    def query_lp_inventories(cls, sale_sku_list, warehouse_id, to_warehouse_id) -> dict:
        """
        :param list sale_sku_list: 销售sku编码列表,格式[(sale_sku,bom),...]
        :param int warehouse_id: 仓库id
        :param int to_warehouse_id: 目的仓库id
        :return: 格式化后的良品库存数据
        """
        result = dict()
        for sale_sku in sale_sku_list:
            qualified_inventory = dict()
            central_inventory = cls.query_format_central_inventory(sale_sku, warehouse_id, to_warehouse_id)
            goods_inventory = cls.query_format_goods_inventory(sale_sku, warehouse_id, to_warehouse_id)
            wares_inventory = cls.query_format_wares_inventory_self(sale_sku, warehouse_id, to_warehouse_id)
            if central_inventory:
                qualified_inventory.update(central_inventory)
            if goods_inventory:
                qualified_inventory.update(goods_inventory)
            if wares_inventory:
                qualified_inventory.update(wares_inventory)
            result.update({
                sale_sku: qualified_inventory
            })
        return result

    @classmethod
    def get_sale_skus(cls, ware_sku_qty_list):
        sale_sku_list = list()
        ware_sku_list = [_[0] for _ in cls.combine_ware_sku_qty_list(ware_sku_qty_list)]
        for ware_sku in ware_sku_list:
            sale_sku = IMSDBO.query_bom_detail_by_ware_sku_code(ware_sku)['goods_sku_code']
            if sale_sku not in sale_sku_list:
                sale_sku_list.append(sale_sku)
        return sale_sku_list

    @classmethod
    def query_format_cp_inventory(cls, sale_sku_code, warehouse_id, bom_version='') -> dict:
        """
        :param string sale_sku_code: 销售sku编码
        :param int warehouse_id: 仓库id
        :param string bom_version: bom版本
        :return: bom版本仓库sku明细字典
        """
        items = IMSDBO.query_unqualified_inventory(sale_sku_code, warehouse_id, bom_version)
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
            sale_sku_info = IMSDBO.query_bom_detail_by_ware_sku_code(ware_sku)
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
                bom_detail = IMSDBO.query_bom_detail(sale_sku, bom)
                if len(sale_sku_dict[sale_sku][bom]) < len(bom_detail):
                    result_sku_suites.update(
                        {sale_sku: 0}
                    )
                else:
                    result_suites = list()
                    for ware_sku, qty in sale_sku_dict[sale_sku][bom].items():
                        suites = qty // IMSDBO.query_bom_detail(sale_sku, bom)[ware_sku]
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
    def calc_suites(cls, sale_sku, bom, wares_inventory, level):
        """
        :param string sale_sku: 销售sku编码
        :param string bom: bom版本
        :param dict wares_inventory: 销售sku对应bom的wares_inventory库存数据
        :param string level: 库存计算维度，central对应warehouse_total，goods对应location_total
        :return: min_stock:成套库存数, max_block:成套预占数, remain:剩余数（库存-预占)
        """
        result_stock = list()
        result_block = list()
        bom_detail = IMSDBO.query_bom_detail(sale_sku, bom)
        if len(wares_inventory) < len(bom_detail):
            return 0, 0, 0
        else:
            for ware_sku in wares_inventory:
                stock = wares_inventory[ware_sku][level]['stock']
                block = wares_inventory[ware_sku][level]['block']
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
        return min_stock, max_block, remain

    @classmethod
    def combine_ware_sku_qty_list(cls, ware_sku_qty_list):
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

    @classmethod
    def format_ware_sku_qty_list_for_expect_inventory(cls, ware_sku_qty_list, kw_ids_list=None):
        """
        :param list ware_sku_qty_list: 变动的ware_sku、qty列表，格式[(ware_sku,qty),...]
        :param list optional kw_ids_list: 库位id列表

        """
        result_dict = dict()
        if kw_ids_list:
            for (ware_sku, qty), kw_id in zip(ware_sku_qty_list, kw_ids_list):
                bom_detail_info = IMSDBO.query_bom_detail_by_ware_sku_code(ware_sku)
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
                bom_detail_info = IMSDBO.query_bom_detail_by_ware_sku_code(ware_sku)
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

    @classmethod
    def get_expect_wares_inventory(cls, ware_sku_qty_list, kw_ids_list, ck_id, to_ck_id, data_type):
        result_dict = dict()

        change_inventory = cls.format_ware_sku_qty_list_for_expect_inventory(ware_sku_qty_list, kw_ids_list)
        for sale_sku in change_inventory:
            if data_type == 1:
                wares_inventory = cls.query_format_wares_inventory_self(sale_sku, ck_id, to_ck_id)
            else:
                wares_inventory = cls.query_format_wares_inventory_all(sale_sku, ck_id, to_ck_id)
            temp_dict = dict()
            for bom in change_inventory[sale_sku]:

                for ware_sku in change_inventory[sale_sku][bom]:
                    for kw_id, qty in change_inventory[sale_sku][bom][ware_sku].items():
                        # 如果查到库存数据，根据仓库sku是否在库存数据中存在处理库存数据
                        if wares_inventory:
                            if bom not in wares_inventory:
                                wares_inventory.update(
                                    {bom: {ware_sku: {
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
                                wares_inventory[bom][ware_sku]['location_total']['stock'] += qty
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

    @classmethod
    def get_expect_goods_inventory(cls, wares_inventory, warehouse_id, to_warehouse_id):
        result_dict = dict()
        for sale_sku in wares_inventory:
            total_stock = 0
            total_remain = 0
            for bom in wares_inventory[sale_sku]:
                inventory = wares_inventory[sale_sku][bom]
                stock, block, remain = cls.calc_suites(sale_sku, bom, inventory, 'location_total')
                total_stock += stock
                total_remain += remain
            goods_inventory = cls.query_format_goods_inventory(sale_sku, warehouse_id, to_warehouse_id)
            if goods_inventory:
                goods_inventory['spot_goods_stock'] = total_stock
                goods_inventory['spot_goods_remain'] = total_remain
            else:
                goods_inventory.update({
                    'spot_goods_stock': total_stock,
                    'spot_goods_remain': total_remain
                })
            result_dict.update({
                sale_sku: goods_inventory
            })
        return result_dict

    @classmethod
    def get_expect_central_inventory(cls, wares_inventory, warehouse_id, to_warehouse_id):
        result_dict = dict()
        for sale_sku in wares_inventory:
            total_stock = 0
            total_remain = 0
            for bom in wares_inventory[sale_sku]:
                inventory = wares_inventory[sale_sku][bom]
                stock, block, remain = cls.calc_suites(sale_sku, bom, inventory, 'warehouse_total')
                total_stock += stock
                total_remain += remain
            central_inventory = cls.query_format_central_inventory(sale_sku, warehouse_id, to_warehouse_id)
            if central_inventory:
                central_inventory['central_stock'] = total_stock
                central_inventory['central_remain'] = total_remain
            else:
                central_inventory.update({
                    'central_stock': total_stock,
                    'central_block': 0,
                    'central_remain': total_remain
                })
            result_dict.update({
                sale_sku: central_inventory
            })
        return result_dict

    @classmethod
    def get_expect_inventory_with_kws(cls, ware_sku_qty_list, kw_ids_list, ck_id, to_ck_id):
        wares_inventory_for_goods = cls.get_expect_wares_inventory(ware_sku_qty_list, kw_ids_list, ck_id, to_ck_id, 1)
        wares_inventory_for_central = cls.get_expect_wares_inventory(ware_sku_qty_list, kw_ids_list, ck_id, to_ck_id, 2)
        wares_inventory = cls.get_expect_wares_inventory(ware_sku_qty_list, kw_ids_list, ck_id, to_ck_id, 1)

        expect_goods_inventory = cls.get_expect_goods_inventory(wares_inventory_for_goods, ck_id, to_ck_id)
        expect_central_inventory = cls.get_expect_central_inventory(wares_inventory_for_central, ck_id, to_ck_id)

        for sale_sku in wares_inventory:
            wares_inventory[sale_sku].update(expect_goods_inventory[sale_sku])
            wares_inventory[sale_sku].update(expect_central_inventory[sale_sku])
        return wares_inventory

    @classmethod
    def get_cp_other_in_expect_inventory(cls, ware_sku_qty_list, location_list):
        result_dict = dict()
        sale_sku_suites_dict = cls.calculate_sets(ware_sku_qty_list)
        for sale_sku in sale_sku_suites_dict:
            # 构造库位期望库存，更新到temp_ware_dict中
            expect_cp_inventory = dict()
            for (ware_sku, qty), cp_location_id in zip(ware_sku_qty_list, location_list):
                if IMSDBO.query_bom_detail_by_ware_sku_code(ware_sku)['goods_sku_code'] != sale_sku:
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
                if IMSDBO.query_bom_detail_by_ware_sku_code(ware_sku)['goods_sku_code'] != sale_sku:
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
                if IMSDBO.query_bom_detail_by_ware_sku_code(ware_sku)['goods_sku_code'] != sale_sku:
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
        details = IMSDBO.query_bom_detail(sale_sku_code, bom_version)
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
        details = IMSDBO.query_bom_detail(sale_sku_code, bom_version)
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
