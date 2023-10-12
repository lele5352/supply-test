from utils.custom_wrapper import until
from cases import *
from utils.log_handler import logger
from robots.robot_biz_exception import InventoryNotEnough


def create_sale_order(order_sku_info_list):
    """
    创建销售出库单
    :param list order_sku_info_list: 销售sku及数量的数组，格式：[{"sku_code":"","qty":1,"bom":"A","warehouse_id":""}]
    :return: sale_order_no，销售出库单号
    """
    create_result = oms_app.create_sale_order(order_sku_info_list)
    if oms_app.is_data_empty(create_result):
        return
    # 提取销售单号，从data中直接提取
    sale_order_no = create_result.get('data')
    return sale_order_no


def create_verified_order(order_sku_info_list, auto_add_stock=True):
    # 创建销售订单并自动审单
    sale_order_no = create_sale_order(order_sku_info_list)
    if not sale_order_no:
        return

    # 根据销售单号查询oms单，从data中直接提取
    query_oms_order_result = oms_app.query_oms_order_by_sale_no(sale_order_no)
    if oms_app.is_data_empty(query_oms_order_result):
        return

    oms_order_list = query_oms_order_result.get('data')
    oms_order_no_list = [record['orderNo'] for record in oms_order_list]

    # 根据销售订单号找出oms单号执行审单
    dispatch_result = oms_app_ip.dispatch_oms_order(oms_order_no_list)
    if not oms_app.is_success(dispatch_result):
        return

    # 审单之后可能会拆单，需要再根据销售单号从新查出来oms单,从data中直接提取
    query_oms_order_result = oms_app.query_oms_order_by_sale_no(sale_order_no)
    if oms_app.is_data_empty(query_oms_order_result):
        return
    # oms_order_list = query_oms_order_result.get('data')

    follow_order_list = list()
    for oms_order in oms_order_list:
        order_id = oms_order["id"]
        order_sku_items_result = oms_app.query_oms_order_sku_items(order_id)
        if oms_app.is_data_empty(order_sku_items_result):
            return

        order_sku_items = order_sku_items_result.get("data")

        for item in order_sku_items:
            if not (item['deliveryWarehouseId'] and item['bomVersion']):
                return
            sku_code, qty, bom = item["itemSkuCode"], item["itemQty"], item['bomVersion']

            # 添加库存
            if auto_add_stock:
                # 若库存不足指定增加库存（默认）
                # 获取指定仓库
                warehouse_code = item["warehouseCode"]

                # 获取审单出来的共享仓
                common_warehouse_code = item["deliveryWarehouseCode"]
                common_warehouse_info_result = oms_app.query_common_warehouse(common_warehouse_code)
                if not common_warehouse_info_result["code"]:
                    return
                common_warehouse_info = common_warehouse_info_result.get("data")

                if not warehouse_code:
                    # 如果未指定仓库，则查共享仓，往共享仓取其中一个物理仓加库存即可
                    warehouse_id = common_warehouse_info["records"][0]["extResBoList"][0]["warehouseId"]
                else:
                    # 如果指定了仓库则只需往对应仓库加库存
                    warehouse_list = common_warehouse_info["records"][0]["extResBoList"]
                    warehouse_id = list(filter(lambda x: x["warehouseCode"] == warehouse_code, warehouse_list))[0].get(
                        "warehouseId")
                get_kw_result = wms_app.base_get_kw(1, 5, len(order_sku_info_list), warehouse_id, warehouse_id)
                if oms_app.is_data_empty(get_kw_result):
                    return
                kw_ids = get_kw_result.get('data')
                add_stock_result = ims_robot.add_bom_stock(sku_code, bom, qty, kw_ids, warehouse_id, warehouse_id)
                if oms_app.is_data_empty(add_stock_result):
                    return

            # 构造跟单参数，重复数据不再重复增加
            if {"skuCode": sku_code, "bomVersion": bom} not in follow_order_list:
                follow_order_list.append({"skuCode": sku_code, "bomVersion": bom})

    # 加库存是异步，需要检查库存是否满足
    for order_sku_info in order_sku_info_list:
        # 库存不足时，直接抛异常
        if not ims_robot.is_bom_stock_enough(
                order_sku_info["sku_code"], order_sku_info["bom"],
                order_sku_info["qty"], order_sku_info["warehouse_id"],
                order_sku_info["warehouse_id"]):
            raise InventoryNotEnough(order_sku_info["sku_code"], order_sku_info["bom"], order_sku_info["warehouse_id"])

    # 执行跟单
    follow_result = oms_app_ip.oms_order_follow(follow_order_list)
    if not oms_app.is_success(follow_result):
        return
    # fix: 如果出现审单拆单的情况，用生成的原oms订单无法找到订单，需要通过销售单查询对应oms订单
    # 跟单是异步操作，需要等待跟单完成,通过查询oms单状态是否为已预占待下发，满足才可执行下发
    # for order in oms_order_no_list:
    #     until(99, 0.5)(
    #         lambda: "已预占待下发" == oms_app.query_oms_order_by_oms_no(order).get("data")[0].get("orderStatusName"))()
    until(99, 0.5)(
        lambda: False not in [
            True if "已预占待下发" == order.get("orderStatusName") else False for order in
            oms_app.query_oms_order_by_sale_no(sale_order_no).get("data")]
    )()
    return sale_order_no


def create_wms_sale_outbound_order(order_sku_info_list, auto_add_stock=True):
    # 新建销售出库单
    sale_order_no = create_verified_order(order_sku_info_list, auto_add_stock)

    if not sale_order_no:
        raise ValueError("create_verified_order 返回的销售单号为空，请检查")

    push_result = oms_app_ip.push_order_to_wms()
    if oms_app.is_data_empty(push_result):
        return
    # fix: 如果出现审单拆单的情况，用生成的原oms订单无法找到订单，需要通过销售单查询
    # 订单下发也是异步，需要等待下发执行完成，通过查询oms单是否有出库单号确认是否下发成功
    # for order in oms_order_no_list:
    #     until(99, 0.5)(lambda: oms_app.query_oms_order_by_oms_no(order).get("data")[0].get("salesOutNo") is not None)()
    until(99, 0.5)(
        lambda: None not in [True if order.get("salesOutNo") else False for order in
                             oms_app.query_oms_order_by_sale_no(sale_order_no).get("data")])()

    # 根据销售单号查询oms单，从data中直接提取发货仓和出库单号
    query_oms_order_result = oms_app.query_oms_order_by_sale_no(sale_order_no)
    oms_order_list = query_oms_order_result.get('data')
    ck_order_list = [{
        "delivery_warehouse_code": record['deliveryWarehouseCode'],
        "sale_out_no": record['salesOutNo']
    } for record in oms_order_list]
    logger.info("生成数据销售订单：{}，对应出库单：{}".format(sale_order_no, ck_order_list), True)
    return {sale_order_no: ck_order_list}


if __name__ == '__main__':
    # data = [{"sku_code": "67330337129", "qty": 2, "bom": "A", "warehouse_id": "520"},
    #         {"sku_code": "63203684930", "qty": 3, "bom": "A", "warehouse_id": "520"}]
    # data = [{"sku_code": "63203684930", "qty": 2, "bom": "A", "warehouse_id": "513"},
    #         {"sku_code": "67330337129", "qty": 2, "bom": "A", "warehouse_id": "513"}]
    # data = [{"sku_code": "63203684930", "qty": 2, "bom": "B", "warehouse_id": "513"}]
    data = [{"sku_code": "HW855K290Z", "qty": 5, "bom": "A", "warehouse_id": "532"}]
    # create_verified_order(data, False)
    create_wms_sale_outbound_order(data, False)
    # [{"skuCode": "KK29O72S66", "bomVersion": "A"}]
