import time
from copy import deepcopy

from config.api_config.wms_api_config import wms_api_config
from db_operator.wms_db_operator import WMSDBOperator


class WmsLogics:
    def __init__(self, wms_app_request):
        self.wms_app_request = wms_app_request

    @classmethod
    def ck_id_to_code(cls, warehouse_id):
        """
        根据仓库id获取仓库编码

        :param int warehouse_id: 仓库id
        """
        if not warehouse_id:
            return
        data = WMSDBOperator.query_warehouse_info_by_id(warehouse_id)
        return data.get('warehouse_code')

    @classmethod
    def ck_code_to_id(cls, warehouse_code):
        """
        根据仓库编码获取仓库id

        :param string warehouse_code: 仓库编码
        """
        if not warehouse_code:
            return
        data = WMSDBOperator.query_warehouse_info_by_code(warehouse_code)
        return data.get('id')

    @classmethod
    def kw_id_to_code(cls, kw_id):
        """
        根据库位id获取库位编码

        :param int kw_id: 库位id
        """
        data = WMSDBOperator.query_warehouse_location_info_by_id(kw_id)
        return data.get('warehouse_location_code')

    @classmethod
    def kw_code_to_id(cls, kw_code):
        """
        根据库位编码获取库位id

        :param string kw_code: 库位编码
        """
        data = WMSDBOperator.query_warehouse_location_info_by_code(kw_code)
        return data.get('id')

    @classmethod
    def get_ck_area_id(cls, warehouse_id, area_type):
        """
        获取指定区域类型的仓库区域id

        :param int warehouse_id: 仓库id
        :param int area_type: 区域类型
        """
        data = WMSDBOperator.query_warehouse_area_info_by_type(warehouse_id, area_type)
        return str(data.get('id'))

    def get_kw(self, return_type, kw_type, num, ck_id, to_ck_id):
        """
        获取指定库位类型、指定目的仓、指定数量的仓库库位

        :param int return_type: 1-返回库位id；2-返回库位编码
        :param int kw_type: 库位类型
        :param int num: 获取的库位个数
        :param int ck_id: 库位的所属仓库id
        :param to_ck_id: 库位的目的仓id
        """
        location_data = WMSDBOperator.query_warehouse_locations(kw_type, num, ck_id, to_ck_id)
        if not location_data:
            new_locations = self.wms_app_request.create_location(num, kw_type, ck_id, to_ck_id)
            # 创建完缺口个数的库位后，重新获取库位
            location_data = WMSDBOperator.query_warehouse_locations(kw_type, num, ck_id, to_ck_id)
            if not new_locations:
                print('创建库位失败！')
                return
        elif num - len(location_data) > 0:
            # 库位不够，则新建对应缺少的库位
            new_locations = self.wms_app_request.create_location(num - len(location_data), kw_type, ck_id, to_ck_id)
            if not new_locations:
                print('创建库位失败！')
                return
            # 创建完缺口个数的库位后，重新获取库位
            location_data = WMSDBOperator.query_warehouse_locations(kw_type, num, ck_id, to_ck_id)
        # 库位够的
        if return_type == 1:
            if len(location_data) == 1:
                return location_data[0]['id']
            else:
                return [location['id'] for location in location_data]
        elif return_type == 2:
            if len(location_data) == 1:
                return location_data[0]['warehouse_location_code']
            else:
                return [location['warehouse_location_code'] for location in location_data]

    def mock_express_label_callback(self, delivery_order_code, package_list):
        """
        :param string delivery_order_code: 出库单号
        :param list package_list: 包裹列表

        """
        order_list = list()
        count = 0
        for package in package_list:
            count += 1
            temp_order_info = deepcopy(wms_api_config['label_callback']['data']['orderList'][0])
            temp_order_info.update({
                "deliveryNo": delivery_order_code,
                "packageNoList": [package],
                "logistyNo": "logistyNo" + str(int(time.time() * 1000 + count)),
                "barCode": "barCode" + str(int(time.time() * 1000 + count)),
                "turnOrderNo": str(int(time.time() * 1000)),
                "drawOrderNo": str(int(time.time() * 1000))
            })
            order_list.append(temp_order_info)
        res = self.wms_app_request.label_callback(delivery_order_code, order_list)
        if res['code'] == 200:
            return True
        else:
            return False

    @classmethod
    def query_delivery_order_package_list(cls, delivery_order_code):
        data = WMSDBOperator.query_delivery_order_package_info(delivery_order_code)
        package_no_list = [package['package_code'] for package in data]
        return package_no_list
