from locust import TaskSet, task, HttpUser
import queue
import os

from utils.ums_login_handler import ums_login


class UserBehavior(TaskSet):
    def on_start(self):
        try:

            account = self.user.user_data_queue.get()
            print(account)
            authorization = ums_login('test_26', True, account['username'], account['password'])
            self.headers = {
                'Content-Type': 'application/json;charset=UTF-8',
                'Authorization': authorization
            }
        except queue.Empty:
            print('account data run out, test ended.')
            exit(0)

    @task(9)
    def test_app_create_entry_order(self):
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
        },
        {
            'username': 'xuhongwei5@popicorns.com',
            'password': '123456',
            'user_id': 209
        },
        {
            'username': 'xuhongwei6@popicorns.com',
            'password': '123456',
            'user_id': 210
        },
        {
            'username': 'xuhongwei7@popicorns.com',
            'password': '123456',
            'user_id': 211
        },
        {
            'username': 'xuhongwei8@popicorns.com',
            'password': '123456',
            'user_id': 212
        },
        {
            'username': 'xuhongwei9@popicorns.com',
            'password': '123456',
            'user_id': 213
        }
    ]
    for account in accounts:
        user_data_queue.put_nowait(account)
    min_wait = 1000
    max_wait = 1000


if __name__ == '__main__':
    os.system('locust -f locust_multiuser_test_entryorder_no_generate.py --host=https://test-26.popicorns.com/')
