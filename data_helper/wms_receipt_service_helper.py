import time

from utils.barcode_handler import barcode_generate
from utils.request_handler import RequestHandler
from config.wms_app_api_config import wms_app_api_config
from utils.mysql_handler import MysqlHandler
from utils.log_handler import LoggerHandler
from utils.ums_handler import get_service_headers


class WmsReceiptServiceHelper(RequestHandler):
    def __init__(self):
        self.prefix_key = 'receipt_service_26'
        self.service_headers = get_service_headers()
        super().__init__(self.prefix_key, self.service_headers)
        self.db = MysqlHandler('test_163', 'supply_wms')
        self.log_handler = LoggerHandler('WmsReceiptServiceHelper')

    # 创建入库单
    def entry_order_create(self, sale_sku_count=1, extra=None):
        """
        :param sale_sku_count:入库单中的销售SKU数
        :param extra: dict：额外参数，用于更新从接口配置中获取到的默认参数
        :return: string：返回入库单号
        """
        if extra:
            wms_app_api_config['service_entry_order_create']['data'].update(extra)

        # 修正采购单号、分货单号
        suffix = int(time.time() * 1000)
        temp_data = {
            "purchaseOrderCode": 'CG' + str(suffix),
            "distributeOrderCode": 'FH' + str(suffix),
            "planArrivalTime": suffix + 10000000
        }
        wms_app_api_config['service_entry_order_create']['data']['entryOrderInput'].update(temp_data)

        # 根据销售SKU数量更新仓库SKU的数量和销售SKU数量
        for sku in wms_app_api_config['service_entry_order_create']['data']['skuList']:
            sku['planSkuQty'] *= sale_sku_count
            sku['saleSkuQty'] *= sale_sku_count

        service_entry_order_create_res = self.send_request(
            **wms_app_api_config['service_entry_order_create'])
        if service_entry_order_create_res['code'] != 200:
            self.log_handler.log('入库单创建失败', 'ERROR')
            return
        barcode_generate(service_entry_order_create_res['data']['entryOrderCode'], 'entry_order')
        return service_entry_order_create_res['data']['entryOrderCode']


if __name__ == '__main__':
    pa = WmsReceiptServiceHelper()
    entry_order_code = pa.entry_order_create(2)
    print(entry_order_code)