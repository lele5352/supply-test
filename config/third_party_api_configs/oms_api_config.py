from config.third_party_api_configs import ApiConfig


class OMSApiConfig:
    class GetFollowOrderPage(ApiConfig):
        uri_path = "/api/ec-oms-api/order/trackOrder/page"
        method = "POST"
        data = {"current": 1, "size": 10, "sortKey": "follow_time", "direction": 1, "itemSkuCode": "",
                "salesOrderNo": "",
                "orderNo": "", "siteCode": "", "buyerName": "", "platformCodeList": [], "deliveryWarehouseCode": [],
                "country": [], "excludeCountry": [], "relateSalesOrderNos": "", "intercept": "",
                "interceptTypeList": [],
                "followOrderTypeList": [], "buyerId": "", "followTimeStart": "", "followTimeEnd": "",
                "payTimeStart": "",
                "payTimeEnd": ""}

    class GetProductInfo(ApiConfig):
        uri_path = "/api/ec-oms-api/salesorder/listProduct"
        method = "GET"
        data = {
            "current": 1,
            "size": 10,
            "type": 1,
            "skuCode": "JJH3C94287",
            "productNameCn": "",
            "siteCode": "US",
            "t": 1663229253518
        }


oms_api_config = {
    "get_warehouse_info": {
        "uri_path": "/ec-oms-api/base/actual/getWarehouseList",
        "method": "GET",
        "data": {}
    },
    "create_sale_order": {
        "uri_path": "/ec-oms-api/salesorder/addSalesOrder",
        "method": "POST",
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
        "method": "POST",
        "data": {"current": 1, "size": 150, "sortKey": "follow_time", "direction": 1, "orderNos": "",
                 "salesOrderNos": "", "salesOutNos": "", "siteCodes": "", "buyerId": "",
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
        "method": "POST",
        "data": []
    },
    "query_oms_order_detail": {
        "uri_path": "/ec-oms-api/order/getOrder/%s",
        "method": "GET",
        "data": []
    },
    "query_oms_order_sku_items": {
        "uri_path": "/ec-oms-api/order/getOrder/item/%s",
        "method": "GET",
        "data": []
    },
    "push_order_to_wms": {
        "uri_path": "/order/issue",
        "method": "POST",
        "data": {
            "orderNos": ['OMS2402270001']
        }
    },
    "oms_order_follow": {
        "uri_path": "/order/follow",
        "method": "POST",
        "data": [{"skuCode": "demoData", "bomVersion": "demoData"}]
    },
    "query_common_warehouse": {
        "uri_path": "/ec-oms-api/virtual/warehouse/page",
        "method": "POST",
        "data": {"virtualWarehouseCodes": [], "warehouseCodes": [], "current": 1, "size": 10}
    },
    "product_detail": {
        "uri_path": "ec-oms-api/order/productDetail?skuCode=%s&siteCode=%s&country=%s&postalCode=%s",
        "method": "GET"
    },
    "warehouse_allocation_rule": {
        "uri_path": "/ec-oms-api/warehouseAllocationRule/getByPage",
        "method": "POST",
        "data": {"countryCode": ["US"], "postCodes": ["10001"], "logisticsType": [3], "status": 1,
                 "orderByUpdateTime": 2, "current": 1, "size": 10}
    },
    "check_lock": {
        "uri_path": '/api/ec-oms-api/order/checkLock',
        "method": "POST",
        "data": [57284]
    },
    "release_lock": {
        "uri_path": '/api/ec-oms-api/order/releaseLock',
        "method": "POST",
        "data": [57284]
    },
    "apply_modify": {
        "uri_path": '/api/ec-oms-api/order/apply/modify/%s?t=%s',
        "method": "GET"
    },
    "update_buyer": {
        "uri_path": "/ec-oms-api/order/updateBuyer",
        "method": "POST",
        "data": {
            "orderId": 57032, "buyerId": "1", "firstName": "hongwei", "lastName": "xu", "mobilePhone": "12345678",
            "email": "1@1.com", "country": "US", "countryName": "United States", "province": "NY",
            "provinceName": "New York", "city": "New York", "postalCode": "10001", "company": "popicorns",
            "address1": "address 1", "address2": "address 2", "locationType": "Business with Dock",
            "deliveryTimeStart": "01:30", "deliveryTimeEnd": "01:30", "refreshFollowTimeFlag": 0, "details": [
                {"orderItemExtId": "201387", "cancelQty": 10, "itemSkuCode": "KK5340V73Y", "bomVersion": "A",
                 "warehouseCode": None, "warehouseId": None, "warehouseName": None}]}
    },
    "labor_update": {
        "uri_path": 'ec-oms-api/labor/updateOrder',
        "method": "POST",
        "data": {"orderId": 64122, "buyerId": "1", "firstName": "hongwei", "lastName": "xu", "mobilePhone": "12345678",
                 "email": "oms_auto@test.com", "country": "US", "countryName": "United States", "province": "NE",
                 "provinceName": "Nebraska", "city": "TEST DATA", "postalCode": "OMSTEST", "company": "popicorns",
                 "address1": "address 1", "address2": "address 2", "locationType": "Business with Dock",
                 "deliveryTimeStart": "01:30", "deliveryTimeEnd": "01:30", "details": [
                {"orderItemExtId": "221189", "cancelQty": 1, "itemSkuCode": "HWY169W884", "bomVersion": None,
                 "warehouseCode": "WHFH01", "warehouseId": None, "warehouseName": None}]}
    },
    "order_follow_trace_page": {
        "uri_path": "/api/ec-oms-api/orderFollowTrace/page",
        "method": "POST",
        'data': {"current": 1, "size": 10, "sortKey": "pay_time", "direction": 0, "salesOrderNoList": [],
                 "itemSkuCodeList": [], "actOverdueStart": "", "actOverdueEnd": "", "expectedOverdueStart": "",
                 "expectedOverdueEnd": "", "preemptTypeList": [], "deliveryState": "", "payTimeStart": "",
                 "payTimeEnd": "", "productEtaStart": "", "productEtaEnd": "", "orderTypeList": [],
                 "expectedDeliveryEtaStart": "", "expectedDeliveryEtaEnd": "", "actDeliveryEtaStart": "",
                 "actDeliveryEtaEnd": ""}
    },
    "order_follow_trace_detail": {
        "uri_path": "/api/ec-oms-api/orderFollowTrace/detailPage",
        "method": "POST",
        'data': {"current": 1, "size": 10, "id": "1764554437103153156"}

    },
    "order_invalid_page": {
        "uri_path": "/api/ec-oms-api/order/invalid/page",
        "method": "POST",
        'data': {"current": 1, "size": 10, "orderNos": "", "salesOrderNos": "",
                 "salesOutNos": "", "invalidTimeStart": "", "invalidTimeEnd": ""}
    },
    "get_province_list": {
        "uri_path": "/api/ec-oms-api/base/getProvinceList/%s?t=%d",
        "method": "GET"
    },
    "eta_warehouse_rule_page": {
        "uri_path": "/api/ec-oms-api/eta-warehouse-rule/page",
        "method": "POST",
        'data': {"warehouseRuleStatus": 1, "warehouseCode": "", "warehouseType": "", "updateTimeEnd": "",
                 "updateTimeStart": "", "updateTime": "", "current": 1, "size": 150, "total": 0}
    },
    "eta_warehouse_rule_info": {
        "uri_path": "/api/ec-oms-api/eta-warehouse-rule/info",
        "method": "POST",
        'data': {"current": 1, "size": 10, "total": 0, "id": "1"}
    },
    "get_shipping_eta_rule": {
        "uri_path": "/api/ec-oms-api/eta-shipping-rule/info",
        "method": "POST"
    },
    "salesorder_item_detail": {
        "uri_path": "/api/ec-oms-api/salesorder/item/detail/%s?t=%d",
        "method": "GET"
    },
    'get_order_item': {
        'uri_path': '/api/ec-oms-api/order/getOrder/item/%d?t=%d',
        "method": "GET"
    },

}
