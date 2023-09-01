import json
from copy import deepcopy

from config.third_party_api_configs.pwms_api_config import *
from robots.robot_biz_exception import *
from robots.robot import AppRobot
from robots.bpms_robot import BPMSRobot
from utils.wait_handler import until
from utils.log_handler import logger as log
from openpyxl import Workbook


class PWMSRobot(AppRobot):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def excel_import(self):
        """
        文件上传
        """
        content = deepcopy(PWmsApi.ExcelImport.get_attributes())
        api_path = content["uri_path"]
        file_name = "plat_import.xlsx"
        file_path = PWmsApi.Template.abs_file_path

        rs = self.post_excel_import(api_path, file_name, file_path, "xlsx")
        try:
            file_url = rs["data"]
        except KeyError:
            raise FileImportError(file_name)

        return file_url

    def import_save(self, file_path):

        user_info = self.get_user_info()
        user_id = user_info["userId"]
        content = deepcopy(PWmsApi.Save.get_attributes())
        content["data"].update(
            {
                "operateUserId": user_id,
                "filePath": file_path
            }
        )
        return self.call_api(**content)

    @until(30, 0.1)
    def check_status(self):
        """
        检查保存结果
        """
        content = deepcopy(PWmsApi.Check.get_attributes())
        user_info = self.get_user_info()
        content["data"]["operateUserId"] = user_info["userId"]

        save_rs = self.call_api(**content)
        rs_path = save_rs.get("data", {}).get("result", None)
        rs_status = save_rs.get("data", {}).get("status")

        if rs_status == 1 and not rs_path:
            return True
        elif rs_status == 1 and rs_path:
            raise PlatTransferDemandSaveError(rs_path)

        return False

    def write_template(self, sku_code, demand_qty, delivery_warehouse,
                       target_warehouse, receive_warehouse
                       ):
        """
        写入数据到 平台调拨需求导入 模板
        :param sku_code: 销售sku编码
        :param demand_qty: 需求数量
        :param delivery_warehouse: 发货仓库编码
        :param receive_warehouse: 收货仓库编码
        :param target_warehouse: 目的仓库编码
        """
        work_book = Workbook()
        work_sheet = work_book.active
        work_sheet.append(PWmsApi.Template.sheet_headers)
        save_path = PWmsApi.Template.abs_file_path
        sku_list = BPMSRobot().plat_product_page(sku_code)
        if not sku_list:
            raise PlatSkuNotFoundError(sku_code)

        for sku in sku_list:
            row = []
            order_code = f"TS-FBA-{self.timestamp}"
            try:
                row.extend([order_code, delivery_warehouse, target_warehouse, receive_warehouse,
                            sku["platformCode"], sku["storeCode"], sku["fnSkuCode"], sku_code, demand_qty])
            except KeyError:
                log.error(f"平台sku详情：{json.dumps(sku)}")
                raise PlatSkuValueError(sku)

            work_sheet.append(row)

        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        work_book.save(save_path)

    def plat_transfer_demand_page(self, **kwargs):
        """
        查询平台调拨需求列表
        """
        kwargs_list = ["saleSkuCodeList", "createUserId"]
        if kwargs.get("saleSkuCodeList"):
            if not isinstance(kwargs.get("saleSkuCodeList"), list):
                raise ValueError("saleSkuCodeList 参数值必须是列表")

        content = deepcopy(PWmsApi.PlatformTransferDemandPage.get_attributes())

        content["data"].update({key: value for key, value in kwargs.items() if key in kwargs_list})

        return self.call_api(**content)


