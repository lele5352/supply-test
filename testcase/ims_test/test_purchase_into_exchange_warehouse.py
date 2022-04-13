import pytest

from testcase import *


class TestPurchaseIntoExchangeWarehouse(object):
    def setup_class(self):
        self.warehouse_id = exchange_warehouse_id
        self.to_warehouse_id = delivery_warehouse_id
        self.ware_sku_qty_list = [('67330337129G01', 1), ('67330337129G02', 2), ('67330337129G03', 3)]
        self.sale_sku_suite_dict = ims_logics.calculate_sets(self.ware_sku_qty_list)
        self.sj_kw_ids = wms_request.db_get_kw(1, 5, len(self.ware_sku_qty_list), self.warehouse_id, self.to_warehouse_id)

    def test_1_purchase_create_order(self):
        sale_sku_list = [i for i in self.sale_sku_suite_dict]
        IMSDBOperator.delete_qualified_inventory(sale_sku_list)

        res = ims_request.purchase_create_order(
            self.ware_sku_qty_list,
            self.warehouse_id,
            self.to_warehouse_id
        )

        for sale_sku in self.sale_sku_suite_dict.keys():
            # 获取库存数据
            current_qualified_inventory = IMSDBOperator.query_qualified_inventory(
                sale_sku,
                self.warehouse_id,
                self.to_warehouse_id)
            current_unqualified_inventory = IMSDBOperator.query_unqualified_inventory(
                sale_sku,
                self.warehouse_id,
                self.to_warehouse_id
            )
            expect_qualified_inventory = ims_logics.get_purchase_create_order_expect_inventory(self.ware_sku_qty_list).get(
                sale_sku)
            assert res['code'] == 200
            assert expect_qualified_inventory == current_qualified_inventory
            assert current_unqualified_inventory  == {}

    def test_2_purchase_into_warehouse(self):
        res = ims_request.purchase_into_warehouse(
            self.ware_sku_qty_list,
            self.sj_kw_ids,
            self.warehouse_id,
            self.to_warehouse_id)
        for sale_sku in self.sale_sku_suite_dict.keys():
            # 获取库存数据
            current_qualified_inventory = IMSDBOperator.query_qualified_inventory(
                sale_sku,
                self.warehouse_id,
                self.to_warehouse_id)
            current_unqualified_inventory = IMSDBOperator.query_unqualified_inventory(
                sale_sku,
                self.warehouse_id,
                self.to_warehouse_id)
            expect_qualified_inventory = ims_logics.get_purchase_in_expect_inventory(self.ware_sku_qty_list,
                                                                                      self.sj_kw_ids).get(sale_sku)
            assert res['code'] == 200
            assert expect_qualified_inventory == current_qualified_inventory
            assert current_unqualified_inventory  == {}


if __name__ == '__main__':
    pytest.main()
