import requests
import json
from urllib.parse import urljoin

from utils.log_handler import LoggerHandler
from config import url_prefix

log_handler = LoggerHandler("RequestHandler")


class RequestHandler:
    def __init__(self, prefix_key, headers, infix=''):
        self.prefix = url_prefix.get(prefix_key)
        self.infix = infix
        self.headers = headers

    def send_request(self, uri_path, method, data):
        combined_prefix = urljoin(self.prefix, self.infix)
        request_url = combined_prefix + uri_path
        log_handler.log('请求方式：' + method)
        log_handler.log('请求地址：' + request_url)
        log_handler.log('请求数据：' + json.dumps(data, ensure_ascii=False))

        try:
            if method == 'post':
                res = requests.post(request_url, headers=self.headers, json=data)
            elif method == 'put':
                res = requests.put(request_url, headers=self.headers, json=data)
            else:
                res = requests.get(request_url, headers=self.headers, json=data)

            result_data = res.json()
            log_handler.log('响应内容：' + json.dumps(result_data, ensure_ascii=False))
            log_handler.log(
                '-------------------------------------------------我是分隔符-------------------------------------------------')
            return result_data
        except:
            log_handler.log('请求错误!', 'ERROR')
