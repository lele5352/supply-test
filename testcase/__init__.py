from controller.ums_controller import UmsController
from controller.wms_controller import WmsController
from controller.ims_controller import ImsController
from controller.wms_transfer_service_controller import WmsTransferServiceController

ums = UmsController()
ims = ImsController()
wms = WmsController(ums)
transfer = WmsTransferServiceController(ums)

# 160的测试数据
sale_sku = '63203684930'
bom = 'A'
ware_sku = '63203684930A01'
delivery_warehouse_id = 513
exchange_warehouse_id = 511
stock_warehouse_id = 512
straight_delivery_warehouse_id = 514

# 26的测试品
# sale_sku = '19109732120'
# bom = 'A'
# ware_sku_code = '19109732120A01'
# delivery_warehouse_id = 31
# exchange_warehouse_id = 29
# stock_warehouse_id = 30

bom_detail = ims.get_sale_sku_bom_detail(sale_sku, bom)

# 发货仓上架库位
fsj_kw_ids = wms.db_get_kw_ids(5, len(bom_detail), delivery_warehouse_id)

# 中转仓上架库位
zsj_kw_ids = wms.db_get_kw_ids(5, len(bom_detail), exchange_warehouse_id, delivery_warehouse_id)

# 备货仓上架库位
bsj_kw_ids = wms.db_get_kw_ids(5, len(bom_detail), stock_warehouse_id)

# 发货仓托盘库位
tp_kw_ids = wms.db_get_kw_ids(3, len(bom_detail), delivery_warehouse_id)

# 中转仓托盘库位
ztp_kw_ids = wms.db_get_kw_ids(3, len(bom_detail), exchange_warehouse_id, delivery_warehouse_id)

# 备货仓托盘库位
btp_kw_ids = wms.db_get_kw_ids(3, len(bom_detail), stock_warehouse_id)

# 发货仓次品库位
fcp_kw_id = wms.db_get_kw_ids(6, 1, delivery_warehouse_id)

# 发货仓移库库位
yk_kw_id = wms.db_get_kw_ids(4, 1, delivery_warehouse_id)
