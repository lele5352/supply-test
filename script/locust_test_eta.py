import requests
from locust import HttpUser, TaskSet, task, between
import os


class TestETA(TaskSet):

    def on_start(self):
        pass

    @task(1)
    def mall_warehouse_sku(self):
        """商品ETA-根据sku、站点、国家和邮编获取分仓信息"""
        payload = [
            {
                "countryCode": "us",
                "siteCode": "us",
                "skuCode": "00892369536",
                "zipCode": "55555"
            }
        ]

        with self.client.post('mall/warehouses/sku', json=payload, catch_response=True) as response:
            result = response.json()
            if result['code'] == 200:
                response.success()
            else:
                response.failure('Failed!')

    @task(1)
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

    @task(1)
    def mall_country(self):
        """商品ETA-获取发货仓库数据(按国家分组)"""
        payload = {}

        with self.client.get('mall/country', json=payload, catch_response=True) as response:
            result = response.json()
            if result['code'] == 200:
                response.success()
            else:
                response.failure('Failed!')

    @task(1)
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

    @task(1)
    def mall_warehouses(self):
        """根据国家和邮编信息获取分仓信息"""
        payload = [{"countryCode": "mx", "zipCode": ""}]

        with self.client.post('mall/warehouses', json=payload, catch_response=True) as response:
            result = response.json()
            if result['code'] == 200:
                response.success()
            else:
                response.failure('Failed!')

    @task(3)
    def mall_eta_trade_self(self):
        """商品ETA-自提"""
        payload = {
            "countryCode": "us",
            "siteCode": "us",
            "skuInfos": [
                {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }
            ],
            "zipCode": "55555"
        }

        with self.client.post('mall/eta/trade/self', json=payload, catch_response=True) as response:
            result = response.json()
            if result['code'] == 200:
                response.success()
            else:
                response.failure('Failed!')

    @task(3)
    def mall_calculate_list(self):
        """商品ETA-自提"""
        payload = {
            "countryCode": "us",
            "siteCode": "us",
            "skuCodes": [
                "00892369536"
            ],
            "zipCode": "55555"
        }

        with self.client.post('mall/calculate/list', json=payload, catch_response=True) as response:
            result = response.json()
            # print(result)
            if result['code'] == 200:
                response.success()
            else:
                response.failure('Failed!')

    @task(3)
    def mall_calculate(self):
        """商品ETA-自提"""
        payload = {
            "countryCode": "us",
            "siteCode": "us",
            "skuCodes": [
                "00892369536"
            ],
            "zipCode": "55555"
        }
        with self.client.post('mall/calculate', json=payload, catch_response=True) as response:
            result = response.json()
            if result['code'] == 200:
                response.success()
            else:
                response.failure('Failed!')

    @task(3)
    def mall_eta_trade_self_batch(self):
        """商品ETA-自提"""
        payload = {
            "countryCode": "us",
            "siteCode": "us",
            "skuInfos": [
                {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }, {
                    "skuCode": "00892369536",
                    "warehouseCode": ""
                }
            ],
            "zipCode": "55555"
        }

        with self.client.post('mall/eta/trade/self', json=payload, catch_response=True) as response:
            result = response.json()
            if result['code'] == 200:
                response.success()
            else:
                response.failure('Failed!')

    @task(3)
    def mall_calculate_list_batch(self):
        """商品ETA-自提"""
        payload = {
            "countryCode": "us",
            "siteCode": "us",
            "skuCodes": [
                "00892369536", "00892369309", "00892369125", "00872889542", "00866948991",
                "00866948930", "00858408493", "00841585365", "00821205694", "00763074781",
                "00746439821", "00746439701", "00689226914", "00641988196", "00618485731",
                "00598525651", "00598525450", "00573582109", "00573582034", "00549376181",
                "00531657707", "00531657070", "00504796015", "00413320473", "00413320134",
                "00401693838", "00374666794", "00374666489", "00316797904", "00316797491",
                "00290149782", "00287498183", "00233225982", "00233225576", "00233225407",
                "00233225327", "00227768705", "00197052631", "00092090077", "00047749788"

            ],
            "zipCode": "55555"
        }

        with self.client.post('mall/calculate/list', json=payload, catch_response=True) as response:
            result = response.json()
            if result['code'] == 200:
                response.success()
            else:
                response.failure('Failed!')

    @task(3)
    def mall_calculate_batch(self):
        """商品ETA-自提"""
        payload = {
            "countryCode": "us",
            "siteCode": "us",
            "skuCodes": [
                "00892369536", "00892369309", "00892369125", "00872889542", "00866948991",
                "00866948930", "00858408493", "00841585365", "00821205694", "00763074781",
                "00746439821", "00746439701", "00689226914", "00641988196", "00618485731",
                "00598525651", "00598525450", "00573582109", "00573582034", "00549376181",
                "00531657707", "00531657070", "00504796015", "00413320473", "00413320134",
                "00401693838", "00374666794", "00374666489", "00316797904", "00316797491",
                "00290149782", "00287498183", "00233225982", "00233225576", "00233225407",
                "00233225327", "00227768705", "00197052631", "00092090077", "00047749788"
            ],
            "zipCode": "55555"
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
