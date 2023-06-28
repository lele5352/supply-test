from config.third_party_api_configs import ApiConfig


class SeaCabinetApiConfig:
    class GetCabinetOrder(ApiConfig):
        uri_path = "/api/ec-cds-api/sea/cabinet/order/page"
        method = "POST"
        data = {
            "seaCabinetOrderNoList": [],
            "cabinetNoList": [],
            "vesselBookingNoList": [],
            "handOverNoList": [],
            "statusList": [],
            "deliveryWarehouseIdList": [],
            "receiveWarehouseIdList": [],
            "salesSkuCodeList": [],
            "salesSkuName": "",
            "createUserIdList": [],
            "createTimeStart": "",
            "createTimeEnd": "",
            "confirmUserIdList": [],
            "confirmTimeStart": "",
            "confirmTimeEnd": "",
            "pageNumber": 1, "pageSize": 10,
            "sortInfoList": [{"sortField": "", "sortType": ""}]
        }

    class CabinetOrderDetail(ApiConfig):
        uri_path = "/api/ec-cds-api/sea/cabinet/order/detail?id={0}&t={1}"
        method = "GET"

    class ConfirmCabinetOrder(ApiConfig):
        uri_path = "/api/ec-cds-api/sea/cabinet/order/confirm?id={0}&t={1}"
        method = "GET"

    class CabinetOrderSkuDetail(ApiConfig):
        uri_path = "/api/ec-cds-api/sea/cabinet/order/out/sku/page"
        method = "POST"
        data = {"pageNumber": 1, "pageSize": 10, "seaCabinetOrderId": "1673888517525508097"}

    class DownloadCabinetOrder(ApiConfig):
        uri_path = "/api/ec-cds-api/sea/cabinet/order/export"
        method = "POST"
        data = {
            "seaCabinetOrderNoList": [],
            "cabinetNoList": [],
            "vesselBookingNoList": [],
            "handOverNoList": [],
            "statusList": [],
            "deliveryWarehouseIdList": [],
            "receiveWarehouseIdList": [],
            "salesSkuCodeList": [],
            "salesSkuName": "",
            "createUserIdList": [],
            "createTimeStart": "",
            "createTimeEnd": "",
            "confirmUserIdList": [],
            "confirmTimeStart": "",
            "confirmTimeEnd": "",
            "pageNumber": 1, "pageSize": 10,
            "sortInfoList": [{"sortField": "", "sortType": ""}]
        }

    class EditCabinetOrder(ApiConfig):
        uri_path = "/api/ec-cds-api/sea/cabinet/order/edit"
        method = "POST"
        data = {
            "operateType": 2,
            "seaCabinetOrderId": "1673940362239315970",
            "seaCabinetGoodsEditDTOList": [
                {"drawbackType": 0, "seaCabinetGoodsId": "1673940494343114753"},
                {"drawbackType": 1, "seaCabinetGoodsId": "1673940494368280577"},
                {"drawbackType": 1, "seaCabinetGoodsId": "1673940494376669186"},
                {"drawbackType": 1, "seaCabinetGoodsId": "1673940494389252098"},
                {"drawbackType": 0, "seaCabinetGoodsId": "1673940494397640706"},
                {"drawbackType": 0, "seaCabinetGoodsId": "1673940494406029313"}
            ]
        }


class DeclarationApiConfig:
    class GetDeclaration(ApiConfig):
        uri_path = "/api/ec-cds-api/cds/api/customs/declaration/page"
        method = "POST"
        data = {
            "systemDeclarationOrderNos": [],
            "containerNos": [],
            "customsDeclarationOrderNos": [],
            "drawbackType": "",
            "declarationStatusList": [],
            "salesContractNos": [],
            "exportInvoiceNos": [],
            "purchaseInvoiceNos": [],
            "taxRefundNos": [],
            "vesselBookingNos": [],
            "createUserId": "",
            "createTimeStart": "",
            "createTimeEnd": "",
            "finishTimeStart": "",
            "finishTimeEnd": "",
            "pageNumber": 1, "pageSize": 10,
            "sortInfo": {"sortField": "", "sortType": ""}
        }

    class BindDeclarationNo(ApiConfig):
        uri_path = "/api/ec-cds-api/cds/api/customs/declaration/update/declaration/no"
        method = "POST"
        data = {
            "customsDeclarationId": "1673943899228770306",
            "customsDeclarationOrderNo": "TEST123"
        }

    class DeclarationDetail(ApiConfig):
        uri_path = "/api/ec-cds-api/cds/api/customs/declaration/{0}?t={1}"
        method = "GET"


class InvoiceApiConfig:
    class GetInvoice(ApiConfig):
        uri_path = "/api/ec-cds-api/cds/api/invoice/detail/page"
        method = "POST"
        data = {
            "containerNos": [],
            "taxRefundNos": [],
            "vesselBookingNos": [],
            "salesContractNos": [],
            "exportInvoiceNos": [],
            "purchaseInvoiceNos": [],
            "systemDeclarationOrderNos": [],
            "customsDeclarationOrderNos": [],
            "declarationStatus": "1",
            "exportInvoiceStatus": None,
            "taxRefundStatusList": [],
            "purchaseInvoiceStatusList": [],
            "createTimeEnd": "",
            "createTimeStart": "",
            "createUserId": None,
            "supplierId": None,
            "detailIds": [],
            "pageNumber": 1, "pageSize": 10,
            "sortInfo": {"sortField": "", "sortType": ""}
        }

    class DownloadExportInvoice(ApiConfig):
        uri_path = '/api/ec-cds-api/cds/api/invoice/detail/export/invoice'
        method = "POST"
        data = {}

    class DownloadPurchaseInvoice(ApiConfig):
        uri_path = '/api/ec-cds-api/cds/api/invoice/detail/export/purchase/invoice'
        method = "POST"
        data = {}

    class DownloadInvoice(ApiConfig):
        uri_path = '/api/ec-cds-api/cds/api/invoice/detail/export'
        method = "POST"
        data = {
            "containerNos": [],
            "taxRefundNos": [],
            "vesselBookingNos": [],
            "salesContractNos": [],
            "exportInvoiceNos": [],
            "purchaseInvoiceNos": [],
            "systemDeclarationOrderNos": [],
            "customsDeclarationOrderNos": [],
            "declarationStatus": "1",
            "exportInvoiceStatus": None,
            "taxRefundStatusList": [],
            "purchaseInvoiceStatusList": [],
            "createTimeEnd": "",
            "createTimeStart": "",
            "createUserId": None,
            "supplierId": None,
            "detailIds": [],
            "pageNumber": 1, "pageSize": 10,
            "sortInfo": {"sortField": "", "sortType": ""}
        }


class GoodsApiConfig:
    class GetGoods(ApiConfig):
        uri_path = "/api/ec-cds-api/goods/declaration/info/page"
        method = "POST"
        data = {
            "pageNumber": 1, "pageSize": 150,
            "salesSkuCodeList": [],
            "salesSkuName": "",
            "customsCodeList": [],
            "inspectionFlag": "",
            "sortInfoList": [{"sortField": "", "sortType": ""}]
        }

    class AddGood(ApiConfig):
        uri_path = "/api/ec-cds-api/goods/declaration/info/add"
        method = "POST"
        data = {
            "salesSkuCode": "P31559628",
            "customsCode": "1000000000",
            "salesSkuName": "TS零部件测试非退税",
            "customsName": "自动化脚本生成",
            "declarationInfo": "自动化脚本生成",
            "unit": "1",
            "inspectionFlag": "1"
        }


class TaxationApiConfig:
    class GetTaxation(ApiConfig):
        uri_path = "/api/ec-cds-api/taxation/info/page"
        method = "POST"
        data = {
            "pageNumber": 1, "pageSize": 150,
            "salesSkuCodes": [],
            "salesSkuNameLike": "",
            "taxationCodes": [],
            "taxationNameLike": "",
            "sortInfoList": [{"sortField": "", "sortType": ""}]
        }

    class AddTaxation(ApiConfig):
        uri_path = "/api/ec-cds-api/taxation/info/add"
        method = "POST"
        data = {
            "salesSkuCode": "P31559628",
            "taxationCode": "1000000000000000000",
            "salesSkuName": "TS零部件测试非退税",
            "taxationName": "*automatictest*",
            "taxationDesc": "自动化脚本生成",
            "specification": "1*1*1"
        }
