import pytest
import allure
import os

from cases import *


@allure.feature("测试模块：调拨")
class TestTransfer(object):
    fhc_to_fhc_data = get_excel_data("test_data/transfer_test_data.xlsx")

    @allure.story("测试场景：调拨出库、调拨入库")
    @pytest.mark.parametrize("goods_list, trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id,expected,bak",
                             fhc_to_fhc_data)
    def test_transfer_flow(self, goods_list, trans_out_id, trans_out_to_id, trans_in_id, trans_in_to_id, expected, bak):
        with allure.step("获取调出仓上架库位"):
            get_out_sj_kw_ids_result = wms_app.db_get_kw(1, 5, len(goods_list), trans_out_id, trans_out_to_id)
            assert get_out_sj_kw_ids_result['code'] == expected
            out_sj_kw_ids = get_out_sj_kw_ids_result['data']

        with allure.step("往调出仓添加相应库存"):
            for sku, bom, qty in goods_list:
                add_stck_result = ims_robot.add_bom_stock(sku, bom, qty, out_sj_kw_ids, trans_out_id, trans_out_to_id)
                assert add_stck_result['code'] == expected

        with allure.step("切到调出仓"):
            # 切到调出仓
            switch_warehouse_result = wms_app.common_switch_warehouse(trans_out_id)
            assert switch_warehouse_result['code'] == expected

        with allure.step("生成调拨需求"):
            # 生成调拨需求
            trans_out_code = wms_app.db_ck_id_to_code(trans_out_id)
            trans_out_to_code = wms_app.db_ck_id_to_code(trans_out_to_id)
            trans_in_code = wms_app.db_ck_id_to_code(trans_in_id)
            trans_in_to_code = wms_app.db_ck_id_to_code(trans_in_to_id)
            demand_list = wms_transfer.get_demand_list(goods_list, trans_out_code, trans_out_to_code,
                                                       trans_in_code, trans_in_to_code)
            assert demand_list is not None

        with allure.step("创建调拨拣货单"):
            # 创建调拨拣货单
            create_pick_order_result = wms_app.transfer_out_create_pick_order(demand_list, 1)
            assert create_pick_order_result['code'] == expected
            pick_order_code = create_pick_order_result['data']

        with allure.step("分配调拨拣货人"):
            # 分配调拨拣货人
            pick_order_assign_result = wms_app.transfer_out_pick_order_assign([pick_order_code], 'admin', 1)
            assert pick_order_assign_result['code'] == expected

        with allure.step("获取调拨拣货单详情数据"):
            # 获取调拨拣货单详情数据
            pick_order_details_result = wms_app.transfer_out_pick_order_detail(pick_order_code)
            assert pick_order_details_result['code'] == expected

            pick_order_details = pick_order_details_result['data']['details']

        with allure.step("获取拣货单sku详情数据"):
            # 获取拣货单sku详情数据
            pick_sku_list = wms_app.transfer_get_pick_sku_list(pick_order_details)

        with allure.step("调拨拣货单确认拣货-纸质"):
            # 调拨拣货单确认拣货-纸质
            confirm_pick_result = wms_app.transfer_out_confirm_pick(pick_order_code, pick_order_details)
            assert confirm_pick_result['code'] == expected

        with allure.step("获取调拨出库托盘库位"):
            get_trans_out_tp_kw_ids_result = wms_app.db_get_kw(1, 3, len(pick_sku_list), trans_out_id,
                                                               trans_out_to_id)
            assert get_trans_out_tp_kw_ids_result['code'] == expected
            trans_out_tp_kw_ids = get_trans_out_tp_kw_ids_result['data']
        with allure.step("调拨拣货单按需装托提交"):
            # 调拨拣货单按需装托提交
            submit_tray_result = wms_app.transfer_out_submit_tray(pick_order_code, pick_order_details,
                                                                  trans_out_tp_kw_ids)
            assert submit_tray_result['code'] == expected

        with allure.step("查看整单获取已装托的托盘"):
            # 查看整单获取已装托的托盘
            tray_detail_result = wms_app.transfer_out_pick_order_tray_detail(pick_order_code)
            assert tray_detail_result['code'] == expected
            tray_code_list = [tray['storageLocationCode'] for tray in tray_detail_result['data']]

        with allure.step("获取生成的调拨出库单号"):
            # 获取生成的调拨出库单号
            finish_result = wms_app.transfer_out_finish_packing(pick_order_code, tray_code_list)
            assert finish_result['code'] == expected
            transfer_out_order_no = finish_result['data']

        with allure.step("获取调拨出库单明细"):
            # 获取调拨出库单明细
            transfer_out_order_detail_result = wms_app.transfer_out_order_detail(transfer_out_order_no)
            assert transfer_out_order_detail_result['code'] == expected
            transfer_out_order_detail = transfer_out_order_detail_result['data']['details']

        with allure.step("调拨箱单复核"):
            # 从调拨出库单明细中提取箱单和库位编码对应关系
            details = [(_['boxNo'], _['storageLocationCode']) for _ in transfer_out_order_detail]
            sorted_details = sorted(details, key=lambda a: a[1])
            # 按箱单和托盘对应逐个复核
            for box_no, tray_code in details:
                review_result = wms_app.transfer_out_order_review(box_no, tray_code)
                assert review_result['code'] == expected

        with allure.step("调拨发货绑定交接单和箱单"):
            for detail in details:
                bind_result = wms_app.transfer_out_box_bind(detail[0], '', '')  # 交接单号和收货仓编码实际可以不用传
                assert bind_result['code'] == expected
                handover_no = bind_result['data']['handoverNo']

        with allure.step("调拨交接单发货"):
            delivery_result = wms_app.transfer_out_delivery(handover_no)
            assert delivery_result['code'] == expected

        with allure.step("切换仓库到调入仓"):
            switch_warehouse_result = wms_app.common_switch_warehouse(trans_in_id)
            assert switch_warehouse_result['code'] == expected

        with allure.step("获取调入仓托盘库位"):
            trans_in_sj_kw_ids_result = wms_app.db_get_kw(1, 5, len(pick_sku_list), trans_in_id, trans_in_to_id)
            assert trans_in_sj_kw_ids_result['code'] == expected
            trans_in_sj_kw_codes = [wms_app.db_kw_id_to_code(kw_id) for kw_id in trans_in_sj_kw_ids_result['data']]

        with allure.step("调拨入库收货"):
            # 调拨入库收货
            receive_result = wms_app.transfer_in_received(handover_no)
            assert receive_result['code'] == expected

        with allure.step("调拨入库按箱单逐个整箱上架"):
            # 调拨入库按箱单逐个整箱上架
            for detail, sj_kw_code in zip(sorted_details, trans_in_sj_kw_codes):
                up_shelf_result = wms_app.transfer_in_up_shelf(detail[0], sj_kw_code)
                assert up_shelf_result['code'] == expected


if __name__ == '__main__':
    os.system("pytest -v -s cases/wms/test_transfer.py --alluredir=./allure-report-files")
    os.system("allure generate ./allure-report-files -o ./reports --clean")
