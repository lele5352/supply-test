import pytest
import allure
import os

from data_generator import *
from data_generator.scm_data_generator import ScmDataGenerator

scm_data = ScmDataGenerator(scm_app)
distribute_order_list = scm_data.create_distribute_order(["63203684930"], 1, 'ESZZ', 'ESFH')
entry_order_data = [
    (
        order[0],
        wms_app.db_ck_code_to_id(order[1]),
        wms_app.db_ck_code_to_id(order[2]),
        1
    ) for order in distribute_order_list
]


@allure.feature("测试模块：采购入库")
class TestReceive(object):
    @allure.story("测试场景：采购入库主流程")
    @pytest.mark.parametrize("distribute_order_code,warehouse_id,to_warehouse_id,expected", entry_order_data)
    def test_receive_flow(self, distribute_order_code, warehouse_id, to_warehouse_id, expected):
        with allure.step("切换到收货仓库"):
            switch_result = wms_app.common_switch_warehouse(warehouse_id)
            assert switch_result['code'] == expected
        with allure.step("通过入库单列表接口获取分货单对应入库单"):
            search_result = wms_app.receipt_entry_order_page([distribute_order_code])
            assert search_result['code'] == expected
            # 提取入库单信息
            entry_order_info = search_result['data']['records'][0]

        with allure.step("扫描入库单获取入库单商品明细"):
            entry_order_code = entry_order_info.get('entryOrderCode')
            scan_result = wms_app.receipt_entry_order_detail(entry_order_code)
            assert scan_result['code'] == expected
            entry_order_detail = scan_result.get('data')
            pre_receive_order_code = entry_order_detail.get('predictReceiptOrderCode')
            receive_sku_list = entry_order_detail.get("skuInfos")

        with allure.step("获取闲置状态的收货库位和上架库位"):
            get_sh_kw_result = wms_app.db_get_kw(2, 1, len(receive_sku_list), warehouse_id, to_warehouse_id)
            assert get_sh_kw_result["code"] == expected
            sh_kw_codes = get_sh_kw_result['data']

            get_sj_kw_result = wms_app.db_get_kw(2, 5, len(receive_sku_list), warehouse_id, to_warehouse_id)
            assert get_sj_kw_result["code"] == expected
            sj_kw_codes = get_sj_kw_result['data']

        with allure.step("扫描收货库位和sku并确认收货，生成预收货单数据"):
            for sku, kw in zip(receive_sku_list, sh_kw_codes):
                sku.update({
                    "locationCode": kw,
                    "skuNumber": sku['totalNumber']
                })
            receive_result = wms_app.receipt_confirm_receive(entry_order_code, pre_receive_order_code, receive_sku_list)
            assert receive_result["code"] == expected

        with allure.step("提交预收货单"):
            pre_receive_order_list = [pre_receive_order_code]
            submit_pre_receive_order_result = wms_app.receipt_submit_pre_receive_order(pre_receive_order_list)
            assert submit_pre_receive_order_result['code'] == expected

        with allure.step("上架交接"):
            # 跳过质检，直接上架交接
            handover_result = wms_app.receipt_handover_to_upshelf(sh_kw_codes)
            assert handover_result['code'] == expected

        with allure.step("整托上架"):
            # 整托上架
            for sh_kw_code, sj_kw_code in zip(sh_kw_codes, sj_kw_codes):
                kw_detail_result = wms_app.receipt_location_detail(sh_kw_code)
                assert kw_detail_result['code'] == expected

                upshelf_result = wms_app.receipt_upshelf_whole_location(sh_kw_code, sj_kw_code)
                assert upshelf_result['code'] == expected

        with allure.step("上架完成"):
            # 最后需要再调用上架完成接口，结束流程
            complete_upshelf_result = wms_app.receipt_complete_upshelf()
            assert complete_upshelf_result['code'] == expected


if __name__ == '__main__':
    os.system("pytest -v -s cases/wms/test_receive.py --alluredir=./allure-report-files")
    os.system("allure generate ./allure-report-files -o ./reports --clean")
