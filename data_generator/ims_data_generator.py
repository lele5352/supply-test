from data_generator import *
from db_operator.ims_db_operator import IMSDBOperator
from data_generator import ims_logics, wms_logics


class ImsDataGenerator:
    def __init__(self):
        pass

    @classmethod
    def add_bom_stock(cls, sale_sku, bom, count, warehouse_id, to_warehouse_id):
        bom_detail = IMSDBOperator.query_bom_detail(sale_sku, bom)
        location_ids = wms_logics.get_kw(1, 5, len(bom_detail) + 1, warehouse_id, to_warehouse_id)

        res = ims_logics.add_lp_stock_by_other_in(sale_sku, bom, count, location_ids, warehouse_id, to_warehouse_id)
        if res and res['code'] == 200:
            return True
        return

    @classmethod
    def add_ware_stock(cls, ware_qty_list, kw_ids, ck_id, to_ck_id):
        """
        :param list ware_qty_list: 仓库sku个数配置，格式： [('62325087738A01', 4), ('62325087738A01', 5)]
        :param list kw_ids: 仓库库位id数据，与ware_qty_list长度相等
        :param int ck_id: 仓库id
        :param int or None kw_ids: 目的仓id，备货仓时为空
        """
        res = ims_request.lp_other_in(ware_qty_list, kw_ids, ck_id, to_ck_id)
        return res

    @classmethod
    def del_stock(cls, sale_skus):
        IMSDBOperator.delete_qualified_inventory(sale_skus)

