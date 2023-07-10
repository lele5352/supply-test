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

    class GetDistributeOrderDetail(ApiConfig):
        uri_path = "/api/ec-scm-api/scm/api/shipping-order/detail"
        method = "POST"
        data = {"id": "1637737878908071938", "pageNumber": 1, "pageSize": 10}


class SupplierApiConfig:
    class GetSupplier(ApiConfig):
        uri_path = "/api/ec-scm-api/scm/supplierInfo/page"
        method = "POST"
        data = {
            "auditId": "", "auditTimeEnd": "", "auditTimeStart": "", "createId": "", "createTimeEnd": "",
            "createTimeStart": "", "isOpenSupplierPortalSystem": None, "mainCategoryIds": [], "merchandiserId": "",
            "payType": -1, "purchaseMethod": None, "purchaserId": "", "status": 2, "supplierCode": "",
            "supplierDeveloperId": "", "supplierLevel": None, "supplierId": "", "supplierType": None,
            "updateId": "", "updateTimeEnd": "", "updateTimeStart": "", "pageNumber": 1, "pageSize": 50,
            "drawbackType": None, "createTime": [], "updateTime": [], "auditTime": []}

    class GetProduct(ApiConfig):
        uri_path = "/api/ec-scm-api/scm/supplierProduct/page"
        method = "POST"
        data = {
            "status": -1,
            "skuCode": "",
            "supplierId": "",
            "defaultSupplier": None,
            "supplierCode": "",
            "spuCodes": [],
            "productName": "",
            "supplierNum": "",
            "createId": "",
            "createName": "",
            "createTimeStart": "",
            "createTimeEnd": "",
            "productLabel": "",
            "auditId": "",
            "auditName": "",
            "auditTimeStart": "",
            "auditTimeEnd": "",
            "updateId": "",
            "updateName": "",
            "updateTimeStart": "",
            "updateTimeEnd": "",
            "productType": "",
            "pageNumber": 1, "pageSize": 50
        }

    class GetProductDetail(ApiConfig):
        uri_path = "/api/ec-scm-api/scm/supplierProduct/getDetail/{0}"
        method = "GET"

    class AddProduct(ApiConfig):
        uri_path = "/api/ec-scm-api/scm/supplierProduct/add"
        method = "POST"
        data = {
            "defaultPackingProgram": "B1",
            "skuCode": "HWK3S14200",
            "purchaseMethodText": "线上",
            "isDefaultSupplier": False,
            "minOrderQuantity": "1",
            "packageId": "34866",
            "productDetail": {
                "productImageUrl": "https://img.popicorns.com/dev/file/2023/06/27/d76e4266d5854fc5b29a549fec3e082c.jpg",
                "productName": "测试多品多件",
                "productTagId": None,
                "productTagName": None,
                "productTypeId": 1,
                "productType": "成品",
                "skuCode": "HWK3S14200",
                "skuId": "35553"
            },
            "purchaseDeliveryDate": "1",
            "purchaseMethod": 0,
            "purchasePrices": [
                {
                    "moq": 1,
                    "noTaxPurchasePrice": 1,
                    "disabled": True,
                    "id": -1
                }
            ],
            "shopRemarks": "",
            "shopUrl": "ttt.com",
            "supplierId": "1460085434343362561",
            "supplierName": "coco测试",
            "supplierNo": "",
            "taxPoint": 0,
            "packageVersion": "B1",
            "packageDetail": "[{\"detailName\":\"package1\",\"height\":8,\"length\":10,\"num\":1,\"packageSku\":\"B23882865\",\"packageSkuNameCn\":\"package1\",\"packageVersion\":\"B1\",\"volumeDec\":\"10*1*8\",\"weight\":8,\"width\":1},{\"detailName\":\"package0\",\"height\":5,\"length\":7,\"num\":1,\"packageSku\":\"B32287338\",\"packageSkuNameCn\":\"package0\",\"packageVersion\":\"B1\",\"volumeDec\":\"7*3*5\",\"weight\":5,\"width\":3},{\"detailName\":\"package2\",\"height\":1,\"length\":8,\"num\":1,\"packageSku\":\"B71636452\",\"packageSkuNameCn\":\"package2\",\"packageVersion\":\"B1\",\"volumeDec\":\"8*9*1\",\"weight\":9,\"width\":9}]"
        }

    class AuditSupplierProduct(ApiConfig):
        uri_path = "/api/ec-scm-api/scm/supplierProduct/batchAudit"
        method = "PUT"
        data = {"ids": ["1674344833304735746"], "isPass": True, "remarks": ""}
