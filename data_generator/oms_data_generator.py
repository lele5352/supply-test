import time

from utils.wait_handler import until
from cases import *


def create_sale_order(order_sku_info_list):
    """
    创建销售出库单
    @param list order_sku_info_list: 销售sku及数量的数组，格式：[{"sku_code":"","qty":1,"bom":"A","warehouse_id":""}]
    @return: sale_order_no，销售出库单号
    """
    create_result = oms_app.create_sale_order(order_sku_info_list)
    if not create_result['code']:
        return
    # 提取销售单号，从data中直接提取
    sale_order_no = create_result.get('data')
    return sale_order_no


def create_wms_sale_outbound_order(order_sku_info_list):
    # 新建销售出库单
    sale_order_no = create_sale_order(order_sku_info_list)
    if not sale_order_no:
        return
    # 根据销售单号查询oms单，从data中直接提取
    query_oms_order_result = oms_app.query_oms_order_by_sale_no(sale_order_no)
    if not query_oms_order_result['code']:
        return
    oms_order_list = query_oms_order_result.get('data')
    oms_order_no_list = [record['orderNo'] for record in oms_order_list]
    oms_order_no_str = "\n".join(oms_order_no_list)
    # 根据销售订单号找出oms单号执行审单
    # 执行审单
    dispatch_result = oms_app_ip.dispatch_oms_order(oms_order_no_list)
    if not dispatch_result['code']:
        return
    # 审单之后可能会拆单，需要再根据销售单号从新查出来oms单
    # 根据销售单号查询oms单，从data中直接提取
    query_oms_order_result = oms_app.query_oms_order_by_sale_no(sale_order_no)
    if not query_oms_order_result['code']:
        return
    oms_order_list = query_oms_order_result.get('data')
    # 添加库存
    follow_order_list = list()
    # 为了确保订单有库存下发，提前根据订单添加库存
    for oms_order in oms_order_list:
        order_id = oms_order["id"]
        order_sku_items_result = oms_app.query_oms_order_sku_items(order_id)
        if not order_sku_items_result['code']:
            return

        order_sku_items = order_sku_items_result.get("data")

        for item in order_sku_items:
            if not (item['deliveryWarehouseId'] and item['bomVersion']):
                return
            sku_code = item["itemSkuCode"]
            qty = item["itemQty"]
            bom = item['bomVersion']

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
            get_kw_result = wms_app.db_get_kw(1, 5, len(order_sku_info_list), warehouse_id, warehouse_id)
            if not get_kw_result["code"]:
                return
            kw_ids = get_kw_result.get('data')
            add_stock_result = ims_robot.add_bom_stock(sku_code, bom, qty, kw_ids, warehouse_id, warehouse_id)
            if not add_stock_result["code"]:
                return

            # 构造跟单参数
            if {"skuCode": sku_code, "bomVersion": bom} not in follow_order_list:
                follow_order_list.append({"skuCode": sku_code, "bomVersion": bom})

    # 执行跟单
    follow_result = oms_app_ip.oms_order_follow(follow_order_list)
    if not follow_result["code"]:
        return
    # 跟单是异步操作，需要等待跟单完成,通过查询oms单状态是否为已预占待下发，满足才可执行下发
    for order in oms_order_no_list:
        until(99, 0.5)(
            lambda: "已预占待下发" == oms_app.query_oms_order_by_oms_no(order).get("data")[0].get("orderStatusName"))()

    # 执行订单下发
    push_result = oms_app_ip.push_order_to_wms()
    if not push_result["code"]:
        return

    # 订单下发也是异步，需要等待下发执行完成，通过查询oms单是否有出库单号确认是否下发成功
    for order in oms_order_no_list:
        until(99, 0.5)(lambda: oms_app.query_oms_order_by_oms_no(order).get("data")[0].get("salesOutNo") is not None)()

    # 根据销售单号查询oms单，从data中直接提取发货仓和出库单号
    query_oms_order_result = oms_app.query_oms_order_by_sale_no(sale_order_no)
    oms_order_list = query_oms_order_result.get('data')
    ck_order_list = [{
        "delivery_warehouse_code": record['deliveryWarehouseCode'],
        "sale_out_no": record['salesOutNo']
    } for record in oms_order_list]
    return {sale_order_no: ck_order_list}


if __name__ == '__main__':
    # data = [{"sku_code": "67330337129", "qty": 2, "bom": "A", "warehouse_id": "520"},
    #         {"sku_code": "63203684930", "qty": 3, "bom": "A", "warehouse_id": "520"}]
    # data = [{"sku_code": "63203684930", "qty": 2, "bom": "A", "warehouse_id": "513"},
    #         {"sku_code": "67330337129", "qty": 2, "bom": "A", "warehouse_id": "513"}]
    start = time.time()
    data = [{"sku_code": "63203684930", "qty": 2, "bom": "B", "warehouse_id": "513"}]
    print(create_wms_sale_outbound_order(data))
    end = time.time()
    print("花费{}秒".format(round(end-start)))
