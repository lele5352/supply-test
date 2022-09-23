import time

from tasks import *


def push_delivery_order_task(order_sku_info_list):
    """
    生成双指定销售订单，并审单下发至WMS生成销售出库单
    @param order_sku_info_list: 格式：[{"sku_code": "JJH3C94287", "qty": 2, "bom": "A", "warehouse_id": '513'}]

    @return:
    """

    # 创建出库单
    create_result = oms_app_robot.create_sale_order(order_sku_info_list)
    if not create_result['code']:
        return {"code": 0, "msg": "销售单创建失败！", "data": create_result['data']}
    # 提取销售单号，从data中直接提取

    sale_order_no = create_result.get('data')

    # 根据销售单号查询oms单，从data中直接提取
    query_oms_order_result = oms_app_robot.query_oms_order(sale_order_no)
    if not query_oms_order_result['code']:
        return {"code": 0, "msg": "查询oms单号失败！", "data": {}}
    oms_order_list = query_oms_order_result.get('data')

    oms_order_no_list = [record['orderNo'] for record in oms_order_list]
    # 执行审单
    dispatch_result = oms_app_ip_robot.dispatch_oms_order(oms_order_no_list)

    if not dispatch_result['code']:
        return {"code": 0, "msg": "%s审单失败！" % oms_order_no_list, "data": dispatch_result['data']}

    follow_order_list = list()

    # 为了确保订单有库存下发，提前根据订单添加库存
    for oms_order in oms_order_list:
        order_id = oms_order["id"]
        order_sku_items_result = oms_app_robot.query_oms_order_sku_items(order_id)
        if not order_sku_items_result['code']:
            return {"code": 0, "msg": "获取oms单sku信息失败！", "data": order_sku_items_result['data']}
        order_sku_items = order_sku_items_result.get("data")

        for item in order_sku_items:
            if not (item['deliveryWarehouseId'] or item['bomVersion']):
                return {"code": 0, "msg": "sku%s未审出可发仓库和版本！" % item['itemSkuCode'], "data": {}}
            sku_code = item["itemSkuCode"]
            qty = item["itemQty"] * 10
            bom = item['bomVersion']
            common_warehouse_code = item["deliveryWarehouseCode"]
            common_warehouse_info_result = oms_app_robot.query_common_warehouse(common_warehouse_code)

            if not common_warehouse_info_result["code"]:
                return {"code": 0, "msg": "获取不到共享仓%s配置信息！" % common_warehouse_code, "data": {}}

            # 获取到共享仓之后，取其中一个物理仓加库存即可
            common_warehouse_info = common_warehouse_info_result.get("data")
            warehouse_id = common_warehouse_info["records"][0]["extResBoList"][0]["warehouseId"]
            get_kw_result = wms_app_robot.get_kw(1, 5, len(order_sku_info_list), warehouse_id, warehouse_id)
            if not get_kw_result:
                return {"code": 0, "msg": "添加库存时查询库位失败！", "data": {}}
            kw_ids = get_kw_result.get('data')

            add_stock_result = ims_robot.add_bom_stock(sku_code, bom, qty, kw_ids, warehouse_id, warehouse_id)

            if not add_stock_result:
                return {"code": 0, "msg": "添加库存失败！", "data": item}

            if {"skuCode": sku_code, "bomVersion": "demoData"} not in follow_order_list:
                follow_order_list.append({"skuCode": sku_code, "bomVersion": bom})

    # sku和bom执行跟单
    follow_result = oms_app_ip_robot.oms_order_follow(follow_order_list)
    if not follow_result["code"]:
        return {"code": 0, "msg": "跟单失败！", "data": follow_order_list}

    # 执行订单下发
    push_result = oms_app_ip_robot.push_order_to_wms()
    if not push_result:
        return {"code": 0, "msg": "订单下发wms失败！", "data": {}}
    return {"code": 1, "msg": "订单下发wms成功！", "data": sale_order_no}


if __name__ == '__main__':
    res = push_delivery_order_task(
        [{"sku_code": "67330337129", "qty": 2, "bom": "", "warehouse_id": ''},
         {"sku_code": "63203684930", "qty": 3, "bom": "A", "warehouse_id": '513'},
         ]
    )
    print(res)