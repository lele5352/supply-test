from db_operator.wms_db_operator import WMSDBOperator


class WmsLogics:
    def __init__(self, wms_app_request):
        self.wms_app_request = wms_app_request

    @classmethod
    def db_ck_id_to_code(cls, warehouse_id):
        """
        根据仓库id获取仓库编码

        :param int warehouse_id: 仓库id
        """
        if not warehouse_id:
            return
        data = WMSDBOperator.query_warehouse_info_by_id(warehouse_id)
        return data.get('warehouse_code')

    @classmethod
    def db_ck_code_to_id(cls, warehouse_code):
        """
        根据仓库编码获取仓库id

        :param string warehouse_code: 仓库编码
        """
        if not warehouse_code:
            return
        data = WMSDBOperator.query_warehouse_info_by_code(warehouse_code)
        return data.get('id')

    @classmethod
    def db_kw_id_to_code(cls, kw_id):
        """
        根据库位id获取库位编码

        :param int kw_id: 库位id
        """
        data = WMSDBOperator.query_warehouse_location_info_by_id(kw_id)
        return data.get('warehouse_location_code')

    @classmethod
    def db_kw_code_to_id(cls, kw_code):
        """
        根据库位编码获取库位id

        :param string kw_code: 库位编码
        """
        data = WMSDBOperator.query_warehouse_location_info_by_code(kw_code)
        return data.get('id')

    @classmethod
    def db_get_ck_area_id(cls, warehouse_id, area_type):
        """
        获取指定区域类型的仓库区域id

        :param int warehouse_id: 仓库id
        :param int area_type: 区域类型
        """
        data = WMSDBOperator.query_warehouse_area_info_by_type(warehouse_id, area_type)
        return str(data.get('id'))

    def db_get_kw(self, return_type, kw_type, num, warehouse_id, target_warehouse_id):
        """
        获取指定库位类型、指定目的仓、指定数量的仓库库位

        :param int return_type: 1-返回库位id；2-返回库位编码
        :param int kw_type: 库位类型
        :param int num: 获取的库位个数
        :param int warehouse_id: 库位的所属仓库id
        :param target_warehouse_id: 库位的目的仓id
        """
        location_data = WMSDBOperator.query_warehouse_locations(kw_type, num, warehouse_id, target_warehouse_id)
        if len(location_data) < num:
            # 库位不够，则新建对应缺少的库位
            new_locations = self.wms_app_request.create_location(num - len(location_data), kw_type, warehouse_id,
                                                                 target_warehouse_id)
            if not new_locations:
                return
            # 创建完缺口个数的库位后，重新获取库位
            location_data = WMSDBOperator.query_warehouse_locations(kw_type, num, warehouse_id, target_warehouse_id)
        # print(location_data)
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
