from data_helper.ims_data_helper import ImsDataHelper

ims = ImsDataHelper()
sale_sku_code = '11471839197'
bom_version = 'A'
ware_sku_code = '11471839197A01'
delivery_warehouse_id = 31
exchange_warehouse_id = 30
stock_warehouse_id = 29


bom_detail = ims.get_sale_sku_bom_detail(sale_sku_code, bom_version)
