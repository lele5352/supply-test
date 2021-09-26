import requests
from locust import HttpUser, TaskSet, task
import os
from utils.ums_login_handler import ums_login

from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class TestOrderNoGenerate(TaskSet):
    def on_start(self):
        # authorization = ums_login('test_26', True, 'admin', 'admin')
        self.headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1SWQiOjEsInVzZXJfbmFtZSI6ImFkbWluIiwidiI6NDIsInNjb3BlIjpbImFsbCJdLCJleHAiOjE2Mjc1ODA4MzIsImp0aSI6IjA4ZmMzMWViLTk1NWUtNGEwYS05NzMyLTY0NTdlYjFkMjk0YyIsImNsaWVudF9pZCI6ImhvbWFyeS1lYyJ9.mFximYw7Na8ZHWr2wR58dOy6vFPC6oALkDNLpETKYsGjv1OtEqmRn7dZ-N2AyTmO8PSqgOlXHnH0gceaVOtrP_sxH1otfWkTgBRQfXsKZ48uW_uXLmiZgfrWqHYsFZH-kHUUfQQaexzauzmLCGkNzby-DN30lhGcVd0LnZycBx4'
        }
        print('1111')

    @task(1)
    def test_entry_order_generate(self):

        # 定义请求头
        data = {
            'entryOrderType': 3,
            'eta': 1630058027000,
            'fromOrderCode': 'LY000002',
            'logisticsInfoList':
                [
                    {'carNumber': '粤A·88888',
                     'delivererName': '许宏伟',
                     'logisticsCompanyCode': 'WULI0002',
                     'logisticsCompanyName': '艾斯物流有限公司',
                     'phone': '18888888888',
                     'shipmentNumber': 'YD10000000002',
                     'telephone': '020-88888888'
                     }
                ],
            'operationFlag': 1,
            'qualityType': 1,
            'remark': '测试新增其他入库单',
            'supplierCode': 'S37501617',
            'skuInfoList': [
                {
                    'warehouseSkuCode': 'W21047361',
                    'planSkuQty': '40',
                    'warehouseSkuName': '小部件sku内部bom包裹1',
                    'warehouseSkuNameEn': '',
                    'warehouseSkuLength': 56.34,
                    'warehouseSkuWidth': 4.12,
                    'warehouseSkuHeight': 34.00,
                    'warehouseSkuWeight': 4.00,
                    'saleSkuCode': 'P68687174',
                    'saleSkuImg': 'https://img.popicorns.com/dev/file/2021/07/21/9736810758dc4fc8b9d1b4829a72b779.jpg',
                    'bomVersion': '1',
                    'saleSkuName': '小部件sku'
                },
                {
                    'warehouseSkuCode': 'W64185400',
                    'planSkuQty': '70',
                    'warehouseSkuName': '小部件sku内部bom包裹2',
                    'warehouseSkuNameEn': '',
                    'warehouseSkuLength': 55.00,
                    'warehouseSkuWidth': 34.00,
                    'warehouseSkuHeight': 34.00,
                    'warehouseSkuWeight': 3.00,
                    'saleSkuCode': 'P68687174',
                    'saleSkuImg': 'https://img.popicorns.com/dev/file/2021/07/21/9736810758dc4fc8b9d1b4829a72b779.jpg',
                    'bomVersion': '1',
                    'saleSkuName': '小部件sku'
                }
            ]
        }

        with self.client.post('api/ec-wms-api/entryorder', headers=self.headers, json=data,
                              catch_response=True) as response:
            result = response.json()
            print(result)
            if result['code'] == 200:

                response.success()
            else:
                response.failure('Failed!')


class WebSitUser(HttpUser):
    tasks = [TestOrderNoGenerate]
    min_wait = 1000  # 单位为毫秒
    max_wait = 1000  # 单位为毫秒


if __name__ == "__main__":
    os.system("locust -f locust_test_entryorder_no_generate.py --host=https://test-26.popicorns.com/")
