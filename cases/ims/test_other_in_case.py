import json
import pytest
import allure
import os

from cases import *


@allure.feature("测试模块：其他入库")
class TestOtherInStock(object):
    fhc_cp_other_in_data = ExcelTool("../../test_data/ims_test_data.xlsx").read_data("fhc_cp_other_in", 2)
    bhc_cp_other_in_data = ExcelTool("../../test_data/ims_test_data.xlsx").read_data("bhc_cp_other_in", 2)
    zzc_cp_other_in_data = ExcelTool("../../test_data/ims_test_data.xlsx").read_data("zzc_cp_other_in", 2)
    fhc_lp_other_in_data = ExcelTool("../../test_data/ims_test_data.xlsx").read_data("fhc_lp_other_in", 2)
    bhc_lp_other_in_data = ExcelTool("../../test_data/ims_test_data.xlsx").read_data("bhc_lp_other_in", 2)
    zzc_lp_other_in_data = ExcelTool("../../test_data/ims_test_data.xlsx").read_data("zzc_lp_other_in", 2)

    # @pytest.mark.skip("调试，暂时跳过")
    @allure.story("测试场景：发货仓其他入库，上架次品")
    @allure.severity(allure.severity_level.BLOCKER)  # p0阻塞级用例
    @pytest.mark.parametrize("ware_sku_qty_list,kw_num,warehouse_id,to_warehouse_id,expected,bak", fhc_cp_other_in_data)
    def test_fhc_cp_other_in_stock(self, ware_sku_qty_list, kw_num, warehouse_id, to_warehouse_id, expected, bak):
        ware_sku_qty_list = json.loads(ware_sku_qty_list)
        sale_skus = ims_robot.get_sale_skus(ware_sku_qty_list)

        if kw_num == "one":
            get_kw_result = wms_app.base_get_kw(1, 6, 1, warehouse_id, to_warehouse_id)
            assert get_kw_result['code'] == expected
            cp_kw_id = get_kw_result['data']
            cp_location_ids = cp_kw_id * len(ware_sku_qty_list)
        else:
            get_kw_result = wms_app.base_get_kw(1, 6, len(ware_sku_qty_list), warehouse_id, to_warehouse_id)
            assert get_kw_result['code'] == expected
            cp_location_ids = get_kw_result['data']
        other_in_result = ims_robot.cp_other_in(ware_sku_qty_list, cp_location_ids, warehouse_id, to_warehouse_id)
        assert other_in_result['code'] == expected

        for sale_sku in sale_skus:
            unqualified_inventory = ims_robot.get_format_cp_inventory(sale_sku, warehouse_id)
            expect_cp_inventory = ims_robot.get_cp_other_in_expect_inventory(
                unqualified_inventory, ware_sku_qty_list, cp_location_ids).get(sale_sku)
            assert expect_cp_inventory == unqualified_inventory

    # @pytest.mark.skip("调试，暂时跳过")
    @allure.story("测试场景：备货仓其他入库，上架次品")
    @allure.severity(allure.severity_level.BLOCKER)  # p0阻塞级用例
    @pytest.mark.parametrize("ware_sku_qty_list,kw_num,warehouse_id,to_warehouse_id,expected,bak", bhc_cp_other_in_data)
    def test_bhc_cp_other_in_stock(self, ware_sku_qty_list, kw_num, warehouse_id, to_warehouse_id, expected, bak):
        ware_sku_qty_list = json.loads(ware_sku_qty_list)
        sale_skus = ims_robot.get_sale_skus(ware_sku_qty_list)

        if kw_num == "one":
            get_kw_result = wms_app.base_get_kw(1, 6, 1, warehouse_id, to_warehouse_id)
            assert get_kw_result['code'] == expected
            cp_kw_id = get_kw_result['data']
            cp_location_ids = cp_kw_id * len(ware_sku_qty_list)
        else:
            get_kw_result = wms_app.base_get_kw(1, 6, len(ware_sku_qty_list), warehouse_id, to_warehouse_id)
            assert get_kw_result['code'] == expected
            cp_location_ids = get_kw_result['data']
        other_in_result = ims_robot.cp_other_in(ware_sku_qty_list, cp_location_ids, warehouse_id, to_warehouse_id)
        assert other_in_result['code'] == expected

        for sale_sku in sale_skus:
            unqualified_inventory = ims_robot.get_format_cp_inventory(sale_sku, warehouse_id)
            expect_cp_inventory = ims_robot.get_cp_other_in_expect_inventory(
                unqualified_inventory, ware_sku_qty_list, cp_location_ids).get(sale_sku)
            assert expect_cp_inventory == unqualified_inventory

    # @pytest.mark.skip("调试，暂时跳过")
    @allure.story("测试场景：中转仓其他入库，上架次品")
    @allure.severity(allure.severity_level.BLOCKER)  # p0阻塞级用例
    @pytest.mark.parametrize("ware_sku_qty_list,kw_num,warehouse_id,to_warehouse_id,expected,bak", zzc_cp_other_in_data)
    def test_zzc_cp_other_in_stock(self, ware_sku_qty_list, kw_num, warehouse_id, to_warehouse_id, expected, bak):
        ware_sku_qty_list = json.loads(ware_sku_qty_list)
        sale_skus = ims_robot.get_sale_skus(ware_sku_qty_list)

        if kw_num == "one":
            get_kw_result = wms_app.base_get_kw(1, 6, 1, warehouse_id, to_warehouse_id)
            assert get_kw_result['code'] == expected
            cp_kw_id = get_kw_result['data']
            cp_location_ids = cp_kw_id * len(ware_sku_qty_list)
        else:
            get_kw_result = wms_app.base_get_kw(1, 6, len(ware_sku_qty_list), warehouse_id, to_warehouse_id)
            assert get_kw_result['code'] == expected
            cp_location_ids = get_kw_result['data']
        other_in_result = ims_robot.cp_other_in(ware_sku_qty_list, cp_location_ids, warehouse_id, to_warehouse_id)
        assert other_in_result['code'] == expected

        for sale_sku in sale_skus:
            unqualified_inventory = ims_robot.get_format_cp_inventory(sale_sku, warehouse_id)
            expect_cp_inventory = ims_robot.get_cp_other_in_expect_inventory(
                unqualified_inventory, ware_sku_qty_list, cp_location_ids).get(sale_sku)
            assert expect_cp_inventory == unqualified_inventory

    # @pytest.mark.skip("调试，暂时跳过")
    @allure.story("测试场景：发货仓其他入库，上架良品")
    @allure.severity(allure.severity_level.BLOCKER)  # p0阻塞级用例
    @pytest.mark.parametrize("ware_sku_qty_list,kw_num,warehouse_id,to_warehouse_id,expected,bak", fhc_lp_other_in_data)
    def test_fhc_lp_other_in_stock(self, ware_sku_qty_list, kw_num, warehouse_id, to_warehouse_id, expected, bak):
        ware_sku_qty_list = json.loads(ware_sku_qty_list)
        sale_skus = ims_robot.get_sale_skus(ware_sku_qty_list)

        if kw_num == "one":
            get_kw_result = wms_app.base_get_kw(1, 5, 1, warehouse_id, to_warehouse_id)
            assert get_kw_result['code'] == expected
            sj_kw_id = get_kw_result['data']
            sj_kw_ids = sj_kw_id * len(ware_sku_qty_list)
        else:
            get_kw_result = wms_app.base_get_kw(1, 5, len(ware_sku_qty_list), warehouse_id, to_warehouse_id)
            assert get_kw_result['code'] == expected
            sj_kw_ids = get_kw_result['data']
        expect_lp_inventory = ims_robot.get_add_kw_stock_expect_inventory(ware_sku_qty_list, sj_kw_ids, warehouse_id,
                                                                          to_warehouse_id)

        other_in_result = ims_robot.lp_other_in(ware_sku_qty_list, sj_kw_ids, warehouse_id, to_warehouse_id)
        assert other_in_result['code'] == expected
        lp_inventory = ims_robot.get_lp_inventories(sale_skus, warehouse_id, to_warehouse_id)

        assert expect_lp_inventory == lp_inventory

    # @pytest.mark.skip("调试，暂时跳过")
    @allure.story("测试场景：备货仓其他入库，上架良品")
    @allure.severity(allure.severity_level.BLOCKER)  # p0阻塞级用例
    @pytest.mark.parametrize("ware_sku_qty_list,kw_num,warehouse_id,to_warehouse_id,expected,bak", bhc_lp_other_in_data)
    def test_bhc_lp_other_in_stock(self, ware_sku_qty_list, kw_num, warehouse_id, to_warehouse_id, expected, bak):
        ware_sku_qty_list = json.loads(ware_sku_qty_list)
        sale_skus = ims_robot.get_sale_skus(ware_sku_qty_list)

        if kw_num == "one":
            get_kw_result = wms_app.base_get_kw(1, 5, 1, warehouse_id, to_warehouse_id)
            assert get_kw_result['code'] == expected
            sj_kw_id = get_kw_result['data']
            sj_kw_ids = sj_kw_id * len(ware_sku_qty_list)
        else:
            get_kw_result = wms_app.base_get_kw(1, 5, len(ware_sku_qty_list), warehouse_id, to_warehouse_id)
            assert get_kw_result['code'] == expected
            sj_kw_ids = get_kw_result['data']
        expect_lp_inventory = ims_robot.get_add_kw_stock_expect_inventory(ware_sku_qty_list, sj_kw_ids, warehouse_id,
                                                                          to_warehouse_id)

        other_in_result = ims_robot.lp_other_in(ware_sku_qty_list, sj_kw_ids, warehouse_id, to_warehouse_id)
        assert other_in_result['code'] == expected
        lp_inventory = ims_robot.get_lp_inventories(sale_skus, warehouse_id, to_warehouse_id)
        assert expect_lp_inventory == lp_inventory

    # @pytest.mark.skip("调试，暂时跳过")
    @allure.story("测试场景：中转仓其他入库，上架良品")
    @allure.severity(allure.severity_level.BLOCKER)  # p0阻塞级用例
    @pytest.mark.parametrize("ware_sku_qty_list,kw_num,warehouse_id,to_warehouse_id,expected,bak", zzc_lp_other_in_data)
    def test_zzc_lp_other_in_stock(self, ware_sku_qty_list, kw_num, warehouse_id, to_warehouse_id, expected, bak):
        ware_sku_qty_list = json.loads(ware_sku_qty_list)
        sale_skus = ims_robot.get_sale_skus(ware_sku_qty_list)

        if kw_num == "one":
            get_kw_result = wms_app.base_get_kw(1, 5, 1, warehouse_id, to_warehouse_id)
            assert get_kw_result['code'] == expected
            sj_kw_id = get_kw_result['data']
            sj_kw_ids = sj_kw_id * len(ware_sku_qty_list)
        else:
            get_kw_result = wms_app.base_get_kw(1, 5, len(ware_sku_qty_list), warehouse_id, to_warehouse_id)
            assert get_kw_result['code'] == expected
            sj_kw_ids = get_kw_result['data']
        expect_lp_inventory = ims_robot.get_add_kw_stock_expect_inventory(ware_sku_qty_list, sj_kw_ids, warehouse_id,
                                                                          to_warehouse_id)

        other_in_result = ims_robot.lp_other_in(ware_sku_qty_list, sj_kw_ids, warehouse_id, to_warehouse_id)
        assert other_in_result['code'] == expected
        lp_inventory = ims_robot.get_lp_inventories(sale_skus, warehouse_id, to_warehouse_id)
        assert expect_lp_inventory == lp_inventory


if __name__ == '__main__':
    os.system("pytest -v -s cases/ims/test_other_in_case.py --alluredir=./allure-report-files")
    os.system("allure generate ./allure-report-files -o ./reports --clean")
