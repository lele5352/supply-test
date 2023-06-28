from config.third_party_api_configs import ApiConfig


class BaseApiConfig:
    class GetCabinetOrder(ApiConfig):
        uri_path = "/api/ec-cds-api/sea/cabinet/order/page"
        method = "POST"
        data = {"pageNumber": 1, "pageSize": 10, "seaCabinetOrderNoList": [], "cabinetNoList": [],
                "vesselBookingNoList": [], "handOverNoList": [], "statusList": [], "deliveryWarehouseIdList": [],
                "receiveWarehouseIdList": [], "salesSkuCodeList": [], "salesSkuName": "", "createUserIdList": [],
                "createTimeStart": "", "createTimeEnd": "", "confirmUserIdList": [], "confirmTimeStart": "",
                "confirmTimeEnd": "", "sortInfoList": [{"sortField": "", "sortType": ""}]}

    class CabinetOrderSkuDetail(ApiConfig):
        uri_path = "/api/ec-cds-api/sea/cabinet/order/out/sku/page"
        method = "POST"
        data = {"pageNumber": 1, "pageSize": 10, "seaCabinetOrderId": "1673888517525508097"}

    class CabinetOrderDetail(ApiConfig):
        uri_path = "/api/ec-cds-api/sea/cabinet/order/detail?id={0}&t={1}"
        method = "GET"
