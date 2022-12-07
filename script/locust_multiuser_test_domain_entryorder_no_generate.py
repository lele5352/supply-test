import time

from locust import TaskSet, task, HttpUser
import queue
import os
import json
from urllib import parse


class UserBehavior(TaskSet):
    def on_start(self):
        try:
            account = self.user.user_data_queue.get()
            user = {"username": account['username'], 'user_id': account['user_id']}
            self.headers = {"user": json.dumps(user)}

            print('login with user: {}, pwd: {}, headers: {}'.format(account['username'], account['password'], self.headers))
        except queue.Empty:
            print('account data run out, test ended.')
            exit(0)

    @task(9)
    def test_domain_create_entry_order(self):
        suffix = str(int(time.time()*1000))
        payload = {
            'entryOrderInput': {
                'purchaseOrderCode': 'CG' + suffix,
                'distributeOrderCode': 'FH' + suffix,
                'entryOrderType': 0,
                'entryOrderState': 1,
                'qualityType': 1,
                'planArrivalTime': 1630058027000,
                'supplierCode': 'S68911462',
                'remark': '我只是个备注',
                'warehouseId': 7,
                'destWarehouseId': 19
            },
            'skuList': [
                {
                    'warehouseSkuCode': 'W21047361',
                    'planSkuQty': '4',
                    'warehouseSkuName': '小部件sku内部bom包裹1',
                    'warehouseSkuNameEn': '',
                    'warehouseSkuLength': 56.34,
                    'warehouseSkuWidth': 4.12,
                    'warehouseSkuHeight': 34.00,
                    'warehouseSkuWeight': 4.00,
                    'saleSkuCode': 'P68687174',
                    'saleSkuQty': 10,
                    'saleSkuImg': 'https://img.popicorns.com/dev/file/2021/07/21/9736810758dc4fc8b9d1b4829a72b779.jpg',
                    'bomVersion': '1',
                    'saleSkuName': '小部件sku'
                },
                {
                    'warehouseSkuCode': 'W64185400',
                    'planSkuQty': '7',
                    'warehouseSkuName': '小部件sku内部bom包裹2',
                    'warehouseSkuNameEn': '',
                    'warehouseSkuLength': 55.00,
                    'warehouseSkuWidth': 34.00,
                    'warehouseSkuHeight': 34.00,
                    'warehouseSkuWeight': 3.00,
                    'saleSkuCode': 'P68687174',
                    'saleSkuQty': 10,
                    'saleSkuImg': 'https://img.popicorns.com/dev/file/2021/07/21/9736810758dc4fc8b9d1b4829a72b779.jpg',
                    'bomVersion': '1',
                    'saleSkuName': '小部件sku'
                }
            ],
            'logisticsList': [
                {
                    'logisticsCompanyCode': 'SF072611',
                    'logisticsCompanyName': '顺丰物流',
                    'shipmentNumber': 'SF23425289472',
                    'carNumber': '粤·A88888',
                    'delivererName': '万老板',
                    'phone': '18434223434',
                    'telephone': '0203423432'
                }
            ]
        }
        with self.client.post('en-entry-order/saveEntryOrder', headers=self.headers, json=payload,
                              catch_response=True) as response:
            result = response.json()
            print(result)
            if result['code'] == 200:
                response.success()
            else:
                response.failure('Failed!')


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    user_data_queue = queue.Queue()

    accounts = [
        {
            'username': 'xuhongwei@popicorns.com',
            'password': '123456',
            'user_id': 204
        },
        {
            'username': 'xuhongwei1@popicorns.com',
            'password': '123456',
            'user_id': 205
        },
        {
            'username': 'xuhongwei2@popicorns.com',
            'password': '123456',
            'user_id': 206
        },
        {
            'username': 'xuhongwei3@popicorns.com',
            'password': '123456',
            'user_id': 207
        },
        {
            'username': 'xuhongwei4@popicorns.com',
            'password': '123456',
            'user_id': 208
        }
    ]
    for account in accounts:
        user_data_queue.put_nowait(account)

    min_wait = 1000
    max_wait = 1000


if __name__ == '__main__':
    os.system('locust -f locust_multiuser_test_domain_entryorder_no_generate.py --host=http://10.0.0.26:8323/')
