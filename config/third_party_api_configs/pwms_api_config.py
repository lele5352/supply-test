from config.third_party_api_configs import ApiConfig
import os


class PWmsApi:
    class ExcelImport(ApiConfig):
        uri_path = "/api/ec-pwms-api/platformTransferDemand/excelImport"
        method = "POST"

    class Save(ApiConfig):
        uri_path = "/api/ec-pwms-api/file/import/save"
        method = "POST"
        data = {
            "bizType": "platform_order_imp",
            "filePath": None,
            "operateUserId": None
        }

    class Check(ApiConfig):
        uri_path = "/api/ec-pwms-api/file/import/check"
        method = "POST"
        data = {
            "bizType": "platform_order_imp", "operateUserId": None
        }

    class Template:

        sheet_headers = ["平台单号", "发货仓", "目的仓", "收货仓",
                         "平台", "店铺", "平台Barcode", "销售SKU编码", "需求数"]
        file_path = "../test_data/plat_import_template.xlsx"

        abs_file_path = os.path.abspath(file_path)

    class PlatformTransferDemandPage(ApiConfig):

        uri_path = "/api/ec-pwms-api/platformTransferDemand/page"
        method = "POST"
        data = {
            "shortPick": None,
            "storeCode": None,
            "saleSkuCodeList": [],
            "createUserId": None,
            "size": 10,
            "current": 1
        }

