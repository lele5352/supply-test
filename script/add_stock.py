from testcase import ims_logics, wms_logics
from db_operator.ims_db_operator import IMSDBOperator

sale_sku = '67330337129'
bom = 'D'
warehouse_id = 513
to_warehouse_id = 513

bom_detail = IMSDBOperator.query_bom_detail(sale_sku, bom)
location_ids = wms_logics.get_kw(1, 5, len(bom_detail), warehouse_id, to_warehouse_id)

res = ims_logics.add_lp_stock_by_other_in(sale_sku, bom, 200, location_ids, warehouse_id, to_warehouse_id)

print(res)
