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
    }
}
