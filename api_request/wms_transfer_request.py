import time

from config.sys_config import env_prefix_config
from config.api_config.wms_api_config import wms_api_config
from utils.request_handler import RequestHandler


class WmsTransferRequest(RequestHandler):
    def __init__(self, service_headers):
        self.prefix = env_prefix_config.get('transfer_service_prefix')
        super().__init__(self.prefix, service_headers)

    def transfer_out_create_demand(self, delivery_warehouse_code, delivery_target_warehouse_code,
                                   receive_warehouse_code, receive_target_warehouse_code, sale_sku_code, demand_qty,
                                   demand_type=1, customer_type=1, remark=''):
        """
        :param string delivery_warehouse_code: 调出仓库
        :param string receive_warehouse_code: 调入仓库
        :param string delivery_target_warehouse_code: 调出仓库的目的仓，仅调出仓为中转仓时必填
        :param string receive_target_warehouse_code: 调入仓库的目的仓，仅调入仓为中转仓时必填
        :param string sale_sku_code: 调拨的商品的销售sku
        :param int demand_qty: 调拨数量
        :param int demand_type: 调拨类型
        :param int customer_type: 客户类型：1-普通客户；2-大客户
        :param string remark: 备注
        """
        wms_api_config['create_transfer_demand']['data'].update(
            {
                "deliveryWarehouseCode": delivery_warehouse_code,
                "receiveWarehouseCode": receive_warehouse_code,
                "deliveryTargetWarehouseCode": delivery_target_warehouse_code,
                "receiveTargetWarehouseCode": receive_target_warehouse_code,
                "goodsSkuCode": sale_sku_code,
                "demandQty": demand_qty,
                "demandType": demand_type,
                "customerType": customer_type,  # 1：普通客户 2 ：大客户
                "customerRemark": remark,
                "sourceCode": "ZDH" + str(int(time.time())),
            }
        )
        create_transfer_demand_res = self.send_request(**wms_api_config['create_transfer_demand'])
        return create_transfer_demand_res
