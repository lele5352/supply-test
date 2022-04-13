from logics.ums_logics import UmsLogics
from db_operator.ims_db_operate import IMSDBOperator
from api_request.wms_app_request import WmsAppRequest
from logics.ims_logics import ImsLogics

ums_logics = UmsLogics()
ims_logics = ImsLogics()
app_headers = ums_logics.get_app_headers()
service_headers = ums_logics.get_service_headers()

ims_request = ims_logics.ims_request

wms_request = WmsAppRequest(app_headers, service_headers)

# 160的测试数据
# sale_sku = '63203684930'
sale_sku = '67330337129'
bom = 'G'
ware_sku = '63203684930A01'
delivery_warehouse_id = 513
delivery_warehouse_id2 = 568
exchange_warehouse_id = 511
exchange_warehouse_id2 = 566
stock_warehouse_id = 512
stock_warehouse_id2 = 565
straight_delivery_warehouse_id = 514

# 26的测试品
# sale_sku = '19109732120'
# bom = 'A'
# ware_sku_code = '19109732120A01'
# delivery_warehouse_id = 31
# exchange_warehouse_id = 29
# stock_warehouse_id = 30

bom_detail = IMSDBOperator.query_bom_detail(sale_sku, bom)

# 发货仓上架库位
fsj_kw_ids = wms_request.db_get_kw(1, 5, 2, delivery_warehouse_id, delivery_warehouse_id)

# 中转仓上架库位
zsj_kw_ids = wms_request.db_get_kw(1, 5, 2, exchange_warehouse_id, delivery_warehouse_id)

# 备货仓上架库位
bsj_kw_ids = wms_request.db_get_kw(1, 5, 2, stock_warehouse_id, '')

# 发货仓托盘库位
tp_kw_ids = wms_request.db_get_kw(1, 3, 2, delivery_warehouse_id, delivery_warehouse_id)

# 中转仓托盘库位
ztp_kw_ids = wms_request.db_get_kw(1, 3, 2, exchange_warehouse_id, delivery_warehouse_id)

# 备货仓托盘库位
btp_kw_ids = wms_request.db_get_kw(1, 3, 2, stock_warehouse_id, '')

# 发货仓次品库位
fcp_kw_id = wms_request.db_get_kw(1, 6, 1, delivery_warehouse_id, delivery_warehouse_id)

# 发货仓次品库位
fcp_kw_ids = wms_request.db_get_kw(1, 6, 2, delivery_warehouse_id, delivery_warehouse_id)

# 发货仓移库库位
yk_kw_id = wms_request.db_get_kw(1, 4, 1, delivery_warehouse_id, delivery_warehouse_id)
