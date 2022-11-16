from cases import *


def get_demand_sku_bom(demand_code):
    data = wms_app.dbo.query_demand_detail(demand_code)
    bom = data[0]['bom_version']
    return bom


def get_wait_transfer_data():
    """获取待执行调拨流程的调拨需求"""
    data = wms_app.dbo.query_wait_assign_demands()
    if not data:
        return
    demands_list = [
        (
            _['demand_code'],
            _['warehouse_id'],
            _['delivery_target_warehouse_id'],
            _['receive_warehouse_id'],
            _['receive_target_warehouse_id'],
            _['delivery_warehouse_code']
        ) for _ in data]
    return demands_list


def run_transfer(demand_code,  trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id):
    # 切到调出仓
    switch_warehouse_result = wms_app.common_switch_warehouse(trans_out_id)
    if not switch_warehouse_result['code']:
        return 'Fail', None

    # 创建调拨拣货单
    create_pick_order_result = wms_app.transfer_out_create_pick_order([demand_code], 1)
    if not create_pick_order_result['code']:
        return 'Fail', None

    pick_order_code = create_pick_order_result['data']

    # 分配调拨拣货人
    pick_order_assign_result = wms_app.transfer_out_pick_order_assign([pick_order_code], 'admin', 1)
    if not pick_order_assign_result['code']:
        return 'Fail', None

    # 获取调拨拣货单详情数据
    pick_order_details_result = wms_app.transfer_out_pick_order_detail(pick_order_code)
    if not pick_order_details_result['code']:
        return 'Fail', None

    pick_order_details = pick_order_details_result['data']['details']

    # 获取拣货单sku详情数据
    pick_sku_list = wms_app.transfer_get_pick_sku_list(pick_order_details)

    # 调拨拣货单确认拣货-纸质
    confirm_pick_result = wms_app.transfer_out_confirm_pick(pick_order_code, pick_order_details)
    if not confirm_pick_result['code']:
        return 'Fail', None

    get_trans_out_tp_kw_ids_result = wms_app.db_get_kw(1, 3, len(pick_sku_list), trans_out_id, trans_out_to_id)
    if not get_trans_out_tp_kw_ids_result['code']:
        return 'Fail', None

    trans_out_tp_kw_ids = get_trans_out_tp_kw_ids_result['data']

    # 调拨拣货单按需装托提交
    submit_tray_result = wms_app.transfer_out_submit_tray(pick_order_code, pick_order_details,
                                                          trans_out_tp_kw_ids)
    if not submit_tray_result['code']:
        return 'Fail', None

    # 查看整单获取已装托的托盘
    tray_detail_result = wms_app.transfer_out_pick_order_tray_detail(pick_order_code)
    if not tray_detail_result['code']:
        return
    tray_code_list = [tray['storageLocationCode'] for tray in tray_detail_result['data']]

    # 获取生成的调拨出库单号
    finish_result = wms_app.transfer_out_finish_packing(pick_order_code, tray_code_list)
    if not finish_result['code']:
        return 'Fail', None

    transfer_out_order_no = finish_result['data']

    # 获取调拨出库单明细
    transfer_out_order_detail_result = wms_app.transfer_out_order_detail(transfer_out_order_no)
    if not transfer_out_order_detail_result['code']:
        return 'Fail', None

    transfer_out_order_detail = transfer_out_order_detail_result['data']['details']

    # 从调拨出库单明细中提取箱单和库位编码对应关系
    details = [(_['boxNo'], _['storageLocationCode']) for _ in transfer_out_order_detail]
    sorted_details = sorted(details, key=lambda a: a[1])
    # 按箱单和托盘对应逐个复核
    for box_no, tray_code in details:
        review_result = wms_app.transfer_out_order_review(box_no, tray_code)
        if not review_result['code']:
            return 'Fail', None

    for detail in details:
        bind_result = wms_app.transfer_out_box_bind(detail[0], '', '')  # 交接单号和收货仓编码实际可以不用传
        if not bind_result['code']:
            return 'Fail', None

        handover_no = bind_result['data']['handoverNo']

    delivery_result = wms_app.transfer_out_delivery(handover_no)
    if not delivery_result['code']:
        return 'Fail', None

    switch_warehouse_result = wms_app.common_switch_warehouse(trans_in_id)
    if not switch_warehouse_result['code']:
        return 'Fail', None

    trans_in_sj_kw_ids_result = wms_app.db_get_kw(1, 5, len(pick_sku_list), trans_in_id, trans_in_to_id)
    if not trans_in_sj_kw_ids_result['code']:
        return 'Fail', None

    trans_in_sj_kw_codes = [wms_app.db_kw_id_to_code(kw_id) for kw_id in trans_in_sj_kw_ids_result['data']]

    # 调拨入库收货
    receive_result = wms_app.transfer_in_received(handover_no)
    if not receive_result['code']:
        return 'Fail', None

    # 调拨入库按箱单逐个整箱上架
    for detail, sj_kw_code in zip(sorted_details, trans_in_sj_kw_codes):
        up_shelf_result = wms_app.transfer_in_up_shelf(detail[0], sj_kw_code)
        if not up_shelf_result['code']:
            return 'Fail', None
    return True, transfer_out_order_no

