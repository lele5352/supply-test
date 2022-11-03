import json
import time
from copy import deepcopy

from config.third_party_api_configs.wms_api_config import ReceiptApiConfig, DeliveryApiConfig, BaseApiConfig, \
    TransferApiConfig
from robots.robot import ServiceRobot, AppRobot
from dbo.wms_dbo import WMSDBOperator
from utils.log_handler import logger as log


class WMSAppRobot(AppRobot):
    def __init__(self):
        super().__init__(WMSDBOperator)

    def ck_id_to_code(self, warehouse_id):
        """
        根据仓库id获取仓库编码

        :param int warehouse_id: 仓库id
        """
        if not warehouse_id:
            return
        data = self.dbo.query_warehouse_info_by_id(warehouse_id)
        return data.get('warehouse_code')

    def ck_code_to_id(self, warehouse_code):
        """
        根据仓库编码获取仓库id

        :param string warehouse_code: 仓库编码
        """
        if not warehouse_code:
            return
        data = self.dbo.query_warehouse_info_by_code(warehouse_code)
        return data.get('id')

    def kw_id_to_code(self, kw_id):
        """
        根据库位id获取库位编码

        :param int kw_id: 库位id
        """
        data = self.dbo.query_warehouse_location_info_by_id(kw_id)
        return data.get('warehouse_location_code')

    def kw_code_to_id(self, kw_code):
        """
        根据库位编码获取库位id

        :param string kw_code: 库位编码
        """
        data = self.dbo.query_warehouse_location_info_by_code(kw_code)
        return data.get('id')

    def get_ck_area_id(self, warehouse_id, area_type):
        """
        获取指定区域类型的仓库区域id

        :param int warehouse_id: 仓库id
        :param int area_type: 区域类型
        """
        data = self.dbo.query_warehouse_area_info_by_type(warehouse_id, area_type)
        return str(data.get('id'))

    def mock_label_callback(self, delivery_order_code, package_list):
        """
        :param string delivery_order_code: 出库单号
        :param list package_list: 包裹列表

        """
        order_list = list()
        count = 0
        for package in package_list:
            count += 1
            temp_order_info = deepcopy(DeliveryApiConfig.LabelCallBack.get_attributes())
            temp_order_info['data']['orderList'][0].update({
                "deliveryNo": delivery_order_code,
                "packageNoList": [package],
                "logistyNo": "logistyNo" + str(int(time.time() * 1000 + count)),
                "barCode": "barCode" + str(int(time.time() * 1000 + count)),
                "turnOrderNo": str(int(time.time() * 1000)),
                "drawOrderNo": str(int(time.time() * 1000))
            })
            order_list.append(temp_order_info)
        res = self.label_callback(delivery_order_code, order_list)
        if res['code'] == 200:
            return True
        else:
            return False

    def query_delivery_order_package_list(self, delivery_order_code):
        data = self.dbo.query_delivery_order_package_info(delivery_order_code)
        package_no_list = [package['package_code'] for package in data]
        return package_no_list

    @classmethod
    def get_pick_sku_list(cls, pick_order_details):
        pick_sku_list = [(_['waresSkuCode'], _['shouldPickQty'], _['storageLocationId']) for _ in pick_order_details]

        pick_sku_list = sorted(pick_sku_list, key=lambda pick_sku: pick_sku[2])
        return pick_sku_list

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
            new_locations = self.create_location(num, kw_type, ck_id, to_ck_id)
            # 创建完缺口个数的库位后，重新获取库位
            location_data = WMSDBOperator.query_warehouse_locations(kw_type, num, ck_id, to_ck_id)
            if not new_locations:
                print('创建库位失败！')
                return self.report(0, False, {})
        elif num - len(location_data) > 0:
            # 库位不够，则新建对应缺少的库位
            new_locations = self.create_location(num - len(location_data), kw_type, ck_id, to_ck_id)
            if not new_locations:
                print('创建库位失败！')
                return self.report(0, False, {})
            # 创建完缺口个数的库位后，重新获取库位
            location_data = WMSDBOperator.query_warehouse_locations(kw_type, num, ck_id, to_ck_id)
        # 库位够的
        if return_type == 1:
            data = [location['id'] for location in location_data]

        else:
            data = [location['warehouse_location_code'] for location in location_data]
        return self.report(1, True, data)

    def get_warehouse_info_by_id(self, warehouse_id):
        """
        根据仓库编码获取仓库信息
        @param str warehouse_id : 仓库id
        @return : 仓库的信息
        """
        content = deepcopy(BaseApiConfig.GetWarehouseInfoById.get_attributes())
        content["uri_path"] += warehouse_id
        res_data = self.call_api(**content)

        if not res_data:
            return []
        return res_data["data"]

    def get_switch_warehouse_data_perm_id(self, warehouse_id):
        content = deepcopy(BaseApiConfig.GetSwitchWarehouseList.get_attributes())
        content['data'].update({
            't': int(time.time() * 1000)
        })
        res = self.call_api(**content)
        if not res:
            log.error("获取不到切换仓库列表！")
            return
        for perm in res['data']:
            if perm['dataId'] == warehouse_id:
                return perm['id']
        return

    def switch_default_warehouse(self, warehouse_id):
        data_perm_id = self.get_switch_warehouse_data_perm_id(warehouse_id)
        content = deepcopy(BaseApiConfig.SwitchDefaultWarehouse.get_attributes())
        content['data'].update({
            'dataPermId': data_perm_id
        })
        switch_res = self.call_api(**content)
        return self.formatted_result(switch_res)

    # 创建库位
    def create_location(self, num, kw_type, warehouse_id, target_warehouse_id=None) -> list or None:
        """
        创建库位

        @param int kw_type:
            1:收货库位 area_type:5(容器库区)
            2:质检库位 area_type:5(容器库区)
            3:托盘库位 area_type:5(容器库区)
            4:移库库位 area_type:5(容器库区)
            5:上架库位 area_type:1(上架库区)
            6:不良品库位 area_type:2(不良品库区)
            7:入库异常库位 area_type:3(入库异常库区)
            8:出库异常库位 area_type:4(出库异常库区)
        @param int num: 新建的库位数
        @param int warehouse_id: 所属仓库id
        @param int target_warehouse_id: 目的仓id
        @return: list 创建出来的库位列表
        """
        if warehouse_id == target_warehouse_id or target_warehouse_id == 0:
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
            area_info = self.dbo.query_warehouse_area_info_by_type(warehouse_id, kw_maps[kw_type][
                'area_type'])
            location_info = {
                'warehouseLocationCode': kw_maps[kw_type]['code_prefix'] + now,
                'warehouseLocationName': kw_maps[kw_type]['name_prefix'] + now,
                'warehouseLocationType': kw_type,
                'belongWarehouseAreaId': area_info.get('id'),
                'warehouseAreaType': kw_maps[kw_type]['area_type'],
                'belongWarehouseId': warehouse_id,
                'destWarehouseId': target_warehouse_id if kw_type != 6 else ''
            }
            content = deepcopy(BaseApiConfig.CreateLocation.get_attributes())
            content['data'].update(location_info)
            location_create_res = self.call_api(**content)
            if location_create_res['code'] != 200:
                log.error('创建库位失败:%s' % json.dumps(location_create_res, ensure_ascii=False))
                return
            location_codes.append(content['data']['warehouseLocationCode'])
        return location_codes

    def transfer_out_create_pick_order(self, demand_list, pick_type):
        """
        创建调拨拣货单
        @param list demand_list: 调拨需求列表
        @param int pick_type: 拣货方式: 1-纸质；2-PDA
        """
        content = deepcopy(TransferApiConfig.CreateTransferPickOrder.get_attributes())
        content['data'].update(
            {"demandCodes": demand_list, "pickType": pick_type, }
        )
        create_transfer_pick_order_res = self.call_api(**content)
        return self.formatted_result(create_transfer_pick_order_res)

    def transfer_out_pick_order_assign(self, pick_order_list, pick_username, pick_userid):
        """
        分配调拨拣货人
        @param list pick_order_list: 调拨拣货单列表
        @param int pick_userid: 拣货人id
        @param string pick_username: 拣货人名称
        """
        content = deepcopy(TransferApiConfig.TransferPickOrderAssign.get_attributes())
        content['data'].update(
            {
                "pickOrderNos": pick_order_list,
                "pickUsername": pick_username,
                "pickUserId": pick_userid
            }
        )
        assign_pick_user_res = self.call_api(**content)
        return self.formatted_result(assign_pick_user_res)

    def transfer_out_pick_order_detail(self, pick_order_code):
        """
        调拨拣货单详情
        @param string pick_order_code: 调拨拣货单号
        """
        t = int(time.time() * 1000)
        content = deepcopy(TransferApiConfig.TransferPickOrderDetail.get_attributes())
        content.update(
            {
                'uri_path': content['uri_path'] % pick_order_code,
                "data": {"t": t}
            }
        )
        detail_res = self.call_api(**content)
        return self.formatted_result(detail_res)

    def transfer_out_confirm_pick(self, pick_order_code, pick_order_details):
        """
        调拨拣货单确认拣货
        @param str pick_order_code: 拣货单号
        @param dict pick_order_details: 拣货单详情
        """
        # 通过获取拣货单明细，构造确认拣货不短拣情况下该传的参数
        details = [{
            'id': detail['id'],
            'goodsSkuCode': detail['goodsSkuCode'],
            'waresSkuCode': detail['waresSkuCode'],
            'realPickQty': detail['shouldPickQty']
        } for detail in pick_order_details]
        content = deepcopy(TransferApiConfig.TransferConfirmPick.get_attributes())
        content['data'].update(
            {
                "pickOrderNo": pick_order_code,
                "details": details
            }
        )
        confirm_pick_res = self.call_api(**content)
        return self.formatted_result(confirm_pick_res)

    def transfer_out_submit_tray(self, pick_order_code, pick_order_details, tp_kw_ids):
        """
        调拨按需装托
        @param str pick_order_code: 拣货单号
        @param dict pick_order_details: 拣货单详情数据
        @param list tp_kw_ids: 托盘库位id列表
        """
        # 获取托盘编码
        tp_kw_codes = [self.kw_id_to_code(kw_id) for kw_id in tp_kw_ids]
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
                        'skuQty': detail['shouldPickQty'],
                        'batchInfos': [{
                            'batchNo': '',
                            'skuQty': detail['shouldPickQty']
                        }]
                    }]
                }
            )
        content = deepcopy(TransferApiConfig.TransferSubmitTray.get_attributes())
        content.update({'data': tray_info_list})
        submit_tray_res = self.call_api(**content)
        return self.formatted_result(submit_tray_res)

    def transfer_out_pick_order_tray_detail(self, pick_order_no):
        """
        获取调拨拣货单装托明细
        @param string pick_order_no: 拣货单号
        """
        content = deepcopy(TransferApiConfig.TransferPickOrderTrayDetail.get_attributes())
        content.update(
            {'uri_path': content['uri_path'] % pick_order_no}
        )
        tray_detail_res = self.call_api(**content)
        return self.formatted_result(tray_detail_res)

    def transfer_out_finish_packing(self, pick_order_no, tray_list):
        """
        创建调拨出库单

        :param string pick_order_no: 拣货单号
        :param list tray_list: 托盘列表
        """
        content = deepcopy(TransferApiConfig.TransferFinishPacking.get_attributes())
        content['data'].update(
            {
                'pickOrderNo': pick_order_no,
                'storageLocationCodes': tray_list
            }
        )
        finish_packing_res = self.call_api(**content)
        return self.formatted_result(finish_packing_res)

    def transfer_out_order_detail(self, transfer_out_order_no):
        content = deepcopy(TransferApiConfig.TransferOutOrderDetail.get_attributes())

        content.update(
            {'uri_path': content['uri_path'] % transfer_out_order_no}
        )
        detail_res = self.call_api(**content)
        return self.formatted_result(detail_res)

    def transfer_out_order_review(self, box_no, tray_code):
        content = deepcopy(TransferApiConfig.TransferOutOrderReview.get_attributes())
        content['data'].update(
            {
                'boxNo': box_no,
                'storageLocationCode': tray_code
            }
        )
        review_res = self.call_api(**content)
        return self.formatted_result(review_res)

    def transfer_out_box_bind(self, box_no, handover_no, receive_warehouse_code):
        content = deepcopy(TransferApiConfig.TransferBoxBind.get_attributes())
        content['data'].update(
            {
                "boxNo": box_no,
                "handoverNo": handover_no,
                "receiveWarehouseCode": receive_warehouse_code
            }
        )
        bind_res = self.call_api(**content)
        return self.formatted_result(bind_res)

    def transfer_out_delivery(self, handover_no):
        content = deepcopy(TransferApiConfig.TransferDelivery.get_attributes())
        content['data'].update({"handoverNo": handover_no})
        delivery_res = self.call_api(**content)
        return self.formatted_result(delivery_res)

    def transfer_in_received(self, handover_no):
        content = deepcopy(TransferApiConfig.TransferInReceived.get_attributes())
        content['data'].update({"handoverNo": handover_no})
        received_res = self.call_api(**content)
        return self.formatted_result(received_res)

    def transfer_in_up_shelf(self, box_no, sj_kw_code):
        content = deepcopy(TransferApiConfig.TransferBoxUpShelf.get_attributes())

        content['data'].update(
            {
                "boxNo": box_no,
                "storageLocationCode": sj_kw_code
            })
        up_shelf_res = self.call_api(**content)
        return self.formatted_result(up_shelf_res)

    def label_callback(self, delivery_order_code, order_list):
        """
        :param string delivery_order_code: 出库单号
        :param list order_list: 出库单下的包裹物流单信息列表

        """
        content = deepcopy(DeliveryApiConfig.LabelCallBack.get_attributes())
        content['data'].update(
            {
                "deliveryNo": delivery_order_code,
                "orderList": order_list
            })
        callback_res = self.call_api(**content)
        return callback_res

    def entry_order_page(self, distribute_order_code_list):
        """
        @param list distribute_order_code_list: 分货单号列表
        """
        content = deepcopy(ReceiptApiConfig.EntryOrderPage.get_attributes())
        content['data'].update(
            {"distributeOrderCodeList": distribute_order_code_list}
        )
        res = self.call_api(**content)
        return self.formatted_result(res)

    def entry_order_detail(self, entry_order_code):
        """
        @param string entry_order_code: 分货单/入库单号
        """
        content = deepcopy(ReceiptApiConfig.EntryOrderDetail.get_attributes())
        content['uri_path'] = content['uri_path'] % entry_order_code
        res = self.call_api(**content)
        return self.formatted_result(res)

    def confirm_receive(self, entry_order_code, pre_receive_order_code, receive_sku_list):
        """
        @param pre_receive_order_code: 预售货单号
        @param entry_order_code: 入库单号
        @param dict receive_sku_list: 收货sku明细
        """
        content = deepcopy(ReceiptApiConfig.PreReceiveOrder.get_attributes())
        content['data'].update({
            "entryOrderCode": entry_order_code,
            "predictReceiptOrderCode": pre_receive_order_code,
            "skuList": receive_sku_list
        })

        res = self.call_api(**content)
        return self.formatted_result(res)

    def submit_pre_receive_order(self, pre_receive_order_list):
        """
        提交预收货单
        @param pre_receive_order_list: 预收货单号列表
        @return:
        """
        content = deepcopy(ReceiptApiConfig.SubmitPreReceiveOrder.get_attributes())
        content['data'].update({
            "predictReceiptOrderCodeList": pre_receive_order_list
        })
        res = self.call_api(**content)
        return self.formatted_result(res)

    def handover_to_upshelf(self, kw_codes):
        """
        上架交接
        @param kw_codes: 上架交接的库位编码列表
        @return:
        """
        content = deepcopy(ReceiptApiConfig.HandoverToUpShelf.get_attributes())
        content['data'].update(
            {
                "locationCodes": kw_codes
            }
        )
        res = self.call_api(**content)
        return self.formatted_result(res)

    def upshelf_whole_location(self, old_kw_code, sj_kw_code):
        """
        整托上架
        @param sj_kw_code: 上架库位
        @param old_kw_code: 原库位，可以是收货库位或者质检库位
        @return:
        """
        content = deepcopy(ReceiptApiConfig.UpShelfWholeLocation.get_attributes())
        content['data'].update(
            {
                "upshelfLocationCode": sj_kw_code,
                "oldLocationCode": old_kw_code
            }
        )
        res = self.call_api(**content)
        return self.formatted_result(res)

    def complete_upshelf(self):
        """
        上架完成
        @return:
        """
        content = deepcopy(ReceiptApiConfig.CompleteUpShelf.get_attributes())
        res = self.call_api(**content)
        return self.formatted_result(res)

    def location_detail(self, kw_code):
        """
        查询库位明细数据
        @return:
        """
        content = deepcopy(ReceiptApiConfig.LocationDetail.get_attributes())
        content['uri_path'] = content['uri_path'] % kw_code
        res = self.call_api(**content)
        return self.formatted_result(res)


class WMSTransferServiceRobot(ServiceRobot):
    def __init__(self):
        super().__init__("transfer")

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
        content = deepcopy(TransferApiConfig.CreateTransferDemand.get_attributes())
        content['data'].update(
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
        res_data = self.call_api(**content)
        return self.formatted_result(res_data)

    def get_demand_list(self, goods_list, trans_out_code, trans_out_to_code, trans_in_code, trans_in_to_code):
        demand_list = list()
        for sku, bom, qty in goods_list:
            demand_res = self.transfer_out_create_demand(
                trans_out_code,
                trans_out_to_code,
                trans_in_code,
                trans_in_to_code,
                sku,
                qty)
            if not demand_res['code']:
                log.error("创建调拨需求失败")
            demand_no = demand_res['data']['demandCode']
            demand_list.append(demand_no)
        return demand_list


class WMSDeliveryServiceRobot(ServiceRobot):
    def __init__(self):
        super().__init__("delivery")


if __name__ == '__main__':
    wms = WMSAppRobot()
    # print(wms.entry_order_page(["FH2211022680"]))
    for kw in ['SH1667384662143', 'SH1667384662515']:
        print(wms.location_detail(kw))
