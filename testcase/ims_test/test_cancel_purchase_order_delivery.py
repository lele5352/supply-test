import pytest

from testcase import *


class TestCancelPurchaseOrderDelivery(object):
    def setup_class(self):
        # 采购下单的商品
        self.ware_sku_qty_list = [('63203684930A01', 1), ('63203684930A02', 5)]

    def test_1_cancel_delivery_warehouse_purchase_order_delivery(self):
        """
        测试发货仓全部采购单商品终止来货
        """
        cancel_ware_sku_qty_list = [('63203684930A01', 1), ('63203684930A02', 5)]
        self.sale_sku_suite_dict = ims.calculate_sets(self.ware_sku_qty_list)
        ims.delete_qualified_inventory(self.sale_sku_suite_dict.keys())
        warehouse_id = delivery_warehouse_id
        to_warehouse_id = delivery_warehouse_id

        self.sj_kw_ids = wms.db_get_kw(1, 5, len(self.ware_sku_qty_list), warehouse_id, to_warehouse_id)

        create_res = ims.purchase_create_order(
            self.ware_sku_qty_list,
            warehouse_id,
            to_warehouse_id
        )

        for sale_sku in self.sale_sku_suite_dict.keys():
            # 获取库存数据
            after_create_inventory = ims.get_qualified_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id)
            current_unqualified_inventory = ims.get_unqualified_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id
            )
            expect_qualified_inventory = ims.get_purchase_create_order_expect_inventory(self.ware_sku_qty_list).get(
                sale_sku)
            assert create_res['code'] == 200
            assert expect_qualified_inventory == after_create_inventory
            assert current_unqualified_inventory is None

            cancel_res = ims.cancel_purchase_order_delivery(cancel_ware_sku_qty_list, warehouse_id, to_warehouse_id)
            after_cancel_inventory = ims.get_qualified_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id)
            expect_qualified_inventory['central_stock'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_qualified_inventory['central_remain'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_qualified_inventory['purchase_on_way_stock'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_qualified_inventory['purchase_on_way_remain'] -= self.sale_sku_suite_dict.get(sale_sku)
            for (ware_sku, qty), sj_kw_id in zip(cancel_ware_sku_qty_list, self.sj_kw_ids):
                expect_qualified_inventory[ware_sku]['warehouse_total']['stock'] -= qty
                expect_qualified_inventory[ware_sku]['purchase_on_way']['stock'] -= qty

            assert cancel_res['code'] == 200
            assert after_cancel_inventory == expect_qualified_inventory

    def test_2_cancel_exchange_warehouse_purchase_order_delivery(self):
        """
        测试中转仓全部采购单商品终止来货
        """
        cancel_ware_sku_qty_list = [('63203684930A01', 1), ('63203684930A02', 5)]
        self.sale_sku_suite_dict = ims.calculate_sets(self.ware_sku_qty_list)
        ims.delete_qualified_inventory(self.sale_sku_suite_dict.keys())
        warehouse_id = exchange_warehouse_id
        to_warehouse_id = delivery_warehouse_id

        self.sj_kw_ids = wms.db_get_kw(1, 5, len(self.ware_sku_qty_list), warehouse_id, to_warehouse_id)

        create_res = ims.purchase_create_order(
            self.ware_sku_qty_list,
            warehouse_id,
            to_warehouse_id
        )

        for sale_sku in self.sale_sku_suite_dict.keys():
            # 获取库存数据
            after_create_inventory = ims.get_qualified_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id)
            current_unqualified_inventory = ims.get_unqualified_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id
            )
            expect_qualified_inventory = ims.get_purchase_create_order_expect_inventory(self.ware_sku_qty_list).get(
                sale_sku)
            assert create_res['code'] == 200
            assert expect_qualified_inventory == after_create_inventory
            assert current_unqualified_inventory is None

            cancel_res = ims.cancel_purchase_order_delivery(cancel_ware_sku_qty_list, warehouse_id, to_warehouse_id)
            after_cancel_inventory = ims.get_qualified_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id)
            expect_qualified_inventory['central_stock'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_qualified_inventory['central_remain'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_qualified_inventory['purchase_on_way_stock'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_qualified_inventory['purchase_on_way_remain'] -= self.sale_sku_suite_dict.get(sale_sku)
            for (ware_sku, qty), sj_kw_id in zip(cancel_ware_sku_qty_list, self.sj_kw_ids):
                expect_qualified_inventory[ware_sku]['warehouse_total']['stock'] -= qty
                expect_qualified_inventory[ware_sku]['purchase_on_way']['stock'] -= qty

            assert cancel_res['code'] == 200
            assert after_cancel_inventory == expect_qualified_inventory

    def test_3_cancel_exchange_warehouse_purchase_order_delivery(self):
        """
        测试备货仓全部采购单商品终止来货
        """
        cancel_ware_sku_qty_list = [('63203684930A01', 1), ('63203684930A02', 5)]
        self.sale_sku_suite_dict = ims.calculate_sets(self.ware_sku_qty_list)
        ims.delete_qualified_inventory(self.sale_sku_suite_dict.keys())
        warehouse_id = stock_warehouse_id
        to_warehouse_id = ''

        self.sj_kw_ids = wms.db_get_kw(1, 5, len(self.ware_sku_qty_list), warehouse_id, to_warehouse_id)

        create_res = ims.purchase_create_order(
            self.ware_sku_qty_list,
            warehouse_id,
            to_warehouse_id
        )

        for sale_sku in self.sale_sku_suite_dict.keys():
            # 获取库存数据
            after_create_inventory = ims.get_qualified_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id)
            current_unqualified_inventory = ims.get_unqualified_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id
            )
            expect_qualified_inventory = ims.get_purchase_create_order_expect_inventory(self.ware_sku_qty_list).get(
                sale_sku)
            assert create_res['code'] == 200
            assert expect_qualified_inventory == after_create_inventory
            assert current_unqualified_inventory is None

            cancel_res = ims.cancel_purchase_order_delivery(cancel_ware_sku_qty_list, warehouse_id, to_warehouse_id)
            after_cancel_inventory = ims.get_qualified_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id)
            expect_qualified_inventory['central_stock'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_qualified_inventory['central_remain'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_qualified_inventory['purchase_on_way_stock'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_qualified_inventory['purchase_on_way_remain'] -= self.sale_sku_suite_dict.get(sale_sku)
            for (ware_sku, qty), sj_kw_id in zip(cancel_ware_sku_qty_list, self.sj_kw_ids):
                expect_qualified_inventory[ware_sku]['warehouse_total']['stock'] -= qty
                expect_qualified_inventory[ware_sku]['purchase_on_way']['stock'] -= qty

            assert cancel_res['code'] == 200
            assert after_cancel_inventory == expect_qualified_inventory

    def test_4_cancel_delivery_warehouse_purchase_order_delivery_partly(self):
        """
        测试发货仓部分采购单商品终止来货，只留一件
        """
        cancel_ware_sku_qty_list = [('63203684930A01', 1), ('63203684930A02', 4)]
        self.sale_sku_suite_dict = ims.calculate_sets(self.ware_sku_qty_list)
        ims.delete_qualified_inventory(self.sale_sku_suite_dict.keys())
        warehouse_id = delivery_warehouse_id
        to_warehouse_id = delivery_warehouse_id

        self.sj_kw_ids = wms.db_get_kw(1, 5, len(self.ware_sku_qty_list), warehouse_id, to_warehouse_id)

        create_res = ims.purchase_create_order(
            self.ware_sku_qty_list,
            warehouse_id,
            to_warehouse_id
        )

        for sale_sku in self.sale_sku_suite_dict.keys():
            # 获取库存数据
            after_create_inventory = ims.get_qualified_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id)
            current_unqualified_inventory = ims.get_unqualified_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id
            )
            expect_qualified_inventory = ims.get_purchase_create_order_expect_inventory(self.ware_sku_qty_list).get(
                sale_sku)
            assert create_res['code'] == 200
            assert expect_qualified_inventory == after_create_inventory
            assert current_unqualified_inventory is None

            cancel_res = ims.cancel_purchase_order_delivery(cancel_ware_sku_qty_list, warehouse_id, to_warehouse_id)
            after_cancel_inventory = ims.get_qualified_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id)
            expect_qualified_inventory['central_stock'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_qualified_inventory['central_remain'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_qualified_inventory['purchase_on_way_stock'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_qualified_inventory['purchase_on_way_remain'] -= self.sale_sku_suite_dict.get(sale_sku)
            for (ware_sku, qty), sj_kw_id in zip(cancel_ware_sku_qty_list, self.sj_kw_ids):
                expect_qualified_inventory[ware_sku]['warehouse_total']['stock'] -= qty
                expect_qualified_inventory[ware_sku]['purchase_on_way']['stock'] -= qty

            assert cancel_res['code'] == 200
            assert after_cancel_inventory == expect_qualified_inventory

    def test_5_cancel_exchange_warehouse_purchase_create_delivery_partly(self):
        """
        测试中转仓部分采购单商品终止来货，只留一件
        """
        cancel_ware_sku_qty_list = [('63203684930A01', 1), ('63203684930A02', 4)]
        self.sale_sku_suite_dict = ims.calculate_sets(self.ware_sku_qty_list)
        ims.delete_qualified_inventory(self.sale_sku_suite_dict.keys())
        warehouse_id = exchange_warehouse_id
        to_warehouse_id = delivery_warehouse_id

        self.sj_kw_ids = wms.db_get_kw(1, 5, len(self.ware_sku_qty_list), warehouse_id, to_warehouse_id)

        create_res = ims.purchase_create_order(
            self.ware_sku_qty_list,
            warehouse_id,
            to_warehouse_id
        )

        for sale_sku in self.sale_sku_suite_dict.keys():
            # 获取库存数据
            after_create_inventory = ims.get_qualified_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id)
            current_unqualified_inventory = ims.get_unqualified_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id
            )
            expect_qualified_inventory = ims.get_purchase_create_order_expect_inventory(self.ware_sku_qty_list).get(
                sale_sku)
            assert create_res['code'] == 200
            assert expect_qualified_inventory == after_create_inventory
            assert current_unqualified_inventory is None

            cancel_res = ims.cancel_purchase_order_delivery(cancel_ware_sku_qty_list, warehouse_id, to_warehouse_id)
            after_cancel_inventory = ims.get_qualified_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id)
            expect_qualified_inventory['central_stock'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_qualified_inventory['central_remain'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_qualified_inventory['purchase_on_way_stock'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_qualified_inventory['purchase_on_way_remain'] -= self.sale_sku_suite_dict.get(sale_sku)
            for (ware_sku, qty), sj_kw_id in zip(cancel_ware_sku_qty_list, self.sj_kw_ids):
                expect_qualified_inventory[ware_sku]['warehouse_total']['stock'] -= qty
                expect_qualified_inventory[ware_sku]['purchase_on_way']['stock'] -= qty

            assert cancel_res['code'] == 200
            assert after_cancel_inventory == expect_qualified_inventory

    def test_6_cancel_stock_warehouse_purchase_create_delivery_partly(self):
        """
        测试中转仓部分采购单商品终止来货，只留一件
        """
        cancel_ware_sku_qty_list = [('63203684930A01', 1), ('63203684930A02', 4)]
        self.sale_sku_suite_dict = ims.calculate_sets(self.ware_sku_qty_list)
        ims.delete_qualified_inventory(self.sale_sku_suite_dict.keys())
        warehouse_id = stock_warehouse_id
        to_warehouse_id = ''

        self.sj_kw_ids = wms.db_get_kw(1, 5, len(self.ware_sku_qty_list), warehouse_id, to_warehouse_id)

        create_res = ims.purchase_create_order(
            self.ware_sku_qty_list,
            warehouse_id,
            to_warehouse_id
        )

        for sale_sku in self.sale_sku_suite_dict.keys():
            # 获取库存数据
            after_create_inventory = ims.get_qualified_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id)
            current_unqualified_inventory = ims.get_unqualified_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id
            )
            expect_qualified_inventory = ims.get_purchase_create_order_expect_inventory(self.ware_sku_qty_list).get(
                sale_sku)
            assert create_res['code'] == 200
            assert expect_qualified_inventory == after_create_inventory
            assert current_unqualified_inventory is None

            cancel_res = ims.cancel_purchase_order_delivery(cancel_ware_sku_qty_list, warehouse_id, to_warehouse_id)
            after_cancel_inventory = ims.get_qualified_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id)
            expect_qualified_inventory['central_stock'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_qualified_inventory['central_remain'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_qualified_inventory['purchase_on_way_stock'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_qualified_inventory['purchase_on_way_remain'] -= self.sale_sku_suite_dict.get(sale_sku)
            for (ware_sku, qty), sj_kw_id in zip(cancel_ware_sku_qty_list, self.sj_kw_ids):
                expect_qualified_inventory[ware_sku]['warehouse_total']['stock'] -= qty
                expect_qualified_inventory[ware_sku]['purchase_on_way']['stock'] -= qty

            assert cancel_res['code'] == 200
            assert after_cancel_inventory == expect_qualified_inventory


if __name__ == '__main__':
    pytest.main()
