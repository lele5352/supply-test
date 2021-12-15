scm_api_config = {
    "get_product_info": {
        "uri_path": "/api/ec-scm-api/scm/common/getProductPage",
        "method": "post",
        "data": {
            "pageNumber": 1,
            "pageSize": 10,
            "total": 25225,
            "skuCode": "P52652725"
        }
    },
    "stock_plan_submit": {
        "uri_path": "/api/ec-scm-api/scm/stockPlan/submit",
        "method": "post",
        "data": {
            "baseInfo": {
                "destinationWarehouse": "USLA01",
                "deliveryWarehouse": "FSZZ02"
            },
            "productInfos": []
        }
    },
    "stock_plan_batch_audit": {
        "uri_path": "/api/ec-scm-api/scm/stockPlan/batchAudit",
        "method": "put",
        "data": {
            "ids": ["1469197356305092610"],
            "isPass": True,
            "remarks": "自动化脚本审核通过！"
        }
    },

    "get_purchase_demand_page": {
        "uri_path": "/api/ec-scm-api/scm/purchaseDemand/page",
        "method": "post",
        "data": {
            "pageNumber": 1,
            "pageSize": 10,
            "total": 100,
            "status": "",
            "destinationWarehouse": [],
            "deliveryWarehouse": [],
            "productType": -1,
            "purchaseType": -1,
            "tracerId": "",
            "orderNos": []
        }
    },
    "get_purchase_demand_detail": {
        "uri_path": "/api/ec-scm-api/scm/purchaseDemand/getDetail/",
        "method": "get",
        "data": ""
    },
    "batch_get_purchase_demand_detail": {
        "uri_path": "/api/ec-scm-api/scm/purchaseDemand/getBatchDetail",
        "method": "post",
        "data": ""
    },
    "confirm_and_generate_purchase_order": {
        "uri_path": "/api/ec-scm-api/scm/purchaseDemand/confirmAndGeneratePurchaseOrder",
        "method": "put",
        "data": []
    },
    "get_purchase_order_detail": {
        "uri_path": "/api/ec-scm-api/scm/purchaseOrder/getAllDetail/%s",
        "method": "get",
        "data": ""
    },
    "get_purchase_order_page": {
        "uri_path": "/api/ec-scm-api/scm/purchaseOrder/page",
        "method": "post",
        "data": {
            "pageNumber": 1,
            "pageSize": 10,
            "total": 100,
            "status": "",
            "destinationWarehouse": "",
            "deliveryWarehouse": "",
            "qualityInspectionType": -1,
            "arrivalStatus": [-1],
            "payStatus": [-1],
            "dispatchStatus": [-1],
            "supplierAcceptStatus": -1,
            "tracerId": "",
            "isExportImage": True,
            "stockOrderNos": []
        }
    },
    "purchase_order_update": {
        "uri_path": "/api/ec-scm-api/scm/purchaseOrder/update",
        "method": "put",
        "data": ""
    },
    "purchase_order_batch_audit": {
        "uri_path": "/api/ec-scm-api/scm/purchaseOrder/batchAudit",
        "method": "put",
        "data": {
            "ids": ["1469197356305092610"],
            "isPass": True,
            "remarks": "自动化脚本审核通过！"
        }
    },
    "purchase_order_batch_buy": {
        "uri_path": "/api/ec-scm-api/scm/purchaseOrder/batchBuy",
        "method": "put",
        "data": ["1469197356305092610"]
    },
    "get_purchase_order_delivery_detail": {
        "uri_path": "/api/ec-scm-api/scm/purchaseOrder/getDeliveryDetailPage",
        "method": "post",
        "data": {
            "ids": [],
            "pageNumber": 1,
            "pageSize": 10,
            "total": 0
        }
    },
    "generate_distribute_order": {
        "uri_path": "/api/ec-scm-api/scm/purchaseOrder/generateDistributeOrder",
        "method": "post",
        "data": []
    },
    "purchase_order_delivery": {
        "uri_path": "/api/ec-scm-api/scm/purchaseOrder/distributeOrderSubmit",
        "method": "post",
        "data": {}
    },
    "get_distribute_order_page": {
        "uri_path": "/api/ec-scm-api/scm/api/shipping-order/page",
        "method": "post",
        "data": {
            "pageNumber": 1,
            "pageSize": 10,
            "total": 100,
            "arrivedStatus": -1,
            "deliveryWarehouse": "",
            "destinationWarehouse": "",
            "marketSku": [],
            "orderNo": "",
            "purchaseOrderNos": [],
            "qualityTestType": -1,
            "shippingOrderStatus": -1,
            "supplierName": "",
            "tracerId": "",
            "expectTime": "",
            "shippingOrders": [],
            "merchandiser": ""
        }
    }
}
