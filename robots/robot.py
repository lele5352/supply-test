import requests
import json
from urllib.parse import urljoin
from copy import deepcopy
import time

from utils.log_handler import logger as log
from config import env_prefix_config
from robots import service_headers, app_prefix, login, default_user
from config.third_party_api_configs.ums_api_config import UMSApiConfig

_cache_headers = {}


class Robot:
    """
    定义基础机器人
    """
    timestamp = int(time.time() * 1000)   # 时间戳

    def __init__(self, prefix=None, headers=None):
        self.headers = headers
        self.prefix = prefix
        self.methods_mapping = {
            "GET": self.call_get,
            "POST": self.call_post,
            "PUT": self.call_put,
            "DELETE": self.call_delete
        }

    def call_get(self, url, data=None):
        response = requests.get(url, params=data, headers=self.headers)
        return response

    def call_post(self, url, data=None, files=None):
        response = requests.post(url, json=data, files=files, headers=self.headers)
        return response

    def call_put(self, url, data):
        response = requests.put(url, json=data, headers=self.headers)
        return response

    def call_delete(self, url, data=None):
        response = requests.delete(url, headers=self.headers, params=data)
        return response

    def call_api(self, uri_path, method, **kwargs) -> dict:

        url = urljoin(self.prefix, uri_path)
        method = method.upper()

        log.info("请求头：%s" % json.dumps(self.headers, ensure_ascii=False))
        log.info("请求内容：%s" % json.dumps({"method": method, "url": url, "data": kwargs.get('data')}, ensure_ascii=False))

        if method in self.methods_mapping:
            response_data = self.methods_mapping[method](url, **kwargs)
        else:
            raise ValueError("Invalid request method")

        log.info(f"traceId：{response_data.headers.get('Trace-Id')}")
        log.info("响应内容：" + json.dumps(response_data.json(), ensure_ascii=False))
        log.info(
            "-------------------------------------------------我是分隔符-------------------------------------------------")
        return response_data.json()

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

    def get_user_info(self):

        content = deepcopy(UMSApiConfig.UserInfo.get_attributes())
        content["data"].update({
            "t": str(int(time.time() * 1000))
        })
        url = urljoin(self.prefix, content["uri_path"])
        res = requests.get(url, headers=self.headers, params=content["data"]).json()
        return res["data"]


class MissingPasswordError(Exception):
    pass


class AppRobot(Robot):
    """
    基础应用层机器人，包含应用机器人初始化及接口调用行为
    """
    def __init__(self, **kwargs):
        """
        用传入的用户信息执行登录，未传入时默认取配置的用户
        :param username
        :param password
        """
        user_name = default_user["username"]
        password = default_user["password"]

        if kwargs.get('username'):
            if not kwargs.get('password'):
                raise MissingPasswordError("Password is required when username is provided")

            user_name = kwargs.get("username")
            password = kwargs.get("password")

        if user_name not in _cache_headers:
            app_headers = login(user_name, password)
            _cache_headers[user_name] = app_headers
            log.info(f"用户{user_name} 请求头信息已缓存")
        else:
            log.debug(f"读取用户{user_name} 请求头缓存")
            app_headers = _cache_headers[user_name]

        self.prefix = app_prefix
        super().__init__(self.prefix, app_headers)


class ServiceRobot(Robot):
    def __init__(self, service_name):
        self.prefix = env_prefix_config.get(service_name)
        super().__init__(self.prefix, service_headers)
