from cases import *
import random


class TransferProcessNode:
    assign_stock = "create_pick_order"  # 调出-分配库存并创建拣货单
    confirm_pick = "confirm_pick"  # 调出-拣货单拣货完成
    submit_tray = "submit_tray"  # 调出-装托完成
    finish_review = "finish_review"  # 调出-装箱复核完成
    bind_box = "bind"  # 调出-发货交接扫描绑定箱单
    handover = "handover"  # 调出-发货交接完成
    received = "received"  # 调入-收货完成


def run_transfer(demand_code, flow_flag=None, kw_force=False, up_shelf_mode="box"):
    """
    执行调拨流程，可指定流程节点
    :param demand_code: 调拨需求编码
    :param flow_flag: 流程标识，执行到该指定节点中断流程
    :param kw_force: 强制创建库位
    :param string up_shelf_mode: 上架模式，整箱-box；逐件-sku
    """
    demand_data = wms_app.dbo.query_demand(demand_code)
    trans_out_id = demand_data[0].get("warehouse_id")
    trans_out_to_id = demand_data[0].get("delivery_target_warehouse_id")
    trans_in_id = demand_data[0].get("receive_warehouse_id")
    trans_in_to_id = demand_data[0].get("receive_target_warehouse_id")

    # 切到调出仓
    switch_warehouse_result = wms_app.common_switch_warehouse(trans_out_id)
    if not wms_app.is_success(switch_warehouse_result):
        return False, "Fail to switch to trans out warehouse!"

    # 创建调拨拣货单
    create_pick_order_result = wms_app.transfer_out_create_pick_order([demand_code], 1)
    if not wms_app.is_success(create_pick_order_result):
        return False, "Fail to create pick order!"
    pick_order_code = create_pick_order_result['data']
    print('生成调拨拣货单：%s' % pick_order_code)

    # 如果流程标识为创建调拨拣货单，则执行就返回，中断流程
    if flow_flag == TransferProcessNode.assign_stock:
        return True, pick_order_code

    # 分配调拨拣货人
    pick_order_assign_result = wms_app.transfer_out_pick_order_assign([pick_order_code], 'admin', 1)
    if not wms_app.is_success(pick_order_assign_result):
        return False, "Fail to assign pick user!"

    # 获取调拨拣货单详情数据
    pick_order_details_result = wms_app.transfer_out_pick_order_detail(pick_order_code)
    if not wms_app.is_success(pick_order_details_result):
        return False, "Fail to get pick order detail!"

    pick_order_details = pick_order_details_result['data']['details']

    # 获取拣货单sku详情数据
    pick_sku_list = wms_app.transfer_get_pick_sku_list(pick_order_details)

    # 调拨拣货单确认拣货-纸质
    confirm_pick_result = wms_app.transfer_out_confirm_pick(pick_order_code, pick_order_details)
    if not wms_app.is_success(confirm_pick_result):
        return False, "Fail to confirm pick!"

    # 如果流程标识为调拨拣货单确认拣货完成，则执行就返回，中断流程
    if flow_flag == TransferProcessNode.confirm_pick:
        return True, pick_order_code

    get_trans_out_tp_kw_ids_result = wms_app.base_get_kw(
        1, 3, len(pick_sku_list), trans_out_id, trans_out_to_id, force=kw_force)
    if not wms_app.is_success(get_trans_out_tp_kw_ids_result):
        return False, "Fail to get trans out tp location!"

    trans_out_tp_kw_ids = get_trans_out_tp_kw_ids_result['data']

    # 调拨拣货单按需装托提交
    submit_tray_result = wms_app.transfer_out_submit_tray(pick_order_code, pick_order_details,
                                                          trans_out_tp_kw_ids)
    if not wms_app.is_success(submit_tray_result):
        return False, "Fail to submit tray!"

    # 查看整单获取已装托的托盘
    tray_detail_result = wms_app.transfer_out_pick_order_tray_detail(pick_order_code)
    if not wms_app.is_success(tray_detail_result):
        return False, "Fail to get pick order tray detail!"
    tray_code_list = [tray['storageLocationCode'] for tray in tray_detail_result['data']]

    # 获取生成的调拨出库单号
    finish_result = wms_app.transfer_out_finish_packing(pick_order_code, tray_code_list)
    if not wms_app.is_success(finish_result):
        return False, "Fail to finish tray packing!"

    # 如果流程标识为装托完成，则执行就返回，中断流程
    if flow_flag == TransferProcessNode.submit_tray:
        return True, pick_order_code

    transfer_out_order_no = finish_result['data']
    print('生成调拨出库单：%s' % transfer_out_order_no)

    # 获取调拨出库单明细
    transfer_out_order_detail_result = wms_app.transfer_out_order_detail(transfer_out_order_no)
    if not wms_app.is_success(transfer_out_order_detail_result):
        return False, "Fail to get trans out order detail!"

    transfer_out_order_detail = transfer_out_order_detail_result['data']['details']

    # 从调拨出库单明细中提取箱单和库位编码对应关系
    box_kw_map_list = [(_['boxNo'], _['storageLocationCode']) for _ in transfer_out_order_detail]
    sorted_box_kw_map = sorted(box_kw_map_list, key=lambda a: a[1])
    box_nos = [_[0] for _ in sorted_box_kw_map]
    # 按箱单和托盘对应逐个复核
    for box_no, tray_code in box_kw_map_list:
        review_result = wms_app.transfer_out_order_review(box_no, tray_code)
        if not wms_app.is_success(review_result):
            return False, "Fail to review trans out order!"

    # 如果流程标识为复核完成，则执行就返回，中断流程
    if flow_flag == TransferProcessNode.finish_review:
        return True, pick_order_code

    for box_no in box_nos:
        bind_result = wms_app.transfer_out_box_bind(box_no, '', '')  # 交接单号和收货仓编码实际可以不用传
        if not wms_app.is_success(bind_result):
            return False, "Fail to bind box to handover order!"

        handover_no = bind_result['data']['handoverNo']
    # 如果流程标识为生成交接单，则执行就返回，中断流程
    if flow_flag == TransferProcessNode.bind_box:
        return True, handover_no
    print('生成调拨出库交接单：%s' % handover_no)

    # 获取交接货单id
    order_detail = wms_app.transfer_handover_order(handoverNos=[handover_no]).get('data').get('records')[0]
    handover_id = order_detail.get('id')

    cabinet_info = random.choice(
        [cabinet for cabinet in wms_app.transfer_cabinet_list().get('data') if cabinet.get('cabinetNumber')])
    container_no = cabinet_info.get('cabinetNumber')
    print('交接单关联柜号：%s' % container_no)

    so_number = cabinet_info.get('soNumber')
    wms_app.transfer_out_update_delivery_config(handover_id, container_no, so_number)

    delivery_result = wms_app.transfer_out_delivery(handover_no)
    if not wms_app.is_success(delivery_result):
        return False, "Fail to ship trans out order!"

    # 如果流程标识为发货交接，则执行就返回，中断流程
    if flow_flag == TransferProcessNode.handover:
        return True, handover_no

    switch_warehouse_result = wms_app.common_switch_warehouse(trans_in_id)
    if not wms_app.is_success(switch_warehouse_result):
        return False, "Fail to switch to trans in warehouse!"

    # 根据调拨出库单获取对应调拨入库单
    search_result = wms_app.transfer_in_order_page(transfer_out_order_no)
    if not wms_app.is_success(search_result):
        return False, "Fail to get transfer in order page data!"
    transfer_in_no = search_result.get("data").get("transferInNo")
    print('生成调拨入库单号：%s' % transfer_in_no)
    # 调拨入库收货
    receive_result = wms_app.transfer_in_received(handover_no)
    if not wms_app.is_success(receive_result):
        return False, "Fail to receive trans in order!"

    # 如果流程标识为发货交接，则执行就返回，中断流程
    if flow_flag == TransferProcessNode.received:
        return True, handover_no

    trans_in_sj_kw_codes_result = wms_app.base_get_kw(2, 5, len(pick_sku_list), trans_in_id, trans_in_to_id)
    if not wms_app.is_success(trans_in_sj_kw_codes_result):
        return False, "Fail to get trans in sj location!"
    trans_in_sj_kw_codes = trans_in_sj_kw_codes_result['data']

    for box_no, sj_kw_code in zip(box_nos, trans_in_sj_kw_codes):
        # 如果没有设置上架数量，则调拨入库按箱单逐个整箱上架
        if up_shelf_mode == "box":
            up_shelf_res = wms_app.transfer_in_up_shelf_whole_box(box_no, sj_kw_code)
            if not wms_app.is_success(up_shelf_res):
                return False, "Fail to up shelf trans in!"
        elif up_shelf_mode == "sku":
            box_info_res = wms_app.transfer_in_box_scan(box_no)
            if not wms_app.is_success(box_info_res):
                return False, "Fail to get box sku detail!"
            box_sku_data = box_info_res.get("data").get("details")
            for sku in box_sku_data:
                qty = sku["waresSkuQty"]
                sku_code = sku["waresSkuCode"]
                detail = [{
                    "waresSkuCode": sku_code,
                    "quantity": 1
                }]
                for num in range(qty):
                    up_shelf_res = wms_app.transfer_in_up_shelf_box_by_sku(box_no, sj_kw_code, transfer_in_no, detail)
                    if not wms_app.is_success(up_shelf_res):
                        return False, "Fail to up shelf trans in!"
        else:
            return False, "unsupported up up shelf mode"
    return True, transfer_in_no


class PlatTransfer:
    """
    平台调拨
    """
    def __init__(self, app_entity=None):
        self.pwms_app = app_entity or pwms_app

    def create_transfer_demand(self, sku_code, demand_qty, delivery_warehouse,
                               receive_warehouse, target_warehouse=None):
        """
        创建平台调拨需求
        """
        self.pwms_app.write_template(sku_code, demand_qty,
                                     delivery_warehouse, target_warehouse, receive_warehouse)
        import_url = self.pwms_app.excel_import()
        self.pwms_app.import_save(import_url)
        self.pwms_app.check_status()
