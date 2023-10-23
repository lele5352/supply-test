from cases import *
from enum import Enum
from utils.custom_wrapper import until
from abc import ABC, abstractmethod


class DeliveryFlow(Enum):
    ASSIGN_STOCK = "assign_stock"
    CONFIRM_PICK = "confirm_pick"
    CALL_PACKAGE = "call_package"
    CALL_LABEL = "call_label"
    SAVE_PACKAGE = "save_package"
    FINISH_REVIEW = "finish_review"


class ExecuteResult(Enum):
    SKIPPED = "Skipped"
    SUCCESS = "Success"
    FAIL = "Fail"


def get_wait_delivery_data():
    data = wms_app.dbo.query_wait_delivery_order()
    order_list = [_["delivery_order_code"] for _ in data]
    return order_list


def get_delivery_order_info(delivery_order_code):
    data = wms_app.dbo.query_delivery_order_info(delivery_order_code)
    if data:
        return data[0]
    return {}


def get_delivery_order_statuses(delivery_order_code):
    data = get_delivery_order_info(delivery_order_code)
    return {
        "order_status": data.get("state"),
        "package_status": data.get("package_state"),
        "express_status": data.get("express_state")
    }


def check_status(get_status, status_type, status):
    """检验获取到的状态是否在状态列表中
    :param get_status: 获取状态函数
    :param status_type: 状态类型：order_status、package_status、express_status
    :param list status: 状态列表"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            order_status = get_status(args[1]).get(status_type)
            if order_status in status:
                result = func(*args, **kwargs)
                return result
            else:
                return {
                    "result": ExecuteResult.SKIPPED,
                    "data": ""
                }

        return wrapper

    return decorator


class DeliveryProcessTemplate(ABC):
    def __init__(self, app_entity=None):
        self.wms_app = app_entity or wms_app
        self.execute_info = "开始-->"

    @check_status(get_delivery_order_statuses, "order_status", [0, 5])
    def execute_assign_stock(self, delivery_order_code):
        assign_stock_result = self.wms_app.delivery_assign_stock([delivery_order_code])
        if not self.wms_app.is_success(assign_stock_result) or assign_stock_result["data"]["failNum"] > 0:
            return {"result": ExecuteResult.FAIL, "data": assign_stock_result}
        return {"result": ExecuteResult.SUCCESS, "data": assign_stock_result}

    @check_status(get_delivery_order_statuses, "package_status", [0, 1, 3])
    def execute_mock_package_call_back(self, delivery_order_code, transport_mode, order_sku_list):
        package_call_back_result = self.wms_app.delivery_mock_package_call_back(delivery_order_code, transport_mode,
                                                                                order_sku_list)
        if not self.wms_app.is_success(package_call_back_result):
            return {"result": ExecuteResult.FAIL, "data": package_call_back_result}
        return {"result": ExecuteResult.SUCCESS, "data": package_call_back_result}

    @check_status(get_delivery_order_statuses, "express_status", [0, 1, 3])
    def execute_mock_label_call_back(self, delivery_order_code, package_list):
        label_call_back_result = self.wms_app.delivery_mock_label_callback(delivery_order_code, package_list)
        if not self.wms_app.is_success(label_call_back_result):
            return {"result": ExecuteResult.FAIL, "data": label_call_back_result}
        return {"result": ExecuteResult.SUCCESS, "data": label_call_back_result}

    @check_status(get_delivery_order_statuses, "order_status", [10])
    @check_status(get_delivery_order_statuses, "package_status", [2])
    def backend_execute_create_pick_order(self, delivery_order_code, prod_type):
        create_pick_order_result = self.wms_app.delivery_create_pick_order(delivery_order_code, prod_type)
        if not self.wms_app.is_success(create_pick_order_result):
            return {"result": ExecuteResult.FAIL, "data": create_pick_order_result}
        return {"result": ExecuteResult.SUCCESS, "data": create_pick_order_result}

    @check_status(get_delivery_order_statuses, "order_status", [20])
    def execute_pick(self, delivery_order_code, pick_order_code, pick_order_id):
        # 分配拣货人
        assign_pick_user_result = self.wms_app.delivery_assign_pick_user(pick_order_code)
        if not self.wms_app.is_success(assign_pick_user_result):
            self.execute_info += "分配拣货人失败"
            return {"result": ExecuteResult.FAIL, "data": assign_pick_user_result}
        # 获取拣货明细
        get_to_pick_data_result = self.wms_app.delivery_get_pick_data(pick_order_id)
        if not self.wms_app.is_success(get_to_pick_data_result):
            self.execute_info += "获取拣货单待拣货明细失败"
            return {"result": ExecuteResult.FAIL, "data": get_to_pick_data_result}
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
            return {"result": ExecuteResult.FAIL, "data": confirm_pick_result}
        return {"result": ExecuteResult.SUCCESS, "data": confirm_pick_result}

    @check_status(get_delivery_order_statuses, "order_status", [30])
    @check_status(get_delivery_order_statuses, "package_status", [2])
    def execute_backend_save_package(self, delivery_order_code):
        # 获取出库单包裹方案信息
        package_info_result = self.wms_app.delivery_package_info(delivery_order_code)
        if not self.wms_app.is_success(package_info_result):
            self.execute_info += "获取包裹方案信息失败"
            return {"result": ExecuteResult.FAIL, "data": package_info_result}
        package_info = package_info_result["data"]

        # 提交维护包裹
        save_package_result = self.wms_app.delivery_save_package(package_info)
        if not self.wms_app.is_success(save_package_result):
            return {"result": ExecuteResult.FAIL, "data": save_package_result}
        return {"result": ExecuteResult.SUCCESS, "data": save_package_result}

    @check_status(get_delivery_order_statuses, "order_status", [30])
    def execute_review(self, delivery_order_code, delivery_order_id):
        # 构造复核正常数据
        normal_list = [{"deliveryOrderId": delivery_order_id, "deliveryOrderCode": delivery_order_code}]
        # 执行复核
        review_result = self.wms_app.delivery_review(normal_list, [])
        if not self.wms_app.is_success(review_result) or review_result["data"]["failSize"] > 0:
            return {"result": ExecuteResult.FAIL, "data": review_result}
        return {"result": ExecuteResult.SUCCESS, "data": review_result}

    @check_status(get_delivery_order_statuses, "order_status", [40])
    def execute_shipped(self, delivery_order_code, delivery_order_id):
        # 构造发货正常数据
        normal_ids = [delivery_order_id]
        normal_codes = [delivery_order_code]
        # 执行发货
        shipping_result = self.wms_app.delivery_shipping(normal_ids, normal_codes, [])
        if not self.wms_app.is_success(shipping_result):
            return {"result": ExecuteResult.FAIL, "data": shipping_result}
        return {"result": ExecuteResult.SUCCESS, "data": shipping_result}

    @abstractmethod
    def execute_specific_flow(self, delivery_order_code, flow_flag):
        # 执行特定流程的抽象方法，子类必须实现
        pass

    def handle_result(self, execute_result, success_msg="", fail_msg="", skipped_msg=""):
        if execute_result.get("result") == ExecuteResult.FAIL:
            self.execute_info += fail_msg
            return ExecuteResult.FAIL
        elif execute_result.get("result") == ExecuteResult.SKIPPED:
            self.execute_info += skipped_msg
            return ExecuteResult.SKIPPED
        else:
            self.execute_info += success_msg
            return execute_result.get("data")

    def run_delivery(self, delivery_order_info, flow_flag=None):
        """
        执行后置面单销售出库单发货流程
        :param delivery_order_info: 通过数据库查询到的销售出库单表的数据
        :param flow_flag: 流程标识，默认为空，执行全部；可选标识：assign_stock,confirm_pick,call_package,call_label,finish_review
        :return:
        """
        # 通过查询获取出库单所属仓库
        warehouse_id = delivery_order_info.get("warehouse_id")
        delivery_order_id = delivery_order_info["id"]
        delivery_order_code = delivery_order_info["delivery_order_code"]
        transport_mode = delivery_order_info["transport_mode"]
        # 切换到对应仓库
        switch_result = self.wms_app.common_switch_warehouse(warehouse_id)
        if not self.wms_app.is_success(switch_result):
            return "Fail", "Fail to switch warehouse!"

        # 获取出库单明细
        delivery_order_detail_result = self.wms_app.delivery_get_delivery_order_detail(delivery_order_id)
        if not self.wms_app.is_success(delivery_order_detail_result):
            return "Fail", "Fail to get delivery order detail!"

        delivery_order_detail = delivery_order_detail_result["data"]

        # 出库单分配库存
        assign_res = self.execute_assign_stock(delivery_order_code)
        assign_result = self.handle_result(assign_res, "分配库存成功-->", "分配库存失败", "跳过执行分配库存-->")
        if assign_result == ExecuteResult.FAIL:
            return "Fail", self.execute_info
        # 如果流程标识为分配库存，则执行就返回，中断流程
        if flow_flag == DeliveryFlow.ASSIGN_STOCK:
            self.execute_info += "流程结束"
            return "Success", self.execute_info

        # 提取出库单sku明细
        order_sku_list = [
            {
                "skuCode": _["skuCode"], "skuName": _["skuName"], "num": _["skuQty"]
            } for _ in delivery_order_detail["packageItems"]]

        # 模拟包裹回调
        mock_pkg_res = self.execute_mock_package_call_back(delivery_order_code, transport_mode, order_sku_list)
        mock_pkg_result = self.handle_result(mock_pkg_res, "包裹方案回调成功-->", "包裹方案回调失败",
                                             "跳过回调包裹方案-->")
        # 如果流程标识为生成包裹方案，则执行就返回，中断流程
        if mock_pkg_result == ExecuteResult.FAIL:
            return "Fail", self.execute_info
        if flow_flag == DeliveryFlow.CALL_PACKAGE:
            self.execute_info += "流程结束"
            return "Success", self.execute_info

        result, info = self.execute_specific_flow(delivery_order_code, flow_flag)
        if result == ExecuteResult.FAIL:
            return "Fail", info
        # 子类里面执行结果为成功时代表子类行为触发了流程标识需要中断流程，所以这里强行退出
        elif result == ExecuteResult.SUCCESS:
            return "Success", info

        # 执行复核
        review_res = self.execute_review(delivery_order_code, delivery_order_id)
        review_result = self.handle_result(review_res, "复核成功-->", "复核失败", "跳过复核-->")
        if review_result == ExecuteResult.FAIL:
            return "Fail", self.execute_info
        # 如果流程标识为完成复核，则执行就返回，中断流程
        if flow_flag == "finish_review":
            self.execute_info += "流程结束"
            return "Success", self.execute_info

        # 执行发货
        shipped_res = self.execute_shipped(delivery_order_code, delivery_order_id)
        shipped_result = self.handle_result(shipped_res, "发货成功", "发货失败", "跳过发货")
        if shipped_result == ExecuteResult.FAIL:
            return "Fail", self.execute_info
        return "Success", self.execute_info


class FrontLabelDeliveryProcess(DeliveryProcessTemplate):
    def execute_specific_flow(self, delivery_order_code, flow_flag):
        # 通过销售出库单列表用出库单号查询获取销售出库单信息
        query_result = self.wms_app.delivery_get_delivery_order_page([delivery_order_code])
        if not self.wms_app.is_success(query_result) or self.wms_app.is_data_empty(query_result):
            return "Fail", "Fail to get delivery order page info"

        delivery_order_info = query_result["data"]["records"][0]

        prod_type = delivery_order_info["operationMode"]
        pick_order_code_list = delivery_order_info["pickOrderCodeList"] or []
        pick_order_id_list = delivery_order_info["pickOrderIdList"] or []

        # 生成包裹是异步，有延迟，等待包裹数据生成
        until(99, 0.5)(
            lambda: self.wms_app.dbo.query_delivery_order_package_info(delivery_order_code) is not None)()
        # 获取维护好的包裹信息
        package_list = self.wms_app.db_get_delivery_order_package_list(delivery_order_code)

        # 面单回调
        mock_label_res = self.execute_mock_label_call_back(delivery_order_code, package_list)
        mock_label_result = self.handle_result(mock_label_res, "面单回调成功-->", "面单回调失败", "跳过回调面单-->")
        if mock_label_result == ExecuteResult.FAIL:
            return "Fail", self.execute_info
        # 如果流程标识为生成面单，则执行就返回，中断流程
        if flow_flag == DeliveryFlow.CALL_LABEL:
            self.execute_info += "流程结束"
            return "Success", self.execute_info

        # 创建拣货单
        create_pick_order_res = self.backend_execute_create_pick_order(delivery_order_code, prod_type)
        create_result = self.handle_result(create_pick_order_res, "创建拣货单成功-->", "创建拣货单失败",
                                           "跳过创建拣货单-->")
        if create_result == ExecuteResult.FAIL:
            return "Fail", self.execute_info
        elif create_result == ExecuteResult.SKIPPED:
            pick_order_list = list(zip(pick_order_code_list, pick_order_id_list))
        else:
            pick_order_list = [
                (pick_order["pickOrderCode"],
                 pick_order["pickOrderId"])
                for pick_order in create_result.get("data")
            ]

        # 执行拣货
        for pick_order_code, pick_order_id in pick_order_list:
            pick_res = self.execute_pick(delivery_order_code, pick_order_code, pick_order_id)
            pick_result = self.handle_result(pick_res, "拣货成功-->", "拣货失败", f"跳过拣货{pick_order_code}-->")
            if pick_result == ExecuteResult.FAIL:
                return "Fail", self.execute_info
        # 如果流程标识为拣货完成，则执行就返回，中断流程
        if flow_flag == DeliveryFlow.CONFIRM_PICK:
            self.execute_info += "流程结束"
            return "Success", self.execute_info
        return "Continue", self.execute_info


class BackendLabelDeliveryProcess(DeliveryProcessTemplate):
    def execute_specific_flow(self, delivery_order_info, flow_flag):
        # 通过销售出库单列表用出库单号查询获取销售出库单信息
        query_result = self.wms_app.delivery_get_delivery_order_page([delivery_order_code])
        if not self.wms_app.is_success(query_result) or self.wms_app.is_data_empty(query_result):
            return "Fail", "Fail to get delivery order page info"

        delivery_order_info = query_result["data"]["records"][0]

        prod_type = delivery_order_info["operationMode"]
        pick_order_code_list = delivery_order_info["pickOrderCodeList"] or []
        pick_order_id_list = delivery_order_info["pickOrderIdList"] or []
        # 创建拣货单
        create_pick_order_res = self.backend_execute_create_pick_order(delivery_order_code, prod_type)
        create_result = self.handle_result(create_pick_order_res, "创建拣货单成功-->", "创建拣货单失败",
                                           "跳过创建拣货单-->")
        if create_result == ExecuteResult.FAIL:
            return "Fail", self.execute_info
        elif create_result == ExecuteResult.SKIPPED:
            pick_order_list = list(zip(pick_order_code_list, pick_order_id_list))
        else:
            pick_order_list = [
                (pick_order["pickOrderCode"],
                 pick_order["pickOrderId"])
                for pick_order in create_result.get("data")
            ]

        # 执行拣货
        for pick_order_code, pick_order_id in pick_order_list:
            pick_res = self.execute_pick(delivery_order_code, pick_order_code, pick_order_id)
            pick_result = self.handle_result(pick_res, "拣货成功-->", "拣货失败", f"跳过拣货{pick_order_code}-->")
            if pick_result == ExecuteResult.FAIL:
                return "Fail", self.execute_info
        # 如果流程标识为拣货完成，则执行就返回，中断流程
        if flow_flag == DeliveryFlow.CONFIRM_PICK:
            self.execute_info += "流程结束"
            return "Success", self.execute_info

        # 维护包裹
        save_package_res = self.execute_backend_save_package(delivery_order_code)
        save_package_result = self.handle_result(save_package_res, "维护包裹成功-->", "维护包裹失败", "跳过维护包裹-->")
        if save_package_result == ExecuteResult.FAIL:
            return "Fail", self.execute_info
        # 如果流程标识为维护包裹完成，则执行就返回，中断流程
        if flow_flag == DeliveryFlow.SAVE_PACKAGE:
            self.execute_info += "流程结束"
            return "Success", self.execute_info

        # 获取维护好的包裹信息
        package_list = self.wms_app.db_get_delivery_order_package_list(delivery_order_code)
        # 面单回调
        mock_label_res = self.execute_mock_label_call_back(delivery_order_code, package_list)
        mock_label_result = self.handle_result(mock_label_res, "面单回调成功-->", "面单回调失败", "跳过回调面单-->")
        if mock_label_result == ExecuteResult.FAIL:
            return "Fail", self.execute_info
        # 如果流程标识为生成面单，则执行就返回，中断流程
        if flow_flag == DeliveryFlow.CALL_LABEL:
            self.execute_info += "流程结束"
            return "Success", self.execute_info
        return "Continue", self.execute_info


def main(delivery_order_code, flow_flag=""):
    delivery_order_info = get_delivery_order_info(delivery_order_code)
    operate_mode = delivery_order_info.get("operation_mode")
    if operate_mode == 1:
        # 作业模式为1代表前置面单，执行前置面单出库流程
        print("执行前置面单发货流程:")
        result = FrontLabelDeliveryProcess().run_delivery(delivery_order_info, flow_flag)
    else:
        # 其他代表后置面单，执行后置面单出库流程
        print("执行后置面单发货流程:")
        result = BackendLabelDeliveryProcess().run_delivery(delivery_order_info, flow_flag)
    return result


if __name__ == "__main__":
    delivery_order_code = "PRE-CK2211100004"
    flag = DeliveryFlow.CONFIRM_PICK
    print(main(delivery_order_code, flag))
