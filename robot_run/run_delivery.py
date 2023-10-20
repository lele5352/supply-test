from cases import *
from utils.log_handler import logger
from utils.custom_wrapper import until


class DeliveryFlow:
    assign_stock = "assign_stock"
    confirm_pick = "confirm_pick"
    call_package = "call_package"
    call_label = "call_label"
    save_package = "save_package"
    finish_review = "finish_review"


class ExecuteResult:
    skipped = "skipped"
    success = "success"
    fail = "fail"


def get_delivery_order_status(delivery_order_code):
    data = wms_app.dbo.get_delivery_order_info(delivery_order_code)
    return data[0].get("state")


def get_delivery_order_package_status(delivery_order_code):
    data = wms_app.dbo.get_delivery_order_info(delivery_order_code)
    return data[0].get("package_state")


def get_delivery_order_express_status(delivery_order_code):
    data = wms_app.dbo.get_delivery_order_info(delivery_order_code)
    return data[0].get("express_state")


def check_status(get_status, status):
    """检验获取到的状态是否在状态列表中
    :param get_status: 获取状态函数
    :param list status: 状态列表"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            order_status = get_status(args[1])
            if order_status in status:
                result = func(*args, **kwargs)
                return result
            else:
                print("状态为%s,无需执行%s，跳过执行" % (order_status, func.__name__))
                return {
                    "result": ExecuteResult.skipped,
                    "info": "状态为%s,无需执行%s，跳过执行" % (order_status, func.__name__),
                    "data": ""
                }

        return wrapper

    return decorator


class RunDelivery:

    def __init__(self, app_entity=None):
        self.wms_app = app_entity or wms_app
        self.execute_info = ""

    def get_wait_delivery_data(self):
        data = self.wms_app.dbo.query_wait_delivery_order()

        warehouse_id_set = [_["warehouse_id"] for _ in self.wms_app.dbo.query_warehouse_config()]
        if not data:
            return
        order_list = [
            (
                _["warehouse_id"],
                _["warehouse_code"],
                _["delivery_order_code"]
            ) for _ in data if _["warehouse_id"] in warehouse_id_set]
        return order_list

    @check_status(get_delivery_order_status, [0, 5])
    def execute_assign_stock(self, delivery_order_code):
        assign_stock_result = self.wms_app.delivery_assign_stock([delivery_order_code])
        if not self.wms_app.is_success(assign_stock_result) or assign_stock_result["data"]["failNum"] > 0:
            return {"result": ExecuteResult.fail, "info": "分配库存失败！", "data": assign_stock_result}
        self.execute_info += "分配库存成功-->"
        return {"result": ExecuteResult.success, "info": "分配库存成功！", "data": assign_stock_result}

    @check_status(get_delivery_order_package_status, [0, 1, 3])
    def execute_mock_package_call_back(self, delivery_order_code, transport_mode, order_sku_list):
        package_call_back_result = self.wms_app.delivery_mock_package_call_back(delivery_order_code, transport_mode,
                                                                                order_sku_list)
        if not self.wms_app.is_success(package_call_back_result):
            return {"result": ExecuteResult.fail, "info": "包裹方案回调失败！", "data": package_call_back_result}
        self.execute_info += "回调包裹方案成功-->"

        return {"result": ExecuteResult.success, "info": "包裹方案回调成功！", "data": package_call_back_result}

    @check_status(get_delivery_order_express_status, [0, 1, 3])
    def execute_mock_label_call_back(self, delivery_order_code, package_list):
        label_call_back_result = self.wms_app.delivery_mock_label_callback(delivery_order_code, package_list)
        if not self.wms_app.is_success(label_call_back_result):
            return {"result": ExecuteResult.fail, "info": "面单回调失败！", "data": label_call_back_result}
        self.execute_info += "回调面单成功-->"
        return {"result": ExecuteResult.success, "info": "面单回调成功！", "data": label_call_back_result}

    @check_status(get_delivery_order_status, [10])
    @check_status(get_delivery_order_package_status, [2])
    def backend_execute_create_pick_order(self, delivery_order_code, prod_type):
        create_pick_order_result = self.wms_app.delivery_create_pick_order(delivery_order_code, prod_type)
        if not self.wms_app.is_success(create_pick_order_result):
            return {"result": ExecuteResult.fail, "info": "创建拣货单失败！", "data": create_pick_order_result}
        self.execute_info += "创建拣货单成功-->"

        return {"result": ExecuteResult.success, "info": "创建拣货单成功！", "data": create_pick_order_result["data"]}

    @check_status(get_delivery_order_status, [20])
    def execute_pick(self, delivery_order_code, pick_order_code, pick_order_id):
        # 分配拣货人
        assign_pick_user_result = self.wms_app.delivery_assign_pick_user(pick_order_code)
        if not self.wms_app.is_success(assign_pick_user_result):
            return {"result": ExecuteResult.fail, "info": "分配拣货人失败！", "data": assign_pick_user_result}
        # 获取拣货明细
        get_to_pick_data_result = self.wms_app.delivery_get_pick_data(pick_order_id)
        if not self.wms_app.is_success(get_to_pick_data_result):
            return {"result": ExecuteResult.fail, "info": "获取拣货单待拣货明细失败！", "data": get_to_pick_data_result}
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
        # 确认拣货
        confirm_pick_result = self.wms_app.delivery_confirm_pick(pick_order_code, normal_list, [])
        if not self.wms_app.is_success(confirm_pick_result):
            return {"result": ExecuteResult.fail, "info": "确认拣货失败！", "data": confirm_pick_result}
        self.execute_info += "拣货成功-->"

        return {"result": ExecuteResult.success, "info": "确认拣货成功！", "data": confirm_pick_result}

    @check_status(get_delivery_order_status, [30])
    @check_status(get_delivery_order_package_status, [2])
    def backend_save_package(self, delivery_order_code):
        # 获取出库单包裹方案信息
        package_info_result = self.wms_app.delivery_package_info(delivery_order_code)
        if not self.wms_app.is_success(package_info_result):
            return {"result": ExecuteResult.fail, "info": "获取包裹方案信息失败！", "data": package_info_result}
        package_info = package_info_result["data"]

        # 提交维护包裹
        save_package_result = self.wms_app.delivery_save_package(package_info)
        if not self.wms_app.is_success(save_package_result):
            return {"result": ExecuteResult.fail, "info": "提交维护包裹信息失败！", "data": save_package_result}
        self.execute_info += "维护包裹成功-->"
        return {"result": ExecuteResult.success, "info": "提交维护包裹信息成功！", "data": save_package_result}

    @check_status(get_delivery_order_status, [30])
    def execute_review(self, delivery_order_code, delivery_order_id):
        # 构造复核正常数据
        normal_list = [{"deliveryOrderId": delivery_order_id, "deliveryOrderCode": delivery_order_code}]
        # 执行复核
        review_result = self.wms_app.delivery_review(normal_list, [])
        if not self.wms_app.is_success(review_result) or review_result["data"]["failSize"] > 0:
            return {"result": ExecuteResult.fail, "info": "复核失败！", "data": review_result}
        self.execute_info += "复核成功-->"
        return {"result": ExecuteResult.success, "info": "复核成功！", "data": review_result}

    @check_status(get_delivery_order_status, [40])
    def execute_shipped(self, delivery_order_code, delivery_order_id):
        # 构造发货正常数据
        normal_ids = [delivery_order_id]
        normal_codes = [delivery_order_code]
        # 执行发货
        shipping_result = self.wms_app.delivery_shipping(normal_ids, normal_codes, [])
        if not self.wms_app.is_success(shipping_result):
            return {"result": ExecuteResult.fail, "info": "发货失败！", "data": shipping_result}
        self.execute_info += "发货成功"

        return {"result": ExecuteResult.success, "info": "发货成功！", "data": shipping_result}

    def run_front_label_delivery(self, delivery_order_info, delivery_order_detail, flow_flag=None):
        """
        执行前置面单销售出库单发货流程
        :param flow_flag: 流程标识，默认为空，执行全部；可选标识：assign_stock,confirm_pick,call_package,call_label,finish_review
        :param delivery_order_detail: 出库单详情
        :param delivery_order_info: 销售出库单信息
        :return
        """
        delivery_order_code = delivery_order_info["deliveryOrderCode"]
        delivery_order_id = delivery_order_info["deliveryOrderId"]
        prod_type = delivery_order_info["operationMode"]
        transport_mode = delivery_order_info["transportMode"]

        pick_order_code_list = delivery_order_info["pickOrderCodeList"] or []
        pick_order_id_list = delivery_order_info["pickOrderIdList"] or []

        # 出库单分配库存
        assign_result = self.execute_assign_stock(delivery_order_code)
        if assign_result.get("result") == ExecuteResult.fail:
            return "Fail", assign_result.get("info")
        # 如果流程标识为分配库存，则执行就返回，中断流程
        if flow_flag == DeliveryFlow.assign_stock:
            return "Success", None

        # 提取出库单sku明细
        order_sku_list = [
            {
                "skuCode": _["skuCode"], "skuName": _["skuName"], "num": _["skuQty"]
            } for _ in delivery_order_detail["packageItems"]]

        # 模拟包裹回调
        mock_package_result = self.execute_mock_package_call_back(delivery_order_code, transport_mode, order_sku_list)
        # 如果流程标识为生成包裹方案，则执行就返回，中断流程
        if mock_package_result.get("result") == ExecuteResult.fail:
            return "Fail", mock_package_result.get("info")
        if flow_flag == DeliveryFlow.call_package:
            return "Success", None

        # 生成包裹是异步，有延迟，等待包裹数据生成
        until(99, 0.5)(
            lambda: self.wms_app.dbo.query_delivery_order_package_info(delivery_order_code) is not None)()

        # 获取维护好的包裹信息
        package_list = self.wms_app.db_get_delivery_order_package_list(delivery_order_code)
        # 面单回调
        mock_label_result = self.execute_mock_label_call_back(delivery_order_code, package_list)
        if mock_label_result.get("result") == ExecuteResult.fail:
            return "Fail", mock_label_result.get("info")
        # 如果流程标识为生成面单，则执行就返回，中断流程
        if flow_flag == DeliveryFlow.call_label:
            return "Success", None

        # 创建拣货单
        create_pick_order_result = self.backend_execute_create_pick_order(delivery_order_code, prod_type)

        if create_pick_order_result.get("result") == ExecuteResult.fail:
            return "Fail", create_pick_order_result.get("info")
        elif create_pick_order_result.get("result") == ExecuteResult.skipped:
            pick_order_list = list(zip(pick_order_code_list, pick_order_id_list))
        else:
            pick_order_list = [
                (pick_order["pickOrderCode"],
                 pick_order["pickOrderId"]
                 ) for pick_order in create_pick_order_result.get("data")
            ]
        # 执行拣货
        for pick_order_code, pick_order_id in pick_order_list:
            pick_result = self.execute_pick(delivery_order_code, pick_order_code, pick_order_id)
            if pick_result.get("result") == ExecuteResult.fail:
                return "Fail", pick_result.get("info")

        # 如果流程标识为拣货完成，则执行就返回，中断流程
        if flow_flag == DeliveryFlow.confirm_pick:
            return "Success", None

        review_result = self.execute_review(delivery_order_code, delivery_order_id)
        if review_result.get("result") == ExecuteResult.fail:
            return "Fail", review_result.get("info")
        # 如果流程标识为完成复核，则执行就返回，中断流程
        if flow_flag == "finish_review":
            return "Success", None

        # 执行发货
        shipped_result = self.execute_shipped(delivery_order_code, delivery_order_id)
        if shipped_result.get("result") == ExecuteResult.fail:
            return "Fail", shipped_result.get("info")
        return "Success", None

    def run_backend_label_delivery(self, delivery_order_info, delivery_order_detail, flow_flag=None):
        """
        执行后置面单销售出库单发货流程
        :param flow_flag: 流程标识，默认为空，执行全部；可选标识：assign_stock,confirm_pick,call_package,call_label,finish_review
        :param delivery_order_detail: 销售出库单详情
        :param delivery_order_info: 销售出库单信息
        :return:
        """
        delivery_order_code = delivery_order_info["deliveryOrderCode"]
        delivery_order_id = delivery_order_info["deliveryOrderId"]
        prod_type = delivery_order_info["operationMode"]
        transport_mode = delivery_order_info["transportMode"]

        pick_order_code_list = delivery_order_info["pickOrderCodeList"] or []
        pick_order_id_list = delivery_order_info["pickOrderIdList"] or []

        # 出库单分配库存
        assign_result = self.execute_assign_stock(delivery_order_code)
        if assign_result.get("result") == ExecuteResult.fail:
            return "Fail", assign_result.get("info")
        # 如果流程标识为分配库存，则执行就返回，中断流程
        if flow_flag == DeliveryFlow.assign_stock:
            return "Success", None

        # 提取出库单sku明细
        order_sku_list = [
            {
                "skuCode": _["skuCode"], "skuName": _["skuName"], "num": _["skuQty"]
            } for _ in delivery_order_detail["packageItems"]]

        # 模拟包裹回调
        mock_package_result = self.execute_mock_package_call_back(delivery_order_code, transport_mode, order_sku_list)
        # 如果流程标识为生成包裹方案，则执行就返回，中断流程
        if mock_package_result.get("result") == ExecuteResult.fail:
            return "Fail", mock_package_result.get("info")
        if flow_flag == DeliveryFlow.call_package:
            return "Success", None

        # 创建拣货单
        create_pick_order_result = self.backend_execute_create_pick_order(delivery_order_code, prod_type)

        if create_pick_order_result.get("result") == ExecuteResult.fail:
            return "Fail", create_pick_order_result.get("info")
        elif create_pick_order_result.get("result") == ExecuteResult.skipped:
            pick_order_list = list(zip(pick_order_code_list, pick_order_id_list))
        else:
            pick_order_list = [
                (pick_order["pickOrderCode"],
                 pick_order["pickOrderId"]
                 ) for pick_order in create_pick_order_result.get("data")
            ]
        # 执行拣货
        for pick_order_code, pick_order_id in pick_order_list:
            pick_result = self.execute_pick(delivery_order_code, pick_order_code, pick_order_id)
            if pick_result.get("result") == ExecuteResult.fail:
                return "Fail", pick_result.get("info")

        # 如果流程标识为拣货完成，则执行就返回，中断流程
        if flow_flag == DeliveryFlow.confirm_pick:
            return "Success", None
        # 维护包裹
        save_package_result = self.backend_save_package(delivery_order_code)
        if save_package_result.get("result") == ExecuteResult.fail:
            return "Fail", save_package_result.get("info")
        # 如果流程标识为维护包裹完成，则执行就返回，中断流程
        if flow_flag == DeliveryFlow.save_package:
            return "Success", None

        # 获取维护好的包裹信息
        package_list = self.wms_app.db_get_delivery_order_package_list(delivery_order_code)
        # 面单回调
        mock_label_result = self.execute_mock_label_call_back(delivery_order_code, package_list)
        if mock_label_result.get("result") == ExecuteResult.fail:
            return "Fail", mock_label_result.get("info")
        # 如果流程标识为生成面单，则执行就返回，中断流程
        if flow_flag == DeliveryFlow.call_label:
            return "Success", None

        review_result = self.execute_review(delivery_order_code, delivery_order_id)
        if review_result.get("result") == ExecuteResult.fail:
            return "Fail", review_result.get("info")
        # 如果流程标识为完成复核，则执行就返回，中断流程
        if flow_flag == "finish_review":
            return "Success", None

        # 执行发货
        shipped_result = self.execute_shipped(delivery_order_code, delivery_order_id)
        if shipped_result.get("result") == ExecuteResult.fail:
            return "Fail", shipped_result.get("info")
        return "Success", self.execute_info

    def run_delivery(self, delivery_order_code, warehouse_id, flow_flag=None):
        """
        执行销售出库发货流程
        :param flow_flag: 流程标识，默认为空，执行全部；可选标识：assign_stock,confirm_pick,call_package,call_label,finish_review
        :param warehouse_id: 仓库id
        :param delivery_order_code: 销售出库单号列表
        :return:
        """
        switch_result = self.wms_app.common_switch_warehouse(warehouse_id)
        if not self.wms_app.is_success(switch_result):
            return "Fail", "Fail to switch warehouse!"

        # 通过销售出库单列表用出库单号查询获取销售出库单信息
        delivery_order_page_result = self.wms_app.delivery_get_delivery_order_page([delivery_order_code])
        if not self.wms_app.is_success(delivery_order_page_result) or self.wms_app.is_data_empty(
                delivery_order_page_result):
            return "Fail", "Fail to get delivery order page info"

        delivery_order_info = delivery_order_page_result["data"]["records"][0]
        delivery_order_id = delivery_order_info["deliveryOrderId"]

        # 提取出库单作业模式
        operate_mode = delivery_order_info["operationMode"]

        # 获取出库单明细
        delivery_order_detail_result = self.wms_app.delivery_get_delivery_order_detail(delivery_order_id)
        if not self.wms_app.is_success(delivery_order_detail_result):
            return "Fail", "Fail to get delivery order detail!"

        delivery_order_detail = delivery_order_detail_result["data"]

        if operate_mode == 1:
            # 作业模式为1代表前置面单，执行前置面单出库流程
            print("执行前置面单发货流程:")
            result = self.run_front_label_delivery(delivery_order_info, delivery_order_detail, flow_flag)
        else:
            # 其他代表后置面单，执行后置面单出库流程
            print("执行后置面单发货流程:")
            result = self.run_backend_label_delivery(delivery_order_info, delivery_order_detail, flow_flag)
        return result


#
if __name__ == "__main__":
    delivery_order_code = "PRE-CK2306280011"
    warehouse_id = 513
    flag = DeliveryFlow.call_package
    run = RunDelivery()
    print(run.run_delivery(delivery_order_code, warehouse_id))
