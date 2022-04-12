from models.ims_model import *
from playhouse.shortcuts import model_to_dict


class IMSDBOperator:
    @classmethod
    def query_wares_inventory(cls, sale_sku_code, warehouse_id, to_warehouse_id, bom_version=''):
        """
        :param str sale_sku_code: 销售sku编码
        :param int warehouse_id: 仓库id
        :param int to_warehouse_id: 目的仓id
        :param any bom_version: bom版本

        :return dict: 查询结果数据，字典格式
        """
        if bom_version:
            items = WaresInventory.select().order_by(WaresInventory.ware_sku_code).where(
                WaresInventory.goods_sku_code == sale_sku_code,
                WaresInventory.bom_version == bom_version,
                WaresInventory.warehouse_id == warehouse_id,
                WaresInventory.target_warehouse_id == to_warehouse_id)
        else:
            items = WaresInventory.select().order_by(WaresInventory.ware_sku_code).where(
                WaresInventory.goods_sku_code == sale_sku_code,
                WaresInventory.warehouse_id == warehouse_id,
                WaresInventory.target_warehouse_id == to_warehouse_id)
        if not items:
            return
        items = [model_to_dict(item) for item in items]
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
    def query_goods_inventory(cls, sale_sku_code, warehouse_id, to_warehouse_id):
        """
        :param str sale_sku_code: 销售sku编码
        :param int warehouse_id: 仓库id
        :param int to_warehouse_id: 目的仓id

        :return dict: 查询结果数据，字典格式
        """
        to_warehouse_id = to_warehouse_id if to_warehouse_id else 0
        items = GoodsInventory.select().where(
            GoodsInventory.goods_sku_code == sale_sku_code,
            GoodsInventory.current_warehouse_id == warehouse_id,
            GoodsInventory.target_warehouse_id == to_warehouse_id)
        if not items:
            return
        items = [model_to_dict(item) for item in items]
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
    def query_central_inventory(cls, sale_sku_code, warehouse_id, to_warehouse_id):
        """
        :param str sale_sku_code: 销售sku编码
        :param int warehouse_id: 仓库id
        :param int to_warehouse_id: 目的仓id

        :return dict: 查询结果数据，字典格式
        """
        warehouse_id = to_warehouse_id if to_warehouse_id else warehouse_id
        item = CentralInventory.get_or_none(CentralInventory.goods_sku_code == sale_sku_code,
                                            CentralInventory.warehouse_id == warehouse_id)
        if not item:
            return
        item = model_to_dict(item)
        return {
            "central_stock": item['stock'],
            "central_block": item['block'],
            "central_remain": item['remain']
        }

    @classmethod
    def delete_wares_inventory_by_goods_sku_codes(cls, goods_sku_codes) -> None:
        """
        :param list goods_sku_codes: 销售sku编码列表
        """
        WaresInventory.delete().where(WaresInventory.goods_sku_code << goods_sku_codes).execute()

    @classmethod
    def delete_goods_inventory_by_goods_sku_codes(cls, goods_sku_codes) -> None:
        """
        :param list goods_sku_codes: 销售sku编码列表
        """
        GoodsInventory.delete().where(GoodsInventory.goods_sku_code << goods_sku_codes).execute()

    @classmethod
    def delete_central_inventory_by_goods_sku_codes(cls, goods_sku_codes) -> None:
        """
        :param list goods_sku_codes: 销售sku编码列表
        """
        CentralInventory.delete().where(CentralInventory.goods_sku_code << goods_sku_codes).execute()

    @classmethod
    def delete_unqualified_inventory(cls, goods_sku_codes) -> None:
        """
        :param list goods_sku_codes: 销售sku编码列表
        """
        NogoodWaresInventory.delete().where(NogoodWaresInventory.goods_sku_code << goods_sku_codes).execute()

    @classmethod
    def delete_qualified_inventory(cls, goods_sku_codes):
        """
        :param list goods_sku_codes: 销售sku编码列表
        """
        cls.delete_central_inventory_by_goods_sku_codes(goods_sku_codes)
        cls.delete_goods_inventory_by_goods_sku_codes(goods_sku_codes)
        cls.delete_wares_inventory_by_goods_sku_codes(goods_sku_codes)

    @classmethod
    def query_bom_detail(cls, sale_sku_code, bom_version) -> dict:
        """
        :param string sale_sku_code: 销售sku编码
        :param string bom_version: bom版本
        :return: bom版本仓库sku明细字典
        """
        items = BomDetail.select().order_by(BomDetail.id).where(
            BomDetail.goods_sku_code == sale_sku_code, BomDetail.bom_version == bom_version)
        items = [model_to_dict(item) for item in items]

        sale_sku_bom_detail = dict()
        for item in items:
            sale_sku_bom_detail.update(
                {
                    item['ware_sku_code']: item['bom_qty']
                })
        return sale_sku_bom_detail

    @classmethod
    def query_bom_detail_by_ware_sku_code(cls, ware_sku_code) -> dict:
        """
        :param string ware_sku_code: 仓库sku编码
        :return: 仓库sku的对应的bom明细
        """
        item = BomDetail.get(BomDetail.ware_sku_code == ware_sku_code)
        return model_to_dict(item)

    @classmethod
    def query_qualified_inventory(cls, sale_sku_code, warehouse_id, to_warehouse_id, bom_version='') -> dict:
        """
        :param string sale_sku_code: 销售sku编码
        :param int warehouse_id: 仓库id
        :param int to_warehouse_id: 目的仓库id
        :param string bom_version: bom版本
        :return: bom版本仓库sku明细字典
        """
        central_inventory = cls.query_central_inventory(sale_sku_code, warehouse_id, to_warehouse_id)
        goods_inventory = cls.query_goods_inventory(sale_sku_code, warehouse_id, to_warehouse_id)
        wares_inventory = cls.query_wares_inventory(sale_sku_code, warehouse_id, to_warehouse_id, bom_version)

        qualified_inventory = dict()
        if central_inventory:
            qualified_inventory.update(central_inventory)
        if goods_inventory:
            qualified_inventory.update(goods_inventory)
        if wares_inventory:
            qualified_inventory.update(wares_inventory)
        return qualified_inventory

    @classmethod
    def query_unqualified_inventory(cls, sale_sku_code, warehouse_id, bom_version='') -> dict:
        """
        :param string sale_sku_code: 销售sku编码
        :param int warehouse_id: 仓库id
        :param string bom_version: bom版本
        :return: bom版本仓库sku明细字典
        """
        if bom_version:
            items = NogoodWaresInventory.select().order_by(NogoodWaresInventory.ware_sku_code).where(
                NogoodWaresInventory.goods_sku_code == sale_sku_code,
                NogoodWaresInventory.bom_version == bom_version,
                NogoodWaresInventory.warehouse_id == warehouse_id)
        else:
            items = NogoodWaresInventory.select().order_by(NogoodWaresInventory.ware_sku_code).where(
                NogoodWaresInventory.goods_sku_code == sale_sku_code,
                NogoodWaresInventory.warehouse_id == warehouse_id)
        items = [model_to_dict(item) for item in items]

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

