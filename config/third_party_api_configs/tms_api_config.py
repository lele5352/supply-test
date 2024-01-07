from config.third_party_api_configs import ApiConfig, BizEnum


class TMSApiConfig:
    class GetAvailableStock(ApiConfig):
        uri_path = "/mall/availableStock"
        method = "POST"
        data = {
            "current": 1,
            "size": 1000,
            "deliveryWarehouseCodes": []}

    class SubPackage(ApiConfig):
        uri_path = "/subPackage/calc/bm"
        method = "POST"
        data = {"unit": 10,
                "subRule": {"maxQuantity": 1, "girdSize": 410, "maxWeight": 65, "maxLength": 270, "maxVolumeWeight": 65,
                            "volumeCoefficient": 9032},
                "goodsDetails": [
                    {
                        "prodName": "JFT073L898A01",
                        "qty": 2,
                        "weight": 2.1,
                        "length": 15.1,
                        "width": 18.3,
                        "height": 21.74}
                ]
                }

    class CalcPackParamTest(ApiConfig):
        uri_path = "/trial/calcPackParamTest"
        method = "POST"
        data = {
            "packs": [
                {
                    "pack": {
                        "weight": 14363213.55030495,
                        "length": -5227445.767588228,
                        "width": -79208136.93745315,
                        "height": 75598943.52105388,
                        "packCode": "mollit dolor",
                        "goods": [
                            {
                                "prodName": "voluptate in cupidatat",
                                "qty": 47673721,
                                "weight": 87908786.60719624,
                                "length": 30416820.517926842,
                                "width": 8699843.03494808,
                                "height": 48842372.30599743
                            }
                        ]
                    },
                    "oldUnit": -97309722,
                    "newUnit": 31589393,
                    "sortFlag": True,
                    "volumeCoefficient":1000,
                    "trialCalcInfo":{}
                }
            ]
        }

    class SyncTrial(ApiConfig):
        uri_path = '/trial/doTrial'
        method = 'POST'
        data = None

    class SyncOrder(ApiConfig):
        uri_path = '/trial/doOrder'
        method = 'POST'
        data = None

    class TrialAddress(ApiConfig):
        """
        经过调试，可正常试算下单的测试地址
        """
        # 美国地址
        US = {
            "deliveryContactEmail": "et@aa.com",
            "countryCode": "US",
            "countryName": "Unite States",
            "province": "CA",
            "provinceName": "California",
            "city": "Vacaville",
            "cityName": "Vacaville",
            "postcode": "95688",
            "address": "7681 Harvest Lane",
            "addressType": "BUSINESS_ADDRESS_P",
            "firstName": "Will",
            "lastName": "Wilde",
            "contactEmail": "et@aa.com",
            "contactPhone": "248 378 8218"
        }

        # 德国地址
        DE = {
            "deliveryContactEmail": "et@aa.com",
            "countryCode": "DE",
            "countryName": "Germany",
            "province": "Rheinland-Pfalz",
            "provinceName": "Rheinland-Pfalz",
            "city": "Burscheid",
            "cityName": "Burscheid",
            "postcode": "51399",
            "address": "Burbachstraße 2",
            "addressType": "BUSINESS_ADDRESS_P",
            "firstName": "Will",
            "lastName": "Wilde",
            "contactEmail": "et@aa.com",
            "contactPhone": "102-02931"
        }

        # 法国地址
        FR = {
            "deliveryContactEmail": "et@aa.com",
            "countryCode": "FR",
            "countryName": "France",
            "province": "Île-de-France",
            "provinceName": "Île-de-France",
            "city": "Paris",
            "cityName": "Paris",
            "postcode": "75018",
            "address": "73 Ter Rue Lamarck",
            "addressType": "BUSINESS_ADDRESS_P",
            "firstName": "Will",
            "lastName": "Wilde",
            "contactEmail": "et@aa.com",
            "contactPhone": "102-02931"
        }


class TransportType(BizEnum):
    EXPRESS = (1, "快递")
    TRACK = (2, "卡车")


class UnitType(BizEnum):
    NATIONAL = (10, "国标kg/cm")
    FRACTIONAL = (20, "英制lb/inch")


class AddressType(BizEnum):
    RESIDENTIAL_ADDRESS = ("RESIDENTIAL_ADDRESS", "住宅地址")
    BUSINESS_ADDRESS = ("BUSINESS_ADDRESS", "商业地址")
    BUSINESS_ADDRESS_P = ("BUSINESS_ADDRESS_P", "商业地址带月台")
    BUSINESS_ADDRESS_NO_P = ("BUSINESS_ADDRESS_NO_P", "商业地址无月台")


class FaultPerson(BizEnum):
    我司 = (1, "我司")
    客户 = (2, "客户")
    双方 = (3, "双方")


class AdditionalService(BizEnum):
    上门提货 = ("door_pickup", "上门提货")
    升降尾板车_收货 = ("liftgate_pickup", "升降尾板车_收货")
    升降尾板车_送货 = ("liftgate_delivery", "升降尾板车_送货")
    白手套 = ("white_gloves", "白手套")
    预约送货 = ("book_delivery", "预约送货")
    当面签收 = ("sign_in_face", "当面签收")
    保险服务 = ("insurance", "保险服务")
    增值服务 = ("additional", "增值服务")
    送货到门 = ("delivery_to_door", "送货到门")
    送货到房间 = ("delivery_to_room", "送货到房间")
