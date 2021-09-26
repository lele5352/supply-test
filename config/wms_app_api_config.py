wms_app_api_config = {
    "location_create": {
        "uri_path": "/api/ec-wms-api/location/save",
        "method": "post",
        "data": {
            "belongWarehouseId": 19,  # 所属仓库
            "belongWarehouseAreaId": 15,  # 所属库区
            "warehouseAreaType": 1,  # 库区类型 0-上架区 1-不良品区 2-入库异常处理区 3-出库异常处理区 4-出库异常处理区 5-容器库区
            "warehouseLocationCode": "KWBM",  # 库位编码
            "warehouseLocationName": "KW",  # 库位名称
            "destWarehouseId": 7,  # 目的仓id
            "warehouseLocationType": 1  # 库位类型 1-收货库位 2-质检库位 3-调拨库位 4-移库库位 5-上架库位 6-不良品库位 7-入库异常库位 8-出库异常库位}
        }
    },
    "location_edit": {
        "uri_path": "/api/ec-wms-api/location/update",
        "method": "put",
        "data": {
            "warehouseLocationId": 22,
            "warehouseLocationStatus": 1,  # 库位状态更新时传 0-启用 1-禁用
            "warehouseLocationName": "库位",
            "warehouseLocationType": 3,  # 库位类型 1-收货库位 2-质检库位 3-调拨库位 4-移库库位
            "destWarehouseId": 19  # 目的仓
        }
    },
    "location_search": {
        "uri_path": "/api/ec-wms-api/location/page",
        "method": "post",
        "data": {

            "belongWareHouseAreaCode": "cocoakuqu001",
            #    ids: 1
            #    sortField:
            #      field:
            #      type
            "warehouseAreaType": 5,
            "destWarehouseCode": "cocotest005",  # 目的仓编码
            "warehouseId": 7,
            "warehouseLocationCode": "KW1626776828868",
            "warehouseLocationName": "库位1626777231313",
            "warehouseLocationStatus": 1,
            "warehouseLocationType": 4,
            "warehouseLocationUseStatus": 0
        }
    },
    "location_status_edit": {
        "uri_path": "/api/ec-wms-api/location/updateStatus",
        "method": "put",
        "data": {
            "warehouseLocationId": 21,
            "status": 1  # 0 禁用，1 启用
        }
    },
    "receipt_order_create": {
        "uri_path": "/api/ec-wms-api/receivegoods/save",
        "method": "post",
        "data": {
            "entryOrderCode": "RK2107230013",
            "qualityControlType": 1,
            "receiveLocationInfos":
                [
                    {
                        "locationCode": "",
                        "skuCode": "W21047361",
                        "bomVersion": 1,
                        "saleSkuCode": "P68687174",
                        "length": 56.34,
                        "width": 4.12,
                        "height": 34.00,
                        "weight": 4.00,
                        "skuNumber": 4

                    },
                    {
                        "locationCode": "",
                        "skuCode": "W64185400",
                        "bomVersion": 1,
                        "saleSkuCode": "P68687174",
                        "length": 55.00,
                        "width": 34.00,
                        "height": 34.00,
                        "weight": 3.00,
                        "skuNumber": 7
                    }
                ]
        }
    },
    "receipt_handover": {
        "uri_path": "/api/ec-wms-api/receivegoodshandover/confirm",
        "method": "post",
        "data": {"locationCodes": []}
    },
    "service_entry_order_create": {
        "uri_path": "/en-entry-order/saveEntryOrder",
        "method": "post",
        "data": {
            'entryOrderInput': {
                'purchaseOrderCode': 'CG',
                'distributeOrderCode': 'FH',
                'entryOrderType': 0,
                'entryOrderState': 1,
                'qualityType': 1,
                'planArrivalTime': 1630058027000,
                'supplierCode': 'S31637083',
                'remark': '我只是个备注',
                'warehouseId': 19,
                'destWarehouseId': 7
            },
            'skuList': [
                {
                    'warehouseSkuCode': '11471839197A01',
                    'planSkuQty': 2,
                    'warehouseSkuName': '小部件sku内部bom包裹1',
                    'warehouseSkuNameEn': '',
                    'warehouseSkuLength': 56.34,
                    'warehouseSkuWidth': 4.12,
                    'warehouseSkuHeight': 34.00,
                    'warehouseSkuWeight': 4.00,
                    'saleSkuCode': '11471839197',
                    'saleSkuQty': 1,
                    'saleSkuImg': 'https://img.popicorns.com/dev/file/2021/07/21/9736810758dc4fc8b9d1b4829a72b779.jpg',
                    'bomVersion': 'A',
                    'saleSkuName': '小部件sku'
                },
                {
                    'warehouseSkuCode': '11471839197A02',
                    'planSkuQty': 1,
                    'warehouseSkuName': '小部件sku内部bom包裹2',
                    'warehouseSkuNameEn': '',
                    'warehouseSkuLength': 55.00,
                    'warehouseSkuWidth': 34.00,
                    'warehouseSkuHeight': 34.00,
                    'warehouseSkuWeight': 3.00,
                    'saleSkuCode': '11471839197',
                    'saleSkuQty': 1,
                    'saleSkuImg': 'https://img.popicorns.com/dev/file/2021/07/21/9736810758dc4fc8b9d1b4829a72b779.jpg',
                    'bomVersion': 'A',
                    'saleSkuName': '小部件sku'
                }
            ],
            'logisticsList': [
                {
                    'logisticsCompanyCode': 'SF072611',
                    'logisticsCompanyName': '顺丰物流',
                    'shipmentNumber': 'SF23425289472',
                    'carNumber': '粤·A88888',
                    'delivererName': '万老板',
                    'phone': '18434223434',
                    'telephone': '0203423432'
                }
            ]
        }
    },
    "quality_order_create": {
        "uri_path": "/api/ec-wms-api/qualitycheck/save",
        "method": "post",
        "data": {
            "skuList": [
                {
                    "receiveLocationCode": "",
                    "entryOrderCode": "",
                    "receiveOrderCode": "",
                    "qcResult": 0,  # 1-不良品；0-良品
                    "skuCode": "W21047361",
                    "number": 4,
                    "qcLocationCode": "",
                    "errorLocationCode": "",
                    "length": "66.6",
                    "width": "77.7",
                    "height": "88.8",
                    "weight": "99.9"
                },
                {
                    "receiveLocationCode": "",
                    "entryOrderCode": "",
                    "receiveOrderCode": "",
                    "qcResult": 0,
                    "skuCode": "W64185400",
                    "number": 7,
                    "qcLocationCode": "",
                    "errorLocationCode": "",
                    "length": "22.2",
                    "width": "33.3",
                    "height": "44.4",
                    "weight": "55.5"
                }
            ]

        },
    },
    "quality_handover": {
        "uri_path": "/api/ec-wms-api/qualitycheckhandover/confirm",
        "method": "post",
        "data": {"locationCodes": []}
    },
    "shelves_order_create": {
        "uri_path": "/api/ec-wms-api/upshelf/save",
        "method": "post",
        "data": {
            "oldLocationCode": "",
            "oldLocationType": 2,
            "upshelfLocationCode": "",
            "upshelfType": 0,
            "upShelfMode": 0,
            "skuInfos": []

        }
    },
    "front_label_delivery_order_create": {
        "uri_path": "/delivery-order",
        "method": "post",
        "data": {
            "warehouseCode": "EH",
            "sourceOrderCode": "source",
            "saleOrderId": 825007,
            "saleOrderCode": "sale",
            "transportMode": 1,
            "priority": "9",
            "site": "us",
            "saleAmount": 200.2,
            "currency": "USD",
            "orderTime": "2021-08-23 15:47:09",
            "platformName": "homary-name",
            "platformCode": "homary",
            "storeCode": "ziying",
            "store": "自营",
            "customerRemarks": "这是客户备注",
            "serverRemarks": "这是HW自造的数据",
            "receiptInfo": {
                "firstName": "liang",
                "lastName": "chupeng",
                "phone": "1082007071",
                "identityCard": "",
                "email": "liangchupeng@popicorns.com",
                "countryId": 1,
                "countryCode": "US",
                "country": "United States",
                "stateId": 50,
                "stateCode": "IL",
                "state": "Illinois",
                "city": "Naperville",
                "area": "",
                "address1": "1648 Harris Ln",
                "address2": "",
                "address3": "",
                "lat": "",
                "lon": "",
                "postcode": "60565"
            },
            "skuInfo": [{
                "saleSkuCode": "88892034045",
                "saleSkuName": "沙发组合LG705",
                "saleSkuImg": "https://img.popicorns.com/dev/file/2021/09/06/ec6b5da459564b4cb19c3e61ed34810f.jpg",
                "purchasePrice": 9,
                "purchaseCurrency": "USD",
                "salePrice": 18,
                "saleCurrency": "USD",
                "saleSkuQty": 1
            }]
        }
    },
    "behind_label_delivery_order_create": {
        "uri_path": "/delivery-order",
        "method": "post",
        "data": {
            "warehouseCode": "EH",
            "sourceOrderCode": "sourcem0825003",
            "saleOrderId": 1825003,
            "saleOrderCode": "sale0825003",
            "transportMode": 2,
            "priority": "9",
            "site": "us",
            "saleAmount": 200.2,
            "currency": "USD",
            "orderTime": "2021-08-23 15:47:09",
            "platformName": "homary-name",
            "platformCode": "homary",
            "storeCode": "ziying",
            "store": "自营",
            "customerRemarks": "这是客户备注",
            "serverRemarks": "这是HW自造的数据",
            "receiptInfo": {
                "firstName": "liang",
                "lastName": "chupeng",
                "phone": "1082007071",
                "identityCard": "",
                "email": "liangchupeng@popicorns.com",
                "countryId": 1,
                "countryCode": "US",
                "country": "United States",
                "stateId": 50,
                "stateCode": "IL",
                "state": "Illinois",
                "city": "Naperville",
                "area": "",
                "address1": "1648 Harris Ln",
                "address2": "",
                "address3": "",
                "lat": "",
                "lon": "",
                "postcode": "60565"
            },
            "skuInfo": [
                {
                    "saleSkuCode": "88892034045",
                    "saleSkuName": "沙发组合LG705",
                    "saleSkuImg": "https://img.popicorns.com/dev/file/2021/09/06/ec6b5da459564b4cb19c3e61ed34810f.jpg",
                    "purchasePrice": 9,
                    "purchaseCurrency": "USD",
                    "salePrice": 18,
                    "saleCurrency": "USD",
                    "saleSkuQty": 1
                },
                {
                    "saleSkuCode": "19109732485",
                    "saleSkuName": "脚凳LG732",
                    "saleSkuImg": "https://img.popicorns.com/dev/file/2021/05/14/6eb51de377bf4d1cbaad27c52cd4eca8.jpg",
                    "purchasePrice": 19,
                    "purchaseCurrency": "USD",
                    "salePrice": 28,
                    "saleCurrency": "USD",
                    "saleSkuQty": 1
                }]
        }
    },
    "front_label_express_order_call_back": {
        "uri_path": "/delivery-order-api/push-express-order",
        "method": "post",
        "data": {
            "deliveryNo": "CK2108250009",
            "orderList": [
                {
                    "deliveryNo": "CK2108250009",
                    "packageNo": "BG2108250025",
                    "logistyNo": "2108250025",
                    "barCode": "barcode2108250025",
                    "serviceName": "测试服务商1",
                    "serviceCode": "test service1",
                    "channelName": "channel-name1",
                    "channelCode": "channel01",
                    "fileList": [
                        {
                            "filePath": "https://tmsapi.popicorns.com/wh/image/get-label?id=722",
                            "fileType": "PDF",
                            "fileCategory": "1",
                            "fileScale": "7*2.5"
                        },
                        {
                            "filePath": "https://tmsapi.popicorns.com/wh/image/get-label?id=495",
                            "fileType": "PDF",
                            "fileCategory": "2",
                            "fileScale": "7*2.5"
                        }
                    ],
                    "whOrderNo": "wh2108250025",
                    "saleNo": "saleno2108250025",
                    "turnOrderNo": "turn2108250025",
                    "drawOrderNo": "draw2108250025"
                }
            ],
            "code": 1,
            "info": "success"
        }
    },
    "stock_assign": {
        "uri_path": "/delivery-order/stock-assign",
        "method": "post",
        "data": {"deliveryOrderCodes": ["CK2108250017"]}
    },
    "package_assign_call_back": {
        "uri_path": "/delivery-order-api/push-plan",
        "method": "post",
        "data": {
            "deliveryNo": "CK2108250005",
            "status": 1,
            "packageInfo": {
                "channelPrice": "111",
                "packageCount": 2,
                "packageIds": [
                    "35", "36"
                ],
                "packageList": [
                    {
                        "packageNo": "BG2108250018",
                        "channelPrice": "10",
                        "channelId": "1",
                        "channelCode": "channel01",
                        "channelName": "channel-name1",
                        "serviceId": "1",
                        "serviceCode": "test service1",
                        "serviceName": "测试服务商1",
                        "timeValue": "1",
                        "length": "11",
                        "width": "22",
                        "height": "33",
                        "weight": "4",
                        "packageSkuList": [
                            {
                                "skuCode": "W83818168",
                                "skuName": "test1",
                                "num": 1
                            }
                        ]
                    },
                    {
                        "packageNo": "BG2108250019",
                        "channelPrice": "20",
                        "channelId": "2",
                        "channelCode": "channel02",
                        "channelName": "channel-name2",
                        "serviceId": "2",
                        "serviceCode": "test service2",
                        "serviceName": "测试服务商2",
                        "timeValue": "2",
                        "length": "55",
                        "width": "66",
                        "height": "77",
                        "weight": "8",
                        "packageSkuList": [
                            {
                                "skuCode": "W21047361",
                                "skuName": "小部件sku内部bom包裹1",
                                "num": 4
                            },
                            {
                                "skuCode": "W64185400",
                                "skuName": "小部件sku内部bom包裹2",
                                "num": 7
                            }
                        ]
                    }
                ]
            },
            "code": 0,
            "info": ""
        }
    }
}
