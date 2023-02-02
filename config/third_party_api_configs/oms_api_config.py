from config.third_party_api_configs import ApiConfig


class OMSApiConfig:
    class GetFollowOrderPage(ApiConfig):
        uri_path = "/api/ec-oms-api/order/trackOrder/page"
        method = "post"
        data = {"current": 1, "size": 10, "sortKey": "follow_time", "direction": 1, "itemSkuCode": "",
                "salesOrderNo": "",
                "orderNo": "", "siteCode": "", "buyerName": "", "platformCodeList": [], "deliveryWarehouseCode": [],
                "country": [], "excludeCountry": [], "relateSalesOrderNos": "", "intercept": "",
                "interceptTypeList": [],
                "followOrderTypeList": [], "buyerId": "", "followTimeStart": "", "followTimeEnd": "",
                "payTimeStart": "",
                "payTimeEnd": ""}


oms_api_config = {
    "get_product_info": {
        "uri_path": "/ec-oms-api/salesorder/listProduct",
        "method": "get",
        "data": {
            "current": 1,
            "size": 10,
            "type": 1,
            "skuCode": "JJH3C94287",
            "productNameCn": "",
            "siteCode": "US",
            "t": 1663229253518
        }
    },
    "get_warehouse_info": {
        "uri_path": "/ec-oms-api/base/actual/getWarehouseList",
        "method": "get",
        "data": {}
    },
    "create_sale_order": {
        "uri_path": "/ec-oms-api/salesorder/addSalesOrder",
        "method": "post",
        "data": {
            "orderType": 1,
            "shipType": 2,
            "reissueReasonList": [],
            "responsiblePartyList": [],
            "relateSalesOrderNo": "",
            "platformCode": "HOMARY",
            "storeCode": "HOMARY",
            "siteCode": "US",
            "buyerId": "1",
            "firstName": "hongwei",
            "lastName": "xu", "mobilePhone": "12345678",
            "email": "1@1.com",
            "country": "US",
            "province": "NY",
            "city": "New York",
            "postalCode": "10001",
            "company": "popicorns",
            "address1": "address 1",
            "address2": "address 2",
            "locationType": "Business with Dock",
            "deliveryTimeStart": "01:30",
            "deliveryTimeEnd": "01:30",
            "currencyPrice": 123,
            "discountAmount": 111,
            "deliveryFee": 12,
            "currency": "USD",
            "items": [
                {
                    "productNameCn": "LI-测试商品9",
                    "type": 1,
                    "typeName": "销售sku",
                    "relateSku": "",
                    "categoryName": "家具>家具套装>餐桌桌椅套装",
                    "mainUrl": "",
                    "mostBomVersion": None,
                    "skuTotalQty": None,
                    "expressType": None,
                    "deliveryType": "",
                    "deliveryExpressValue": None,
                    "deliveryExpressName": None,
                    "itemSkuCode": "JJH3C94287",
                    "itemQty": 1,
                    "itemCurrencyPrice": 888,
                    "originDeliveryInfo": {},
                    "logisticsValue": None,
                    "mallLabelList": [],
                    "bomVersion": "",
                    "warehouseCode": "",

                }
            ],
            "salesOrderRemarks": "",
            "countryName": "United States",
            "provinceName": "New York",
            "storeName": "HOMARY",
            "platformName": "HOMARY"
        }
    },
    "query_oms_order": {
        "uri_path": "/ec-oms-api/order/page",
        "method": "post",
        "data": {"current": 1, "size": 10, "sortKey": "follow_time", "direction": 1, "orderNos": "",
                 "salesOrderNos": "SO2209200051", "salesOutNos": "", "siteCodes": "", "buyerId": "",
                 "provinceName": "",
                 "city": "", "postalCodes": "", "email": "", "itemSkuCodes": "", "skuLike": "",
                 "relateOrderNos": [],
                 "createUsername": "", "relateSalesOrderNos": "", "orderSources": [], "address": "",
                 "buyerName": "",
                 "salesOrderRemarks": "", "remark": "", "logisticsInfo": "", "visualWarehouseCodes": [],
                 "actualWarehouseCodes": [], "orderQtyType": [], "laborType": [], "orderStatus": [],
                 "salesOutStatus": [], "platforms": [], "stores": [], "countryCodes": [], "excludeCountryCodes": [],
                 "deliveryType": "", "isLabor": "", "urgentStatus": "", "orderDeliveryType": [], "orderTypes": [],
                 "interceptStatusList": [], "interceptTypes": [], "mallLabelList": [], "payTimeStart": "",
                 "payTimeEnd": "", "createTimeStart": "", "createTimeEnd": "", "deliveryTimeStart": "",
                 "deliveryTimeEnd": ""}

    },
    "dispatch_oms_order": {
        "uri_path": "/auto/verification/execute",
        "method": "post",
        "data": []
    },
    "query_oms_order_detail": {
        "uri_path": "/ec-oms-api/order/getOrder/%s",
        "method": "get",
        "data": []
    },
    "query_oms_order_sku_items": {
        "uri_path": "/ec-oms-api/order/getOrder/item/%s",
        "method": "get",
        "data": []
    },
    "push_order_to_wms": {
        "uri_path": "/order/issue",
        "method": "post",
        "data": ""
    },
    "oms_order_follow": {
        "uri_path": "/order/follow",
        "method": "post",
        "data": [{"skuCode": "demoData", "bomVersion": "demoData"}]
    },
    "query_common_warehouse": {
        "uri_path": "/ec-oms-api/virtual/warehouse/page",
        "method": "post",
        "data": {"virtualWarehouseCodes": [], "warehouseCodes": [], "current": 1, "size": 10}
    },
}
