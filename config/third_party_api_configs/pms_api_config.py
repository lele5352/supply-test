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

    class GetSkuAttribution(ApiConfig):
        uri_path = "/api/ec-pms/pmssku/detail/{0}"
        method = "GET"

    class EditSkuAttribution(ApiConfig):
        uri_path = "/api/ec-pms/pmssku/detail"
        method = "POST"
        data = {
            "pmsSkuAttrVoBaseList": [
                {
                    "id": 722951,
                    "attrId": 4,
                    "attrName": "\u9762\u76c6\u6750\u8d28",
                    "usaAttrName": "sink material",
                    "attrCategory": 1,
                    "showType": 2,
                    "baseAttrMallShow": 1,
                    "originBaseAttrMallShow": None,
                    "sort": 400,
                    "originSort": None,
                    "attrUses": [],
                    "usaNameOnMall": "sink material",
                    "isRequired": 2,
                    "attrList": [
                        {
                            "attrDetailId": 1206,
                            "attrDetailNameUs": "Glass",
                            "attrDetailName": "\u73bb\u7483",
                            "attrDetailNameUk": "Glass"
                        },
                        {
                            "attrDetailId": 1211,
                            "attrDetailNameUs": "Stone Resin",
                            "attrDetailName": "\u4eba\u9020\u77f3",
                            "attrDetailNameUk": "Stone Resin"
                        },
                        {
                            "attrDetailId": 1217,
                            "attrDetailNameUs": "Stainless Steel",
                            "attrDetailName": "\u4e0d\u9508\u94a2",
                            "attrDetailNameUk": "Stainless Steel"
                        },
                        {
                            "attrDetailId": 1223,
                            "attrDetailNameUs": "Kaolin Clay",
                            "attrDetailName": "\u9ad8\u5cad\u571f",
                            "attrDetailNameUk": "Kaolin Clay"
                        },
                        {
                            "attrDetailId": 1231,
                            "attrDetailNameUs": "Ceramic",
                            "attrDetailName": "\u9676\u74f7\u54c1",
                            "attrDetailNameUk": "Ceramic"
                        },
                        {
                            "attrDetailId": 1235,
                            "attrDetailNameUs": "Resin",
                            "attrDetailName": "\u6811\u8102",
                            "attrDetailNameUk": "Resin"
                        },
                        {
                            "attrDetailId": 1240,
                            "attrDetailNameUs": "Marble",
                            "attrDetailName": "\u5927\u7406\u77f3",
                            "attrDetailNameUk": "Marble"
                        },
                        {
                            "attrDetailId": 1245,
                            "attrDetailNameUs": "Brass",
                            "attrDetailName": "\u5168\u94dc",
                            "attrDetailNameUk": "Brass"
                        },
                        {
                            "attrDetailId": 1253,
                            "attrDetailNameUs": "Quartz",
                            "attrDetailName": "\u77f3\u82f1\u77f3",
                            "attrDetailNameUk": "Quartz"
                        },
                        {
                            "attrDetailId": 1258,
                            "attrDetailNameUs": "Stone",
                            "attrDetailName": "\u5ca9\u677f",
                            "attrDetailNameUk": "Stone"
                        }
                    ],
                    "attrValueVoList": [
                        {
                            "attrDetailId": 1206,
                            "attrDetailNameUs": "Glass",
                            "attrDetailName": "\u73bb\u7483",
                            "attrDetailNameUk": "Glass"
                        }
                    ],
                    "originAttrValueVoList": None,
                    "modifyStatus": 0,
                    "usaUnit": None,
                    "enUnit": None
                }
            ],
            "pmsSkuAttrVoSellList": [
                {
                    "id": 1179022,
                    "attrId": 979,
                    "attrName": "\u56fe\u7247\u5c5e\u6027\u7b5b\u9009",
                    "usaAttrName": "image filter test",
                    "attrCategory": 2,
                    "showType": 2,
                    "baseAttrMallShow": 1,
                    "originBaseAttrMallShow": None,
                    "sort": None,
                    "originSort": None,
                    "attrUses": [],
                    "usaNameOnMall": "image filter test",
                    "isRequired": 1,
                    "attrList": [
                        {
                            "attrDetailId": 16736,
                            "attrDetailNameUs": "one",
                            "attrDetailName": "1",
                            "attrDetailNameUk": "one"
                        },
                        {
                            "attrDetailId": 16737,
                            "attrDetailNameUs": "two",
                            "attrDetailName": "2",
                            "attrDetailNameUk": "two"
                        }
                    ],
                    "attrValueVoList": [
                        {
                            "attrId": None,
                            "attrDetailType": 2,
                            "attrDetailId": 0,
                            "attrDetailName": "1",
                            "attrDetailNameUs": "one",
                            "attrDetailNameUk": "one",
                            "moreLanguageId": None
                        }
                    ],
                    "originAttrValueVoList": None,
                    "modifyStatus": 0,
                    "usaUnit": None,
                    "enUnit": None,
                    "zharr": [
                        {
                            "attrValueId": "",
                            "propertiesValue": "one",
                            "propertiesValueEn": "one",
                            "propertiesValueZh": "1"
                        }
                    ],
                    "attrDetailNameUk": "one",
                    "attrDetailNameUs": "one"
                }
            ],
            "pmsSkuVo": {
                "id": 43487,
                "spu": "76167253",
                "productName": "\u6d4b\u8bd5\u5355\u54c1\u5355\u4ef6",
                "originProductName": "\u6d4b\u8bd5\u5355\u54c1\u5355\u4ef6",
                "modifyStatus": 1,
                "spuId": 29399,
                "sku": "HW69RA7686",
                "attrCombinedName": "one",
                "link": None,
                "mainImg": "https://img.popicorns.com/dev/file/2023/06/27/d76e4266d5854fc5b29a549fec3e082c.jpg",
                "isSuit": 0,
                "isSuitText": "\u5426"
            },
            "numberAttrParamList": [
                {
                    "id": 722949,
                    "spuId": None,
                    "attrId": 976,
                    "attrCategory": 1,
                    "attrDetailType": None,
                    "attrDetailId": None,
                    "attrDetailName": None,
                    "attrDetailNameUs": None,
                    "originAttrDetailNameUs": None,
                    "attrDetailNameUk": None,
                    "originAttrDetailNameUk": None,
                    "baseAttrMallShow": 0,
                    "originBaseAttrMallShow": None,
                    "usaUnit": "\"(\u82f1\u5bf8)",
                    "enUnit": "mm(\u6beb\u7c73)",
                    "sort": 200,
                    "originSort": None,
                    "attrUses": [],
                    "usaNameOnMall": "range test2",
                    "attrCategoryStr": "\u57fa\u672c\u5c5e\u6027",
                    "usaAttrName": "range test2",
                    "modifyStatus": 0,
                    "isRequired": 1,
                    "showType": 4,
                    "originUsaNameOnMall": "range test2"
                },
                {
                    "id": 722950,
                    "spuId": None,
                    "attrId": 964,
                    "attrCategory": 1,
                    "attrDetailType": None,
                    "attrDetailId": None,
                    "attrDetailName": None,
                    "attrDetailNameUs": None,
                    "originAttrDetailNameUs": None,
                    "attrDetailNameUk": None,
                    "originAttrDetailNameUk": None,
                    "baseAttrMallShow": 0,
                    "originBaseAttrMallShow": None,
                    "usaUnit": "\"(\u82f1\u5bf8)",
                    "enUnit": "mm(\u6beb\u7c73)",
                    "sort": 300,
                    "originSort": None,
                    "attrUses": [],
                    "usaNameOnMall": "range test",
                    "attrCategoryStr": "\u57fa\u672c\u5c5e\u6027",
                    "usaAttrName": "range test",
                    "modifyStatus": 0,
                    "isRequired": 1,
                    "showType": 4,
                    "originUsaNameOnMall": "range test"
                }
            ],
            "pmsSkuModityInfoVoList": [
                {
                    "attrId": 4,
                    "usaAttrName": "sink material"
                },
                {
                    "attrId": 979,
                    "usaAttrName": "image filter test"
                }
            ],
            "operateFlag": 2
        }

    class ApproveSkuAttribution(ApiConfig):
        uri_path = "/api/ec-pms/pmssku/detail/approve"
        method = "POST"
        data = {"auditResult": "1", "remark": "", "skuIds": [43487]}
