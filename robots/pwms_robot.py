from copy import deepcopy

from config.third_party_api_configs.pwms_api_config import *
from robots.robot import AppRobot


class PWMSRobot(AppRobot):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def import_excel(self, file_name, file_path):
        """
        文件上传
        :param file_name: 文件名
        :param file_path: 文件路径
        """
        content = deepcopy(PWmsApi.ExcelImport.get_attributes())
        api_path = content["uri_path"]

        rs = self.post_excel_import(api_path, file_name, file_path)

        if rs.get("code") == 200:
            return rs["data"]

        return None




