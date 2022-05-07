import time

from utils.request_handler import RequestHandler
from config.api_config.oms_api_config import oms_api_config
from config.sys_config import env_prefix_config


class OmsRequest(RequestHandler):
    def __init__(self, ums):
        self.app_headers = ums.app_header
        self.prefix = env_prefix_config.get('app_prefix')
        super().__init__(self.prefix, self.app_headers)

    def sync_mall_order(self, sale_sku, qty):
        oms_api_config['sync_mall_order']['data'].update(
            {
                "salesOrderNo": "USA" + str(int(time.time())),
            }
        )

