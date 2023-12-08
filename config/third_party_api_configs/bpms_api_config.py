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

    class SaleSkuPage(ApiConfig):
        uri_path = "/api/ec-bpms-api/sale/sku/getByPage"
        method = "POST"
        data = {
            "param":
                {
                    "skuCodeList": [],
                    "spuCodeList": [],
                    "ids": [],
                    "exportImage": 2,
                    "exportType": 2
                },
            "pageNo": 1
        }
