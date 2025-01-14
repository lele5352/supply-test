import json

import pytest
import allure
import os

from cases import *


@allure.feature("测试模块：采购入库")
class TestPurchaseInStock(object):
    fhc_purchase_in_data = ExcelTool("../../test_data/ims_test_data.xlsx").read_data("fhc_purchase_in", 2)  # 外部调用时的路径

    # fhc_purchase_in_data = ExcelTool("../../test_data/ims_test_data.xlsx", "fhc_purchase_in") # 本文件main下执行时的路径

    @allure.story("测试场景：发货仓采购入库")
    @allure.severity(allure.severity_level.BLOCKER)  # p0阻塞级用例
    @pytest.mark.parametrize("ware_sku_qty_list,kw_num,warehouse_id,to_warehouse_id,expected,bak", fhc_purchase_in_data)
    def test_fhc_purchase_in_stock(self, ware_sku_qty_list, kw_num, warehouse_id, to_warehouse_id, expected, bak):
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
        # 查询创建采购单前的库存
        expect_lp_inventory = ims_robot.get_purchase_create_order_expect_inventory(ware_sku_qty_list, warehouse_id,
                                                                                   to_warehouse_id)
        # 创建采购单
        create_order_result = ims_robot.purchase_create_order(ware_sku_qty_list, warehouse_id, to_warehouse_id)
        assert create_order_result['code'] == expected
        # 判断采购下单库存是否正确
        lp_inventory = ims_robot.get_lp_inventories(sale_skus, warehouse_id, to_warehouse_id)

        assert expect_lp_inventory == lp_inventory

        expect_lp_inventory = ims_robot.get_add_kw_stock_expect_inventory(ware_sku_qty_list, sj_kw_ids, warehouse_id,
                                                                          to_warehouse_id)
        into_result = ims_robot.purchase_into_warehouse(ware_sku_qty_list, sj_kw_ids, warehouse_id, to_warehouse_id)
        assert into_result['code'] == expected

        lp_inventory = ims_robot.get_lp_inventories(sale_skus, warehouse_id, to_warehouse_id)

        print(json.dumps(lp_inventory))
        print(json.dumps(expect_lp_inventory))

        assert expect_lp_inventory == lp_inventory


if __name__ == '__main__':
    os.system("pytest -v -s cases/ims/test_purchase_in_case.py --alluredir=./allure-report-files")
    os.system("allure generate ./allure-report-files -o ./reports --clean")
