from db_operator.ims_db_operator import IMSDBOperator
from data_generator import ims_logics, wms_logics


class ImsDataGenerator:
    def __init__(self):
        self.ims_logics = ims_logics

    def add_stock(self, sale_sku, bom, count, warehouse_id, to_warehouse_id):
        bom_detail = IMSDBOperator.query_bom_detail(sale_sku, bom)
        location_ids = wms_logics.get_kw(1, 5, len(bom_detail), warehouse_id, to_warehouse_id)

        res = ims_logics.add_lp_stock_by_other_in(sale_sku, bom, count, location_ids, warehouse_id, to_warehouse_id)
        if res and res['code'] == 200:
            return True
        return


if __name__ == '__main__':
    ims = ImsDataGenerator()
    sale_sku = '63203684930'
    bom = 'A'
    count = 10
    warehouse_id = 513
    to_warehouse_id = 513
    ims.add_stock(sale_sku, bom, count, warehouse_id, to_warehouse_id)
