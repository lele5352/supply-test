from robot_run.run_transfer import run_transfer
from cases import *


def get_demand_sku_bom(demand_code):
    data = wms_app_robot.dbo.query_demand_detail(demand_code)
    bom = data[0]['bom_version']
    return bom


def get_wait_run_demands():
    """获取待执行调拨流程的调拨需求"""
    data = wms_app_robot.dbo.query_wait_assign_demands()
    demands_list = [
        (
            _['demand_code'],
            _['goods_sku_code'],
            get_demand_sku_bom(_['demand_code']),
            _['demand_qty'], _['warehouse_id'],
            _['delivery_target_warehouse_id'],
            _['receive_warehouse_id'],
            _['receive_target_warehouse_id']
        ) for _ in data]
    return demands_list


def main():
    demands_list = get_wait_run_demands()
    for (demand_code, sku, bom, qty, trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id) in demands_list:
        print("正在执行调拨需求{0}的调拨流程".format(demand_code))
        result, trans_out_order_code = run_transfer(
            demand_code, sku, bom, qty, trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id
        )
        print("执行结果：{0}；对应调拨出库单号：{1}".format(result, trans_out_order_code))


if __name__ == '__main__':
    main()
