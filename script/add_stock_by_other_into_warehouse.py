from data_helper.ims_data_helper import ImsDataHelper

ims_handler = ImsDataHelper()

current_warehouse_id = 31
target_warehouse_id = 31
sale_sku_code = '11471839197'
# sale_sku_code = '73781610267'

# ims_handler.delete_ims_data(sale_sku_code, current_warehouse_id)
ware_sku_list = [
    # {
    #     "qty": 3,
    #     "storageLocationId": 154,
    #     "storageLocationType": 5,
    #     "wareSkuCode": "73781610267A01"
    # }
    {
        "qty": 6,
        "storageLocationId": 155,
        "storageLocationType": 5,
        "wareSkuCode": "11471839197A01"
    }, {
        "qty": 3,
        "storageLocationId": 155,
        "storageLocationType": 5,
        "wareSkuCode": "11471839197A02"
    }
]
res = ims_handler.other_into_warehouse(ware_sku_list, current_warehouse_id, target_warehouse_id)
print(res)