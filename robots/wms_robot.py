import json
import time
from copy import deepcopy

from config.third_party_api_configs.wms_api_config import *
from robots.robot import ServiceRobot, AppRobot
from dbo.wms_dbo import WMSDBOperator
from utils.log_handler import logger as log
from utils.time_handler import HumanDateTime


class WMSAppRobot(AppRobot):
    def __init__(self):
        self.dbo = WMSDBOperator
        super().__init__()

    def db_ck_id_to_code(self, warehouse_id):
        """
        根据仓库id获取仓库编码

        :param int warehouse_id: 仓库id
        """
        if not warehouse_id:
            return
        data = self.dbo.query_warehouse_info_by_id(warehouse_id)
        return data.get("warehouse_code")

    def db_ck_code_to_id(self, warehouse_code):
        """
        根据仓库编码获取仓库id

        :param string warehouse_code: 仓库编码
        """
        if not warehouse_code:
            return
        data = self.dbo.query_warehouse_info_by_code(warehouse_code)
        return data.get("id")

    def db_kw_id_to_code(self, kw_id):
        """
        根据库位id获取库位编码

        :param int kw_id: 库位id
        """
        data = self.dbo.query_warehouse_location_info_by_id(kw_id)
        return data.get("warehouse_location_code")

    def db_kw_code_to_id(self, kw_code):
        """
        根据库位编码获取库位id

        :param string kw_code: 库位编码
        """
        data = self.dbo.query_warehouse_location_info_by_code(kw_code)
        return data.get("id")

    def db_get_ck_area_id(self, warehouse_id, area_type):
        """
        获取指定区域类型的仓库区域id

        :param int warehouse_id: 仓库id
        :param int area_type: 区域类型
        """
        data = self.dbo.query_warehouse_area_info_by_type(warehouse_id, area_type)
        return str(data.get("id"))

    def db_get_delivery_order_package_list(self, delivery_order_code):
        data = self.dbo.query_delivery_order_package_info(delivery_order_code)
        package_no_list = [package["package_code"] for package in data]
        return package_no_list

    def db_get_kw(self, kw_type, num, ck_id, to_ck_id):
        """
        获取指定库位类型、指定目的仓、指定数量的仓库库位
        :param int kw_type: 库位类型
        :param int num: 获取的库位个数
        :param int ck_id: 库位的所属仓库id
        :param to_ck_id: 库位的目的仓id
        """
        location_data = self.dbo.query_warehouse_locations(kw_type, num, ck_id, to_ck_id)
        return location_data

    def base_get_kw(self, return_type, kw_type, num, ck_id, to_ck_id):
        """
        获取指定库位类型、指定目的仓、指定数量的仓库库位

        :param int return_type: 1-返回库位id；2-返回库位编码
        :param int kw_type: 库位类型
        :param int num: 获取的库位个数
        :param int ck_id: 库位的所属仓库id
        :param to_ck_id: 库位的目的仓id
        """
        location_data = self.db_get_kw(kw_type, num, ck_id, to_ck_id)

        if not location_data:
            new_locations = self.base_create_location(num, kw_type, ck_id, to_ck_id)
            if not new_locations:
                print("无库位，创建库位失败！")
                return self.report(0, False, {})
            # 创建完缺口个数的库位后，重新获取库位
            location_data = WMSDBOperator.query_warehouse_locations(kw_type, num, ck_id, to_ck_id)
        elif num - len(location_data) > 0:
            # 库位不够，则新建对应缺少的库位
            new_locations = self.base_create_location(num - len(location_data), kw_type, ck_id, to_ck_id)
            if not new_locations:
                print("缺库位，创建库位失败！")
                return self.report(0, False, {})
            # 创建完缺口个数的库位后，重新获取库位
            location_data = WMSDBOperator.query_warehouse_locations(kw_type, num, ck_id, to_ck_id)
        # 库位够的
        if return_type == 1:
            data = [location["id"] for location in location_data]

        else:
            data = [location["warehouse_location_code"] for location in location_data]
        return self.report(1, True, data)

    def base_get_warehouse_info_by_id(self, warehouse_id):
        """
        根据仓库编码获取仓库信息
        :param str warehouse_id : 仓库id
        :return : 仓库的信息
        """
        content = deepcopy(BaseApiConfig.GetWarehouseInfoById.get_attributes())
        content["uri_path"] += warehouse_id
        res_data = self.call_api(**content)

        if not res_data:
            return []
        return res_data["data"]

    def common_get_data_perm_id(self, warehouse_id):
        content = deepcopy(BaseApiConfig.GetSwitchWarehouseList.get_attributes())
        content["data"].update({
            "t": int(time.time() * 1000)
        })
        res = self.call_api(**content)
        if not res:
            log.error("获取不到切换仓库列表！")
            return
        for perm in res["data"]:
            if perm["dataId"] == int(warehouse_id):
                return perm["id"]
        return

    def common_switch_warehouse(self, warehouse_id):
        data_perm_id = self.common_get_data_perm_id(warehouse_id)
        content = deepcopy(BaseApiConfig.SwitchDefaultWarehouse.get_attributes())
        content["data"].update({
            "dataPermId": data_perm_id
        })
        switch_res = self.call_api(**content)
        return self.formatted_result(switch_res)

    # 创建库位
    def base_create_location(self, num, kw_type, warehouse_id, target_warehouse_id=None) -> list or None:
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
        if warehouse_id == target_warehouse_id or target_warehouse_id == 0:
            target_warehouse_id = ""
        self.common_switch_warehouse(warehouse_id)
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
                "area_type"])
            if not area_info:
                return
            location_info = {
                "warehouseLocationCode": kw_maps[kw_type]["code_prefix"] + now,
                "warehouseLocationName": kw_maps[kw_type]["name_prefix"] + now,
                "warehouseLocationType": kw_type,
                "belongWarehouseAreaId": area_info.get("id"),
                "warehouseAreaType": kw_maps[kw_type]["area_type"],
                "belongWarehouseId": warehouse_id,
                "destWarehouseId": target_warehouse_id if kw_type != 6 else ""
            }
            content = deepcopy(BaseApiConfig.CreateLocation.get_attributes())
            content["data"].update(location_info)
            location_create_res = self.call_api(**content)
            if location_create_res["code"] != 200:
                log.error("创建库位失败:%s" % json.dumps(location_create_res, ensure_ascii=False))
                return
            location_codes.append(content["data"]["warehouseLocationCode"])
        return location_codes

    def transfer_out_create_pick_order(self, demand_list, pick_type):
        """
        创建调拨拣货单
        :param list demand_list: 调拨需求列表
        :param int pick_type: 拣货方式: 1-纸质；2-PDA
        """
        content = deepcopy(TransferApiConfig.CreateTransferPickOrder.get_attributes())
        content["data"].update(
            {"demandCodes": demand_list, "pickType": pick_type, }
        )
        create_transfer_pick_order_res = self.call_api(**content)
        return self.formatted_result(create_transfer_pick_order_res)

    @classmethod
    def transfer_get_pick_sku_list(cls, pick_order_details):
        pick_sku_list = [(_["waresSkuCode"], _["shouldPickQty"], _["storageLocationId"]) for _ in pick_order_details]

        pick_sku_list = sorted(pick_sku_list, key=lambda pick_sku: pick_sku[2])
        return pick_sku_list

    def transfer_out_pick_order_assign(self, pick_order_list, pick_username, pick_userid):
        """
        分配调拨拣货人
        :param list pick_order_list: 调拨拣货单列表
        :param int pick_userid: 拣货人id
        :param string pick_username: 拣货人名称
        """
        content = deepcopy(TransferApiConfig.TransferPickOrderAssign.get_attributes())
        content["data"].update(
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
        :param string pick_order_code: 调拨拣货单号
        """
        t = int(time.time() * 1000)
        content = deepcopy(TransferApiConfig.TransferPickOrderDetail.get_attributes())
        content.update(
            {
                "uri_path": content["uri_path"] % pick_order_code,
                "data": {"t": t}
            }
        )
        detail_res = self.call_api(**content)
        return self.formatted_result(detail_res)

    def transfer_out_confirm_pick(self, pick_order_code, pick_order_details):
        """
        调拨拣货单确认拣货
        :param str pick_order_code: 拣货单号
        :param dict pick_order_details: 拣货单详情
        """
        # 通过获取拣货单明细，构造确认拣货不短拣情况下该传的参数
        details = [{
            "id": detail["id"],
            "goodsSkuCode": detail["goodsSkuCode"],
            "waresSkuCode": detail["waresSkuCode"],
            "realPickQty": detail["shouldPickQty"]
        } for detail in pick_order_details]
        content = deepcopy(TransferApiConfig.TransferConfirmPick.get_attributes())
        content["data"].update(
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
        :param str pick_order_code: 拣货单号
        :param dict pick_order_details: 拣货单详情数据
        :param list tp_kw_ids: 托盘库位id列表
        """
        # 获取托盘编码
        tp_kw_codes = [self.db_kw_id_to_code(kw_id) for kw_id in tp_kw_ids]
        # 通过获取拣货单明细，构造确认拣货不短拣情况下该传的参数
        tray_info_list = list()
        for detail, code in zip(pick_order_details, tp_kw_codes):
            tray_info_list.append(
                {
                    "storageLocationCode": code,
                    "pickOrderNo": pick_order_code,
                    "trayInfos": [{
                        "waresSkuCode": detail["waresSkuCode"],
                        "goodsSkuCode": detail["goodsSkuCode"],
                        "skuQty": detail["shouldPickQty"],
                        "batchInfos": [{
                            "batchNo": "",
                            "skuQty": detail["shouldPickQty"]
                        }]
                    }]
                }
            )
        content = deepcopy(TransferApiConfig.TransferSubmitTray.get_attributes())
        content.update({"data": tray_info_list})
        submit_tray_res = self.call_api(**content)
        return self.formatted_result(submit_tray_res)

    def transfer_out_pick_order_tray_detail(self, pick_order_no):
        """
        获取调拨拣货单装托明细
        :param string pick_order_no: 拣货单号
        """
        content = deepcopy(TransferApiConfig.TransferPickOrderTrayDetail.get_attributes())
        content.update(
            {"uri_path": content["uri_path"] % pick_order_no}
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
        content["data"].update(
            {
                "pickOrderNo": pick_order_no,
                "storageLocationCodes": tray_list
            }
        )
        finish_packing_res = self.call_api(**content)
        return self.formatted_result(finish_packing_res)

    def transfer_out_order_detail(self, transfer_out_order_no):
        content = deepcopy(TransferApiConfig.TransferOutOrderDetail.get_attributes())

        content.update(
            {"uri_path": content["uri_path"] % transfer_out_order_no}
        )
        detail_res = self.call_api(**content)
        return self.formatted_result(detail_res)

    def transfer_out_order_review(self, box_no, tray_code):
        content = deepcopy(TransferApiConfig.TransferOutOrderReview.get_attributes())
        content["data"].update(
            {
                "boxNo": box_no,
                "storageLocationCode": tray_code
            }
        )
        review_res = self.call_api(**content)
        return self.formatted_result(review_res)

    def transfer_out_box_bind(self, box_no, handover_no, receive_warehouse_code):
        content = deepcopy(TransferApiConfig.TransferBoxBind.get_attributes())
        content["data"].update(
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
        content["data"].update({"handoverNo": handover_no})
        delivery_res = self.call_api(**content)
        return self.formatted_result(delivery_res)

    def transfer_in_received(self, handover_no):
        content = deepcopy(TransferApiConfig.TransferInReceived.get_attributes())
        content["data"].update({"handoverNo": handover_no})
        received_res = self.call_api(**content)
        return self.formatted_result(received_res)

    def transfer_in_up_shelf(self, box_no, sj_kw_code):
        content = deepcopy(TransferApiConfig.TransferBoxUpShelf.get_attributes())

        content["data"].update(
            {
                "boxNo": box_no,
                "storageLocationCode": sj_kw_code
            })
        up_shelf_res = self.call_api(**content)
        return self.formatted_result(up_shelf_res)

    def receipt_entry_order_page(self, distribute_order_code_list):
        """
        :param list distribute_order_code_list: 分货单号列表
        """
        content = deepcopy(ReceiptApiConfig.EntryOrderPage.get_attributes())
        content["data"].update(
            {"distributeOrderCodeList": distribute_order_code_list}
        )
        res = self.call_api(**content)
        return self.formatted_result(res)

    def receipt_entry_order_detail(self, entry_order_code):
        """
        :param string entry_order_code: 分货单/入库单号
        """
        content = deepcopy(ReceiptApiConfig.EntryOrderDetail.get_attributes())
        content["uri_path"] = content["uri_path"] % entry_order_code
        res = self.call_api(**content)
        return self.formatted_result(res)

    def receipt_confirm_receive(self, entry_order_code, pre_receive_order_code, receive_sku_list):
        """
        :param pre_receive_order_code: 预售货单号
        :param entry_order_code: 入库单号
        :param dict receive_sku_list: 收货sku明细
        """
        content = deepcopy(ReceiptApiConfig.PreReceiveOrder.get_attributes())
        content["data"].update({
            "entryOrderCode": entry_order_code,
            "predictReceiptOrderCode": pre_receive_order_code,
            "skuList": receive_sku_list
        })

        res = self.call_api(**content)
        return self.formatted_result(res)

    def receipt_submit_pre_receive_order(self, pre_receive_order_list):
        """
        提交预收货单
        :param pre_receive_order_list: 预收货单号列表
        :return:
        """
        content = deepcopy(ReceiptApiConfig.SubmitPreReceiveOrder.get_attributes())
        content["data"].update({
            "predictReceiptOrderCodeList": pre_receive_order_list
        })
        res = self.call_api(**content)
        return self.formatted_result(res)

    def receipt_handover_to_upshelf(self, kw_codes):
        """
        上架交接
        :param kw_codes: 上架交接的库位编码列表
        :return:
        """
        content = deepcopy(ReceiptApiConfig.HandoverToUpShelf.get_attributes())
        content["data"].update(
            {
                "locationCodes": kw_codes
            }
        )
        res = self.call_api(**content)
        return self.formatted_result(res)

    def receipt_handover_to_quality_check(self, kw_codes):
        """
        上架交接
        :param kw_codes: 质检交接的库位编码列表
        :return:
        """
        content = deepcopy(ReceiptApiConfig.HandoverToQualityCheck.get_attributes())
        content["data"].update(
            {
                "locationCodes": kw_codes
            }
        )
        res = self.call_api(**content)
        return self.formatted_result(res)

    def receipt_get_quality_check_location_detail(self, kw_code):
        """
        获取收货库位中待质检sku信息
        :param kw_code: 收货库位编码
        :return:
        """
        content = deepcopy(ReceiptApiConfig.QualityCheckLocationDetail.get_attributes())
        content["data"].update(
            {
                "locationCode": kw_code
            }
        )
        res = self.call_api(**content)
        return self.formatted_result(res)

    def receipt_upshelf_whole_location(self, old_kw_code, sj_kw_code):
        """
        整托上架
        :param sj_kw_code: 上架库位
        :param old_kw_code: 原库位，可以是收货库位或者质检库位
        :return:
        """
        content = deepcopy(ReceiptApiConfig.UpShelfWholeLocation.get_attributes())
        content["data"].update(
            {
                "upshelfLocationCode": sj_kw_code,
                "oldLocationCode": old_kw_code
            }
        )
        res = self.call_api(**content)
        return self.formatted_result(res)

    def receipt_complete_upshelf(self):
        """
        上架完成
        :return:
        """
        content = deepcopy(ReceiptApiConfig.CompleteUpShelf.get_attributes())
        res = self.call_api(**content)
        return self.formatted_result(res)

    def receipt_location_detail(self, kw_code):
        """
        查询库位明细数据
        :return:
        """
        content = deepcopy(ReceiptApiConfig.LocationDetail.get_attributes())
        content["uri_path"] = content["uri_path"] % kw_code
        res = self.call_api(**content)
        return self.formatted_result(res)

    def receipt_quality_location_bind(self, sh_kw_code, zj_kw_code, received_order_code):
        """
        录入质检结果时绑定质检库位、收货库位、收货单
        :param sh_kw_code: 收货库位编码
        :param zj_kw_code: 质检库位编码
        :param received_order_code: 收货单编码
        :return:
        """
        content = deepcopy(ReceiptApiConfig.QualityCheckLocationBind.get_attributes())
        content["data"].update({
            "receiveLocationCode": sh_kw_code,
            "qcLocationCode": zj_kw_code,
            "receiveOrderCode": received_order_code
        })
        res = self.call_api(**content)
        return self.formatted_result(res)

    def receipt_quality_check_submit(self, sku_list):
        """
        录入质检结构后提交质检
        :param sku_list: 提交质检的sku信息列表
        :return:
        """
        content = deepcopy(ReceiptApiConfig.QualityCheckSubmit.get_attributes())
        content["data"].update({
            "skuList": sku_list
        })
        res = self.call_api(**content)
        return self.formatted_result(res)

    def delivery_get_delivery_order_page(self, delivery_order_code_list):
        """
        销售出库单详情
        :param list delivery_order_code_list: 销售出库单编码列表
        :return:
        """
        content = deepcopy(DeliveryApiConfig.DeliveryOrderPage.get_attributes())
        content["data"].update({
            "deliveryOrderCodeList": delivery_order_code_list
        })
        res = self.call_api(**content)
        return self.formatted_result(res)

    def delivery_get_delivery_order_detail(self, delivery_order_id):
        """
        销售出库单详情
        :param int delivery_order_id: 销售出库单id
        :return:
        """
        content = deepcopy(DeliveryApiConfig.DeliveryOrderDetail.get_attributes())
        content["uri_path"] = content["uri_path"].format(delivery_order_id)
        content["data"].update({
            "t": int(time.time() * 1000)
        })
        res = self.call_api(**content)
        return self.formatted_result(res)

    def delivery_assign_stock(self, delivery_order_code_list):
        """
        销售出库单分配库存
        :param list delivery_order_code_list: 销售出库单号列表
        :return:
        """
        content = deepcopy(DeliveryApiConfig.AssignStock.get_attributes())
        content["data"].update({
            "deliveryOrderCodes": delivery_order_code_list
        })
        res = self.call_api(**content)
        return self.formatted_result(res)

    def delivery_mock_label_callback(self, delivery_order_code, package_list, same_label=False):
        """
        :param same_label: 是否需要包裹都相同运单号，默认为否
        :param string delivery_order_code: 出库单号
        :param list package_list: 包裹列表

        """
        order_list = list()
        count = 0
        content = deepcopy(DeliveryApiConfig.LabelCallBack.get_attributes())
        tail_fix = str(int(time.time() * 1000))
        if same_label:
            temp_order_info = deepcopy(content["data"]["orderList"][0])
            temp_order_info.update({
                "deliveryNo": delivery_order_code,
                "packageNoList": [package for package in package_list],
                "logistyNo": "wl" + tail_fix,
                "barCode": "bc" + tail_fix,
                "turnOrderNo": str(int(time.time() * 1000)),
                "drawOrderNo": str(int(time.time() * 1000))
            })
            order_list.append(temp_order_info)
        else:
            for package in package_list:
                count += 1
                temp_order_info = deepcopy(content["data"]["orderList"][0])
                temp_order_info.update({
                    "deliveryNo": delivery_order_code,
                    "packageNoList": [package],
                    "logistyNo": "wl" + str(int(time.time() * 1000 + count)),
                    "barCode": "bc" + str(int(time.time() * 1000 + count)),
                    "turnOrderNo": str(int(time.time() * 1000)),
                    "drawOrderNo": str(int(time.time() * 1000))
                })
                order_list.append(temp_order_info)
        content["data"].update(
            {
                "deliveryNo": delivery_order_code,
                "orderList": order_list
            })
        callback_res = self.call_api(**content)
        return self.formatted_result(callback_res)

    def delivery_mock_package_call_back(self, delivery_order_code, transport_type, delivery_order_sku_list):
        """
        模拟TMS回调包裹方案
        :param transport_type: 运输方式1快递，2卡车
        :param delivery_order_sku_list: 出库单sku列表
        :param delivery_order_code: 销售出库单号
        :return:
        """
        content = deepcopy(DeliveryApiConfig.PackageCallBack.get_attributes())
        content["data"].update({
            "deliveryNo": delivery_order_code,
            "transportType": transport_type
        })
        content["data"]["packageInfo"]["packageList"][0].update({
            "packageNo": "BG" + delivery_order_code,
            "packageSkuList": delivery_order_sku_list
        })
        res = self.call_api(**content)
        return self.formatted_result(res)

    def delivery_create_pick_order(self, delivery_order_code, prod_type=0):
        """
        创建拣货单
        :param prod_type: 0前置面单；1后置面单
        :param delivery_order_code: 销售出库单编码
        :return:
        """
        content = deepcopy(DeliveryApiConfig.CreatePickOrder.get_attributes())
        if prod_type == 0:
            content["data"].update({
                "singleDeliveryOrderCodes": [delivery_order_code],
                "singleMaxQty": 1,  # 最大单数
                "singlePickType": 0,  # 纸质拣货
                "multiDeliveryOrderCodes": [],
                "multiPickType": 0
            })
        else:
            content["data"].update({
                "singleDeliveryOrderCodes": [],
                "singleMaxQty": None,  # 最大单数
                "singlePickType": 0,  # 纸质拣货
                "multiDeliveryOrderCodes": [delivery_order_code],
                "multiPickType": 0
            })
        res = self.call_api(**content)
        return self.formatted_result(res)

    def delivery_assign_pick_user(self, pick_order_code):
        """
        拣货单分配拣货人
        :param pick_order_code: 拣货单编码
        :return:
        """
        user_info = self.get_user_info()
        content = deepcopy(DeliveryApiConfig.AssignPickUser.get_attributes())
        content["data"].update({
            "pickOrderCodeList": [pick_order_code],
            "userId": user_info["userId"],
            "userName": user_info["nickname"]
        })
        res = self.call_api(**content)
        return self.formatted_result(res)

    def delivery_get_pick_data(self, pick_order_id):
        """
        获取拣货单拣货信息
        :param pick_order_id: 销售出库单id
        :return:
        """
        content = deepcopy(DeliveryApiConfig.GetToPickData.get_attributes())
        content["uri_path"] %= pick_order_id
        res = self.call_api(**content)
        return self.formatted_result(res)

    def delivery_confirm_pick(self, pick_order_code, normal_list, lost_list):
        """
        拣货单确认拣货
        :param lost_list: 拣货异常的sku列表
        :param normal_list: 正常拣货的sku列表
        :param pick_order_code: 销售出库单编码
        :return:
        """
        content = deepcopy(DeliveryApiConfig.PickOrderConfirmPick.get_attributes())
        content["data"].update({
            "pickOrderCode": pick_order_code,
            "normalList": normal_list,
            "errList": lost_list})
        res = self.call_api(**content)
        return self.formatted_result(res)

    def delivery_package_info(self, delivery_order_code):
        """
        获取销售出库单的包裹方案信息
        :param delivery_order_code: 销售出库单编码
        :return:
        """
        content = deepcopy(DeliveryApiConfig.DeliveryPackageInfo.get_attributes())
        content['uri_path'] %= delivery_order_code
        content["data"].update({
            "t": str(int(time.time() * 1000))
        })
        res = self.call_api(**content)
        return self.formatted_result(res)

    def delivery_save_package(self, package_info):
        """
        销售出库单维护包裹
        :param package_info: 销售出库单的包裹信息
        :return:
        """
        package_info_list = list()
        content = deepcopy(DeliveryApiConfig.DeliverySavePackage.get_attributes())
        index = 0
        for package in package_info["packagePlanInfos"]:
            package_info_list.append({
                "packageIndex": index,
                "remarks": package["remarks"],
                "length": package["length"],
                "width": package["width"],
                "height": package["height"],
                "weight": package["weight"],
                "skuInfoList": [
                    {
                        "skuCode": sku["warehouseSkuCode"],
                        "skuQty": sku["warehouseSkuQty"]
                    } for sku in package["skuList"]
                ]
            })
            index += 1
        content["data"].update({
            "deliveryOrderCode": package_info["deliveryOrderCode"],
            "packageInfoList": package_info_list,
            "transportType": package_info["transportType"],
        })
        res = self.call_api(**content)
        return self.formatted_result(res)

    def delivery_review(self, normal_list, abnormal_list):
        """
        销售出库单复核
        :param abnormal_list: 存在拦截、取消的出库单
        :param normal_list: 正常的出库单
        :return:
        """
        content = deepcopy(DeliveryApiConfig.DeliveryOrderReview.get_attributes())
        content["data"].update({
            "unNormalList": abnormal_list, "normalList": normal_list})
        res = self.call_api(**content)
        return self.formatted_result(res)

    def delivery_shipping(self, normal_ids, normal_codes, abnormal_list):
        """
        销售出库单复核
        :param normal_codes: 不存在拦截、取消的出库单编码列表
        :param normal_ids: 不存在拦截、取消的出库单id列表
        :param abnormal_list: 存在拦截、取消的出库单
        :return:
        """
        content = deepcopy(DeliveryApiConfig.DeliveryOrderShipping.get_attributes())
        content["data"].update(
            {"normalIdList": normal_ids, "normalCodeList": normal_codes, "unNormalList": abnormal_list})
        res = self.call_api(**content)
        return self.formatted_result(res)

    def other_in_get_sku_info(self, ware_sku_code_list):
        """
        其他入库添加sku时获取sku信息
        :param ware_sku_code_list:仓库sku编码列表
        :return:info list
        """
        content = deepcopy(OtherInApiConfig.GetSkuInfo.get_attributes())
        content["data"].update(
            {"skuCode": ware_sku_code_list})
        res = self.call_api(**content)
        return self.formatted_result(res)

    def other_in_create_order(self, sku_info_list):
        """
        创建其他入库单
        :param sku_info_list:查找到的仓库sku的信息列表
        :return:
        """
        content = deepcopy(OtherInApiConfig.CreateOtherInOrder.get_attributes())
        now = int(time.time() * 1000)
        content["data"].update(
            {
                "eta": now,
                "remark": "自动化脚本生成",
                "qualityType": 0,
                "timestamp": now,
                "skuInfoList": sku_info_list
            })
        res = self.call_api(**content)
        return self.formatted_result(res)

    def other_in_get_order_sku_info(self, entry_order_code, entry_order_id):
        """
        获取其他入库单信息
        :param entry_order_code: 入库单编码
        :param entry_order_id: 入库单id
        :return:
        """
        content = deepcopy(OtherInApiConfig.GetOtherInOrderSkuInfoByEntryOrderCode.get_attributes())
        now = int(time.time() * 1000)
        content["data"].update({
            "size": 100,
            "current": 1,
            "entryOrderCode": entry_order_code,
            "entryOrderId": entry_order_id
        })
        res = self.call_api(**content)
        return self.formatted_result(res)

    def other_in_submit_order(self, entry_order_code, entry_order_id):
        """
        提交其他入库单
        :param entry_order_code: 入库单编码
        :param entry_order_id: 入库单id
        :return:
        """
        entry_order_sku_info_result = self.other_in_get_order_sku_info(entry_order_code, entry_order_id)
        if not entry_order_sku_info_result["code"]:
            return
        sku_info_records = entry_order_sku_info_result["data"]["records"]
        sku_info_list = [
            {
                "warehouseSkuCode": sku["warehouseSkuCode"],
                "planSkuQty": sku["planSkuQty"],
                "warehouseSkuName": sku["warehouseSkuName"],
                "warehouseSkuWeight": sku["warehouseSkuWeight"],
                "saleSkuCode": sku["saleSkuCode"],
                "saleSkuName": sku["saleSkuName"],
                "bomVersion": sku["bomVersion"],
                "saleSkuImg": sku["skuImgUrl"],
                "warehouseSkuHeight": sku["warehouseSkuHeight"],
                "warehouseSkuLength": sku["warehouseSkuLength"],
                "warehouseSkuWidth": sku["warehouseSkuWidth"]} for sku in sku_info_records
        ]

        content = deepcopy(OtherInApiConfig.SubmitOtherInOrder.get_attributes())
        now = int(time.time() * 1000)
        content["data"].update(
            {"entryOrderId": entry_order_id,
             "entryOrderType": 3, "eta": now,
             "skuInfoList": sku_info_list,
             "operationFlag": 1
             })
        res = self.call_api(**content)
        return self.formatted_result(res)

    def other_in_order_up_shelf(self, entry_order_code, entry_order_id, warehouse_id, to_warehouse_id):
        """
        其他人库单上架
        :param warehouse_id: 所属仓库id
        :param to_warehouse_id: 目的仓id
        :param entry_order_code: 入库单编码
        :param entry_order_id: 入库单id
        :return:
        """
        content = deepcopy(OtherInApiConfig.PutOnTheShelf.get_attributes())
        entry_order_sku_info_result = self.other_in_get_order_sku_info(entry_order_code, entry_order_id)
        if not entry_order_sku_info_result["code"]:
            return
        sku_info_records = entry_order_sku_info_result["data"]["records"]

        get_sj_kw_result = self.base_get_kw(2, 5, len(sku_info_records), warehouse_id, to_warehouse_id)
        if not get_sj_kw_result["code"]:
            return
        sj_kw_codes = get_sj_kw_result["data"]

        sku_info_list = [
            {
                "skuCode": sku["warehouseSkuCode"],
                "shelvesLocationCode": kw_codes,
                "skuQty": sku["planSkuQty"],
                "abnormalQty": 0
            } for sku, kw_codes in zip(sku_info_records, sj_kw_codes)
        ]
        content["data"].update({"entryOrderId": entry_order_id, "skuList": sku_info_list})
        res = self.call_api(**content)
        return self.formatted_result(res)

    def validate_origin_location(self, location_code, usage_type):
        """
        校验源库位
        :param location_code: 库位编码
        :param usage_type: 用途：批量移库、普通移库、转次、转良
        """
        if not isinstance(usage_type, StockOperationApiConfig.UsageType):
            raise TypeError('usage_type 必须是 UsageType 枚举')

        content = deepcopy(
            StockOperationApiConfig.ValidateOriginLocation.get_attributes()
        )
        content["data"].update({
            "locationCode": location_code,
            "usage": usage_type.value
        })

        return self.call_api(**content)

    def validate_des_location(self, origin_code, des_code, usage_type):
        """
        校验目标库位
        :param origin_code: 源库位编码
        :param des_code: 目标库位编码
        :param usage_type: 用途：批量移库、普通移库、转次、转良
        """
        if not isinstance(usage_type, StockOperationApiConfig.UsageType):
            raise TypeError('usage_type 必须是 UsageType 枚举')

        content = deepcopy(
            StockOperationApiConfig.ValidateDesLocation.get_attributes()
        )
        content["data"].update(
            {
                "desLocationCode": des_code,
                "originLocationCode": origin_code,
                "usage": usage_type.value
            }
        )

        return self.call_api(**content)

    def pda_get_inventory(self, ):
        pass




class WMSTransferServiceRobot(ServiceRobot):
    def __init__(self):
        super().__init__("transfer")

    def transfer_out_create_demand(self, delivery_warehouse_code, delivery_target_warehouse_code,
                                   receive_warehouse_code, receive_target_warehouse_code, sale_sku_code, bom,
                                   demand_qty, demand_type=1, customer_type=1, remark=""):
        """
        :param bom: bom版本
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
        content["data"].update(
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
                "bomVersion": bom
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
                bom,
                qty)
            if not demand_res["code"]:
                log.error("创建调拨需求失败")
            demand_no = demand_res["data"]["demandCode"]
            demand_list.append(demand_no)
        return demand_list


class WMSDeliveryServiceRobot(ServiceRobot):
    def __init__(self):
        super().__init__("delivery")


class WMSBaseServiceRobot(ServiceRobot):

    def __init__(self):
        super().__init__('wms_base')
        self.dbo = WMSDBOperator

    def get_workday_duration(self, warehouse_id, start_time, end_time) -> dict:
        """
        获取节假日时长
        :param int warehouse_id: 仓库id
        :param str start_time: 开始时间，北京时间
        :param str end_time: 结束时间，北京时间

        :return dict: 例子 {
                        'code': 200, 'message': '',
                        'data': {'workdays': ['20230301~20230303', '20230306~20230308'],
                      'duration': '5d', 'startTimeStr': '2023-03-01 18:00:00',
                      'endTimeStr': '2023-03-08 18:00:00', 'zoneId': 'Asia/Shanghai'}
                    }
        """
        content = deepcopy(BaseApiConfig.WorkdayDuration.get_attributes())
        content["data"].update(
            {
                "warehouseId": warehouse_id,
                "startTime": start_time,
                "endTime": end_time
            }
        )

        return self.call_api(**content)

    def get_workday_target_time(self, warehouse_id, date_time, duration) -> dict:
        """
        根据时长和工作日数据查询目标时间
        :param int warehouse_id : 仓库id
        :param str date_time: 开始时间，北京时间
        :param str duration: 时长，数值带单位，如：60h,30m,1d,1s

        :return dict : 例子 {'code': 200, 'message': '操作成功', 'data':
        {'dateTimeStr': '2023-03-01 18:00:00', 'duration': '5d',
        'workdays': ['20230301~20230303', '20230306~20230308'],
        'targetDateTime': 1678269600000, 'targetDateTimeStr': '2023-03-08 18:00:00',
        'zoneId': 'Asia/Shanghai'}}
        """
        content = deepcopy(BaseApiConfig.WorkdayTargetDateTime.get_attributes())
        content["data"].update({
            "warehouseId": warehouse_id,
            "dateTime": date_time,
            "duration": duration
        })
        return self.call_api(**content)

    def get_workday_calendar_by_db(self, warehouse_id, start_time, end_time=None) -> list:
        """
        从数据库获取仓库节假日
        :param int warehouse_id: 仓库id
        :param str start_time: 开始时间
        :param str end_time: 结束时间

        :return list or None
        """
        if not isinstance(start_time, str):
            raise TypeError('start_time must be a str type')
        if end_time and not isinstance(end_time, str):
            raise TypeError('end_time must be a str type')

        start_time = start_time.split(' ')[0]
        if end_time:
            end_time = end_time.split(' ')[0]

        return self.dbo.get_workday_calendar(warehouse_id, start_time, end_time)

    def get_warehouse_timezone_by_db(self, warehouse_id) -> str:
        """
        从数据库获取仓库时区
        :param int warehouse_id: 仓库id

        :return str
        """
        return self.dbo.get_warehouse_timezone(warehouse_id)

    def get_workday_targetime(self, warehouse_id, date_time, duration):
        """
        计算目标时间（根据阈值，仓库，开始时间，计算出对应的过期/临期时间）
        :param int warehouse_id: 仓库id
        :param str date_time: 开始时间 '2023-03-01 00:00:00'
        :param str duration: 阈值 '60h,1d,2m,20s'

        :return dict
        """

        # 获取对应仓库时区，将非中国时区的，将开始时间转化成对应时区的时间
        timezone = self.get_warehouse_timezone_by_db(warehouse_id) or "Asia/Shanghai"

        if timezone != "Asia/Shanghai":
            starttime_by_warehouse = HumanDateTime(date_time).astimezone(timezone)
        else:
            starttime_by_warehouse = HumanDateTime(date_time)

        # 根据开始时间,获取对应工作日列表
        warehouse_day_list = self.get_workday_calendar_by_db(
            warehouse_id,
            str(starttime_by_warehouse)
        )
        log.debug(f'查询出来对应的工作日列表：{warehouse_day_list}')

        # 根据阈值转化成秒
        try:
            prod_map = {'d': 24 * 60 * 60, 'm': 60, 'h': 60 * 60}
            number, unit = duration[:-1], duration[-1]
            duration_seconds = prod_map.get(unit.lower(),1) * int(number)
            log.info(f'阈值转成秒值为：{duration_seconds}')
        except Exception as err:
            log.error(f'输入得阈值没有按照格式，导致处理错啦，报错原因：{err}')
            raise

        # 算出对应的结束时间
        if str(starttime_by_warehouse).split()[0] in warehouse_day_list:
            today_remain_seconds = starttime_by_warehouse.tomorrow().timestamp() - starttime_by_warehouse.timestamp()
            if today_remain_seconds > duration_seconds:
                target_time_by_warehouse = starttime_by_warehouse.add(seconds=duration_seconds)
                target_time_by_cn = HumanDateTime(date_time).add(seconds=duration_seconds)

            else:
                workday_index = int((duration_seconds - today_remain_seconds) / 60 / 60 // 24)
                remain_senconds = (duration_seconds - today_remain_seconds) - workday_index * 60 * 60 * 24
                target_time_by_warehouse = HumanDateTime(warehouse_day_list[workday_index + 1]).add(
                    seconds=remain_senconds)
                actually_duration_seconds = target_time_by_warehouse.compare_diff_to(starttime_by_warehouse)
                target_time_by_cn = HumanDateTime(date_time).add(seconds=actually_duration_seconds)
        else:

            workday_index = int(duration_seconds / 60 / 60 // 24)
            remain_senconds = duration_seconds - workday_index * 60 * 60 * 24
            target_time_by_warehouse = HumanDateTime(warehouse_day_list[workday_index]).add(seconds=remain_senconds)
            actually_duration_seconds = target_time_by_warehouse.compare_diff_to(starttime_by_warehouse)
            target_time_by_cn = HumanDateTime(date_time).add(seconds=actually_duration_seconds)

        result = {
            "start_time_by_cntimezone": date_time,
            "start_time_by_warehouse_timezone": str(starttime_by_warehouse),
            "target_time_by_cntimezone": str(target_time_by_cn),
            "target_time_by_warehouse_timezone": str(target_time_by_warehouse),
            "warehouse_timezone": timezone

        }
        return result


# call example

# if __name__ == "__main__":
#     wms = WMSAppRobot()
#     # print(wms.entry_order_page(["FH2211022680"]))
#     # wms.delivery_order_assign_stock(["PRE-CK2211100010"])
#     # print(wms.get_delivery_order_page(["PRE-CK2211100010"]))
#     # print(wms.get_user_info())
#     # print(wms.delivery_get_pick_data("1881"))
#     # print(wms.dbo.query_wait_assign_demands())
#
#     # order_sku_list = [
#     #     {
#     #         "skuCode": "63203684930B01", "skuName": "酒柜-金色A款08 1/2 X1", "num": 2
#     #     },{
#     #         "skuCode": "63203684930B02", "skuName": "酒柜(金色)07 2/2 X5", "num": 10
#     #     }]
#     # wms.delivery_mock_package_call_back("PRE-CK2302020006",1,order_sku_list)
#     wms.delivery_mock_label_callback("PRE-CK2302020007", ["PRE-BG2302020026"], False)
