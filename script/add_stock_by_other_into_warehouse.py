from controller.ims_controller import ImsController
from controller.wms_controller import WmsController
from controller.ums_controller import UmsController


def add_stock_by_other_in(sale_sku_code, bom_version, add_stock_count, current_warehouse_id, target_warehouse_id):
    ums = UmsController()
    ims = ImsController()
    wms = WmsController(ums)
    # ims.delete_ims_data(sale_sku_code)
    location_id = wms.db_get_location_ids(5, 1, current_warehouse_id, target_warehouse_id)
    detail = ims.get_sale_sku_bom_detail(sale_sku_code, bom_version)
    ware_sku_list = list()
    for ware_sku, qty in detail.items():
        ware_sku_list.append(
            {
                "qty": qty * add_stock_count,
                "storageLocationId": location_id,
                "storageLocationType": 5,
                "wareSkuCode": ware_sku
            }
        )
    res = ims.other_into_warehouse(ware_sku_list, current_warehouse_id, target_warehouse_id)
    return res


if __name__ == '__main__':
    current_warehouse_id = 511
    target_warehouse_id = 513
    sale_sku_code = '63203684930'
    bom_version = 'A'
    add_stock_count = 4
    add_stock_by_other_in(sale_sku_code, bom_version, add_stock_count, current_warehouse_id, target_warehouse_id)
