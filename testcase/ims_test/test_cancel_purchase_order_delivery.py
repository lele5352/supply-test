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
        self.sale_sku_suite_dict = ims_logics.calculate_sets(self.ware_sku_qty_list)
        sale_sku_list = [i for i in self.sale_sku_suite_dict]
        IMSDBOperator.delete_qualified_inventory(sale_sku_list)
        warehouse_id = delivery_warehouse_id
        to_warehouse_id = delivery_warehouse_id

        self.sj_kw_ids = wms_request.db_get_kw(1, 5, len(self.ware_sku_qty_list), warehouse_id, to_warehouse_id)

        create_res = ims_request.purchase_create_order(
            self.ware_sku_qty_list,
            warehouse_id,
            to_warehouse_id
        )

        for sale_sku in self.sale_sku_suite_dict.keys():
            # 获取库存数据
            after_create_inventory = ims_logics.query_lp_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id)
            current_unqualified_inventory = ims_logics.query_format_cp_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id
            )
            expect_lp_inventory = ims_logics.get_purchase_create_order_expect_inventory(
                self.ware_sku_qty_list).get(
                sale_sku)
            assert create_res['code'] == 200
            assert expect_lp_inventory == after_create_inventory
            assert current_unqualified_inventory == {}

            cancel_res = ims_request.cancel_purchase_order_delivery(cancel_ware_sku_qty_list, warehouse_id,
                                                                    to_warehouse_id)
            after_cancel_inventory = ims_logics.query_lp_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id)
            expect_lp_inventory['central_stock'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_lp_inventory['central_remain'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_lp_inventory['purchase_on_way_stock'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_lp_inventory['purchase_on_way_remain'] -= self.sale_sku_suite_dict.get(sale_sku)
            for (ware_sku, qty), sj_kw_id in zip(cancel_ware_sku_qty_list, self.sj_kw_ids):
                expect_lp_inventory[ware_sku]['warehouse_total']['stock'] -= qty
                expect_lp_inventory[ware_sku]['purchase_on_way']['stock'] -= qty

            assert cancel_res['code'] == 200
            assert after_cancel_inventory == expect_lp_inventory

    def test_2_cancel_exchange_warehouse_purchase_order_delivery(self):
        """
        测试中转仓全部采购单商品终止来货
        """
        cancel_ware_sku_qty_list = [('63203684930A01', 1), ('63203684930A02', 5)]
        self.sale_sku_suite_dict = ims_logics.calculate_sets(self.ware_sku_qty_list)
        sale_sku_list = [i for i in self.sale_sku_suite_dict]
        IMSDBOperator.delete_qualified_inventory(sale_sku_list)
        warehouse_id = exchange_warehouse_id
        to_warehouse_id = delivery_warehouse_id

        self.sj_kw_ids = wms_request.db_get_kw(1, 5, len(self.ware_sku_qty_list), warehouse_id, to_warehouse_id)

        create_res = ims_request.purchase_create_order(
            self.ware_sku_qty_list,
            warehouse_id,
            to_warehouse_id
        )

        for sale_sku in self.sale_sku_suite_dict.keys():
            # 获取库存数据
            after_create_inventory = ims_logics.query_lp_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id)
            current_unqualified_inventory = ims_logics.query_format_cp_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id
            )
            expect_lp_inventory = ims_logics.get_purchase_create_order_expect_inventory(
                self.ware_sku_qty_list).get(
                sale_sku)
            assert create_res['code'] == 200
            assert expect_lp_inventory == after_create_inventory
            assert current_unqualified_inventory == {}

            cancel_res = ims_request.cancel_purchase_order_delivery(cancel_ware_sku_qty_list, warehouse_id,
                                                                    to_warehouse_id)
            after_cancel_inventory = ims_logics.query_lp_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id)
            expect_lp_inventory['central_stock'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_lp_inventory['central_remain'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_lp_inventory['purchase_on_way_stock'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_lp_inventory['purchase_on_way_remain'] -= self.sale_sku_suite_dict.get(sale_sku)
            for (ware_sku, qty), sj_kw_id in zip(cancel_ware_sku_qty_list, self.sj_kw_ids):
                expect_lp_inventory[ware_sku]['warehouse_total']['stock'] -= qty
                expect_lp_inventory[ware_sku]['purchase_on_way']['stock'] -= qty

            assert cancel_res['code'] == 200
            assert after_cancel_inventory == expect_lp_inventory

    def test_3_cancel_exchange_warehouse_purchase_order_delivery(self):
        """
        测试备货仓全部采购单商品终止来货
        """
        cancel_ware_sku_qty_list = [('63203684930A01', 1), ('63203684930A02', 5)]
        self.sale_sku_suite_dict = ims_logics.calculate_sets(self.ware_sku_qty_list)
        sale_sku_list = [i for i in self.sale_sku_suite_dict]
        IMSDBOperator.delete_qualified_inventory(sale_sku_list)
        warehouse_id = stock_warehouse_id
        to_warehouse_id = ''

        self.sj_kw_ids = wms_request.db_get_kw(1, 5, len(self.ware_sku_qty_list), warehouse_id, to_warehouse_id)

        create_res = ims_request.purchase_create_order(
            self.ware_sku_qty_list,
            warehouse_id,
            to_warehouse_id
        )

        for sale_sku in self.sale_sku_suite_dict.keys():
            # 获取库存数据
            after_create_inventory = ims_logics.query_lp_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id)
            current_unqualified_inventory = ims_logics.query_format_cp_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id
            )
            expect_lp_inventory = ims_logics.get_purchase_create_order_expect_inventory(
                self.ware_sku_qty_list).get(
                sale_sku)
            assert create_res['code'] == 200
            assert expect_lp_inventory == after_create_inventory
            assert current_unqualified_inventory == {}

            cancel_res = ims_request.cancel_purchase_order_delivery(cancel_ware_sku_qty_list, warehouse_id,
                                                                    to_warehouse_id)
            after_cancel_inventory = ims_logics.query_lp_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id)
            expect_lp_inventory['central_stock'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_lp_inventory['central_remain'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_lp_inventory['purchase_on_way_stock'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_lp_inventory['purchase_on_way_remain'] -= self.sale_sku_suite_dict.get(sale_sku)
            for (ware_sku, qty), sj_kw_id in zip(cancel_ware_sku_qty_list, self.sj_kw_ids):
                expect_lp_inventory[ware_sku]['warehouse_total']['stock'] -= qty
                expect_lp_inventory[ware_sku]['purchase_on_way']['stock'] -= qty

            assert cancel_res['code'] == 200
            assert after_cancel_inventory == expect_lp_inventory

    def test_4_cancel_delivery_warehouse_purchase_order_delivery_partly(self):
        """
        测试发货仓部分采购单商品终止来货，只留一件
        """
        cancel_ware_sku_qty_list = [('63203684930A01', 1), ('63203684930A02', 4)]
        self.sale_sku_suite_dict = ims_logics.calculate_sets(self.ware_sku_qty_list)
        sale_sku_list = [i for i in self.sale_sku_suite_dict]
        IMSDBOperator.delete_qualified_inventory(sale_sku_list)
        warehouse_id = delivery_warehouse_id
        to_warehouse_id = delivery_warehouse_id

        self.sj_kw_ids = wms_request.db_get_kw(1, 5, len(self.ware_sku_qty_list), warehouse_id, to_warehouse_id)

        create_res = ims_request.purchase_create_order(
            self.ware_sku_qty_list,
            warehouse_id,
            to_warehouse_id
        )

        for sale_sku in self.sale_sku_suite_dict.keys():
            # 获取库存数据
            after_create_inventory = ims_logics.query_lp_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id)
            current_unqualified_inventory = ims_logics.query_format_cp_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id
            )
            expect_lp_inventory = ims_logics.get_purchase_create_order_expect_inventory(
                self.ware_sku_qty_list).get(
                sale_sku)
            assert create_res['code'] == 200
            assert expect_lp_inventory == after_create_inventory
            assert current_unqualified_inventory == {}

            cancel_res = ims_request.cancel_purchase_order_delivery(cancel_ware_sku_qty_list, warehouse_id,
                                                                    to_warehouse_id)
            after_cancel_inventory = ims_logics.query_lp_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id)
            expect_lp_inventory['central_stock'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_lp_inventory['central_remain'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_lp_inventory['purchase_on_way_stock'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_lp_inventory['purchase_on_way_remain'] -= self.sale_sku_suite_dict.get(sale_sku)
            for (ware_sku, qty), sj_kw_id in zip(cancel_ware_sku_qty_list, self.sj_kw_ids):
                expect_lp_inventory[ware_sku]['warehouse_total']['stock'] -= qty
                expect_lp_inventory[ware_sku]['purchase_on_way']['stock'] -= qty

            assert cancel_res['code'] == 200
            assert after_cancel_inventory == expect_lp_inventory

    def test_5_cancel_exchange_warehouse_purchase_create_delivery_partly(self):
        """
        测试中转仓部分采购单商品终止来货，只留一件
        """
        cancel_ware_sku_qty_list = [('63203684930A01', 1), ('63203684930A02', 4)]
        self.sale_sku_suite_dict = ims_logics.calculate_sets(self.ware_sku_qty_list)
        sale_sku_list = [i for i in self.sale_sku_suite_dict]
        IMSDBOperator.delete_qualified_inventory(sale_sku_list)
        warehouse_id = exchange_warehouse_id
        to_warehouse_id = delivery_warehouse_id

        self.sj_kw_ids = wms_request.db_get_kw(1, 5, len(self.ware_sku_qty_list), warehouse_id, to_warehouse_id)

        create_res = ims_request.purchase_create_order(
            self.ware_sku_qty_list,
            warehouse_id,
            to_warehouse_id
        )

        for sale_sku in self.sale_sku_suite_dict.keys():
            # 获取库存数据
            after_create_inventory = ims_logics.query_lp_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id)
            current_unqualified_inventory = ims_logics.query_format_cp_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id
            )
            expect_lp_inventory = ims_logics.get_purchase_create_order_expect_inventory(
                self.ware_sku_qty_list).get(
                sale_sku)
            assert create_res['code'] == 200
            assert expect_lp_inventory == after_create_inventory
            assert current_unqualified_inventory == {}

            cancel_res = ims_request.cancel_purchase_order_delivery(cancel_ware_sku_qty_list, warehouse_id,
                                                                    to_warehouse_id)
            after_cancel_inventory = ims_logics.query_lp_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id)
            expect_lp_inventory['central_stock'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_lp_inventory['central_remain'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_lp_inventory['purchase_on_way_stock'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_lp_inventory['purchase_on_way_remain'] -= self.sale_sku_suite_dict.get(sale_sku)
            for (ware_sku, qty), sj_kw_id in zip(cancel_ware_sku_qty_list, self.sj_kw_ids):
                expect_lp_inventory[ware_sku]['warehouse_total']['stock'] -= qty
                expect_lp_inventory[ware_sku]['purchase_on_way']['stock'] -= qty

            assert cancel_res['code'] == 200
            assert after_cancel_inventory == expect_lp_inventory

    def test_6_cancel_stock_warehouse_purchase_create_delivery_partly(self):
        """
        测试中转仓部分采购单商品终止来货，只留一件
        """
        cancel_ware_sku_qty_list = [('63203684930A01', 1), ('63203684930A02', 4)]
        self.sale_sku_suite_dict = ims_logics.calculate_sets(self.ware_sku_qty_list)
        sale_sku_list = [i for i in self.sale_sku_suite_dict]
        IMSDBOperator.delete_qualified_inventory(sale_sku_list)
        warehouse_id = stock_warehouse_id
        to_warehouse_id = ''

        self.sj_kw_ids = wms_request.db_get_kw(1, 5, len(self.ware_sku_qty_list), warehouse_id, to_warehouse_id)

        create_res = ims_request.purchase_create_order(
            self.ware_sku_qty_list,
            warehouse_id,
            to_warehouse_id
        )

        for sale_sku in self.sale_sku_suite_dict.keys():
            # 获取库存数据
            after_create_inventory = ims_logics.query_lp_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id)
            current_unqualified_inventory = ims_logics.query_format_cp_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id
            )
            expect_lp_inventory = ims_logics.get_purchase_create_order_expect_inventory(
                self.ware_sku_qty_list).get(
                sale_sku)
            assert create_res['code'] == 200
            assert expect_lp_inventory == after_create_inventory
            assert current_unqualified_inventory == {}

            cancel_res = ims_request.cancel_purchase_order_delivery(cancel_ware_sku_qty_list, warehouse_id,
                                                                    to_warehouse_id)
            after_cancel_inventory = ims_logics.query_lp_inventory(
                sale_sku,
                warehouse_id,
                to_warehouse_id)
            expect_lp_inventory['central_stock'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_lp_inventory['central_remain'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_lp_inventory['purchase_on_way_stock'] -= self.sale_sku_suite_dict.get(sale_sku)
            expect_lp_inventory['purchase_on_way_remain'] -= self.sale_sku_suite_dict.get(sale_sku)
            for (ware_sku, qty), sj_kw_id in zip(cancel_ware_sku_qty_list, self.sj_kw_ids):
                expect_lp_inventory[ware_sku]['warehouse_total']['stock'] -= qty
                expect_lp_inventory[ware_sku]['purchase_on_way']['stock'] -= qty

            assert cancel_res['code'] == 200
            assert after_cancel_inventory == expect_lp_inventory


if __name__ == '__main__':
    pytest.main()
