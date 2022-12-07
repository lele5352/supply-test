from locust import HttpUser, TaskSet, task
import os
import time
from copy import deepcopy
from gevent._semaphore import Semaphore
from locust import TaskSet, events

from config.third_party_api_configs.ims_api_config import IMSForSCMApiConfig

all_locusts_spawned = Semaphore()
all_locusts_spawned.acquire()


def on_hatch_complete(**kwargs):
    all_locusts_spawned.release()  # 创建钩子方法


events.spawning_complete.add_listener(on_hatch_complete)  # 挂载到locust钩子函数（所有的Locust实例产生完成时触发）


class TestImsPurchaseIn(TaskSet):

    def on_start(self):
        all_locusts_spawned.wait()

    @task(2)
    def up_shelf(self):
        content = deepcopy(IMSForSCMApiConfig.PurchaseInOrderUpShelf.get_attributes())
        now = str(int(time.time() * 1000))
        content["data"].update({
            "goodsSkuList": [
                {
                    "bomVersion": "C",
                    "goodsSkuCode": "63203684930",
                    "wareSkuList": [
                        {
                            "bomQty": 5,
                            "qty": 1,
                            "storageLocationId": 257685,
                            "storageLocationType": 5,
                            "wareSkuCode": "63203684930C02"
                        },
                        {
                            "bomQty": 5,
                            "qty": 2,
                            "storageLocationId": 257685,
                            "storageLocationType": 5,
                            "wareSkuCode": "63203684930C01"
                        },
                        {
                            "bomQty": 5,
                            "qty": 1,
                            "storageLocationId": 257686,
                            "storageLocationType": 5,
                            "wareSkuCode": "63203684930C01"
                        }
                    ]
                }
            ],
            "sourceNo": "SJ" + now,
            "targetWarehouseId": 513,
            "warehouseId": 511,
            "idempotentSign": "SJ" + now
        })
        headers = {
            "serviceName": "ec-warehouse-delivery-service"
        }
        self.client.post(content['uri_path'], headers=headers, json=content["data"])


class WebSitUser(HttpUser):
    tasks = [TestImsPurchaseIn]
    min_wait = 1000  # 单位为毫秒
    max_wait = 1000  # 单位为毫秒


if __name__ == "__main__":
    os.system("locust -f locust_test_ims_purchase_in.py --host=http://10.0.0.159:28801/")
