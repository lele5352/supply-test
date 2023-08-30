from config.third_party_api_configs import ApiConfig


class PWmsApi:

    class ExcelImport(ApiConfig):

        uri_path = "/api/ec-pwms-api/platformTransferDemand/excelImport"
        method = "POST"

