import requests
import json
from urllib.parse import urljoin

from utils.log_handler import logger as log


class RequestHandler:
    def __init__(self, prefix, headers, infix=''):
        self.prefix = prefix
        self.infix = infix
        self.headers = headers

    def send_request(self, uri_path, method, data, files=''):
        combined_prefix = urljoin(self.prefix, self.infix)
        request_url = combined_prefix + uri_path
        log.info('请求内容：%s' % json.dumps({'method': method, 'url': request_url, 'data': data}, ensure_ascii=False))
        log.info('请求头：%s' % json.dumps(self.headers, ensure_ascii=False))
        try:
            if method == 'post':
                res = requests.post(request_url, headers=self.headers, json=data, files=files)
            elif method == 'put':
                res = requests.put(request_url, headers=self.headers, json=data)
            else:
                res = requests.get(request_url, headers=self.headers, json=data)

            result_data = res.json()
            log.info('响应内容：' + json.dumps(result_data, ensure_ascii=False))
            log.info(
                '-------------------------------------------------我是分隔符-------------------------------------------------')
            return result_data
        except:
            log.error('请求错误!')
