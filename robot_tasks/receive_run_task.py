from cases import *
from robot_run.run_receive import run_receive


def query_wait_receive_entry_order():
    data = wms_app_robot.dbo.query_wait_receive_entry_order()
    entry_order_list = [
        (_['distribute_order_code'], _['warehouse_id'], _['dest_warehouse_id']) for _ in data

    ]
    return entry_order_list


def main():
    entry_order_list = query_wait_receive_entry_order()
    for (distribute_order_code, warehouse_id, target_warehouse_id) in entry_order_list:
        print("正在执行收货仓：{0}，分货单：{1}的采购入库流程".format(wms_app_robot.ck_id_to_code(warehouse_id),
                                                                   distribute_order_code))
        result, entry_order_code = run_receive(
            distribute_order_code, warehouse_id, target_warehouse_id
        )
        print("执行结果：{0}；对应入库库单号：{1}".format(result, entry_order_code))


if __name__ == '__main__':
    main()
