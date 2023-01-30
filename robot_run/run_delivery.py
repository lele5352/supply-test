import time

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


def run_front_label_delivery(delivery_order_info, delivery_order_detail, flow_flag=None):
    """
    执行前置面单销售出库单发货流程
    @param flow_flag: 流程标识，默认为空，执行全部；可选标识：assign_stock,confirm_pick,call_package,call_label,finish_review
    @param delivery_order_detail: 出库单详情
    @param delivery_order_info: 销售出库单信息
    @return
    """
    delivery_order_code = delivery_order_info["deliveryOrderCode"]
    delivery_order_id = delivery_order_info["deliveryOrderId"]
    transport_mode = delivery_order_info["transportMode"]
    express_state = delivery_order_info["expressOrderState"]
    package_state = delivery_order_info["packageState"]
    # 出库单分配库存
    assign_stock_result = wms_app.delivery_assign_stock([delivery_order_code])
    if not assign_stock_result["code"] or assign_stock_result["data"]["failNum"] > 0:
        return "Fail", "Fail to assign stock!"
    # 如果流程标识为分配库存，则执行完就返回，中断流程
    if flow_flag == "assign_stock":
        return "Success", None
    # 提取出库单sku明细
    order_sku_list = [
        {
            "skuCode": _["skuCode"], "skuName": _["skuName"], "num": _["skuQty"]
        } for _ in delivery_order_detail["packageItems"]]

    if package_state != 2:
        # 模拟包裹回调
        package_call_back_result = wms_app.delivery_mock_package_call_back(delivery_order_code, transport_mode,
                                                                           order_sku_list)
        if not package_call_back_result["code"]:
            return "Fail", "Fail to mock package call back!"
    # 如果流程标识为生成包裹方案，则执行就返回，中断流程
    if flow_flag == "call_package":
        return "Success", None

    # 生成包裹是异步，有延迟，睡眠1秒
    time.sleep(1)

    if express_state != 2:
        # 模拟面单回调
        package_list = wms_app.db_get_delivery_order_package_list(delivery_order_code)
        label_call_back_result = wms_app.delivery_mock_label_callback(delivery_order_code, package_list)
        if not label_call_back_result["code"]:
            return "Fail", "Fail to mock label call back!"
    # 如果流程标识为生成面单，则执行就返回，中断流程
    if flow_flag == "call_label":
        return "Success", None
    # 创建拣货单
    create_pick_order_result = wms_app.delivery_create_pick_order(delivery_order_code)
    if not create_pick_order_result["code"]:
        return "Fail", "Fail to create pick order!"
    pick_order_info = create_pick_order_result["data"]

    # 提取拣货单号
    pick_order_code = pick_order_info[0]["pickOrderCode"]
    pick_order_id = pick_order_info[0]["pickOrderId"]
    # 拣货单分配拣货人为当前登录的用户
    assign_pick_user_result = wms_app.delivery_assign_pick_user(pick_order_code)
    if not assign_pick_user_result["code"]:
        return "Fail", "Fail to assign pick user!"

    get_to_pick_data_result = wms_app.delivery_get_pick_data(pick_order_id)
    if not get_to_pick_data_result["code"]:
        return "Fail", "Fail to get pick order to pick data!"
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
        return "Fail", "Fail to confirm pick!"
    # 如果流程标识为拣货完成，则执行就返回，中断流程
    if flow_flag == "confirm_pick":
        return "Success", None

    # 构造复核正常数据
    normal_list = [{"deliveryOrderId": delivery_order_id, "deliveryOrderCode": delivery_order_code}]
    # 执行复核
    review_result = wms_app.delivery_review(normal_list, [])
    if not review_result["code"] or review_result["data"]["failSize"] > 0:
        return "Fail", "Fail to review delivery order!"
    # 如果流程标识为完成复核，则执行就返回，中断流程
    if flow_flag == "finish_review":
        return "Success", None
    # 构造发货正常数据
    normal_ids = [delivery_order_id]
    normal_codes = [delivery_order_code]

    # 执行发货
    shipping_result = wms_app.delivery_shipping(normal_ids, normal_codes, [])
    if not shipping_result["code"]:
        return "Fail", "Fail to ship the delivery order!"
    return "Success", None


def run_backend_label_delivery(delivery_order_info, delivery_order_detail, flow_flag=None):
    """
    执行后置面单销售出库单发货流程
    @param flow_flag: 流程标识，默认为空，执行全部；可选标识：assign_stock,confirm_pick,call_package,call_label,finish_review
    @param delivery_order_detail: 销售出库单详情
    @param delivery_order_info: 销售出库单信息
    @return:
    """
    delivery_order_code = delivery_order_info["deliveryOrderCode"]
    delivery_order_id = delivery_order_info["deliveryOrderId"]
    prod_type = delivery_order_info["prodType"]
    transport_mode = delivery_order_info["transportMode"]
    express_state = delivery_order_info["expressOrderState"]
    package_state = delivery_order_info["packageState"]
    # 出库单分配库存
    assign_stock_result = wms_app.delivery_assign_stock([delivery_order_code])
    if not assign_stock_result["code"] or assign_stock_result["data"]["failNum"] > 0:
        return "Fail", "Fail to assign stock!"

    # 如果流程标识为分配库存，则执行就返回，中断流程
    if flow_flag == "assign_stock":
        return "Success", None

    # 提取出库单sku明细
    order_sku_list = [
        {
            "skuCode": _["skuCode"], "skuName": _["skuName"], "num": _["skuQty"]
        } for _ in delivery_order_detail["packageItems"]]

    if package_state != 2:
        # 模拟包裹回调
        package_call_back_result = wms_app.delivery_mock_package_call_back(delivery_order_code, transport_mode,
                                                                           order_sku_list)
        if not package_call_back_result["code"]:
            return "Fail", "Fail to mock package call back!"

    # 如果流程标识为生成包裹方案，则执行就返回，中断流程
    if flow_flag == "call_package":
        return "Success", None

    # 生成包裹是异步，有延迟，睡眠1秒
    time.sleep(1)

    # 创建拣货单
    create_pick_order_result = wms_app.delivery_create_pick_order(delivery_order_code, prod_type)
    if not create_pick_order_result["code"]:
        return "Fail", "Fail to create pick order!"
    pick_order_info = create_pick_order_result["data"]

    # 提取拣货单号
    pick_order_code = pick_order_info[0]["pickOrderCode"]
    pick_order_id = pick_order_info[0]["pickOrderId"]
    # 拣货单分配拣货人为当前登录的用户
    assign_pick_user_result = wms_app.delivery_assign_pick_user(pick_order_code)
    if not assign_pick_user_result["code"]:
        return "Fail", "Fail to assign pick user!"

    get_to_pick_data_result = wms_app.delivery_get_pick_data(pick_order_id)
    if not get_to_pick_data_result["code"]:
        return "Fail", "Fail to get pick order to pick data!"
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
        return "Fail", "Fail to confirm pick!"

    # 如果流程标识为拣货完成，则执行就返回，中断流程
    if flow_flag == "confirm_pick":
        return "Success", None

    # 获取出库单包裹方案信息
    package_info_result = wms_app.delivery_package_info(delivery_order_code)
    if not package_info_result["code"]:
        return "Fail", "Fail to get package info!"
    package_info = package_info_result["data"]

    # 提交维护包裹
    save_package_result = wms_app.delivery_save_package(package_info)
    if not save_package_result["code"]:
        return "Fail", "Fail to save package!"

    if express_state != 2:
        # 模拟面单回调
        package_list = wms_app.db_get_delivery_order_package_list(delivery_order_code)
        label_call_back_result = wms_app.delivery_mock_label_callback(delivery_order_code, package_list)
        if not label_call_back_result["code"]:
            return "Fail", "Fail to mock label call back!"
    # 如果流程标识为生成面单，则执行就返回，中断流程
    if flow_flag == "call_label":
        return "Success", None

    # 构造复核正常数据
    normal_list = [{"deliveryOrderId": delivery_order_id, "deliveryOrderCode": delivery_order_code}]
    # 执行复核
    review_result = wms_app.delivery_review(normal_list, [])
    if not review_result["code"] or review_result["data"]["failSize"] > 0:
        return "Fail", "Fail to review delivery order!"

    # 如果流程标识为完成复核，则执行就返回，中断流程
    if flow_flag == "finish_review":
        return "Success", None

    # 构造发货正常数据
    normal_ids = [delivery_order_id]
    normal_codes = [delivery_order_code]
    # 执行发货
    shipping_result = wms_app.delivery_shipping(normal_ids, normal_codes, [])
    if not shipping_result["code"]:
        return "Fail", "Fail to ship the delivery order!"
    return "Success", None


def run_delivery(delivery_order_code, warehouse_id, flow_flag=None):
    """
    执行销售出库发货流程
    @param flow_flag: 流程标识，默认为空，执行全部；可选标识：assign_stock,confirm_pick,call_package,call_label,finish_review
    @param warehouse_id: 所属仓库id
    @param delivery_order_code: 销售出库单号列表
    @return:
    """
    switch_result = wms_app.common_switch_warehouse(warehouse_id)
    if not switch_result["code"]:
        return "Fail", "Fail to switch warehouse!"

    # 通过销售出库单列表用出库单号查询获取销售出库单信息
    delivery_order_page_result = wms_app.delivery_get_delivery_order_page([delivery_order_code])
    if not delivery_order_page_result["code"] or len(delivery_order_page_result["data"]["records"]) == 0:
        return "Fail", "Fail to get delivery order page info"

    delivery_order_info = delivery_order_page_result["data"]["records"][0]
    delivery_order_id = delivery_order_info["deliveryOrderId"]

    # 提取出库单作业模式
    operate_mode = delivery_order_info["operationMode"]

    # 获取出库单明细
    delivery_order_detail_result = wms_app.delivery_get_delivery_order_detail(delivery_order_id)
    if not delivery_order_detail_result["code"]:
        return "Fail", "Fail to get delivery order detail!"

    delivery_order_detail = delivery_order_detail_result["data"]

    if operate_mode == 1:
        # 作业模式为1代表前置面单，执行前置面单出库流程
        result = run_front_label_delivery(delivery_order_info, delivery_order_detail, flow_flag)
    else:
        # 其他代表后置面单，执行后置面单出库流程
        result = run_backend_label_delivery(delivery_order_info, delivery_order_detail, flow_flag)
    return result


if __name__ == "__main__":
    delivery_order_code = "PRE-CK2301290010"
    warehouse_id = 513
    flag = "confirm_pick"
    result, info = run_delivery(delivery_order_code, warehouse_id, flag)
    print("出库单 {} 执行发货流程 {} 结果：{}，执行信息：{}".format(delivery_order_code, flag, result, info))
