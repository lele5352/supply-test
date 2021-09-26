import time

from utils.barcode_handler import barcode_generate
from utils.request_handler import RequestHandler
from config.wms_app_api_config import wms_app_api_config
from utils.ums_handler import get_service_headers
from utils.mysql_handler import MysqlHandler
from utils.log_handler import LoggerHandler


class WmsDeliveryServiceHelper(RequestHandler):
    def __init__(self):
        self.prefix_key = 'delivery_service_26'
        self.service_headers = get_service_headers()
        super().__init__(self.prefix_key, self.service_headers)
        self.db = MysqlHandler('test_163', 'supply_wms')
        self.log_handler = LoggerHandler('WmsDeliveryServiceHelper')

    # 创建出库单
    def front_label_delivery_order_create(self):
        """
        :return: string：返回出库单号
        """
        # 修正来源单号、销售单号、销售单id
        suffix = int(time.time() * 1000)
        temp_data = {
            "sourceOrderCode": 'source' + str(suffix),
            "saleOrderId": suffix,
            "saleOrderCode": 'sale' + str(suffix)
        }
        wms_app_api_config['front_label_delivery_order_create']['data'].update(temp_data)

        service_delivery_order_create_res = self.send_request(
            **wms_app_api_config['front_label_delivery_order_create'])
        if service_delivery_order_create_res['code'] != 200:
            self.log_handler.log('出库单创建失败', 'ERROR')
            return
        delivery_order_code = service_delivery_order_create_res['data']['deliveryOrderCode']
        barcode_generate(delivery_order_code, 'delivery_order')
        return delivery_order_code

    def behind_label_delivery_order_create(self, sale_sku_count=1):
        """
        :return: string：返回出库单号
        """
        # 修正来源单号、销售单号、销售单id
        suffix = int(time.time() * 1000)
        temp_data = {
            "sourceOrderCode": 'source' + str(suffix),
            "saleOrderId": suffix,
            "saleOrderCode": 'sale' + str(suffix)
        }
        wms_app_api_config['behind_label_delivery_order_create']['data'].update(temp_data)

        # 更新销售sku数量
        for sku in wms_app_api_config['behind_label_delivery_order_create']['data']['skuInfo']:
            sku['saleSkuQty'] *= sale_sku_count

        service_delivery_order_create_res = self.send_request(
            **wms_app_api_config['behind_label_delivery_order_create'])
        if service_delivery_order_create_res['code'] != 200:
            self.log_handler.log('出库单创建失败', 'ERROR')
            return
        delivery_order_code = service_delivery_order_create_res['data']['deliveryOrderCode']
        barcode_generate(delivery_order_code, 'delivery_order')
        return delivery_order_code


if __name__ == '__main__':
    dah = WmsDeliveryServiceHelper()
    count = 3

    # 生成后置面单出库单、分配库存并回调包裹方案
    delivery_order_code = dah.behind_label_delivery_order_create(count)
    print(delivery_order_code)