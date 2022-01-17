import json
import time

from config.sys_config import env_config
from config.api_config.wms_api_config import wms_api_config
from utils.request_handler import RequestHandler
from utils.mysql_handler import MysqlHandler
from utils.log_handler import logger as log
from controller.ums_controller import UmsController


class WmsController(RequestHandler):
    def __init__(self, ums):
        self.app_headers = ums.get_app_headers()
        self.prefix = env_config.get('app_prefix')
        self.db = MysqlHandler(**env_config.get('mysql_info_wms'))
        super().__init__(self.prefix, self.app_headers)

    def get_switch_warehouse_data_perm_id(self, warehouse_id):
        now = str(int(time.time() * 1000))
        wms_api_config['get_switch_warehouse_list']['data'].update({
            't': now
        })
        res = self.send_request(**wms_api_config['get_switch_warehouse_list'])
        if not res:
            return
        for perm in res['data']:
            if perm['dataId'] == warehouse_id:
                return perm['id']
        return

    def switch_default_warehouse(self, warehouse_id):
        data_perm_id = self.get_switch_warehouse_data_perm_id(warehouse_id)
        wms_api_config['switch_default_warehouse']['data'].update({
            'dataPermId': data_perm_id
        })
        res = self.send_request(**wms_api_config['switch_default_warehouse'])
        if not res:
            return
        return True

    def get_warehouse(self, search_field_dict):
        """
        :param search_field_dict: dict 搜索条件字段值字典
        :return: list 搜索出来的仓库信息列表

        warehouseStatus: 0,# 仓库状态 int：不传-全部、0-启用、1-禁用
        operatingMode 作业模式 int：不传-全部、1-中转、2-备货、3-直发、4-发货
        warehouseCode 仓库编码 string
        warehouseAbbreviation 仓库简称 string
        warehouseNameEn 仓库英文名称 string
        warehouseNameCn 仓库中文名称 string
        cnWarehouseFlag 是否国内仓库 int：不传-全部、0-否、1-是
        """
        wms_api_config['get_warehouse']['data'].update(search_field_dict)
        res = self.send_request(**wms_api_config['get_warehouse'])
        warehouse_info = res['data']['records']
        return warehouse_info

    def get_warehouse_area(self, search_field_dict):
        """
        :param search_field_dict: dict 搜索条件字段值字典
        :return: list 搜索出来的库区信息列表

        warehouseAreaStatus 库区状态 int：不传-全部、0-启用、1-禁用；
        warehouseAreaType 库区类型 int：不传-全部、1-上架区、2-不良品区、3-入库异常处理区、4-出库异常处理区、5-容器区；
        warehouseAreaCode 库区编码 string；
        warehouseAreaName 库区名称 string；
        warehouseId 仓库ID int；
        """
        wms_api_config['get_warehouse_area']['data'].update(search_field_dict)
        res = self.send_request(**wms_api_config['get_warehouse_area'])
        area_info = res['data']['records']
        return area_info

    def get_warehouse_location(self, search_field_dict):
        """
        :param search_field_dict: dict 搜索条件字段值字典
        :return: list 搜索出来的库位信息列表

        warehouseLocationStatus 库位状态 int：不传-全部、0-启用、1-禁用;
        warehouseAreaType 库区类型 int：不传-全部、1-上架区、2-不良品区、3-入库异常处理区、4-出库异常处理区、5-容器区;
        belongWareHouseAreaCode 所属库区 string;
        destWarehouseCode 目的仓库编码 string;
        warehouseLocationCode 库位编码 string;
        warehouseLocationName 库位名称 string;
        warehouseLocationType 库位类型 int：不传-全部、1-收货库位、2-质检库位、3-调拨库位、4-移库库位、5-上架库位、6-不良品库位、7-入库异常库位、8-出库异常库位;
        warehouseLocationUseStatus 库位使用状态 int：不传-全部、0-闲置、1-收货中、2-已质检交接、3-质检中、4-已上架交接、5-上架中、6-装托中、7-出库异常库位;
        """
        wms_api_config['get_warehouse_location']['data'].update(search_field_dict)
        res = self.send_request(**wms_api_config['get_warehouse_location'])
        location_info = res['data']['records']
        return location_info

    def db_get_location_ids(self, location_type, num, warehouse_id, target_warehouse_id=None):
        if not target_warehouse_id:
            query_location_id_sql = """
            SELECT
                id 
            FROM
                base_warehouse_location 
            WHERE
                state = 0 
                AND type = %s 
                AND warehouse_id = %s 
                AND dest_warehouse_id IS NULL 
                LIMIT %s""" % (location_type, warehouse_id, num)
        else:
            query_location_id_sql = """
            SELECT
                id 
            FROM
                base_warehouse_location 
            WHERE
                state = 0 
                AND type = %s 
                AND warehouse_id = %s 
                AND dest_warehouse_id = %s 
                LIMIT %s""" % (location_type, warehouse_id, target_warehouse_id, num)

        location_data = self.db.get_all(query_location_id_sql)
        if not location_data:
            return
        elif len(location_data) == 1:
            return location_data[0]['id']
        elif len(location_data) < num:
            # 库位不够，则新建对应缺少的库位
            new_locations = self.create_location(num - len(location_data), location_type, warehouse_id,
                                                 target_warehouse_id)
            if not new_locations:
                return
            # 创建完缺口个数的库位后，重新获取库位
            location_data = self.db.get_all(query_location_id_sql)
            location_ids = [location['id'] for location in location_data]
            return location_ids
        else:
            location_ids = [location['id'] for location in location_data]
            return location_ids

    # 创建库位
    def create_location(self, num, location_type, warehouse_id, target_warehouse_id=None):
        """
        :param location_type: 库位类型：1-收货库位 2-质检库位 3-调拨库位 4-移库库位 5-上架库位 6-不良品库位 7-入库异常库位 8-出库异常库位
        :param num: 新建的库位数
        :param warehouse_id: 所属仓库id
        :param target_warehouse_id: 目的仓id
        :return: list 创建出来的库位列表

        库位类型对应的库区类型
        1-收货库位 类型：容器库区-5
        2-质检库位 类型：容器库区-5
        3-调拨库位 类型：容器库区-5
        4-移库库位 类型：容器库区-5
        5-上架库位 类型：上架库区-1
        6-不良品库位 类型：不良品库区-2
        7-入库异常库位 类型：入库异常库区-3
        8-出库异常库位 类型：出库异常库区-4
        """
        location_area_maps = {
            1: {"area_type": 5, "code_prefix": "SH", "name_prefix": "SHKW"},
            2: {"area_type": 5, "code_prefix": "ZJ", "name_prefix": "ZJKW"},
            3: {"area_type": 5, "code_prefix": "TP", "name_prefix": "TPKW"},
            4: {"area_type": 5, "code_prefix": "YK", "name_prefix": "YKKW"},
            5: {"area_type": 1, "code_prefix": "SJ", "name_prefix": "SJKW"},
            6: {"area_type": 2, "code_prefix": "CP", "name_prefix": "CPKW"},
            7: {"area_type": 3, "code_prefix": "RKYC", "name_prefix": "RKYCKW"},
            8: {"area_type": 4, "code_prefix": "CKYC", "name_prefix": "CKYCKW"}
        }

        location_codes = list()
        query_area_dict = {
            "warehouseId": warehouse_id,
            "warehouseAreaType": location_area_maps[location_type]['area_type']
        }
        for i in range(num):
            now = str(int(time.time() * 1000))
            location_info = {
                'warehouseLocationCode': location_area_maps[location_type]['code_prefix'] + now,
                'warehouseLocationName': location_area_maps[location_type]['name_prefix'] + now,
                'warehouseLocationType': location_type,
                'belongWarehouseAreaId': self.get_warehouse_area(query_area_dict)[0]['warehouseAreaId'],
                'warehouseAreaType': location_area_maps[location_type]['area_type'],
                'belongWarehouseId': warehouse_id,
                'destWarehouseId': target_warehouse_id
            }
            wms_api_config['create_location']['data'].update(location_info)
            location_create_res = self.send_request(**wms_api_config['create_location'])
            if location_create_res['code'] != 200:
                log.error('创建库位失败:%s' % json.dumps(location_create_res, ensure_ascii=False))
                return
            location_codes.append(wms_api_config['create_location']['data']['warehouseLocationCode'])
        return location_codes


if __name__ == '__main__':
    ums = UmsController()
    wms = WmsController(ums)
    print(wms.get_switch_warehouse_data_perm_id(513))
    print(wms.switch_default_warehouse(513))
