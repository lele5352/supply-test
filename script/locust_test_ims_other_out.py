import requests
from locust import HttpUser, TaskSet, task
import os
import time

from config.api_config.ims_api_config import ims_api_config
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class TestImsOtherOut(TaskSet):
    def __init__(self, parent):
        super().__init__(parent)
        self.sj_location_id = 1496
        self.ware_skus = ['68718842205A01', '25297066062A01', '58794200526A01', '17067658035A01', '76972538042A01',
                          '46343526649A01', '64337019363A01', '24935910361A01', '58794200075A01', '58794200675A01',
                          '17067658171A01', '32090972682A01', '28265130766A01', '65502337968A01', '44597691661A01',
                          '68718842326A01', '68718842583A01', '24935910793A01', '70316221956A01', '30756027844A01',
                          '28265130607A01', '65502337092A01', '65502337459A01', '46343526431A01', '64337019734A01',
                          '44597691629A01', '76972538839A01', '70316221265A01', '20622209350A01', '70316221939A01']
        self.headers = {
            "serviceName": "ec-warehouse-delivery-service"
        }
        self.ware_sku_list = self.get_ware_sku_list()

    def on_start(self):
        pass

    def get_ware_sku_list(self):
        ware_sku_list = list()
        for ware_sku in self.ware_skus:
            ware_sku_list.append(
                {
                    "qty": 1,
                    "storageLocationId": self.sj_location_id,
                    "storageLocationType": 5,
                    "wareSkuCode": ware_sku
                }
            )
        return ware_sku_list

    def get_data(self):
        ims_api_config['qualified_goods_other_out_block']['data'][0].update(
            {
                "sourceNo": "CK" + str(int(time.time() * 1000)),
                "targetWarehouseId": 513,
                "wareSkuList": self.ware_sku_list,
                "warehouseId": 513
            }
        )

        return ims_api_config['qualified_goods_other_out_block']['data']

    @task(1)
    def ims_other_out_block(self):
        data = self.get_data()
        with self.client.post('ims/service/wms/business/distribute/transfer/block', headers=self.headers, json=data,
                              catch_response=True) as response:
            try:
                result = response.json()
                print(result)
                if result['code'] == 200:

                    response.success()
                else:
                    response.failure('Failed!')
            except Exception:
                response.failure('Failed!')


class WebSitUser(HttpUser):
    tasks = [TestImsOtherOut]
    min_wait = 1000  # 单位为毫秒
    max_wait = 1000  # 单位为毫秒


if __name__ == "__main__":
    os.system('cd /Users/essenxu/PycharmProjects/supply-test/script')
    os.system("locust -f locust_test_ims_other_out.py --host=http://10.0.0.160:28801/")
