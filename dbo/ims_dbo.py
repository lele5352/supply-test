from models.ims_model import *
from playhouse.shortcuts import model_to_dict


class IMSDBOperator:
    @classmethod
    def query_wares_inventory(cls, sale_sku_code, ck_id, to_ck_id, data_type=1) -> list:
        """
        查询wares_inventory表指定条件数据

        :param str sale_sku_code: 销售sku编码
        :param int ck_id: 所属仓库id
        :param int to_ck_id: 目的仓库id
        :param int data_type: 返回类型，1-只返回本仓数据；2-返回全部该销售sku对应的全部wares_inventory数据
        :return: 查询结果数据list
        """
        if data_type == 1:
            items = WaresInventory.select().order_by(WaresInventory.ware_sku_code).where(
                WaresInventory.goods_sku_code == sale_sku_code,
                WaresInventory.warehouse_id == ck_id,
                WaresInventory.target_warehouse_id == to_ck_id)
        else:
            # 发货仓和中转，需要查库存为该销售sku在发货仓和中转仓的库存合集，按目的仓查即可
            if to_ck_id and to_ck_id != 0:
                items = WaresInventory.select().order_by(WaresInventory.ware_sku_code).where(
                    WaresInventory.goods_sku_code == sale_sku_code,
                    WaresInventory.target_warehouse_id == to_ck_id)
            # 备货仓,按所属仓库id查询即可
            else:
                items = WaresInventory.select().order_by(WaresInventory.ware_sku_code).where(
                    WaresInventory.goods_sku_code == sale_sku_code,
                    WaresInventory.warehouse_id == ck_id)
        if not items:
            return []
        items = [model_to_dict(item) for item in items]
        return items

    @classmethod
    def query_stock_with_bom(cls, sku_code, bom, ck_id, to_ck_id) -> list:
        """
        查询wares_inventory表发货仓指定bom的数据
        :param to_ck_id: 目的仓库id
        :param ck_id: 所属仓库id
        :param sku_code: 销售sku编码
        :param bom: bom版本
        :return: 查询结果数据list
        """

        items = WaresInventory.select().order_by(WaresInventory.ware_sku_code).where(
            WaresInventory.goods_sku_code == sku_code,
            WaresInventory.warehouse_id == ck_id,
            WaresInventory.bom_version == bom,
            WaresInventory.target_warehouse_id == to_ck_id)
        if not items:
            return []
        items = [model_to_dict(item) for item in items]
        return items

    @classmethod
    def query_goods_inventory(cls, sale_sku_code, warehouse_id, to_warehouse_id) -> list:
        """
        查询goods_inventory表指定条件数据

        :param str sale_sku_code: 销售sku编码
        :param int warehouse_id: 仓库id
        :param int to_warehouse_id: 目的仓id
        :return: 查询结果数据list
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
        查询central_inventory表指定条件数据

        :param str sale_sku_code: 销售sku编码
        :param int warehouse_id: 仓库id
        :param int or None to_warehouse_id: 目的仓id
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
        删除wares_inventory表指定销售sku的全部数据

        :param list goods_sku_codes: 销售sku编码列表
        """
        WaresInventory.delete().where(WaresInventory.goods_sku_code << goods_sku_codes).execute()

    @classmethod
    def delete_goods_inventory_by_goods_sku_codes(cls, goods_sku_codes) -> None:
        """
        删除goods_inventory表指定销售sku的全部数据

        :param list goods_sku_codes: 销售sku编码列表
        """
        GoodsInventory.delete().where(GoodsInventory.goods_sku_code << goods_sku_codes).execute()

    @classmethod
    def delete_central_inventory_by_goods_sku_codes(cls, goods_sku_codes) -> None:
        """
        删除central_inventory表指定销售sku的全部数据

        :param list goods_sku_codes: 销售sku编码列表
        """
        CentralInventory.delete().where(CentralInventory.goods_sku_code << goods_sku_codes).execute()

    @classmethod
    def delete_unqualified_inventory(cls, goods_sku_codes) -> None:
        """
        删除nogood_wares_inventory表指定销售sku的全部数据

        :param list goods_sku_codes: 销售sku编码列表
        """
        NogoodWaresInventory.delete().where(NogoodWaresInventory.goods_sku_code << goods_sku_codes).execute()

    @classmethod
    def delete_qualified_inventory(cls, goods_sku_codes) -> None:
        """
        删除指定销售sku的全部良品库存数据，包括central_inventory、goods_inventory、central_inventory三个表

        :param list goods_sku_codes: 销售sku编码列表
        """
        cls.delete_central_inventory_by_goods_sku_codes(goods_sku_codes)
        cls.delete_goods_inventory_by_goods_sku_codes(goods_sku_codes)
        cls.delete_wares_inventory_by_goods_sku_codes(goods_sku_codes)

    @classmethod
    def query_bom_detail(cls, sale_sku_code, bom_version) -> dict:
        """
        查询指定销售sku的bom明细数据，并格式化为：{ware_sku1:bom_qty1,ware_sku2:bom_qty2}

        :param string sale_sku_code: 销售sku编码
        :param string bom_version: bom版本
        :return: bom版本仓库sku明细字典
        """
        items = BomDetail.select().order_by(BomDetail.id).where(
            BomDetail.goods_sku_code == sale_sku_code, BomDetail.bom_version == bom_version)
        items = [model_to_dict(item) for item in items]

        sale_sku_bom_detail = {item['ware_sku_code']: item['bom_qty'] for item in items}
        return sale_sku_bom_detail

    @classmethod
    def query_bom_detail_by_ware_sku_code(cls, ware_sku_code) -> dict:
        """
        查询指定仓库sku的bom明细数据

        :param string ware_sku_code: 仓库sku编码
        :return: 仓库sku的对应的bom明细
        """
        item = BomDetail.get(BomDetail.ware_sku_code == ware_sku_code)
        return model_to_dict(item)

    @classmethod
    def query_unqualified_inventory(cls, sale_sku_code, warehouse_id, bom_version='') -> list:
        """
        查询指定销售sku的次品库存数据

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
        data = [model_to_dict(item) for item in items]
        return data
