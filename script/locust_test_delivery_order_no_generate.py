import requests
from locust import HttpUser, TaskSet, task
import os
import time
import json

from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class TestDeliveryOrderNoGenerate(TaskSet):
    def on_start(self):
        user = {"user_id": "204", "username": "xuhongwei@popicorns.com"}
        self.headers = {"user": json.dumps(user)}

    @task(9)
    def domain_create_delivery_order(self):
        # 定义请求头
        suffix = int(time.time() * 1000)
        temp_data = {
            "sourceOrderCode": 'source' + str(suffix),
            "saleOrderId": suffix,
            "saleOrderCode": 'sale' + str(suffix)
        }
        data = {
            "warehouseCode": "EH",
            "sourceOrderCode": "source",
            "saleOrderId": 825007,
            "saleOrderCode": "sale",
            "transportMode": 1,
            "priority": "9",
            "site": "us",
            "saleAmount": 200.2,
            "currency": "USD",
            "orderTime": "2021-08-23 15:47:09",
            "platformName": "homary-name",
            "platformCode": "homary",
            "storeCode": "ziying",
            "store": "自营",
            "customerRemarks": "这是客户备注",
            "serverRemarks": "这是HW自造的数据",
            "receiptInfo": {
                "firstName": "hongwei",
                "lastName": "xu",
                "phone": "18888888888",
                "identityCard": "441581122344556677",
                "email": "xuhongwei@popicorns.com",
                "countryId": "126",
                "countryCode": "United States",
                "country": "united states",
                "stateId": "111",
                "stateCode": "NY",
                "state": "New York",
                "city": "new york city",
                "area": "new york area",
                "address1": "test address1",
                "address2": "test address2",
                "address3": "test address3",
                "lat": "lat111",
                "lon": "lon222",
                "postcode": "510000"
            },
            "skuInfo": [{
                "saleSkuCode": "J020841-US",
                "saleSkuName": "0020841",
                "saleSkuImg": "",
                "purchasePrice": 9,
                "purchaseCurrency": "USD",
                "salePrice": 18,
                "saleCurrency": "USD",
                "saleSkuQty": 1
            }]
        }
        data.update(temp_data)
        with self.client.post('delivery-order', headers=self.headers, json=data,
                              catch_response=True) as response:
            result = response.json()
            if result['code'] == 200:
                print(result['data']['deliveryOrderCode'])
                response.success()
            else:
                response.failure('Failed!')


class WebSitUser(HttpUser):
    tasks = [TestDeliveryOrderNoGenerate]
    min_wait = 1000  # 单位为毫秒
    max_wait = 1000  # 单位为毫秒


if __name__ == '__main__':
    os.system('/Users/essenxu/PycharmProjects/supply-test/script')
    os.system('locust -f locust_test_delivery_order_no_generate.py --host=http://10.0.0.26:8330/')
