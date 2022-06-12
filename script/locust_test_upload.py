import requests
from locust import HttpUser, TaskSet, task
import os

from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class TestUpload(TaskSet):
    def on_start(self):
        # authorization = ums_login('test_26', True, 'admin', 'admin')
        self.headers = {
            # 'Content-Type': 'application/json;charset=UTF-8',
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1SWQiOjQxOCwidXNlcl9uYW1lIjoieHVob25nd2VpQHBvcGljb3Jucy5jb20iLCJ2IjoxNTQsInNjb3BlIjpbImFsbCJdLCJleHAiOjE2NTM0MzY3OTksImp0aSI6IjYzNGJiNDhhLTc0NzQtNDJjMi05YmVmLTMzZjM3NmZiZmY4MyIsImNsaWVudF9pZCI6ImhvbWFyeS1lYyJ9.mvy4tg8E0mQeHn8akMx1K48T22YMcul_xtBQyonwtH786_LSKqzL_QlsyZzGHjP4I9rZtnRuImeaxZvYpoBCV5U7AwlM4eoUuOfrNDsOl_OLILGP6rYc-3VDimwIbX-b2yNnY6w9bCXNeCoAur8vBjLAzpqMNSks50XRXZ3Nn0g'
        }
        print('1111')

    @task(1)
    def cdn_file_upload(self):
        # 定义请求头
        payload = {}
        files = [
            ('file', ('get-label (1).pdf', open('/Users/essenxu/Desktop/get-label (1).pdf', 'rb'), 'application/pdf'))
        ]

        with self.client.post('ec-wms-api/ext/common/upload', headers=self.headers, json=payload,files=files,
                              catch_response=True) as response:
            result = response.json()
            print(result)
            if result['code'] == 200:
                response.success()
            else:
                response.failure('Failed!')


class WebSitUser(HttpUser):
    tasks = [TestUpload]
    min_wait = 1000  # 单位为毫秒
    max_wait = 1000  # 单位为毫秒


if __name__ == "__main__":
    os.system("locust -f locust_test_upload.py --host=https://test-scms.popicorns.com/")
