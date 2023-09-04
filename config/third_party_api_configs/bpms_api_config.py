from config.third_party_api_configs import ApiConfig


class ProductInfo:

    class PlatProductPage(ApiConfig):

        uri_path = "/api/ec-bpms-api/bpms-platform-product/getPage"
        method = "POST"
        data = {
            "param":
                {
                    "storeSkuCodeList": [],
                    "productSkuCodeList": [],
                    "fnSkuCodeList": []
                },
            "pageNo": 1
        }
