from config.third_party_api_configs import ApiConfig


class SeaCabinetApiConfig:
    class GetCabinetOrder(ApiConfig):
        uri_path = "/api/ec-cds-api/sea/cabinet/order/page"
        method = "POST"
        data = {"pageNumber": 1, "pageSize": 10, "seaCabinetOrderNoList": [], "cabinetNoList": [],
                "vesselBookingNoList": [], "handOverNoList": [], "statusList": [], "deliveryWarehouseIdList": [],
                "receiveWarehouseIdList": [], "salesSkuCodeList": [], "salesSkuName": "", "createUserIdList": [],
                "createTimeStart": "", "createTimeEnd": "", "confirmUserIdList": [], "confirmTimeStart": "",
                "confirmTimeEnd": "", "sortInfoList": [{"sortField": "", "sortType": ""}]}

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
        data = {"pageNumber": 1, "pageSize": 10, "seaCabinetOrderNoList": [], "cabinetNoList": [],
                "vesselBookingNoList": [], "handOverNoList": [], "statusList": [], "deliveryWarehouseIdList": [],
                "receiveWarehouseIdList": [], "salesSkuCodeList": [], "salesSkuName": "", "createUserIdList": [],
                "createTimeStart": "", "createTimeEnd": "", "confirmUserIdList": [], "confirmTimeStart": "",
                "confirmTimeEnd": "", "sortInfoList": [{"sortField": "", "sortType": ""}]}

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
