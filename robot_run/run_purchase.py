from cases import *


def get_wait_purchase_shortage_demands():
    data = scm_app.dbo.query_shortage_demand()
    if not data:
        return
    shortage_demand_id_list = [_["id"] for _ in data]
    result_list = [shortage_demand_id_list[i:i + 10] for i in range(0, len(shortage_demand_id_list), 10)]
    return result_list


def get_wait_purchase_demands():
    data = scm_app.dbo.query_purchase_demand()
    if not data:
        return
    purchase_demand_id_list = [_["id"] for _ in data]
    result_list = [purchase_demand_id_list[i:i + 10] for i in range(0, len(purchase_demand_id_list), 10)]
    return result_list


def get_wait_purchase_order():
    data = scm_app.dbo.query_purchase_order()
    if not data:
        return
    purchase_order_no_list = [_["purchase_number"] for _ in data]
    return purchase_order_no_list


def run_purchase(purchase_order_no):
    """
    执行缺货需求确认到发货完成全流程
    @param purchase_order_no:采购单编码
    @return:
    """
    purchase_order_page_result = scm_app.get_purchase_order_page(purchase_order_no=purchase_order_no)
    if not purchase_order_page_result["code"]:
        return "Fail", "Fail to get purchase order page info！"
    purchase_order_list = [
        (
            _["id"],
            _["purchaseOrderNo"],
            _["deliveryWarehouse"]
        ) for _ in purchase_order_page_result["data"]["list"]
    ]

    for purchase_order_id, purchase_order_no, delivery_warehouse_code in purchase_order_list:
        purchase_order_detail_result = scm_app.get_purchase_order_detail(purchase_order_id)
        if not purchase_order_detail_result["code"]:
            return "Fail", "Fail to get purchase order detail！"
        purchase_order_detail = purchase_order_detail_result["data"]
        update_and_submit_to_audit_res = scm_app.update_and_submit_purchase_order_to_audit(
            purchase_order_detail)
        if not update_and_submit_to_audit_res["code"]:
            return "Fail", "Fail to update and submit purchase to audit！"
        # 采购订单批量审核
        audit_res = scm_app.purchase_order_audit([purchase_order_id])
        if not audit_res["code"]:
            return "Fail", "Fail to audit purchase order！"
        # 采购订单批量下单
        purchase_order_buy_res = scm_app.purchase_order_batch_buy([purchase_order_id])
        if not purchase_order_buy_res["code"]:
            return "Fail", "Fail to batch buy purchase order！"
        # 采购订单批量发货

        # 获取采购订单发货明细
        delivery_detail_result = scm_app.get_purchase_order_delivery_detail(purchase_order_id)
        if not delivery_detail_result["code"]:
            return "Fail", "Fail to get purchase order delivery detail！"

        purchase_order_delivery_detail = delivery_detail_result["data"]["list"]
        # 根据采购订单发货明细生成分货单信息
        generate_result = scm_app.generate_distribute_order(purchase_order_delivery_detail, delivery_warehouse_code)
        if not generate_result["code"]:
            return "Fail", "Fail to generate distribute order！"

        distribute_order_info = generate_result["data"]

        # 采购订单发货
        delivery_res = scm_app.purchase_order_delivery(distribute_order_info)
        if not delivery_res["code"]:
            return "Fail", "Fail to ship purchase order！"

    return "Success", None
