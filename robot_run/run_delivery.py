from cases import *


def get_wait_delivery_data():
    data = wms_app.dbo.query_wait_delivery_order()
    if not data:
        return
    order_list = [
        (
            _['delivery_order_code'],
            _['warehouse_id']
        ) for _ in data
    ]
    return order_list


def run_front_label_delivery(delivery_order_info, delivery_order_detail):
    """
    执行后置面单销售出库单发货流程
    @param delivery_order_detail: 出库单详情
    @param delivery_order_info: 销售出库单信息
    @return
    """
    delivery_order_code = delivery_order_info['deliveryOrderCode']
    transport_mode = delivery_order_info['transportMode']
    # 出库单分配库存
    assign_stock_result = wms_app.delivery_order_assign_stock([delivery_order_code])
    if not assign_stock_result['code']:
        return 'Fail', None
    # 提取出库单sku明细
    order_sku_list = [
        {
            "skuCode": _["skuCode"],
            "skuName": _["skuName"],
            "num": _["skuQty"]
        } for _ in delivery_order_detail['packageItems']]
    # 模拟包裹回调
    package_call_back_result = wms_app.mock_package_call_back(delivery_order_code, transport_mode, order_sku_list)
    if not package_call_back_result['code']:
        return 'Fail', None

    # 模拟面单回调
    package_list = wms_app.query_delivery_order_package_list(delivery_order_code)
    label_call_back_result = wms_app.mock_label_callback(delivery_order_code, package_list)
    if not label_call_back_result['code']:
        return 'Fail', None

    # 创建拣货单

    return "Success", delivery_order_code


def run_backend_label_delivery(delivery_order_info, delivery_order_detail):
    """
    执行后置面单销售出库单发货流程
    @param delivery_order_detail: 销售出库单详情
    @param delivery_order_info: 销售出库单信息
    @return:
    """

    delivery_order_code = delivery_order_info['deliveryOrderCode']
    transport_mode = delivery_order_info['transportMode']
    # 出库单分配库存
    assign_stock_result = wms_app.delivery_order_assign_stock([delivery_order_code])
    if not assign_stock_result['code']:
        return 'Fail', None
    # 提取出库单sku明细
    order_sku_list = [
        {
            "skuCode": _["skuCode"],
            "skuName": _["skuName"],
            "num": _["skuQty"]
        } for _ in delivery_order_detail['packageItems']]
    # 模拟包裹回调
    package_call_back_result = wms_app.mock_package_call_back(delivery_order_code, transport_mode, order_sku_list)
    if not package_call_back_result['code']:
        return 'Fail', None

    # 模拟面单回调
    package_list = wms_app.query_delivery_order_package_list(delivery_order_code)
    label_call_back_result = wms_app.mock_label_callback(delivery_order_code, package_list)
    if not label_call_back_result['code']:
        return 'Fail', None

    return "Success", delivery_order_code


def run_delivery(delivery_order_code, warehouse_id):
    """
    执行销售出库发货流程
    @param warehouse_id: 所属仓库id
    @param delivery_order_code: 销售出库单号列表
    @return:
    """
    switch_result = wms_app.switch_default_warehouse(warehouse_id)
    if not switch_result['code']:
        return 'Fail', None

    delivery_order_page_result = wms_app.get_delivery_order_page([delivery_order_code])
    if not delivery_order_page_result['code']:
        return 'Fail', None

    delivery_order_info = delivery_order_page_result['data']['records'][0]
    delivery_order_id = delivery_order_info["deliveryOrderId"]
    # 获取出库单明细
    delivery_order_detail_result = wms_app.get_delivery_order_detail(delivery_order_id)
    if not delivery_order_detail_result['code']:
        return 'Fail', None

    delivery_order_detail = delivery_order_detail_result['data']

    operate_mode = delivery_order_info['operationMode']
    if operate_mode == 1:
        result = run_front_label_delivery(delivery_order_info, delivery_order_detail)
    else:
        result = run_backend_label_delivery(delivery_order_info, delivery_order_detail)
    return result


if __name__ == '__main__':
    print(run_delivery("PRE-CK2211110013", 520))
