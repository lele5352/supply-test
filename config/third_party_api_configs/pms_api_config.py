from config.third_party_api_configs import ApiConfig


class BaseApiConfig:
    class AddProduct(ApiConfig):
        uri_path = "/api/ec-pms/pmsspu/product/add"
        method = "POST"
        data = {
            "mainImg": "https://img.popicorns.com/dev/file/2023/06/27/d76e4266d5854fc5b29a549fec3e082c.jpg",
            "productName": "test_product_automatic",
            "productNameEn": "",
            "brandId": 51,
            "categoryId": 7877,
            "skuList": [
                {
                    "selectProductFlag": 2,
                    "attrCombinedName": "one",
                    "height": "",
                    "length": "",
                    "link": "",
                    "netRemark": "",
                    "sku": "",
                    "relateSkuInfoList": [],
                    "suitPackageInfoList": [
                        {
                            "length": "",
                            "width": "",
                            "height": "",
                            "weight": "",
                            "packageName": "",
                            "packageNum": ""
                        }
                    ],
                    "supplierInfo": {
                        "supplier": "",
                        "supplierEta": "7",
                        "link": "",
                        "netRemark": "",
                        "purchasePrice": 0,
                        "supplierId": ""
                    },
                    "packageInfoList": [
                        {
                            "height": "1",
                            "length": "1",
                            "weight": "1",
                            "width": "1",
                            "packageName": "1",
                            "packageNum": "1"
                        }
                    ],
                    "skuLabelParams": [],
                    "purchasePrice": "1",
                    "productArchiveUrl": "",
                    "supplierEta": 1,
                    "uploadManual": 0,
                    "selectFlag": 1,
                    "skuAttrMapList": [
                        {
                            "attrDetailType": 1,
                            "attrId": 979,
                            "usaAttrValue": "one",
                            "attrDetailId": 16736
                        }
                    ],
                    "supplierId": "1673510057924988930",
                    "weight": "",
                    "width": "",
                    "supplier": "Vincent",
                    "skuLabelVos": []
                }
            ],
            "isSuit": 0,
            "spuSaleSiteList": [
                {
                    "siteCode": "us"
                },
                {
                    "siteCode": "uk"
                },
                {
                    "siteCode": "ca"
                },
                {
                    "siteCode": "au"
                },
                {
                    "siteCode": "fr"
                },
                {
                    "siteCode": "de"
                },
                {
                    "siteCode": "es"
                }
            ],
            "saleAttrValueList": [
                {
                    "attrDetailType": 1,
                    "attrId": 979,
                    "attrDetailId": 16736
                }
            ],
            "operateFlag": 2
        }

    class CalculateProductPrice(ApiConfig):
        uri_path = "/api/ec-pms/pmsspu/calculate/{0}"
        method = "GET"

    class SaveProductPrice(ApiConfig):
        uri_path = "/api/ec-pms/pmsskuprice/save"
        method = "POST"
        data = [
            {
                "deliveryTypeName": "卡车",
                "selectType": 0,
                "freightMsg": None,
                "id": None,
                "spuId": 29372,
                "skuId": 43457,
                "siteCode": "us",
                "deliveryType": 1,
                "expressType": None,
                "purchasePrice": 1,
                "freight": 2235.8,
                "pricingCoefficient": 0.55,
                "trialCost": 4066.91,
                "exchangeRate": 6.5,
                "siteTrialCost": 625.68,
                "siteCurrency": "usd",
                "sitePrice": 625.99,
                "oceanPrice": 0,
                "extraPrice": 0,
                "lastPrice": 2235.8,
                "priceImage": None,
                "check": True,
                "fixedPricelVoListIndex": 0,
                "priceVoListIndex": 0
            },
            {
                "deliveryTypeName": "卡车",
                "selectType": 0,
                "freightMsg": None,
                "id": None,
                "spuId": 29372,
                "skuId": 43457,
                "siteCode": "uk",
                "deliveryType": 1,
                "expressType": None,
                "purchasePrice": 1,
                "freight": 399.7,
                "pricingCoefficient": 0.4,
                "trialCost": 1001.75,
                "exchangeRate": 8.77,
                "siteTrialCost": 114.22,
                "siteCurrency": "gbp",
                "sitePrice": 114.99,
                "oceanPrice": 0,
                "extraPrice": 0,
                "lastPrice": 399.7,
                "priceImage": None,
                "check": True,
                "fixedPricelVoListIndex": 0,
                "priceVoListIndex": 1
            },
            {
                "deliveryTypeName": "卡车",
                "selectType": 0,
                "freightMsg": None,
                "id": None,
                "spuId": 29372,
                "skuId": 43457,
                "siteCode": "ca",
                "deliveryType": 1,
                "expressType": None,
                "purchasePrice": 1,
                "freight": 286.45,
                "pricingCoefficient": 0.4,
                "trialCost": 718.63,
                "exchangeRate": 5.77,
                "siteTrialCost": 124.55,
                "siteCurrency": "cad",
                "sitePrice": 124.99,
                "oceanPrice": 0,
                "extraPrice": 0,
                "lastPrice": 286.45,
                "priceImage": None,
                "check": True,
                "fixedPricelVoListIndex": 0,
                "priceVoListIndex": 2
            },
            {
                "deliveryTypeName": "卡车",
                "selectType": 1,
                "freightMsg": None,
                "id": None,
                "spuId": 29372,
                "skuId": 43457,
                "siteCode": "au",
                "deliveryType": 1,
                "expressType": None,
                "purchasePrice": 1,
                "freight": 100,
                "pricingCoefficient": 0.58,
                "trialCost": 174.14,
                "exchangeRate": 5.33,
                "siteTrialCost": 32.67,
                "siteCurrency": "aud",
                "sitePrice": 32.99,
                "oceanPrice": 0,
                "extraPrice": 0,
                "lastPrice": 100,
                "priceImage": None,
                "check": True,
                "fixedPricelVoListIndex": 0,
                "priceVoListIndex": 3
            },
            {
                "deliveryTypeName": "卡车",
                "selectType": 0,
                "freightMsg": None,
                "id": None,
                "spuId": 29372,
                "skuId": 43457,
                "siteCode": "fr",
                "deliveryType": 1,
                "expressType": None,
                "purchasePrice": 1,
                "freight": 495.73,
                "pricingCoefficient": 0.45,
                "trialCost": 1103.84,
                "exchangeRate": 8.5,
                "siteTrialCost": 129.86,
                "siteCurrency": "eur",
                "sitePrice": 129.99,
                "oceanPrice": 0,
                "extraPrice": 0,
                "lastPrice": 495.73,
                "priceImage": None,
                "check": True,
                "fixedPricelVoListIndex": 0,
                "priceVoListIndex": 4
            },
            {
                "deliveryTypeName": "卡车",
                "selectType": 0,
                "freightMsg": None,
                "id": None,
                "spuId": 29372,
                "skuId": 43457,
                "siteCode": "de",
                "deliveryType": 1,
                "expressType": None,
                "purchasePrice": 1,
                "freight": 390.09,
                "pricingCoefficient": 0.45,
                "trialCost": 869.09,
                "exchangeRate": 8.5,
                "siteTrialCost": 102.25,
                "siteCurrency": "eur",
                "sitePrice": 102.99,
                "oceanPrice": 0,
                "extraPrice": 0,
                "lastPrice": 390.09,
                "priceImage": None,
                "check": True,
                "fixedPricelVoListIndex": 0,
                "priceVoListIndex": 5
            },
            {
                "deliveryTypeName": "卡车",
                "selectType": 0,
                "freightMsg": None,
                "id": None,
                "spuId": 29372,
                "skuId": 43457,
                "siteCode": "es",
                "deliveryType": 1,
                "expressType": None,
                "purchasePrice": 1,
                "freight": 507.67,
                "pricingCoefficient": 0.45,
                "trialCost": 1130.38,
                "exchangeRate": 8.5,
                "siteTrialCost": 132.99,
                "siteCurrency": "eur",
                "sitePrice": 132.99,
                "oceanPrice": 0,
                "extraPrice": 0,
                "lastPrice": 507.67,
                "priceImage": None,
                "check": True,
                "fixedPricelVoListIndex": 0,
                "priceVoListIndex": 6
            }
        ]

    class AuditProduct(ApiConfig):
        uri_path = "/api/ec-pms/pmsspu/sku/audit"
        method = "POST"
        data = [
            {
                "auditResult": 1,
                "remark": "",
                "skuId": 43456
            }
        ]
