import time

from models.oms_model import *
from playhouse.shortcuts import model_to_dict


class OMSDBOperator:
    @classmethod
    def set_oms_order_create_time(cls, oms_no):
        """
        设置订单创建时间为1个小时之前
        :param oms_no: oms单号
        """
        one_hour_ago = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime((time.time() - 3601)))
        OmsOrder.update(create_time=one_hour_ago).where(OmsOrder.order_no == oms_no).execute()

    @classmethod
    def get_virtual_warehouse_info(cls):
        """
        获取虚拟共享仓
        """
        items = OmsVirtualWarehouse.select().where(
            OmsVirtualWarehouse.status == 1)
        items = {
            model_to_dict(item)['virtual_warehouse_code']: model_to_dict(item)['virtual_warehouse_name']
            for item in items}
        return items


if __name__ == '__main__':
    db = OMSDBOperator()
    db.set_oms_order_create_time('OMS2204180001')
