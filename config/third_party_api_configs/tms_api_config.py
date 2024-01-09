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
            "contactPhone": "2483788218"
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
            "contactPhone": "2483788218"
        }

        GB = {
            "deliveryContactEmail": "et@aa.com",
            "countryCode": "GB",
            "countryName": "United Kingdom",
            "province": "England",
            "provinceName": "England",
            "city": "London",
            "cityName": "London",
            "postcode": "SW7 4BQ",
            "address": "100 Cornwall Gardens Flat 6 Lanarkslea House",
            "addressType": "RESIDENTIAL_ADDRESS",
            "firstName": "Will",
            "lastName": "Wilde",
            "contactEmail": "et@aa.com",
            "contactPhone": "2483788218"
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
