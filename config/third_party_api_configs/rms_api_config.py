from config.third_party_api_configs import ApiConfig


class RMSApiConfig:

    class TransferPlanAdd(ApiConfig):
        uri_path = "/api/ec-rms-api/rms/api/transfer/plan/add"
        method = "POST"
        data = {
            "deliveryWarehouseId": "",
            "deliveryWarehouseName": "",
            "deliveryWarehouseCode": "",
            "receiveWarehouseId": "",
            "receiveWarehouseName": "",
            "receiveWarehouseCode": "",
            "remark": "",
            "details": [

            ]
        }
