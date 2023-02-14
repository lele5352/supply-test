from config.third_party_api_configs import ApiConfig


class SCMApiConfig:
    class GetProductInfo(ApiConfig):
        uri_path = "/api/ec-scm-api/scm/common/getProductPage"
        method = "POST"
        data = {
            "pageNumber": 1,
            "pageSize": 10,
            "total": 25225,
            "skuCode": "P52652725"
        }

    class ShortageDemandBatchConfirm(ApiConfig):
        uri_path = "/api/ec-scm-api/scm/lackDemand/batchConfirm"
        method = "PUT"
        data = ["1465875421462663183"]

    class StockPlanSubmit(ApiConfig):
        uri_path = "/api/ec-scm-api/scm/stockPlan/submit"
        method = "POST"
        data = {
            "baseInfo": {
                "destinationWarehouse": "USLA01",
                "deliveryWarehouse": "FSZZ02"
            },
            "productInfos": []
        }

    class StockPlanAudit(ApiConfig):
        uri_path = "/api/ec-scm-api/scm/stockPlan/batchAudit"
        method = "PUT"
        data = {
            "ids": ["1469197356305092610"],
            "isPass": True,
            "remarks": "自动化脚本审核通过！"
        }

    class GetPurchaseDemandPage(ApiConfig):
        uri_path = "/api/ec-scm-api/scm/purchaseDemand/page"
        method = "POST"
        data = {
            "pageNumber": 1,
            "pageSize": 50,
            "total": 100,
            "status": "",
            "destinationWarehouse": [],
            "deliveryWarehouse": [],
            "productType": -1,
            "purchaseType": -1,
            "tracerId": "",
            "orderNos": []
        }

    class GetPurchaseDemandDetail(ApiConfig):
        uri_path = "/api/ec-scm-api/scm/purchaseDemand/getDetail/"
        method = "GET"
        data = ""

    class BatchGetPurchaseDemandDetail(ApiConfig):
        uri_path = "/api/ec-scm-api/scm/purchaseDemand/getBatchDetail"
        method = "POST"
        data = ""

    class ConfirmAndGeneratePurchaseOrder(ApiConfig):
        uri_path = "/api/ec-scm-api/scm/purchaseDemand/confirmAndGeneratePurchaseOrder"
        method = "PUT"
        data = []

    class GetPurchaseOrderDetail(ApiConfig):
        uri_path = "/api/ec-scm-api/scm/purchaseOrder/getAllDetail/%s"
        method = "GET"
        data = ""

    class GetPurchaseOrderPage(ApiConfig):
        uri_path = "/api/ec-scm-api/scm/purchaseOrder/page"
        method = "POST"
        data = {"pageNumber": 1, "pageSize": 10, "total": 1, "status": [], "destinationWarehouse": "",
                "deliveryWarehouse": "", "qualityInspectionType": -1, "arrivalStatus": [-1], "payStatus": [-1],
                "dispatchStatus": [-1], "supplierAcceptStatus": -1, "tracerId": "", "field": None, "type": None,
                "isExportImage": True, "isFirstOrder": None, "purchaseOrderNos": [], "stockOrderNos": []}

    class PurchaseOrderUpdate(ApiConfig):
        uri_path = "/api/ec-scm-api/scm/purchaseOrder/update"
        method = "PUT"
        data = ""

    class PurchaseOrderBatchAudit(ApiConfig):
        uri_path = "/api/ec-scm-api/scm/purchaseOrder/batchAudit"
        method = "PUT"
        data = {
            "ids": ["1469197356305092610"],
            "isPass": True,
            "remarks": "自动化脚本审核通过！"
        }

    class PurchaseOrderBatchBuy(ApiConfig):
        uri_path = "/api/ec-scm-api/scm/purchaseOrder/batchBuy"
        method = "PUT"
        data = ["1469197356305092610"]

    class GetPurchaseOrderDeliveryDetail(ApiConfig):
        uri_path = "/api/ec-scm-api/scm/purchaseOrder/getDeliveryDetailPage"
        method = "POST"
        data = {
            "ids": [],
            "pageNumber": 1,
            "pageSize": 10,
            "total": 0
        }

    class GenerateDistributeOrder(ApiConfig):
        uri_path = "/api/ec-scm-api/scm/purchaseOrder/generateDistributeOrder"
        method = "POST"
        data = []

    class PurchaseOrderDelivery(ApiConfig):
        uri_path = "/api/ec-scm-api/scm/purchaseOrder/distributeOrderSubmit"
        method = "POST"
        data = {}

    class GetDistributeOrderPage(ApiConfig):
        uri_path = "/api/ec-scm-api/scm/api/shipping-order/page"
        method = "POST"
        data = {
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
