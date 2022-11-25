from locust import HttpUser, TaskSet, task
import os
import time

from config.third_party_api_configs.ims_api_config import ims_api_config


class TestImsOtherIn(TaskSet):
    def __init__(self, parent):
        super().__init__(parent)
        self.sj_location_id = 1496
        self.ware_skus = ["12366347A01", "12366589A01", "12366106A01", "12366348A01", "12366590A01", "12366591A01",
                          "12366110A01", "12366352A01", "12366594A01", "12366111A01", "12366353A01", "12366595A01",
                          "12366350A01", "12366592A01", "12366351A01", "12366593A01", "12366136A01", "12366378A01",
                          "12366137A01", "12366379A01", "12366134A01", "12366376A01", "12366135A01", "12366377A01",
                          "12366138A01", "12366139A01", "12366381A01", "12366140A01", "12366382A01", "12366380A01",
                          "12366143A01", "12366385A01", "12366144A01", "12366384A01", "12366141A01", "12366383A01",
                          "12366142A01", "12366386A01", "12366125A01", "12366367A01", "12366126A01", "12366368A01",
                          "12366123A01", "12366365A01", "12366124A01", "12366366A01", "12366129A01", "12366127A01",
                          "12366369A01", "12366128A01", "12366370A01", "12366132A01", "12366374A01", "12366133A01",
                          "12366130A01", "12366372A01", "12366131A01", "12366373A01", "12366158A01", "12366159A01",
                          "12366156A01", "12366162A01", "12366157A01", "12366399A01", "12366161A01", "12366398A01",
                          "12366160A01", "12366165A01", "12366166A01", "12366163A01", "12366145A01", "12366147A01",
                          "12366148A01", "12366389A01", "12366164A01", "12366387A01", "12366146A01", "12366388A01",
                          "12366149A01", "12366150A01", "12366392A01", "12366151A01", "12366393A01", "12366390A01",
                          "12366154A01", "12366391A01", "12366396A01", "12366155A01", "12366397A01", "12366152A01",
                          "12366394A01", "12366153A01", "12366395A01", "12366617A01", "12366618A01", "12366615A01",
                          "12366616A01", "12366619A01", "12366330A01", "12366572A01"]
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
        ims_api_config['other_into_warehouse']['data'][0].update(
            {
                "sourceNo": "RK" + '2828282858',
                "targetWarehouseId": 513,
                "warehouseId": 513,
                "wareSkuList": self.ware_sku_list
            })

        return ims_api_config['other_into_warehouse']['data']

    @task(1)
    def ims_other_in(self):
        data = self.get_data()
        with self.client.post('ims/service/wms/business/other/into/warehouse', headers=self.headers, json=data,
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
    tasks = [TestImsOtherIn]
    min_wait = 1000  # 单位为毫秒
    max_wait = 1000  # 单位为毫秒


if __name__ == "__main__":
    os.system("locust -f locust_test_ims_other_in.py --host=http://10.0.0.160:28801/")