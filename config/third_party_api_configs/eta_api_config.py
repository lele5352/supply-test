from config.third_party_api_configs import ApiConfig


class ETAApiConfig:
    class GetAvailableStock(ApiConfig):
        uri_path = "/mall/availableStock"
        method = "post"
        data = {
            "current": 1,
            "size": 1000,
            "deliveryWarehouseCodes": []}

    class GetGoodsETA(ApiConfig):
        uri_path = "/mall/calculate"
        method = "post"
        data = {
            "countryCode": "26",
            "siteCode": "0",
            "skuCodes": ["1"],
            "zipCode": 2
        }

    class CountryDeliveryWarehouses(ApiConfig):
        uri_path = "/mall/country"
        method = "get"
        data = ""

    class GetTradeSelfGoodsEtA(ApiConfig):
        uri_path = "/mall/eta/trade/self"
        method = "post"
        data = {
            "countryCode": "",
            "skuInfos": [
                {
                    "skuCode": "",
                    "warehouseCode": ""
                }
            ],
            "zipCode": ""
        }

    class GetCountryList(ApiConfig):
        uri_path = "/mall/getList"
        method = "post"
        data = {"countryCode": ""}

    class GetInventory(ApiConfig):
        uri_path = "/mall/inventory/get"
        method = "post"
        data = {
            "abroadFlag": 0,  # 海外仓标识：0全美(包含国内仓)，1海外仓，2国内仓
            "countryCode": "",
            "current": 1,
            "size": 1000
        }

    class GetDistributeWarehousesByCountryAndZipcode(ApiConfig):
        uri_path = "/mall/warehouses"
        method = "post"
        data = [
        ]

    class GetDistributeWarehousesByFourParams(ApiConfig):
        uri_path = "/mall/warehouses/sku"
        method = "post"
        data = [
            {
                "countryCode": "",
                "siteCode": "",
                "skuCode": "",
                "zipCode": ""
            }
        ]
