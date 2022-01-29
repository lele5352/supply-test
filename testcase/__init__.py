from controller.ums_controller import UmsController
from controller.wms_controller import WmsController
from controller.ims_controller import ImsController
from controller.wms_transfer_service_controller import WmsTransferServiceController

ums = UmsController()
wms = WmsController(ums)
transfer_service = WmsTransferServiceController(ums)
ims = ImsController()

# 160的测试数据
sale_sku_code = '63203684930'
bom_version = 'A'
ware_sku_code = '63203684930A01'

# 26的测试品
# sale_sku_code = '19109732120'
# bom_version = 'A'
# ware_sku_code = '19109732120A01'
# delivery_warehouse_id = 31
# exchange_warehouse_id = 29
# stock_warehouse_id = 30

bom_detail = ims.get_sale_sku_bom_detail(sale_sku_code, bom_version)

delivery_warehouse_id = 513
exchange_warehouse_id = 511
stock_warehouse_id = 512
straight_delivery_warehouse_id = 514

id_to_code = {513: 'ESFH',511: 'ESZZ',512: 'ESBH',514: 'ESZF'}

# 发货仓上架库位
fsj_location_ids = wms.db_get_location_ids(5, len(bom_detail), delivery_warehouse_id)

# 中转仓上架库位
zsj_location_ids = wms.db_get_location_ids(5, len(bom_detail), exchange_warehouse_id, delivery_warehouse_id)

# 备货仓上架库位
bsj_location_ids = wms.db_get_location_ids(5, len(bom_detail), stock_warehouse_id)

# 发货仓次品库位
fcp_location_id = wms.db_get_location_ids(6, 1, delivery_warehouse_id)

# 发货仓移库库位
yk_location_id = wms.db_get_location_ids(4, 1, delivery_warehouse_id)
