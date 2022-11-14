import pytest
import allure
import os

from cases import *


@allure.feature("测试模块：采购入库")
class TestReceive(object):
    entry_order_data = get_excel_data("test_data/receive_test_data.xlsx")

    @allure.story("测试场景：采购入库主流程")
    @pytest.mark.parametrize("distribute_order_code,warehouse_id,to_warehouse_id,expected", entry_order_data)
    def test_receive_flow(self, distribute_order_code, warehouse_id, to_warehouse_id, expected):
        with allure.step("切换到收货仓库"):
            switch_result = wms_app.common_switch_warehouse(warehouse_id)
            assert switch_result['code'] == expected

        with allure.step("通过入库单列表接口获取分货单对应入库单"):
            search_result = wms_app.receipt_entry_order_page(distribute_order_code)
            assert search_result['code'] == expected
            entry_order_info = search_result['data']['records'][0]

        with allure.step("扫描入库单获取入库单商品明细"):
            entry_order_code = entry_order_info.get('entryOrderCode')
            scan_result = wms_app.receipt_entry_order_detail(entry_order_code)
            assert scan_result['code'] == expected
            entry_order_detail = scan_result.get('data')
            pre_receive_order_code = entry_order_detail.get('predictReceiptOrderCode')
            receive_sku_list = entry_order_detail.get("skuInfos")
        with allure.step("获取闲置状态的收货库位"):
            sh_kw_codes = wms_app.db_get_kw(2, 1, len(receive_sku_list), warehouse_id, to_warehouse_id)[0]

        with allure.step("扫描收货库位和sku并确认收货，生成预收货单数据"):
            for sku, kw in zip(receive_sku_list, sh_kw_codes):
                sku.update({
                    "locationCode": kw
                })
            receive_result = wms_app.receipt_confirm_receive(entry_order_code, pre_receive_order_code, receive_sku_list)
            assert receive_result == expected

        with allure.step("收货提交"):
            for sku, kw in zip(receive_sku_list, sh_kw_codes):
                sku.update({
                    "locationCode": kw
                })
            receive_result = wms_app.receipt_confirm_receive(entry_order_code, pre_receive_order_code, receive_sku_list)
            assert receive_result == expected


if __name__ == '__main__':
    os.system("pytest -v -s cases/wms/test_receive.py --alluredir=./allure-report-files")
    os.system("allure generate ./allure-report-files -o ./reports --clean")
