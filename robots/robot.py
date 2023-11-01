import requests
import json
from urllib.parse import urljoin
from copy import deepcopy
import time

from utils.log_handler import logger as log
from utils.redis_client import BaseRedisClient
from config import env_prefix_config
from robots import service_headers, app_prefix, login, default_user
from config.third_party_api_configs.ums_api_config import UMSApiConfig
from robots.robot_biz_exception import MissingPasswordError, ConfigImportError, ConfigNotFoundError

_cache_headers = {}


class Robot:
    """
    定义基础机器人
    """

    def __init__(self, prefix=None, headers=None):
        self.rds = None
        self.user_info = None
        self.headers = headers
        self.prefix = prefix
        self.methods_mapping = {
            "GET": self.call_get,
            "POST": self.call_post,
            "PUT": self.call_put,
            "DELETE": self.call_delete
        }

    @property
    def timestamp(self):
        return int(time.time() * 1000)  # 时间戳

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
        log.info("请求接口：%s" % json.dumps({"method": method, "url": url}, ensure_ascii=False))

        try:
            log.info("请求参数：%s" % json.dumps(kwargs.get('data'), ensure_ascii=False))
        except json.JSONDecodeError:
            log.info("请求参数：%s" % kwargs.get('data'))

        if method in self.methods_mapping:
            response_data = self.methods_mapping[method](url, **kwargs)
        else:
            raise ValueError("Invalid request method")

        log.info(f"traceId：{response_data.headers.get('Trace-Id')}")
        log.info("响应内容：%s" % json.dumps(response_data.json(), ensure_ascii=False))
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
    def formatted_result(cls, res_data=None):
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

        if not self.user_info:
            content = deepcopy(UMSApiConfig.UserInfo.get_attributes())
            content["data"].update({
                "t": str(int(time.time() * 1000))
            })
            url = urljoin(self.prefix, content["uri_path"])
            res = requests.get(url, headers=self.headers, params=content["data"]).json()

            self.user_info = res["data"]

        return self.user_info

    def init_redis_client(self, proj_name):
        """
        初始化一个redis客户端实例
        :param proj_name: env_config 配置中的项目名称
        """
        try:
            from config import rds_config
        except ImportError:
            raise ConfigImportError("rds")

        if proj_name not in rds_config:
            raise ConfigNotFoundError("rds", proj_name)

        self.rds = BaseRedisClient(**rds_config[proj_name])


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
                raise MissingPasswordError

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

    def post_excel_import(self, api_path, file_name, file_path, mime):
        """
        公共方法，执行文件上传
        :param api_path: 接口路径
        :param file_name: 文件名
        :param file_path: 文件路径
        :param mime: 文件类型: pdf,doc,xlsx,xls,jpeg,png,txt
        """
        mime_content_type = {
            "pdf": "application/pdf",
            "doc": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "xls": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "jpeg": "image/jpeg",
            "png": "image/png",
            "txt": "text/plain",
            # 添加更多的 MIME 类型和相应的文件类型参数映射
        }
        if mime not in mime_content_type:
            log.warning(f"文件类型{mime} 未匹配到映射值，将使用requests库自定义值，这可能导致文件上传错误")

        upload_headers = self.headers
        upload_headers.pop("Content-Type", None)  # 移除content-type，requests自动生成boundary参数
        url = urljoin(self.prefix, api_path)
        files = {
            "file": (file_name, open(file_path, 'rb'),
                     mime_content_type.get(mime, None)
                     )
        }

        up_rs = requests.post(url=url, headers=upload_headers, files=files)
        log.debug(f"上传文件，请求头：{up_rs.request.headers}")
        log.debug(f"上传文件，接口响应结果：{up_rs.json()}")

        return up_rs.json()


class ServiceRobot(Robot):
    def __init__(self, service_name):
        self.prefix = env_prefix_config.get(service_name)
        super().__init__(self.prefix, service_headers)

