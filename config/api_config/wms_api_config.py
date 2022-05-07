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
    "transfer_pick_order_tray_detail": {
        "uri_path": "/api/ec-wms-api/transferOut/tray/detail?pickOrderNo=%s",
        "method": "get",
        "data": ""
    },
    "transfer_finish_packing": {
        "uri_path": "/api/ec-wms-api/transferOut/pda/finishPacking",
        "method": "post",
        "data": {
            "pickOrderNo": "",
            "storageLocationCodes": []
        }
    },
    "transfer_out_order_detail": {
        "uri_path": "/api/ec-wms-api/transferOut/handover/boxes?transferOutNo=%s",
        "method": "get",
        "data": ""
    },
    "transfer_out_order_review": {
        "uri_path": "/api/ec-wms-api/transferOut/box/review/submit",
        "method": "post",
        "data": {
            "boxNo": "DC2202070002-1",
            "storageLocationCode": "TPKW-001"
        }
    },
    "transfer_box_bind": {
        "uri_path": "/api/ec-wms-api/transferOut/handover/bind",
        "method": "post",
        "data": {
            "boxNo": "DC2202070002-1",
            "handoverNo": "",
            "receiveWarehouseCode": ""
        }
    },
    "transfer_delivery": {
        "uri_path": "/api/ec-wms-api/transferOut/handover/delivery/confirm",
        "method": "post",
        "data": {
            "handoverNo": ""
        }
    },
    "transfer_in_received": {
        "uri_path": "/api/ec-wms-api/transferIn/handover/received/confirm",
        "method": "post",
        "data": {
            "handoverNo": ""
        }
    },
    "transfer_box_up_shelf": {
        "uri_path": "/api/ec-wms-api/transferIn/input/box/shelf",
        "method": "post",
        "data": {
            "boxNo": "DC2202070021-1",
            "storageLocationCode": "SJKW-001"
        }
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
    },
    "label_callback": {
        "uri_path": "/api/ec-wms-api/delivery-order-api/push-express-order/v2",
        "method": "post",
        "data": {
            "deliveryNo": "PRE-CK2205050011",
            "orderList": [
                {
                    "expressChangeFlag": 0,
                    "expressChangeVersion": "1",
                    "deliveryNo": "PRE-CK2205050011",
                    "packageNoList": [
                        "PRE-BG2205050039"
                    ],
                    "logistyNo": "64324234152-119900",
                    "barCode": "534574353214234-119900",
                    "serviceName": "正式-Postpony",
                    "serviceCode": "prod-PostPony",
                    "channelName": "正式-PostPony-PostPony",
                    "channelCode": "UspsFirstClassMail",
                    "fileList": [
                        {
                            "filePath": "https://img.popicorns.com/dev/file/2022/02/28/f8a138a6a3e5447cad33a9ab9cc800fa.pdf",
                            "fileType": "pdf",
                            "fileCategory": "1",
                            "fileScale": "10*10",
                            "fileCopies": "1",
                            "filePrintDirection": "0"
                        }
                    ],
                    "extInfo": "{\"logisticsMerchant\": \"UPS1\", \"turnOrderNo\": \"转运单号123123\"}",
                    "turnOrderNo": "543255",
                    "drawOrderNo": "7879096854"
                }
            ]
        }
    }
}
