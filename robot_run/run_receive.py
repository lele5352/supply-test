from cases import *


def query_wait_receive_data():
    data = wms_app.dbo.query_wait_receive_entry_order()
    if len(data) == 0:
        return
    entry_order_list = [(_['distribute_order_code'], _['warehouse_id'], _['dest_warehouse_id']) for _ in data]
    return entry_order_list


def run_receive(distribute_order_code, warehouse_id, to_warehouse_id):
    # 切换到收货仓
    switch_result = wms_app.common_switch_warehouse(warehouse_id)
    if not switch_result['code']:
        return 'Fail', None
    # 调用入库单列表页接口根据分货单号获取入库单信息
    search_result = wms_app.receipt_entry_order_page([distribute_order_code])
    if not search_result['code']:
        return 'Fail', None

    # 提取入库单信息
    entry_order_info = search_result['data']['records'][0]

    entry_order_code = entry_order_info.get('entryOrderCode')
    scan_result = wms_app.receipt_entry_order_detail(entry_order_code)
    if not scan_result['code']:
        return 'Fail', None

    entry_order_detail = scan_result.get('data')
    pre_receive_order_code = entry_order_detail.get('predictReceiptOrderCode')
    receive_sku_list = entry_order_detail.get("skuInfos")

    get_sh_kw_result = wms_app.db_get_kw(2, 1, len(receive_sku_list), warehouse_id, to_warehouse_id)
    if not get_sh_kw_result['code']:
        return 'Fail', None

    sh_kw_codes = get_sh_kw_result['data']

    get_sj_kw_result = wms_app.db_get_kw(2, 5, len(receive_sku_list), warehouse_id, to_warehouse_id)
    if not get_sj_kw_result['code']:
        return 'Fail', None

    sj_kw_codes = get_sj_kw_result['data']

    for sku, kw in zip(receive_sku_list, sh_kw_codes):
        sku.update({
            "locationCode": kw,
            "skuNumber": sku['totalNumber']
        })
    receive_result = wms_app.receipt_confirm_receive(entry_order_code, pre_receive_order_code, receive_sku_list)
    if not receive_result['code']:
        return 'Fail', None

    pre_receive_order_list = [pre_receive_order_code]

    submit_pre_receive_order_result = wms_app.receipt_submit_pre_receive_order(pre_receive_order_list)
    if not submit_pre_receive_order_result['code']:
        return 'Fail', None

    # 跳过质检，直接上架交接
    handover_result = wms_app.receipt_handover_to_upshelf(sh_kw_codes)
    if not handover_result['code']:
        return 'Fail', None

    # 整托上架
    for sh_kw_code, sj_kw_code in zip(sh_kw_codes, sj_kw_codes):
        kw_detail_result = wms_app.receipt_location_detail(sh_kw_code)
        if not kw_detail_result['code']:
            return 'Fail', None

        upshelf_result = wms_app.receipt_upshelf_whole_location(sh_kw_code, sj_kw_code)
        if not upshelf_result['code']:
            return 'Fail', None

    # 最后需要再调用上架完成接口，结束流程
    complete_upshelf_result = wms_app.receipt_complete_upshelf()
    if not complete_upshelf_result['code']:
        return 'Fail', None

    return 'success', entry_order_code
