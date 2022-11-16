from cases import *


def get_wait_delivery_data():
    data = wms_app.dbo.query_wait_delivery_order()

    warehouse_id_set = [_["warehouse_id"] for _ in wms_app.dbo.query_warehouse_config()]
    if not data:
        return
    order_list = [
        (
            _["warehouse_id"],
            _["warehouse_code"],
            _["delivery_order_code"]
        ) for _ in data if _["warehouse_id"] in warehouse_id_set]
    return order_list


def run_front_label_delivery(delivery_order_info, delivery_order_detail):
    """
    执行前置面单销售出库单发货流程
    @param delivery_order_detail: 出库单详情
    @param delivery_order_info: 销售出库单信息
    @return
    """
    delivery_order_code = delivery_order_info["deliveryOrderCode"]
    delivery_order_id = delivery_order_info["deliveryOrderId"]
    transport_mode = delivery_order_info["transportMode"]
    # 出库单分配库存
    assign_stock_result = wms_app.delivery_assign_stock([delivery_order_code])
    if not assign_stock_result["code"] or assign_stock_result["data"]["failNum"] > 0:
        return "Fail: fail to assign stock!", None
    # 提取出库单sku明细
    order_sku_list = [
        {
            "skuCode": _["skuCode"], "skuName": _["skuName"], "num": _["skuQty"]
        } for _ in delivery_order_detail["packageItems"]]
    # 模拟包裹回调
    package_call_back_result = wms_app.delivery_mock_package_call_back(delivery_order_code, transport_mode,
                                                                       order_sku_list)
    if not package_call_back_result["code"]:
        return "Fail: fail to mock package call back!", None

    # 模拟面单回调
    package_list = wms_app.db_get_delivery_order_package_list(delivery_order_code)
    label_call_back_result = wms_app.delivery_mock_label_callback(delivery_order_code, package_list)
    if not label_call_back_result["code"]:
        return "Fail: fail to mock label call back!", None

    # 创建拣货单
    create_pick_order_result = wms_app.delivery_create_pick_order(delivery_order_code)
    if not create_pick_order_result["code"]:
        return "Fail: fail to create pick order!", None
    pick_order_info = create_pick_order_result["data"]

    # 提取拣货单号
    pick_order_code = pick_order_info[0]["pickOrderCode"]
    pick_order_id = pick_order_info[0]["pickOrderId"]
    # 拣货单分配拣货人为当前登录的用户
    assign_pick_user_result = wms_app.delivery_assign_pick_user(pick_order_code)
    if not assign_pick_user_result["code"]:
        return "Fail: fail to assign pick user!", None

    get_to_pick_data_result = wms_app.delivery_get_pick_data(pick_order_id)
    if not get_to_pick_data_result["code"]:
        return "Fail: fail to get pick order to pick data!", None
    to_pick_data = get_to_pick_data_result["data"]

    # 确认拣货，无异常，非短拣
    normal_list = [
        {
            "deliveryOrderCode": delivery_order_code,
            "skuCode": _["skuCode"],
            "locationCode": _["locationCode"],
            "expressOrderCode": _["pickDetails"][0]["expressOrderCode"],
            "skuQty": _["pickDetails"][0]["skuQty"]
        } for _ in to_pick_data
    ]

    confirm_pick_result = wms_app.delivery_confirm_pick(pick_order_code, normal_list, [])
    if not confirm_pick_result["code"]:
        return "Fail: fail to confirm pick!", None

    # 构造复核正常数据
    normal_list = [{"deliveryOrderId": delivery_order_id, "deliveryOrderCode": delivery_order_code}]
    # 执行复核
    review_result = wms_app.delivery_review(normal_list, [])
    if not review_result["code"] or review_result["data"]["failSize"] > 0:
        return "Fail: fail to review delivery order!", None

    # 构造发货正常数据
    normal_ids = [delivery_order_id]
    normal_codes = [delivery_order_code]
    # 执行发货
    shipping_result = wms_app.delivery_shipping(normal_ids, normal_codes, [])
    if not shipping_result["code"]:
        return "Fail: fail to ship the delivery order!", None
    return "Success", delivery_order_code


def run_backend_label_delivery(delivery_order_info, delivery_order_detail):
    """
    执行后置面单销售出库单发货流程
    @param delivery_order_detail: 销售出库单详情
    @param delivery_order_info: 销售出库单信息
    @return:
    """

    delivery_order_code = delivery_order_info["deliveryOrderCode"]
    delivery_order_id = delivery_order_info["deliveryOrderId"]
    prod_type = delivery_order_info["prodType"]
    transport_mode = delivery_order_info["transportMode"]
    # 出库单分配库存
    assign_stock_result = wms_app.delivery_assign_stock([delivery_order_code])
    if not assign_stock_result["code"] or assign_stock_result["data"]["failNum"] > 0:
        return "Fail: fail to assign stock!", None
    # 提取出库单sku明细
    order_sku_list = [
        {
            "skuCode": _["skuCode"], "skuName": _["skuName"], "num": _["skuQty"]
        } for _ in delivery_order_detail["packageItems"]]
    # 模拟包裹回调
    package_call_back_result = wms_app.delivery_mock_package_call_back(delivery_order_code, transport_mode,
                                                                       order_sku_list)
    if not package_call_back_result["code"]:
        return "Fail: fail to mock package call back!", None

    # 创建拣货单
    create_pick_order_result = wms_app.delivery_create_pick_order(delivery_order_code, prod_type)
    if not create_pick_order_result["code"]:
        return "Fail: fail to create pick order!", None
    pick_order_info = create_pick_order_result["data"]

    # 提取拣货单号
    pick_order_code = pick_order_info[0]["pickOrderCode"]
    pick_order_id = pick_order_info[0]["pickOrderId"]
    # 拣货单分配拣货人为当前登录的用户
    assign_pick_user_result = wms_app.delivery_assign_pick_user(pick_order_code)
    if not assign_pick_user_result["code"]:
        return "Fail: fail to assign pick user!", None

    get_to_pick_data_result = wms_app.delivery_get_pick_data(pick_order_id)
    if not get_to_pick_data_result["code"]:
        return "Fail: fail to get pick order to pick data!", None
    to_pick_data = get_to_pick_data_result["data"]

    # 确认拣货，无异常，非短拣
    normal_list = [
        {
            "deliveryOrderCode": delivery_order_code,
            "skuCode": _["skuCode"],
            "locationCode": _["locationCode"],
            "expressOrderCode": _["pickDetails"][0]["expressOrderCode"],
            "skuQty": _["pickDetails"][0]["skuQty"]
        } for _ in to_pick_data
    ]

    confirm_pick_result = wms_app.delivery_confirm_pick(pick_order_code, normal_list, [])
    if not confirm_pick_result["code"]:
        return "Fail: fail to confirm pick!", None

    # 获取出库单包裹方案信息
    package_info_result = wms_app.delivery_package_info(delivery_order_code)
    if not package_info_result["code"]:
        return "Fail: fail to get package info!", None
    package_info = package_info_result["data"]

    # 提交维护包裹
    save_package_result = wms_app.delivery_save_package(package_info)
    if not save_package_result["code"]:
        return "Fail: fail to save package!", None

    # 模拟面单回调
    package_list = wms_app.db_get_delivery_order_package_list(delivery_order_code)
    label_call_back_result = wms_app.delivery_mock_label_callback(delivery_order_code, package_list)
    if not label_call_back_result["code"]:
        return "Fail: fail to mock label call back!", None

    # 构造复核正常数据
    normal_list = [{"deliveryOrderId": delivery_order_id, "deliveryOrderCode": delivery_order_code}]
    # 执行复核
    review_result = wms_app.delivery_review(normal_list, [])
    if not review_result["code"] or review_result["data"]["failSize"] > 0:
        return "Fail: fail to review delivery order!", None

    # 构造发货正常数据
    normal_ids = [delivery_order_id]
    normal_codes = [delivery_order_code]
    # 执行发货
    shipping_result = wms_app.delivery_shipping(normal_ids, normal_codes, [])
    if not shipping_result["code"]:
        return "Fail: fail to ship the delivery order!", None
    return "Success", delivery_order_code


def run_delivery(delivery_order_code, warehouse_id):
    """
    执行销售出库发货流程
    @param warehouse_id: 所属仓库id
    @param delivery_order_code: 销售出库单号列表
    @return:
    """
    switch_result = wms_app.common_switch_warehouse(warehouse_id)
    if not switch_result["code"]:
        return "Fail", None

    delivery_order_page_result = wms_app.delivery_get_delivery_order_page([delivery_order_code])
    if not delivery_order_page_result["code"] or len(delivery_order_page_result["data"]["records"]) == 0:
        return "Fail", None

    delivery_order_info = delivery_order_page_result["data"]["records"][0]
    delivery_order_id = delivery_order_info["deliveryOrderId"]
    # 获取出库单明细
    delivery_order_detail_result = wms_app.delivery_get_delivery_order_detail(delivery_order_id)
    if not delivery_order_detail_result["code"]:
        return "Fail", None

    delivery_order_detail = delivery_order_detail_result["data"]

    operate_mode = delivery_order_info["operationMode"]
    if operate_mode == 1:
        result = run_front_label_delivery(delivery_order_info, delivery_order_detail)
    else:
        result = run_backend_label_delivery(delivery_order_info, delivery_order_detail)
    return result


if __name__ == "__main__":
    print(run_delivery("PRE-CK2211130026", 540))
