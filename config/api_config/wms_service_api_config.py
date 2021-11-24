wms_service_api_config = {
    "entry_order_create": {
        "uri_path": "/entryorder",
        "method": "post",
        "data": {
            "entryOrderType": 3,
            "eta": 1630058027000,
            "fromOrderCode": "LY000002",
            "logisticsInfoList":
                [
                    {
                        "carNumber": "粤A·88888",
                        "delivererName": "许宏伟",
                        "logisticsCompanyCode": "WULI0002",
                        "logisticsCompanyName": "艾斯物流有限公司",
                        "phone": "18888888888",
                        "shipmentNumber": "YD10000000002",
                        "telephone": "020-88888888"
                    }
                ],
            "operationFlag": 1,
            "qualityType": 1,
            "remark": "测试新增其他入库单",
            "supplierCode": "S37501617",
            "skuInfoList": [
                {
                    "warehouseSkuCode": "W21047361",
                    "planSkuQty": 4,
                    "warehouseSkuName": "小部件sku内部bom包裹1",
                    "warehouseSkuNameEn": "",
                    "warehouseSkuLength": 56.34,
                    "warehouseSkuWidth": 4.12,
                    "warehouseSkuHeight": 34.00,
                    "warehouseSkuWeight": 4.00,
                    "saleSkuCode": "P68687174",
                    "saleSkuImg": "https://img.popicorns.com/dev/file/2021/07/21/9736810758dc4fc8b9d1b4829a72b779.jpg",
                    "bomVersion": "1",
                    "saleSkuName": "小部件sku"
                },
                {
                    "warehouseSkuCode": "W64185400",
                    "planSkuQty": 7,
                    "warehouseSkuName": "小部件sku内部bom包裹2",
                    "warehouseSkuNameEn": "",
                    "warehouseSkuLength": 55.00,
                    "warehouseSkuWidth": 34.00,
                    "warehouseSkuHeight": 34.00,
                    "warehouseSkuWeight": 3.00,
                    "saleSkuCode": "P68687174",
                    "saleSkuImg": "https://img.popicorns.com/dev/file/2021/07/21/9736810758dc4fc8b9d1b4829a72b779.jpg",
                    "bomVersion": "1",
                    "saleSkuName": "小部件sku"
                }
            ]
        }
    }
}
