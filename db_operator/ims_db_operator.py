from models.ims_model import *
from playhouse.shortcuts import model_to_dict


class IMSDBOperator:
    @classmethod
    def query_wares_inventory(cls, sale_sku_code, warehouse_id, to_warehouse_id, bom_version='') -> list:
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
            return []
        items = [model_to_dict(item) for item in items]
        return items

    @classmethod
    def query_goods_inventory(cls, sale_sku_code, warehouse_id, to_warehouse_id) -> list:
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
            return []
        items = [model_to_dict(item) for item in items]
        return items

    @classmethod
    def query_central_inventory(cls, sale_sku_code, warehouse_id, to_warehouse_id) -> dict:
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
            return {}
        item = model_to_dict(item)
        return item

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
    def delete_qualified_inventory(cls, goods_sku_codes) -> None:
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
    def query_unqualified_inventory(cls, sale_sku_code, warehouse_id, bom_version='') -> list:
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
        return items
