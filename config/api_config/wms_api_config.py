wms_api_config = {
    "get_switch_warehouse_list": {
        "uri_path": "/api/ec-wms-api/data/permission/user/list",
        "method": "get",
        "data": {
            "t": 1640053950389
        }
    },
    "switch_default_warehouse": {
        "uri_path": "/api/ec-wms-api/data/permission/switchdefault",
        "method": "put",
        "data": {"dataPermId": 854}
    },
    "get_warehouse": {
        "uri_path": "/api/ec-wms-api/warehouse/page",
        "method": "post",
        "data": {
            "warehouseStatus": None,
            "sortField": [
                {
                    "field": "create_time",
                    "type": "DESC"
                }
            ],
            "operatingMode": None,
            "warehouseCode": "",
            "warehouseAbbreviation": "",
            "warehouseNameEn": "",
            "warehouseNameCn": "",
            "cnWarehouseFlag": "",
            "size": 10,
            "current": 1
        }
    },
    "get_warehouse_area": {
        "uri_path": "/api/ec-wms-api/warehousearea/page",
        "method": "post",
        "data": {
            "warehouseAreaStatus": None,
            "sortField": [{"field": "create_time", "type": "DESC"}],
            "warehouseAreaType": None,
            "warehouseAreaCode": "",
            "warehouseAreaName": "",
            "size": 1,
            "current": 1
        }
    },
    "get_warehouse_location": {
        "uri_path": "/api/ec-wms-api/location/page",
        "method": "post",
        "data": {
            "sortField": [
                {
                    "field": "create_time",
                    "type": "DESC"
                }
            ],
            "warehouseLocationStatus": 0,
            "belongWareHouseAreaCode": "",
            "warehouseAreaType": "",
            "destWarehouseCode": "",
            "warehouseLocationCode": "",
            "warehouseLocationName": "",
            "warehouseLocationType": "",
            "warehouseLocationUseStatus": "",
            "size": 10,
            "current": 1
        }
    },
    "create_location": {
        "uri_path": "/api/ec-wms-api/location/save",
        "method": "post",
        "data": {
            "belongWarehouseId": 19,  # 所属仓库
            "belongWarehouseAreaId": 15,  # 所属库区
            "warehouseAreaType": 1,  # 库区类型 0-上架区 1-不良品区 2-入库异常处理区 3-出库异常处理区 4-出库异常处理区 5-容器库区
            "warehouseLocationCode": "KWBM",  # 库位编码
            "warehouseLocationName": "KW",  # 库位名称
            "destWarehouseId": 7,  # 目的仓id
            "warehouseLocationType": 1,  # 库位类型 1-收货库位 2-质检库位 3-调拨库位 4-移库库位 5-上架库位 6-不良品库位 7-入库异常库位 8-出库异常库位}
            "warehouseLocationUseStatus": 0
        }
    },
    "create_transfer_demand": {
        "uri_path": "/transferDemand/create",
        "method": "post",
        "data": {
            "receiveWarehouseCode": "LA01",
            "receiveTargetWarehouseCode": "",
            "deliveryWarehouseCode": "FSBH",
            "deliveryTargetWarehouseCode": "",
            "userId": 1,
            "username": "admin",
            "goodsSkuCode": "53586714577",
            "demandQty": 5,
            "customerType": 1,  # 1：普通客户 2 ：大客户
            "customerRemark": "客戶備注",
            "sourceCode": "aaaaaaaaaaaaaaa",
            "demandType": 1  # 1:按需调拨需求 2：备货调拨需求
        }
    },
    "create_transfer_pick_order": {
        "uri_path": "/api/ec-wms-api/transferOut/picking/create",
        "method": "post",
        "data": {"demandCodes": ["XQ2201250017"], "pickType": 1}
    },
    "transfer_pick_order_assign_pick_user": {
        "uri_path": "/api/ec-wms-api/transferOut/picking/assignPickUser",
        "method": "post",
        "data": {"pickOrderNos": ["DJH2201250008"], "pickUsername": "李强", "pickUserId": "3"}
    },
    "transfer_confirm_pick": {
        "uri_path": "/api/ec-wms-api/transferOut/picking/doPicking",
        "method": "post",
        "data": {"pickOrderNo": ["DJH2201250008"], "details": []}
    },
    "transfer_pick_order_detail": {
        "uri_path": "/api/ec-wms-api/transferOut/picking/detail/%s",
        "method": "get",
        "data": {"t": 1643333857384}
    },
    "transfer_submit_tray": {
        "uri_path": "/api/ec-wms-api/transferOut/pda/submitTrayInfo",
        "method": "post",
        "data": [{
            "storageLocationCode": "TPKW-001",
            "pickOrderNo": "DJH2201290004",
            "trayInfos": [{
                "id": 792,
                "waresSkuCode": "63203684930A02",
                "waresSkuName": "酒柜(金色)07 2/2 X5",
                "goodsSkuCode": "63203684930",
                "goodsSkuName": "棕色木纹四裙垂直边独立式浴缸3",
                "skuQty": 10
            }]
        }]
    },
    "create_other_entry_order": {
        "uri_path": "/api/ec-wms-api/entryorder",
        "method": "put",
        "data": {
            "receiveWarehouseCode": "LA01",
            "deliveryWarehouseCode": "FSBH",
            "userId": 1,
            "username": "admin",
            "goodsSkuCode": "53586714577",
            "demandQty": 5,
            "customerType": 1,  # 1：普通客户 2 ：大客户
            "customerRemark": "客戶備注",
            "sourceCode": "aaaaaaaaaaaaaaa",
            "demandType": 1  # 1:按需调拨需求 2：备货调拨需求
        }
    },
    "submit_other_entry_order": {
        "uri_path": "/api/ec-wms-api/entryorder",
        "method": "put",
        "data": {
            "receiveWarehouseCode": "LA01",
            "deliveryWarehouseCode": "FSBH",
            "userId": 1,
            "username": "admin",
            "goodsSkuCode": "53586714577",
            "demandQty": 5,
            "customerType": 1,  # 1：普通客户 2 ：大客户
            "customerRemark": "客戶備注",
            "sourceCode": "aaaaaaaaaaaaaaa",
            "demandType": 1  # 1:按需调拨需求 2：备货调拨需求
        }
    }
}
