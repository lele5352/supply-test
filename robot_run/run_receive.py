from cases import *


def query_wait_receive_data():
    data = wms_app.dbo.query_wait_receive_entry_order()
    if len(data) == 0:
        return
    entry_order_list = [(_['distribute_order_code'], _['warehouse_id'], _['dest_warehouse_id']) for _ in data]
    return entry_order_list


def run_receive(distribute_order_code, need_quality_check=False, flow_flag=None, up_shelf_mode="kw",
                is_all_up_shelf="all"):
    """
    执行采购入库流程，默认执行全部
    :param need_quality_check: 是否需要质检
    :param distribute_order_code: 分货单号
    :param flow_flag:流程标识，默认为空，执行全部；可选标识：confirm_received,finish_quality_check
    :param up_shelf_mode:上架方式，为空默认整托上架；可选标识："kw"-整托上架、"sku"-逐件上架
    :param flow_flag:流程标识，默认为空，执行全部；可选标识：confirm_received,finish_quality_check


    @return:
    """
    order_data = wms_app.dbo.query_receive_entry_order_detail(distribute_order_code)
    warehouse_id = order_data[0].get("warehouse_id")
    to_warehouse_id = order_data[0].get("dest_warehouse_id")
    entry_order_code = order_data[0].get('entry_order_code')

    # 切换到收货仓
    switch_result = wms_app.common_switch_warehouse(warehouse_id)
    if not wms_app.is_success(switch_result):
        return False, "Fail to switch warehouse!"

    scan_result = wms_app.receipt_entry_order_detail(entry_order_code)
    if not wms_app.is_success(scan_result):
        return False, "Fail to get entry order detail!"

    entry_order_detail = scan_result.get('data')
    pre_receive_order_code = entry_order_detail.get('predictReceiptOrderCode')
    print('生成预收货单：%s' % pre_receive_order_code)

    receive_sku_list = entry_order_detail.get("skuInfos")

    get_sh_kw_result = wms_app.base_get_kw(2, 1, len(receive_sku_list), warehouse_id, to_warehouse_id)
    if not wms_app.is_success(get_sh_kw_result):
        return False, "Fail to get receipt warehouse location!"
    sh_kw_codes = get_sh_kw_result['data']

    get_sj_kw_result = wms_app.base_get_kw(2, 5, len(receive_sku_list), warehouse_id, to_warehouse_id)
    if not wms_app.is_success(get_sj_kw_result):
        return False, "Fail to get up shelf warehouse location!"
    sj_kw_codes = get_sj_kw_result['data']

    for sku, sh_kw in zip(receive_sku_list, sh_kw_codes):
        sku.update({
            "locationCode": sh_kw,
            "skuNumber": sku['totalNumber']
        })
    receive_result = wms_app.receipt_confirm_receive(entry_order_code, pre_receive_order_code, receive_sku_list)
    if not wms_app.is_success(receive_result):
        return False, "Fail to confirm receiving!"

    pre_receive_order_list = [pre_receive_order_code]

    submit_pre_receive_order_result = wms_app.receipt_submit_pre_receive_order(pre_receive_order_list)
    if not wms_app.is_success(submit_pre_receive_order_result):
        return False, "Fail to submit pre receive order!"

    # 如果流程节点指定为确认收货，则流程结束
    if flow_flag == "confirm_received":
        return True, pre_receive_order_list

    # 如果需要质检则先执行质检交接，再执行质检流程
    if need_quality_check:
        # 执行质检交接
        handover_result = wms_app.receipt_handover_to_quality_check(sh_kw_codes)
        if not wms_app.is_success(handover_result):
            return False, "Fail to handover to quality check!"

        # 质检流程
        # 最终要组装出来提交质检的数据
        quality_check_sku_list = list()
        get_zj_kw_result = wms_app.base_get_kw(2, 2, len(sh_kw_codes), warehouse_id, to_warehouse_id)
        if not wms_app.is_success(get_zj_kw_result):
            return False, "Fail to get receipt warehouse quality check location!"
        zj_kw_codes = get_zj_kw_result.get("data")
        # 获取收货库位待质检sku信息
        for sh_kw, zj_kw in zip(sh_kw_codes, zj_kw_codes):
            location_detail = wms_app.receipt_get_quality_check_location_detail(sh_kw)
            if not wms_app.is_success(location_detail):
                return False, "Fail to get quality check location detail!"
            location_receipt_infos = location_detail.get("data").get("receiptInfos")
            # 按库位下的逐个sku提交质检信息
            for receipt_info in location_receipt_infos:
                received_order_code = receipt_info.get("receiptOrderCode")
                for sku_info in receipt_info.get("skuInfos"):
                    # 录入质检结果，输入良品数量和质检库位，提交后会绑定收货库位、质检库位、收货单关系
                    sku_code = sku_info.get("skuCode")
                    qty = sku_info.get("qcStayNumber")

                    bind_result = wms_app.receipt_quality_location_bind(sh_kw, zj_kw, received_order_code)
                    if not wms_app.is_success(bind_result):
                        return False, "Fail to bind quality check location and received location！"
                    quality_check_sku_list.append({
                        "receiveLocationCode": sh_kw,
                        "entryOrderCode": entry_order_code,
                        "receiveOrderCode": received_order_code,
                        "skuCode": sku_code,
                        "qcResult": 0,
                        "number": qty,
                        "length": 0,
                        "height": 0,
                        "width": 0,
                        "weight": 0,
                        "qcLocationCode": zj_kw
                    })
        # 提交质检
        quality_check_submit_result = wms_app.receipt_quality_check_submit(quality_check_sku_list)
        if not wms_app.is_success(quality_check_submit_result):
            return False, "Fail to submit quality check!"

        # 如果流程节点指定质检完成，则结束流程
        if flow_flag == "finish_quality_check":
            return True, entry_order_code

        # 如果执行了质检，上架交接就用质检库位交接
        sh_kw_codes = zj_kw_codes

    # 上架交接
    handover_result = wms_app.receipt_handover_to_upshelf(sh_kw_codes)
    if not wms_app.is_success(handover_result):
        return False, "Fail to handover to up shelf!"

    # 整托上架
    for sh_kw_code, sj_kw_code in zip(sh_kw_codes, sj_kw_codes):
        kw_detail_result = wms_app.receipt_location_detail(sh_kw_code)
        if not wms_app.is_success(kw_detail_result):
            return False, "Fail to get location received detail!"
        if up_shelf_mode == "kw":
            up_shelf_result = wms_app.receipt_upshelf_whole_location(sh_kw_code, sj_kw_code)
            if not wms_app.is_success(up_shelf_result):
                return False, "Fail to up shelf by location!"
        elif up_shelf_mode == "sku":
            up_shelf_result = wms_app.receipt_up

    # 最后需要再调用上架完成接口，结束流程
    complete_up_shelf_result = wms_app.receipt_complete_upshelf()
    if not wms_app.is_success(complete_up_shelf_result):
        return False, "Fail to complete up shelf!"

    return True, entry_order_code


if __name__ == '__main__':
    wms = run_receive('FH2309011339', False)
    print(wms)
