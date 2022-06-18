eta_api_config = {
    "mall_get_available_stock": {
        "uri_path": "/mall/availableStock",
        "method": "post",
        "data": {
            "current": 1,
            "size": 1000,
            "deliveryWarehouseCodes": [],
            "version": 51668542
        }
    },
    "mall_get_not_trade_self_goods_eta": {
        "uri_path": "/mall/calculate",
        "method": "post",
        "data":
            {
                "countryCode": "26",
                "siteCode": "0",
                "skuCodes": ["1"],
                "zipCode": 2
            }
    },
    "mall_country_delivery_warehouses": {
        "uri_path": "/mall/country",
        "method": "get",
        "data": ''
    },
    "mall_get_trade_self_goods_eta": {
        "uri_path": "/mall/eta/trade/self",
        "method": "post",
        "data": {
            "countryCode": "",
            "skuInfos": [
                {
                    "skuCode": "",
                    "warehouseCode": ""
                }
            ],
            "zipCode": ""
        }
    },
    "mall_get_country_list": {
        "uri_path": "/mall/getList",
        "method": "post",
        "data":
            {
                "countryCode": "",
            }
    },
    "mall_get_inventory": {
        "uri_path": "/mall/inventory/get",
        "method": "post",
        "data": {
            "abroadFlag": 0,  # 海外仓标识：0全美(包含国内仓)，1海外仓，2国内仓
            "countryCode": "",
            "current": 1,
            "size": 1000
        }
    },
    "mall_get_distribute_warehouses_info_by_country_and_zipcode": {
        "uri_path": "/mall/warehouses",
        "method": "post",
        "data": [
            {
                "countryCode": "",
                "zipCode": ""
            }
        ]
    },
    "mall_get_distribute_warehouses_info_by_four_params": {
        "uri_path": "/mall/warehouses/sku",
        "method": "post",
        "data": [
            {
                "countryCode": "",
                "siteCode": "",
                "skuCode": "",
                "zipCode": ""
            }
        ]
    }
}