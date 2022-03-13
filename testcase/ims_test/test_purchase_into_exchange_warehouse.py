import pytest

from testcase import *


class TestPurchaseIntoExchangeWarehouse(object):
    def setup_class(self):
        self.warehouse_id = exchange_warehouse_id
        self.to_warehouse_id = delivery_warehouse_id
        self.ware_sku_qty_list = [('63203684930A01', 1), ('63203684930A02', 5)]
        self.sale_sku_suite_dict = ims.calculate_sets(self.ware_sku_qty_list)
        self.sj_kw_ids = wms.db_get_kw(1, 5, len(self.ware_sku_qty_list), self.warehouse_id, self.to_warehouse_id)

    def test_1_purchase_create_order(self):
        ims.delete_qualified_inventory(self.sale_sku_suite_dict.keys())

        res = ims.purchase_create_order(
            self.ware_sku_qty_list,
            self.warehouse_id,
            self.to_warehouse_id
        )

        for sale_sku in self.sale_sku_suite_dict.keys():
            # 获取库存数据
            current_qualified_inventory = ims.get_qualified_inventory(
                sale_sku,
                self.warehouse_id,
                self.to_warehouse_id)
            current_unqualified_inventory = ims.get_unqualified_inventory(
                sale_sku,
                self.warehouse_id,
                self.to_warehouse_id
            )
            expect_qualified_inventory = ims.get_purchase_create_order_expect_inventory(self.ware_sku_qty_list).get(
                sale_sku)
            assert res['code'] == 200
            assert expect_qualified_inventory == current_qualified_inventory
            assert current_unqualified_inventory is None

    def test_2_purchase_into_warehouse(self):
        res = ims.purchase_into_warehouse(
            self.ware_sku_qty_list,
            self.sj_kw_ids,
            self.warehouse_id,
            self.to_warehouse_id)
        for sale_sku in self.sale_sku_suite_dict.keys():
            # 获取库存数据
            current_qualified_inventory = ims.get_qualified_inventory(
                sale_sku,
                self.warehouse_id,
                self.to_warehouse_id)
            current_unqualified_inventory = ims.get_unqualified_inventory(
                sale_sku,
                self.warehouse_id,
                self.to_warehouse_id)
            expect_qualified_inventory = ims.get_purchase_in_expect_inventory(self.ware_sku_qty_list,
                                                                              self.sj_kw_ids).get(sale_sku)
            assert res['code'] == 200
            assert expect_qualified_inventory == current_qualified_inventory
            assert current_unqualified_inventory is None


if __name__ == '__main__':
    pytest.main()
