import pytest
import allure
import os
from cases import *


@allure.feature("测试链路：新建销售订单→审单→添加库存→跟单→下发wms")
class TestOMSOrderPushWMS(object):
    oms_to_wms_data = ExcelTool("test_data/link_test_data.xlsx", "oms_to_wms")

    @allure.story("测试场景：正常推送wms生成销售出库单场景")
    @allure.severity(allure.severity_level.BLOCKER)  # p0阻塞级用例
    @pytest.mark.parametrize("order_sku_info_list,expected,bak", oms_to_wms_data)
    def test_push_wms_success(self, order_sku_info_list, expected, bak):
        """
        生成销售订单，并审单下发至WMS生成销售出库单
        """
        expected = expected
        with allure.step("步骤1：新建销售单"):
            create_result = oms_app.create_sale_order(order_sku_info_list)
            assert create_result['code'] == expected
            # 提取销售单号，从data中直接提取
            sale_order_no = create_result.get('data')

            # 根据销售单号查询oms单，从data中直接提取
            query_oms_order_result = oms_app.query_oms_order_by_sale_no(sale_order_no)
            assert query_oms_order_result['code'] == expected

            oms_order_list = query_oms_order_result.get('data')
            oms_order_no_list = [record['orderNo'] for record in oms_order_list]

        with allure.step("步骤2：根据销售订单号找出oms单号执行审单"):
            # 执行审单
            dispatch_result = oms_app_ip.dispatch_oms_order(oms_order_no_list)
            assert dispatch_result['code'] == expected

        with allure.step("步骤3：添加库存"):
            follow_order_list = list()
            # 为了确保订单有库存下发，提前根据订单添加库存
            for oms_order in oms_order_list:
                order_id = oms_order["id"]
                order_sku_items_result = oms_app.query_oms_order_sku_items(order_id)
                assert order_sku_items_result['code'] == expected

                order_sku_items = order_sku_items_result.get("data")

                for item in order_sku_items:
                    assert item['deliveryWarehouseId'] is not None
                    assert item['bomVersion'] is not None

                    sku_code = item["itemSkuCode"]
                    qty = item["itemQty"]
                    bom = item['bomVersion']
                    common_warehouse_code = item["deliveryWarehouseCode"]
                    common_warehouse_info_result = oms_app.query_common_warehouse(common_warehouse_code)

                    assert common_warehouse_info_result["code"] == expected

                    # 获取到共享仓之后，取其中一个物理仓加库存即可
                    common_warehouse_info = common_warehouse_info_result.get("data")
                    warehouse_id = common_warehouse_info["records"][0]["extResBoList"][0]["warehouseId"]
                    get_kw_result = wms_app.base_get_kw(1, 5, len(order_sku_info_list), warehouse_id, warehouse_id)
                    assert get_kw_result["code"] == expected

                    kw_ids = get_kw_result.get('data')
                    add_stock_result = ims_robot.add_bom_stock(sku_code, bom, qty, kw_ids, warehouse_id, warehouse_id)
                    assert add_stock_result["code"] == expected

                    if {"skuCode": sku_code, "bomVersion": bom} not in follow_order_list:
                        follow_order_list.append({"skuCode": sku_code, "bomVersion": bom})

        with allure.step("步骤4：按sku和bom版本执行跟单"):
            follow_result = oms_app_ip.oms_order_follow(follow_order_list)
            assert follow_result["code"] == expected

        with allure.step("步骤5：执行订单下发"):
            push_result = oms_app_ip.push_order_to_wms()
            assert push_result["code"] == expected


if __name__ == '__main__':
    pytest.main()
    os.system("pytest -v -s cases/links/test_oms_order_push_wms.py --alluredir=./allure-report-files")
    os.system("allure generate ./allure-report-files -o ./reports --clean")
