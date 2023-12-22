import time
from multiprocessing import Process

from robot_run.run_receive import *
from robot_run.run_transfer import *
from robot_run.run_delivery import *
from robot_run.run_purchase import *


def robot_run_receive():
    entry_order_list = query_wait_receive_data()
    if not entry_order_list:
        print('当前无新建状态的采购入库单！')
        return
    for (order_code, ck_id, to_ck_id) in entry_order_list:
        print("正在执行收货仓：{0}，分货单：{1}的采购入库流程".format(wms_app.db_ck_id_to_code(ck_id), order_code))
        result, info = run_receive(order_code, False)
        print("执行结果：{0}；对应分货单号：{1}；错误信息：{2}".format(result, order_code, info))


def robot_run_transfer():
    data = wms_app.dbo.query_wait_assign_demands()
    if not data:
        return
    demands_list = [
        (
            _['demand_code'],
            _['warehouse_id'],
            _['delivery_target_warehouse_id'],
            _['receive_warehouse_id'],
            _['receive_target_warehouse_id'],
            _['delivery_warehouse_code']
        ) for _ in data]
    if not demands_list:
        print('当前无待分配状态的调拨需求！')
        return
    for (demand_code, trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id, warehouse_code) in demands_list:
        print("正在执行仓库：{0}、调拨需求编码为：{1} 的调拨流程".format(warehouse_code, demand_code))
        result, info = run_transfer(demand_code)
        print("执行结果：{0}；对应调拨需求编码：{1}；错误信息：{2}".format(result, demand_code, info))


def robot_run_delivery():
    order_list = get_wait_delivery_data()
    if not order_list:
        print('当前无待发货状态的销售出库单！')
        return
    for order_no in order_list:
        print(f"正在执行销售出库单号为{order_no}的出库流程")
        result, info = main(order_no)
        print("执行结果：{0}；对应销售出库单号：{1}；错误信息：{2}".format(result, order_no, info))


def robot_run_purchase():
    shortage_demand_ids = get_wait_purchase_shortage_demands()

    if not shortage_demand_ids:
        print('当前无待采购的缺货需求！')
    else:
        for child_list in shortage_demand_ids:
            confirm_result = scm_app.shortage_demand_batch_confirm(child_list)
            if not confirm_result["code"]:
                print("缺货需求{0}确认失败".format(child_list))

    purchase_demand_ids = get_wait_purchase_demands()
    if not purchase_demand_ids:
        print("当前无待采购的采购需求!")
    else:
        for child_list in purchase_demand_ids:
            # 根据采购需求id批量确认并生单
            confirm_and_buy_res = scm_app.confirm_and_generate_purchase_order(child_list)
            if not confirm_and_buy_res["code"]:
                print("采购需求批量确认并生单失败！")
    # 采购需求下单是异步，可能有延迟
    time.sleep(3)

    purchase_order_list = get_wait_purchase_order()
    if not purchase_order_list:
        print("当前无待采购的采购单!")
    else:
        for purchase_order_no in purchase_order_list:
            print("正在执行采购单{0}的采购流程".format(purchase_order_no))
            result, info = run_purchase(purchase_order_no)
            print("采购单{0}执行结果为：{1}； 错误原因：{2}".format(purchase_order_no, result, info))


if __name__ == '__main__':
    # p1 = Process(target=robot_run_transfer)
    # p2 = Process(target=robot_run_receive)
    p3 = Process(target=robot_run_delivery)
    # p4 = Process(target=robot_run_purchase)
    # p1.start()
    # p2.start()
    p3.start()
    # p4.start()
    # p1.join()
    # p2.join()
    p3.join()
    # p4.join()
    # robot_run_purchase()
    # robot_run_receive()
    # robot_run_transfer()
    robot_run_delivery()
    print('tasks have been completely run!')
