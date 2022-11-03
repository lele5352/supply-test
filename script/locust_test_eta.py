import requests
from locust import HttpUser, TaskSet, task, between
import os


class TestETA(TaskSet):

    def on_start(self):
        pass

    @task(0)
    def mall_warehouse_sku(self):
        """商品ETA-根据sku、站点、国家和邮编获取分仓信息"""
        payload = [
            {
                "countryCode": "us",
                "siteCode": "us",
                "skuCode": "j020053-11",
                "zipCode": "07450"
            }
        ]

        with self.client.post('mall/warehouses/sku', json=payload, catch_response=True) as response:
            result = response.json()
            if result['code'] == 200:
                response.success()
            else:
                response.failure('Failed!')

    @task(0)
    def mall_get_list(self):
        """商品ETA-获取所有仓库"""
        payload = {
            "countryCode": "us"
        }

        with self.client.post('mall/getList', json=payload, catch_response=True) as response:
            result = response.json()
            if result['code'] == 200:
                response.success()
            else:
                response.failure('Failed!')

    @task(0)
    def mall_country(self):
        """商品ETA-获取发货仓库数据(按国家分组)"""
        payload = {}

        with self.client.get('mall/country', json=payload, catch_response=True) as response:
            result = response.json()
            if result['code'] == 200:
                response.success()
            else:
                response.failure('Failed!')

    @task(0)
    def mall_inventory_get(self):
        """商品ETA-获取现货库存"""
        payload = {
            "abroadFlag": 1,
            "countryCode": "us",
            "current": 1,
            "size": 1000
        }

        with self.client.post('mall/inventory/get', json=payload, catch_response=True) as response:
            result = response.json()
            if result['code'] == 200:
                response.success()
            else:
                response.failure('Failed!')

    @task(0)
    def mall_warehouses(self):
        """根据国家和邮编信息获取分仓信息"""
        payload = [{"countryCode": "mx", "zipCode": ""}]

        with self.client.post('mall/warehouses', json=payload, catch_response=True) as response:
            result = response.json()
            if result['code'] == 200:
                response.success()
            else:
                response.failure('Failed!')

    @task(0)
    def mall_eta_trade_self(self):
        """商品ETA-自提"""
        payload = {
            "countryCode": "us",
            "siteCode": "us",
            "skuInfos": [
                {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }
            ],
            "zipCode": "07450"
        }

        with self.client.post('mall/eta/trade/self', json=payload, catch_response=True) as response:
            result = response.json()
            if result['code'] == 200:
                response.success()
            else:
                response.failure('Failed!')

    @task(0)
    def mall_calculate_list(self):
        """商品ETA-自提"""
        payload = {
            "countryCode": "us",
            "siteCode": "us",
            "skuCodes": [
                "j020053-11"
            ],
            "zipCode": "07450"
        }

        with self.client.post('mall/calculate/list', json=payload, catch_response=True) as response:
            result = response.json()
            # print(result)
            if result['code'] == 200:
                response.success()
            else:
                response.failure('Failed!')

    @task(0)
    def mall_calculate(self):
        """商品ETA-自提"""
        payload = {
            "countryCode": "us",
            "siteCode": "us",
            "skuCodes": [
                "j020053-11"
            ],
            "zipCode": "07450"
        }
        with self.client.post('mall/calculate', json=payload, catch_response=True) as response:
            result = response.json()
            if result['code'] == 200:
                response.success()
            else:
                response.failure('Failed!')

    @task(0)
    def mall_eta_trade_self_batch(self):
        """商品ETA-自提"""
        payload = {
            "countryCode": "us",
            "siteCode": "us",
            "skuInfos": [
                {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }, {
                    "skuCode": "j020053-11",
                    "warehouseCode": ""
                }
            ],
            "zipCode": "91201"
        }

        with self.client.post('mall/eta/trade/self', json=payload, catch_response=True) as response:
            result = response.json()
            if result['code'] == 200:
                response.success()
            else:
                response.failure('Failed!')

    @task(1000)
    def mall_calculate_list_batch(self):
        """商品ETA-自提"""
        payload = {
            "countryCode": "us",
            "siteCode": "us",
            "skuCodes": [
                "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11",
                "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11",
                "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11",
                "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11",
                "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11",
                "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11",
                "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11",
                "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11",
                "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11",
                "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11",
                "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11",
                "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11",
                "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11",
                "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11",
                "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11",
                "j020053-11", "j020053-11"

            ],
            "zipCode": "07450"
        }

        with self.client.post('mall/calculate/list', json=payload, catch_response=True) as response:
            result = response.json()
            if result['code'] == 200:
                response.success()
            else:
                response.failure('Failed!')

    @task(0)
    def mall_calculate_batch(self):
        """商品ETA-自提"""
        payload = {
            "countryCode": "us",
            "siteCode": "us",
            "skuCodes": [
                "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11",
                "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11",
                "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11",
                "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11",
                "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11",
                "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11",
                "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11",
                "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11",
                "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11",
                "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11",
                "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11",
                "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11",
                "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11",
                "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11",
                "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11", "j020053-11",
                "j020053-11", "j020053-11"
            ],
            "zipCode": "07450"
        }
        with self.client.post('mall/calculate', json=payload, catch_response=True) as response:
            result = response.json()
            if result['code'] == 200:
                response.success()
            else:
                response.failure('Failed!')


class WebSitUser(HttpUser):
    wait_time = between(1, 1)
    tasks = [TestETA]


if __name__ == "__main__":
    os.system("locust -f locust_test_eta.py --host=http://10.0.0.159:8701/")
