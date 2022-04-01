import time

from utils.request_handler import RequestHandler
from utils.mysql_handler import MysqlHandler
from config.api_config.oms_api_config import oms_api_config
from controller.ums_controller import UmsController
from config.sys_config import env_config


class OmsController(RequestHandler):
    def __init__(self, ums):
        self.app_headers = ums.app_header
        self.prefix = env_config.get('app_prefix')
        self.db = MysqlHandler(**env_config.get('mysql_info_oms'))
        super().__init__(self.prefix, self.app_headers)

    def sync_mall_order(self, sale_sku, qty):
        oms_api_config['sync_mall_order']['data'].update(
            {
                "salesOrderNo": "USA" + str(int(time.time())),
            }
        )


if __name__ == '__main__':
    ums = UmsController()
    oms = OmsController(ums)
