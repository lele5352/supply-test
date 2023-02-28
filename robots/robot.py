import requests
import json
from urllib.parse import urljoin
from copy import deepcopy
import time

from utils.log_handler import logger as log
from config import env_prefix_config
from robots import app_headers, service_headers
from config.third_party_api_configs.ums_api_config import UMSApiConfig


class Robot:
    """
    定义基础机器人
    """

    def __init__(self, prefix=None, headers=None):
        self.headers = headers
        self.prefix = prefix

    def call_api(self, uri_path, method, data=None, files=None) -> dict:
        url = urljoin(self.prefix, uri_path)
        if method == "GET":
            response = requests.get(url, params=data, headers=self.headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=self.headers, files=files)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=self.headers)
        elif method == "DELETE":
            response = requests.delete(url, headers=self.headers)
        else:
            raise ValueError("Invalid request method")

        log.info("请求头：%s" % json.dumps(self.headers, ensure_ascii=False))
        log.info("请求内容：%s" % json.dumps({"method": method, "url": url, "data": data}, ensure_ascii=False))
        log.info("响应内容：" + json.dumps(response.json(), ensure_ascii=False))
        log.info(
            "-------------------------------------------------我是分隔符-------------------------------------------------")
        return response.json()

    @classmethod
    def is_data_empty(cls, response_data):
        result = False
        if not response_data:
            result = True

        data = response_data.get("data")

        if not data:
            result = True

        if isinstance(data, str):
            result = False if len(data) > 0 else True

        if isinstance(data, dict):
            if data.__contains__("records"):
                result = len(data.get("records")) <= 0
            elif data.__contains__("list"):
                result = len(data.get("list")) <= 0
            else:
                result = True
        if isinstance(data, list):
            result = False if len(data) > 0 else True
        return result

    @classmethod
    def is_success(cls, response_data):
        if not response_data:
            result = False
        else:
            code = response_data.get("code")
            if not code:
                result = False
            elif code == 1:
                result = True
            else:
                result = False
        return result

    @classmethod
    def formatted_result(cls, res_data):
        if not res_data:
            return cls.report(0, "操作失败", None)
        elif res_data.get("code") == 200:
            return cls.report(1, "操作成功,msg:%s" % res_data["message"], res_data["data"])
        elif res_data.get("data") and res_data.get("message"):
            return cls.report(0, "操作失败,msg:%s" % res_data["message"], res_data["data"])
        elif res_data.get("message"):
            return cls.report(0, "操作失败,msg:%s" % res_data["message"], None)
        else:
            return cls.report(0, "操作失败", None)

    @classmethod
    def report(cls, code, msg, data):
        return {
            "code": code,
            "msg": msg,
            "data": data
        }

    @classmethod
    def get_user_info(cls):
        prefix = env_prefix_config.get("app")
        content = deepcopy(UMSApiConfig.UserInfo.get_attributes())
        content["data"].update({
            "t": str(int(time.time() * 1000))
        })
        url = urljoin(prefix, content["uri_path"])
        res = requests.get(url, headers=app_headers, params=content["data"]).json()
        return res["data"]


class AppRobot(Robot):
    """
    基础应用层机器人，包含应用机器人初始化及接口调用行为
    """

    def __init__(self):
        self.prefix = env_prefix_config.get("app")
        super().__init__(self.prefix, app_headers)


class ServiceRobot(Robot):
    def __init__(self, service_name):
        self.prefix = env_prefix_config.get(service_name)
        super().__init__(self.prefix, service_headers)
