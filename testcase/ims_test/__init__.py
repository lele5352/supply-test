from controller import ims, wms


sale_sku_code = '63203684930'
bom_version = 'A'
ware_sku_code = '63203684930A01'
delivery_warehouse_id = 513
exchange_warehouse_id = 511
stock_warehouse_id = 512

bom_detail = ims.get_sale_sku_bom_detail(sale_sku_code, bom_version)
# 发货仓上架库位
fsj_location_codes = wms.get_location_codes(len(bom_detail), 5, delivery_warehouse_id)
fsj_location_ids = [wms.get_location_id(location_code, delivery_warehouse_id) for location_code in
                    fsj_location_codes]
# 中转仓上架库位
zsj_location_codes = wms.get_location_codes(len(bom_detail), 5, exchange_warehouse_id, delivery_warehouse_id)
zsj_location_ids = [wms.get_location_id(location_code, exchange_warehouse_id) for location_code in
                    zsj_location_codes]
# 备货仓上架库位
bsj_location_codes = wms.get_location_codes(len(bom_detail), 5, stock_warehouse_id)
bsj_location_ids = [wms.get_location_id(location_code, stock_warehouse_id) for location_code in
                    bsj_location_codes]

# 发货仓次品库位
fcp_location_code = wms.get_location_codes(1, 6, delivery_warehouse_id)
fcp_location_id = wms.get_location_id(fcp_location_code[0], delivery_warehouse_id)

# 发货仓移库库位
yk_location_code = wms.get_location_codes(1, 4, delivery_warehouse_id)
yk_location_id = wms.get_location_id(yk_location_code[0], delivery_warehouse_id)
