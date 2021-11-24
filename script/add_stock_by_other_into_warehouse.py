from controller.ims_controller import ImsController


def add_stock_by_other_in(sale_sku_code, bom_version, add_stock_count, current_warehouse_id, target_warehouse_id):
    ims = ImsController()
    # ims.delete_ims_data(sale_sku_code,current_warehouse_id)
    detail = ims.get_sale_sku_bom_detail(sale_sku_code, bom_version)
    ware_sku_list = list()
    for ware_sku, qty in detail.items():
        ware_sku_list.append(
            {
                "qty": qty * add_stock_count,
                "storageLocationId": 1505,
                "storageLocationType": 5,
                "wareSkuCode": ware_sku
            }
        )
    res = ims.other_into_warehouse(ware_sku_list, current_warehouse_id, target_warehouse_id)
    return res


if __name__ == '__main__':
    current_warehouse_id = 513
    target_warehouse_id = 513
    sale_sku_code = '63203684457'
    bom_version = 'A'
    add_stock_count = 1
    add_stock_by_other_in(sale_sku_code, bom_version, add_stock_count, current_warehouse_id, target_warehouse_id)
