import requests
import json
from urllib.parse import urljoin

from utils.log_handler import logger as log
from config import env_prefix_config
from robots import app_headers, service_headers


class Robot:
    """
    定义基础机器人
    """

    def __init__(self, prefix, headers, db_operator=None):
        self.prefix = prefix
        self.headers = headers
        self.dbo = db_operator

    @classmethod
    def content_parse(cls, uri_path, method, data):
        return {
            "uri_path": uri_path,
            "method": method,
            "data": data
        }

    def call_api(self, uri_path, method, data, files='') -> dict:
        req_url = urljoin(self.prefix, uri_path)

        if method == 'post':
            res = requests.post(req_url, headers=self.headers, json=data, files=files)
        elif method == 'get':
            res = requests.get(req_url, headers=self.headers, params=data)
        elif method == 'put':
            res = requests.put(req_url, headers=self.headers, json=data)
        else:
            return {}

        result_data = res.json()
        log.info('请求头：%s' % json.dumps(self.headers, ensure_ascii=False))
        log.info('请求内容：%s' % json.dumps({'method': method, 'url': req_url, 'data': data}, ensure_ascii=False))
        log.info('响应内容：' + json.dumps(result_data, ensure_ascii=False))
        log.info(
            '-------------------------------------------------我是分隔符-------------------------------------------------')
        return result_data

    @classmethod
    def formatted_result(cls, res_data):
        if res_data['code'] == 200:
            return cls.report(1, "操作成功,msg:%s" % res_data['message'], res_data['data'])
        return cls.report(0, "操作失败,msg:%s" % res_data['message'], res_data['data'])

    @classmethod
    def report(cls, code, msg, data):
        return {
            "code": code,
            "msg": msg,
            "data": data
        }


class AppRobot(Robot):
    """
    基础应用层机器人，包含应用机器人初始化及接口调用行为
    """

    def __init__(self, db_operator=None):
        self.prefix = env_prefix_config.get('app')
        super().__init__(self.prefix, app_headers, db_operator)


class ServiceRobot(Robot):
    def __init__(self, service_name, db_operator=None):
        self.prefix = env_prefix_config.get(service_name)
        super().__init__(self.prefix, service_headers, db_operator)
