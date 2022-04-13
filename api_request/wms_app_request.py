import json
import time
from copy import deepcopy

from config.sys_config import env_config
from config.api_config.wms_api_config import wms_api_config
from utils.request_handler import RequestHandler
from db_operator.wms_db_operator import WMSDBOperator
from utils.log_handler import logger as log

from api_request.wms_transfer_request import WmsTransferRequest


class WmsAppRequest(RequestHandler):
    def __init__(self, app_headers, service_headers):
        self.prefix = env_config.get('app_prefix')
        self.transfer = WmsTransferRequest(service_headers)
        super().__init__(self.prefix, app_headers)

    def get_switch_warehouse_data_perm_id(self, warehouse_id):
        wms_api_config['get_switch_warehouse_list']['data'].update({
            't': int(time.time() * 1000)
        })
        res = self.send_request(**wms_api_config['get_switch_warehouse_list'])
        if not res:
            log.error("获取不到切换仓库列表！")
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
        switch_res = self.send_request(**wms_api_config['switch_default_warehouse'])
        if not switch_res:
            log.error('切换仓库失败！')
            return
        return True

    # 创建库位
    def create_location(self, num, kw_type, warehouse_id, target_warehouse_id=None) -> list or None:
        """
        创建库位

        :param int kw_type:
            1:收货库位 area_type:5(容器库区)
            2:质检库位 area_type:5(容器库区)
            3:托盘库位 area_type:5(容器库区)
            4:移库库位 area_type:5(容器库区)
            5:上架库位 area_type:1(上架库区)
            6:不良品库位 area_type:2(不良品库区)
            7:入库异常库位 area_type:3(入库异常库区)
            8:出库异常库位 area_type:4(出库异常库区)
        :param int num: 新建的库位数
        :param int warehouse_id: 所属仓库id
        :param int target_warehouse_id: 目的仓id
        :return: list 创建出来的库位列表
        """
        if warehouse_id == target_warehouse_id:
            target_warehouse_id = ''
        self.switch_default_warehouse(warehouse_id)
        kw_maps = {
            1: {"area_type": 5, "code_prefix": "SH", "name_prefix": "SHN"},
            2: {"area_type": 5, "code_prefix": "ZJ", "name_prefix": "ZJN"},
            3: {"area_type": 5, "code_prefix": "TP", "name_prefix": "TPN"},
            4: {"area_type": 5, "code_prefix": "YK", "name_prefix": "YKN"},
            5: {"area_type": 1, "code_prefix": "SJ", "name_prefix": "SJN"},
            6: {"area_type": 2, "code_prefix": "CP", "name_prefix": "CPN"},
            7: {"area_type": 3, "code_prefix": "RYC", "name_prefix": "RYCN"},
            8: {"area_type": 4, "code_prefix": "CYC", "name_prefix": "CYCN"}
        }

        location_codes = list()
        for i in range(num):
            now = str(int(time.time() * 1000))
            location_info = {
                'warehouseLocationCode': kw_maps[kw_type]['code_prefix'] + now,
                'warehouseLocationName': kw_maps[kw_type]['name_prefix'] + now,
                'warehouseLocationType': kw_type,
                'belongWarehouseAreaId': WMSDBOperator.query_warehouse_area_info_by_type(warehouse_id, kw_maps[kw_type][
                    'area_type']).get('id'),

                'warehouseAreaType': kw_maps[kw_type]['area_type'],
                'belongWarehouseId': warehouse_id,
                'destWarehouseId': target_warehouse_id if kw_type != 6 else ''
            }
            wms_api_config['create_location']['data'].update(location_info)
            location_create_res = self.send_request(**wms_api_config['create_location'])
            if location_create_res['code'] != 200:
                log.error('创建库位失败:%s' % json.dumps(location_create_res, ensure_ascii=False))
                return
            location_codes.append(wms_api_config['create_location']['data']['warehouseLocationCode'])
        return location_codes

    def transfer_out_create_demand(self, trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id, sale_sku_code,
                                   trans_qty, demand_type=1, customer_type=1, remark=''):
        """
            创建调拨需求

            :param int trans_out_id: 调出仓库id
            :param int trans_in_id: 调入仓库id
            :param int trans_out_to_id: 调出仓库的目的仓id
            :param int trans_in_to_id: 调入仓库的目的仓id
            :param string sale_sku_code: 调拨的商品的销售sku
            :param int trans_qty: 调拨数量
            :param int demand_type: 调拨类型
            :param int customer_type: 客户类型：1-普通客户；2-大客户
            :param string remark: 备注
        """
        create_demand_res = self.transfer.transfer_out_create_demand(
            WMSDBOperator.query_warehouse_info_by_id(trans_out_id).get('warehouse_code'),
            WMSDBOperator.query_warehouse_info_by_id(trans_out_to_id).get('warehouse_code'),
            WMSDBOperator.query_warehouse_info_by_id(trans_in_id).get('warehouse_code'),
            WMSDBOperator.query_warehouse_info_by_id(trans_in_to_id).get('warehouse_code'),
            sale_sku_code,
            trans_qty,
            demand_type,
            customer_type,
            remark)
        return create_demand_res

    def transfer_out_create_pick_order(self, demand_list, pick_type):
        """
        创建调拨拣货单

        :param list demand_list: 调拨需求列表
        :param int pick_type: 拣货方式: 1-纸质；2-PDA
        """
        wms_api_config['create_transfer_pick_order']['data'].update(
            {
                "demandCodes": demand_list,
                "pickType": pick_type,
            }
        )
        create_transfer_pick_order_res = self.send_request(**wms_api_config['create_transfer_pick_order'])
        return create_transfer_pick_order_res

    def transfer_out_pick_order_assign(self, pick_order_list, pick_username, pick_userid):
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

    def transfer_out_pick_order_detail(self, pick_order_code):
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

    def transfer_out_confirm_pick(self, pick_order_code, pick_order_details):
        """
        调拨拣货单确认拣货
        :param str pick_order_code: 拣货单号
        :param dict pick_order_details: 拣货单详情
        """
        # 通过获取拣货单明细，构造确认拣货不短拣情况下该传的参数
        details = list()
        for detail in pick_order_details:
            details.append({
                'id': detail['id'],
                'goodsSkuCode': detail['goodsSkuCode'],
                'waresSkuCode': detail['waresSkuCode'],
                'realPickQty': detail['shouldPickQty']
            })
        wms_api_config['transfer_confirm_pick']['data'].update(
            {
                "pickOrderNo": pick_order_code,
                "details": details
            }
        )
        confirm_pick_res = self.send_request(**wms_api_config['transfer_confirm_pick'])
        return confirm_pick_res

    def transfer_out_submit_tray(self, pick_order_code, pick_order_details, tp_kw_ids):
        """
        调拨按需装托

        :param str pick_order_code: 拣货单号
        :param dict pick_order_details: 拣货单详情数据
        :param list tp_kw_ids: 托盘库位id列表
        """
        # 获取托盘编码
        tp_kw_codes = [WMSDBOperator.query_warehouse_location_info_by_id(kw_id).get('warehouse_location_code') for kw_id
                       in tp_kw_ids]
        # 通过获取拣货单明细，构造确认拣货不短拣情况下该传的参数
        tray_info_list = list()
        for detail, code in zip(pick_order_details, tp_kw_codes):
            tray_info_list.append(
                {
                    'storageLocationCode': code,
                    'pickOrderNo': pick_order_code,
                    'trayInfos': [{
                        'waresSkuCode': detail['waresSkuCode'],
                        'goodsSkuCode': detail['goodsSkuCode'],
                        'skuQty': detail['shouldPickQty']
                    }]
                }
            )
        wms_api_config['transfer_submit_tray'].update({'data': tray_info_list})
        submit_tray_res = self.send_request(**wms_api_config['transfer_submit_tray'])
        return submit_tray_res

    def transfer_out_pick_order_tray_detail(self, pick_order_no):
        """
        获取调拨拣货单装托明细

        :param string pick_order_no: 拣货单号
        """
        data = deepcopy(wms_api_config['transfer_pick_order_tray_detail'])
        data.update(
            {'uri_path': wms_api_config['transfer_pick_order_tray_detail']['uri_path'] % pick_order_no}
        )
        tray_detail_res = self.send_request(**data)
        return tray_detail_res

    def transfer_out_finish_packing(self, pick_order_no, tray_list):
        """
        创建调拨出库单

        :param string pick_order_no: 拣货单号
        :param list tray_list: 托盘列表
        """
        wms_api_config['transfer_finish_packing']['data'].update(
            {
                'pickOrderNo': pick_order_no,
                'storageLocationCodes': tray_list
            }
        )
        finish_packing_res = self.send_request(**wms_api_config['transfer_finish_packing'])
        return finish_packing_res

    def transfer_out_order_detail(self, transfer_out_order_no):
        data = deepcopy(wms_api_config['transfer_out_order_detail'])
        data.update(
            {'uri_path': wms_api_config['transfer_out_order_detail']['uri_path'] % transfer_out_order_no}
        )
        detail_res = self.send_request(**data)
        return detail_res

    def transfer_out_order_review(self, box_no, tray_code):
        wms_api_config['transfer_out_order_review']['data'].update(
            {
                'boxNo': box_no,
                'storageLocationCode': tray_code
            }
        )
        review_res = self.send_request(**wms_api_config['transfer_out_order_review'])
        return review_res

    def transfer_out_box_bind(self, box_no, handover_no, receive_warehouse_code):
        wms_api_config['transfer_box_bind']['data'].update(
            {
                "boxNo": box_no,
                "handoverNo": handover_no,
                "receiveWarehouseCode": receive_warehouse_code
            }
        )
        bind_res = self.send_request(**wms_api_config['transfer_box_bind'])
        return bind_res

    def transfer_out_delivery(self, handover_no):
        wms_api_config['transfer_delivery']['data'].update({"handoverNo": handover_no})
        delivery_res = self.send_request(**wms_api_config['transfer_delivery'])
        return delivery_res

    def transfer_in_received(self, handover_no):
        wms_api_config['transfer_in_received']['data'].update({"handoverNo": handover_no})
        received_res = self.send_request(**wms_api_config['transfer_in_received'])
        return received_res

    def transfer_in_up_shelf(self, box_no, sj_kw_code):
        wms_api_config['transfer_box_up_shelf']['data'].update(
            {
                "boxNo": box_no,
                "storageLocationCode": sj_kw_code
            })
        up_shelf_res = self.send_request(**wms_api_config['transfer_box_up_shelf'])
        return up_shelf_res

