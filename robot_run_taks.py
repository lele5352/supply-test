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
    for (distribute_order_code, ck_id, to_ck_id) in entry_order_list:
        print("正在执行收货仓：{0}，分货单：{1}的采购入库流程".format(wms_app.db_ck_id_to_code(ck_id),
                                                                   distribute_order_code))
        result, entry_order_code = run_receive(distribute_order_code, ck_id, to_ck_id)
        print("执行结果：{0}；对应入库库单号：{1}".format(result, entry_order_code))


def robot_run_transfer():
    demands_list = get_wait_transfer_data()
    if not demands_list:
        print('当前无待分配状态的调拨需求！')
        return
    for (demand_code, sku, bom, qty, trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id) in demands_list:
        print("正在执行调拨需求{0}的调拨流程".format(demand_code))
        result, trans_out_order_code = run_transfer(
            demand_code, sku, bom, qty, trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id
        )
        print("执行结果：{0}；对应调拨出库单号：{1}".format(result, trans_out_order_code))


def robot_run_delivery():
    order_list = get_wait_delivery_data()
    if not order_list:
        print('当前无待发货状态的销售出库单！')
        return
    for (ck_id, ck_code, order_no) in order_list:
        print("正在执行仓库id为：{0}、仓库编码：{1}的销售出库单号为{2}的销售发货流程".format(ck_id, ck_code, order_no))
        result, delivery_order_code = run_delivery(order_no, ck_id)
        print("执行结果：{0}；对应销售出库单号：{1}".format(result, order_no))


def robot_run_purchase():
    shortage_demand_ids = get_wait_purchase_shortage_demands()

    if not shortage_demand_ids:
        print('当前无待采购的缺货需求！')
    for child_list in shortage_demand_ids:
        confirm_result = scm_app.shortage_demand_batch_confirm(child_list)
        if not confirm_result["code"]:
            print("缺货需求{0}确认失败".format(child_list))

    purchase_demand_ids = get_wait_purchase_demands()
    if not purchase_demand_ids:
        print("当前无待采购的采购需求")

    for child_list in purchase_demand_ids:
        # 根据采购需求id批量确认并生单
        confirm_and_buy_res = scm_app.confirm_and_generate_purchase_order(child_list)
        if not confirm_and_buy_res["code"]:
            print("采购需求批量确认并生单失败！")
    # 采购需求下单是异步，可能有延迟
    time.sleep(3)

    purchase_order_list = get_wait_purchase_order()
    for purchase_order_no in purchase_order_list:
        print("正在执行采购单{0}的采购流程".format(purchase_order_no))
        result, purchase_order_no = run_purchase(purchase_order_no)
        print("采购单{0}执行结果为：{1}".format(purchase_order_no, result))


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
    print('tasks have been completely run!')
