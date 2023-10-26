from config.third_party_api_configs import ApiConfig, BizEnum


class TMSApiConfig:
    class GetAvailableStock(ApiConfig):
        uri_path = "/mall/availableStock"
        method = "POST"
        data = {
            "current": 1,
            "size": 1000,
            "deliveryWarehouseCodes": []}

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
