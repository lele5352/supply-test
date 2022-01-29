import json
import time
from copy import deepcopy

from controller.ums_controller import UmsController
from config.sys_config import env_config
from config.api_config.wms_api_config import wms_api_config
from utils.request_handler import RequestHandler
from utils.mysql_handler import MysqlHandler
from utils.barcode_handler import barcode_generate
from utils.log_handler import logger as log


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

    def get_warehouse_area(self, search_field_dict) -> list:
        """
        :param dict search_field_dict:
            warehouseAreaStatus: 库区状态 ：不传-全部、0-启用、1-禁用
            warehouseAreaType 库区类型 int：不传-全部、1-上架区、2-不良品区、3-入库异常处理区、4-出库异常处理区、5-容器区；
            warehouseAreaCode 库区编码 string；
            warehouseAreaName 库区名称 string；
            warehouseId 仓库ID int；
        :return: list 搜索出来的库区信息列表
        """
        wms_api_config['get_warehouse_area']['data'].update(search_field_dict)
        res = self.send_request(**wms_api_config['get_warehouse_area'])
        area_info = res['data']['records']
        return area_info

    def get_warehouse_location(self, search_field_dict) -> list:
        """
        :param dict search_field_dict: 搜索条件字段值字典
            warehouseLocationStatus 库位状态 int：不传-全部、0-启用、1-禁用;
            warehouseAreaType 库区类型 int：不传-全部、1-上架区、2-不良品区、3-入库异常处理区、4-出库异常处理区、5-容器区;
            belongWareHouseAreaCode 所属库区 string;
            destWarehouseCode 目的仓库编码 string;
            warehouseLocationCode 库位编码 string;
            warehouseLocationName 库位名称 string;
            warehouseLocationType 库位类型 int：不传-全部、1-收货库位、2-质检库位、3-调拨库位、4-移库库位、5-上架库位、6-不良品库位、7-入库异常库位、8-出库异常库位;
            warehouseLocationUseStatus 库位使用状态 int：不传-全部、0-闲置、1-收货中、2-已质检交接、3-质检中、4-已上架交接、5-上架中、6-装托中、7-出库异常库位;
        :return: list 搜索出来的库位信息列表


        """
        wms_api_config['get_warehouse_location']['data'].update(search_field_dict)
        res = self.send_request(**wms_api_config['get_warehouse_location'])
        location_info = res['data']['records']
        return location_info

    def db_warehouse_id_to_code(self, warehouse_id):
        if not warehouse_id:
            return
        sql = "select warehouse_code from base_warehouse where id=%s" % warehouse_id
        data = self.db.get_one(sql)
        return data['warehouse_code']

    def db_location_id_to_code(self, location_id):
        sql = "select warehouse_location_code from base_warehouse_location where id=%s" % location_id
        data = self.db.get_one(sql)
        return data['warehouse_location_code']

    def db_get_location_ids(self, location_type, num, warehouse_id, target_warehouse_id=None):
        if target_warehouse_id:
            temp_sql = "AND dest_warehouse_id = %s" % target_warehouse_id
        else:
            temp_sql = "AND dest_warehouse_id is NULL"
        query_location_id_sql = """
            SELECT 
                id 
            FROM 
                base_warehouse_location 
            WHERE 
                state = 0 
                AND type = %s 
                AND warehouse_id = %s 
                %s 
                LIMIT %s 
        """ % (location_type, warehouse_id, temp_sql, num)

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
    def create_location(self, num, location_type, warehouse_id, target_warehouse_id=None) -> list or None:
        """
        :param int location_type: 库位类型：1-收货库位 2-质检库位 3-调拨库位 4-移库库位 5-上架库位 6-不良品库位 7-入库异常库位 8-出库异常库位
            库位类型对应的库区类型
            1-收货库位 类型：容器库区-5
            2-质检库位 类型：容器库区-5
            3-调拨库位 类型：容器库区-5
            4-移库库位 类型：容器库区-5
            5-上架库位 类型：上架库区-1
            6-不良品库位 类型：不良品库区-2
            7-入库异常库位 类型：入库异常库区-3
            8-出库异常库位 类型：出库异常库区-4
        :param int num: 新建的库位数
        :param int warehouse_id: 所属仓库id
        :param int target_warehouse_id: 目的仓id
        :return: list 创建出来的库位列表
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

    def create_transfer_pick_order(self, demand_list, pick_type):
        """
        创建调拨拣货单

        :param list demand_list: 调拨需求列表
        :param int pick_type: 拣货方式：1-纸质；2-PDA
        """
        wms_api_config['create_transfer_pick_order']['data'].update(
            {
                "demandCodes": demand_list,
                "pickType": pick_type,
            }
        )
        create_transfer_pick_order_res = self.send_request(**wms_api_config['create_transfer_pick_order'])
        return create_transfer_pick_order_res

    def transfer_pick_order_assign_pick_user(self, pick_order_list, pick_username, pick_userid):
        """
        分配调拨拣货人

        :param list pick_order_list: 调拨拣货单列表
        :param int pick_userid: 拣货人id
        :param string pick_username: 拣货人名称
        """
        wms_api_config['transfer_pick_order_assign_pick_user']['data'].update(
            {
                "pickOrderNos": pick_order_list,
                "pickUsername": pick_username,
                "pickUserId": pick_userid
            }
        )
        assign_pick_user_res = self.send_request(**wms_api_config['transfer_pick_order_assign_pick_user'])
        return assign_pick_user_res

    def transfer_pick_order_detail(self, pick_order_code):
        """
        调拨拣货单详情

        :param string pick_order_code: 调拨拣货单号
        """
        t = int(time.time() * 1000)
        data = deepcopy(wms_api_config['transfer_pick_order_detail'])
        data.update(
            {
                'uri_path': data['uri_path'] % pick_order_code,
                "data": {"t": t}
            }
        )
        detail_res = self.send_request(**data)
        return detail_res['data']

    def transfer_pick_order_confirm_pick(self, pick_order_details):
        """
        调拨拣货单确认拣货

        :param dict pick_order_details: 拣货单详情
        """
        # 通过获取拣货单明细，构造确认拣货不短拣情况下该传的参数
        details = list()
        for detail in pick_order_details['details']:
            details.append({
                'id': detail['id'],
                'goodsSkuCode': detail['goodsSkuCode'],
                'waresSkuCode': detail['waresSkuCode'],
                'realPickQty': detail['shouldPickQty']
            })
        wms_api_config['transfer_confirm_pick']['data'].update(
            {
                "pickOrderNo": pick_order_details['pickOrderNo'],
                "details": details
            }
        )
        confirm_pick_res = self.send_request(**wms_api_config['transfer_confirm_pick'])
        return confirm_pick_res

    def transfer_submit_tray(self, pick_order_details, tp_location_ids):
        """
        调拨按需装托

        :param dict pick_order_details: 拣货单详情数据
        :param string tp_location_ids: 托盘库位id列表
        """
        # 获取托盘编码
        tp_location_codes = [self.db_location_id_to_code(location_id) for location_id in tp_location_ids]
        # 通过获取拣货单明细，构造确认拣货不短拣情况下该传的参数
        tray_info_list = list()
        for detail, code in zip(pick_order_details['details'], tp_location_codes):
            tray_info_list.append(
                {
                    'storageLocationCode': code,
                    'pickOrderNo': pick_order_details['pickOrderNo'],
                    'trayInfos': [{
                        'waresSkuCode': detail['waresSkuCode'],
                        'goodsSkuCode': detail['goodsSkuCode'],
                        'skuQty': detail['shouldPickQty']
                    }]
                }
            )
        wms_api_config['transfer_submit_tray'].update(
            {
                'data': tray_info_list
            }
        )
        submit_tray_res = self.send_request(**wms_api_config['transfer_submit_tray'])
        return submit_tray_res


if __name__ == '__main__':
    ums = UmsController()
    wms = WmsController(ums)
    res = wms.transfer_pick_order_detail('DJH2201280001')
    print(res)
