import pytest
import allure
import os

from cases import *


@allure.feature("测试模块：其他入库")
class TestOtterInStock(object):
    fhc_cp_other_in_data = get_excel_data("data/ims_test_data.xlsx", "fhc_cp_other_in")
    bhc_cp_other_in_data = get_excel_data("data/ims_test_data.xlsx", "bhc_cp_other_in")
    zzc_cp_other_in_data = get_excel_data("data/ims_test_data.xlsx", "zzc_cp_other_in")

    @allure.story("测试场景：发货仓其他入库，上架次品")
    @allure.severity(allure.severity_level.BLOCKER)  # p0阻塞级用例
    @pytest.mark.parametrize("ware_sku_qty_list,kw_num,warehouse_id,to_warehouse_id,expected,bak", fhc_cp_other_in_data)
    def test_fhc_cp_other_in_stock(self, ware_sku_qty_list, kw_num, warehouse_id, to_warehouse_id, expected, bak):
        sale_skus = ims_robot.get_sale_skus(ware_sku_qty_list)

        if kw_num == "one":
            get_kw_result = wms_app_robot.get_kw(1, 6, 1, warehouse_id, to_warehouse_id)
            assert get_kw_result['code'] == expected
            cp_kw_id = get_kw_result['data']
            cp_location_ids = cp_kw_id * len(ware_sku_qty_list)
        else:
            get_kw_result = wms_app_robot.get_kw(1, 6, len(ware_sku_qty_list), warehouse_id, to_warehouse_id)
            assert get_kw_result['code'] == expected
            cp_location_ids = get_kw_result['data']
        other_in_result = ims_robot.cp_other_in(ware_sku_qty_list, cp_location_ids, warehouse_id, to_warehouse_id)
        assert other_in_result['code'] == expected

        for sale_sku in sale_skus:
            unqualified_inventory = ims_robot.query_format_cp_inventory(sale_sku, warehouse_id)
            expect_cp_inventory = ims_robot.get_cp_other_in_expect_inventory(
                unqualified_inventory, ware_sku_qty_list, cp_location_ids).get(sale_sku)
            assert expect_cp_inventory == unqualified_inventory

    @allure.story("测试场景：备货仓其他入库，上架次品")
    @allure.severity(allure.severity_level.BLOCKER)  # p0阻塞级用例
    @pytest.mark.parametrize("ware_sku_qty_list,kw_num,warehouse_id,to_warehouse_id,expected,bak", bhc_cp_other_in_data)
    def test_bhc_cp_other_in_stock(self, ware_sku_qty_list, kw_num, warehouse_id, to_warehouse_id, expected, bak):
        sale_skus = ims_robot.get_sale_skus(ware_sku_qty_list)

        if kw_num == "one":
            get_kw_result = wms_app_robot.get_kw(1, 6, 1, warehouse_id, to_warehouse_id)
            assert get_kw_result['code'] == expected
            cp_kw_id = get_kw_result['data']
            cp_location_ids = cp_kw_id * len(ware_sku_qty_list)
        else:
            get_kw_result = wms_app_robot.get_kw(1, 6, len(ware_sku_qty_list), warehouse_id, to_warehouse_id)
            assert get_kw_result['code'] == expected
            cp_location_ids = get_kw_result['data']
        other_in_result = ims_robot.cp_other_in(ware_sku_qty_list, cp_location_ids, warehouse_id, to_warehouse_id)
        assert other_in_result['code'] == expected

        for sale_sku in sale_skus:
            unqualified_inventory = ims_robot.query_format_cp_inventory(sale_sku, warehouse_id)
            expect_cp_inventory = ims_robot.get_cp_other_in_expect_inventory(
                unqualified_inventory, ware_sku_qty_list, cp_location_ids).get(sale_sku)
            assert expect_cp_inventory == unqualified_inventory

    @allure.story("测试场景：中专仓其他入库，上架次品")
    @allure.severity(allure.severity_level.BLOCKER)  # p0阻塞级用例
    @pytest.mark.parametrize("ware_sku_qty_list,kw_num,warehouse_id,to_warehouse_id,expected,bak", zzc_cp_other_in_data)
    def test_zzc_cp_other_in_stock(self, ware_sku_qty_list, kw_num, warehouse_id, to_warehouse_id, expected, bak):
        sale_skus = ims_robot.get_sale_skus(ware_sku_qty_list)

        if kw_num == "one":
            get_kw_result = wms_app_robot.get_kw(1, 6, 1, warehouse_id, to_warehouse_id)
            assert get_kw_result['code'] == expected
            cp_kw_id = get_kw_result['data']
            cp_location_ids = cp_kw_id * len(ware_sku_qty_list)
        else:
            get_kw_result = wms_app_robot.get_kw(1, 6, len(ware_sku_qty_list), warehouse_id, to_warehouse_id)
            assert get_kw_result['code'] == expected
            cp_location_ids = get_kw_result['data']
        other_in_result = ims_robot.cp_other_in(ware_sku_qty_list, cp_location_ids, warehouse_id, to_warehouse_id)
        assert other_in_result['code'] == expected

        for sale_sku in sale_skus:
            unqualified_inventory = ims_robot.query_format_cp_inventory(sale_sku, warehouse_id)
            expect_cp_inventory = ims_robot.get_cp_other_in_expect_inventory(
                unqualified_inventory, ware_sku_qty_list, cp_location_ids).get(sale_sku)
            assert expect_cp_inventory == unqualified_inventory


if __name__ == '__main__':
    pytest.main()
    os.system("allure generate ../allure-report-files -o ../reports --clean")
