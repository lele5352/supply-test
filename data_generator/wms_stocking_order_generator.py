from cases import *

from utils.log_handler import logger as log
from dbo.warehouse_manage_dbo import WarehouseManageDBOperator


class WmsStockingGenerator:
    def __init__(self):
        self.wms_app = wms_app

    def inventory_process_order_create(self, warehouse_id, **order_info):
        """
        盘点单-造单据脚本
        :param warehouse_id: 仓库
        :param order_info: {
                "inventoryProcessLatitude": 0,  # 盘点类型(0-常规盘点;1-短拣盘点;2-抽盘)
                "inventoryProcessRange": 0,     # 盘点维度(0-库位;1-SKU)
                "inventoryProcessType": 0,      # 盘点范围(0-库位;1-库存+SKU)
                "locDetails": [                 # 盘点单库位详情(盘点纬度是库位时，不能为空)--非必须
                    {
                        "locCode": "KW-SJQ-01"
                    }
                ]，
                "skuDetails": [   #盘点单SKU详情(盘点纬度是SKU时，不能为空)
                    {
                      "locCode": 库位编码,
                      "skuCode": sku编码
                    }
                ]
        }
        :return:
        """
        self.wms_app.common_switch_warehouse(warehouse_id)
        create_res = self.wms_app.inventory_process_order_create(**order_info)
        if not create_res or create_res['code'] != 1:
            log.error('创建盘点单失败！')
            return
        return create_res['data']


class WmsStockingProcess(WmsStockingGenerator):
    def wms_stocking_process(self, warehouse_id, now_qty, audit_state, **order_info):
        """

        :param warehouse_id: int 相关仓库id
        :param now_qty: int 相对当前数量的盘点差异数量（例：当前2个，输入1，实盘数量就为：2+1，输入-1，实盘数量就为：2-1）
        :param audit_state: int 审核结果：1-通过，2-不通过
        :param order_info: dict 盘点单基本信息
        :return:
        """
        stocktaking_order_code = self.inventory_process_order_create(warehouse_id, **order_info)
        # stocktaking_order_code = "PD2306280008"
        page_kwargs = {
            "inventoryProcessOrderNoLike": stocktaking_order_code
        }
        res = self.wms_app.inventory_process_order_page(**page_kwargs)
        qty = res.get("data")["records"][0]["locQty"]
        self.wms_app.inventory_process_order_generate_task(stocktaking_order_code, qty)
        task_list = WarehouseManageDBOperator.stocktaking_task_by_order_code(stocktaking_order_code)
        # task_list = [(2109, 'PD2306280008_T2-1')]
        self.wms_app.inventory_process_assign([i[1] for i in task_list])
        for i in task_list:
            self.wms_app.inventory_process_print(i[1])
            # 调打印次数接口，变更盘点任务单的状态为：盘点中。以便继续作业
            self.wms_app.inventory_process_print_times(i[1])
        for task_item in task_list:
            res = self.wms_app.inventory_process_task_detail_page(task_item[0])
            task_detail = res.get("data")["records"]
            rep_list = []
            for item in task_detail:
                old_qty = item.get("skuInventoryStartQty")
                if int(now_qty) < 0 and old_qty < abs(int(now_qty)):
                    now_qty = int(-old_qty)
                item = {
                    "skuCode": item.get("skuCode"),
                    "locCode": item.get("locCode"),
                    "inventoryProcessTaskNo": task_item[1],
                    "inventoryProcessTaskDetailId": item.get("inventoryProcessTaskDetailId"),
                    "inventoryProcessQty": old_qty + int(now_qty),  # 实际盘点数量
                    "inventoryStartQty": item.get("skuInventoryStartQty")
                }
                rep_list.append(item)

            self.wms_app.inventory_process_commit(task_item[1], rep_list)
        # 盘点单列表页-生成差异单
        self.wms_app.inventory_process_generate_diff(stocktaking_order_code)

        res = self.wms_app.inventory_process_diff_page(**page_kwargs)
        diff_no = res.get("data")["records"][0]["inventoryProcessDiffNo"]

        res = self.wms_app.inventory_process_diff_detail(diff_no)
        diff_detail = res.get("data")
        # 拼接审核时所需的差异单详情信息
        details = [{"inventoryProcessDiffDetailId": i.get("inventoryProcessDiffDetailId"),
                    "auditState": audit_state, "auditRemarks": "脚本自动审核"} for i in diff_detail]
        self.wms_app.inventory_process_diff_audit(diff_no, details)


if __name__ == '__main__':
    wms_stocking = WmsStockingProcess()
    kwargs = {
        "inventoryProcessLatitude": 0,  # 盘点类型(0-常规盘点;1-短拣盘点;2-抽盘)
        "inventoryProcessRange": 0,  # 盘点维度(0-库位;1-SKU)
        "inventoryProcessType": 0,  # 盘点范围(0-库位;1-库存+SKU)
        "locDetails": [  # 盘点单库位详情(盘点纬度是库位时，不能为空)--非必须
            {
                "locCode": "KW-SJQ-10"
            }
        ]
    }
    wms_stocking.wms_stocking_process(539, -5, 1, **kwargs)
