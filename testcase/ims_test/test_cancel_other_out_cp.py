import pytest

from testcase import *


class TestCancelOtherOutCP(object):
    def setup_class(self):
        self.warehouse_id = delivery_warehouse_id
        self.to_warehouse_id = delivery_warehouse_id

    # @pytest.mark.skip(reason='test')
    def test_1_cancel_unqualified_goods_other_out_from_one_location(self):
        """
        先添加多个仓库sku的次品库存，放在1个库位上，然后生成次品其他出库单，再取消
        """
        sale_sku = '63203684930'

        cp_kw_id = wms_logics.db_get_kw(1, 6, 1, self.warehouse_id, self.to_warehouse_id)
        ware_sku_qty_list = [('63203684930A01', 1), ('63203684930A01', 1), ('63203684930A02', 5), ('63203684930A02', 5)]
        cp_kw_ids = [cp_kw_id for i in range(len(ware_sku_qty_list))]

        IMSDBOperator.delete_unqualified_inventory([sale_sku])
        ims_request.cp_other_in(ware_sku_qty_list, cp_kw_ids, self.warehouse_id, self.to_warehouse_id)
        self.expect_inventory = ims_logics.query_format_cp_inventory(sale_sku, self.warehouse_id)

        for (ware_sku, qty), cp_kw_id in zip(ware_sku_qty_list, cp_kw_ids):
            sub_ware_sku_qty_list = [(ware_sku, qty)]
            sub_cp_kw_ids = [cp_kw_id]
            block_res = ims_request.cp_other_out_block(sub_ware_sku_qty_list, sub_cp_kw_ids,
                                                       self.warehouse_id)
            self.expect_inventory[ware_sku][cp_kw_id]['block'] += qty
            self.expect_inventory[ware_sku]['total']['block'] += qty

            after_block_inventory = ims_logics.query_format_cp_inventory(sale_sku, self.warehouse_id)
            assert block_res['code'] == 200
            assert after_block_inventory == self.expect_inventory

            source_no = block_res['data'][0]['sourceNo']
            block_book_id = block_res['data'][0]['blockBookId']

            cancel_res = ims_request.cancel_cp_other_out_block(block_book_id, source_no)
            self.expect_inventory[ware_sku][cp_kw_id]['block'] -= qty
            self.expect_inventory[ware_sku]['total']['block'] -= qty
            after_cancel_block_inventory = ims_logics.query_format_cp_inventory(sale_sku, self.warehouse_id)

            assert cancel_res['code'] == 200
            assert after_cancel_block_inventory == self.expect_inventory

    def test_2_unqualified_goods_other_out_from_several_locations(self):
        """
        先添加次品库存，放在多个不同库位，然后循环预占再出库发货
        """
        sale_sku = '63203684930'
        ware_sku_qty_list = [('63203684930A01', 1), ('63203684930A01', 1), ('63203684930A02', 5), ('63203684930A02', 5)]
        cp_kw_ids = wms_logics.db_get_kw(1, 6, len(ware_sku_qty_list), self.warehouse_id, self.to_warehouse_id)

        IMSDBOperator.delete_unqualified_inventory([sale_sku])
        ims_request.cp_other_in(ware_sku_qty_list, cp_kw_ids, self.warehouse_id, self.to_warehouse_id)
        self.expect_inventory = ims_logics.query_format_cp_inventory(sale_sku, self.warehouse_id, 'A')

        for (ware_sku, qty), cp_kw_id in zip(ware_sku_qty_list, cp_kw_ids):
            sub_ware_sku_qty_list = [(ware_sku, qty)]
            sub_cp_kw_ids = [cp_kw_id]
            block_res = ims_request.cp_other_out_block(sub_ware_sku_qty_list, sub_cp_kw_ids,
                                                       self.warehouse_id)
            self.expect_inventory[ware_sku][cp_kw_id]['block'] += qty
            self.expect_inventory[ware_sku]['total']['block'] += qty

            after_block_inventory = ims_logics.query_format_cp_inventory(sale_sku, self.warehouse_id)
            assert block_res['code'] == 200
            assert after_block_inventory == self.expect_inventory

            source_no = block_res['data'][0]['sourceNo']
            block_book_id = block_res['data'][0]['blockBookId']

            cancel_res = ims_request.cancel_cp_other_out_block(block_book_id, source_no)
            self.expect_inventory[ware_sku][cp_kw_id]['block'] -= qty
            self.expect_inventory[ware_sku]['total']['block'] -= qty
            after_cancel_block_inventory = ims_logics.query_format_cp_inventory(sale_sku, self.warehouse_id)

            assert cancel_res['code'] == 200
            assert after_cancel_block_inventory == self.expect_inventory

    def test_3_unqualified_goods_other_out_from_several_locations(self):
        """
        先添加次品库存，放在多个不同库位，然后一次性预占再出库发货
        """
        sale_sku = '63203684930'
        ware_sku_qty_list = [('63203684930A01', 1), ('63203684930A01', 1), ('63203684930A02', 5), ('63203684930A02', 5)]
        cp_kw_ids = wms_logics.db_get_kw(1, 6, len(ware_sku_qty_list), self.warehouse_id, self.to_warehouse_id)

        IMSDBOperator.delete_unqualified_inventory([sale_sku])
        ims_request.cp_other_in(ware_sku_qty_list, cp_kw_ids, self.warehouse_id, self.to_warehouse_id)
        self.expect_inventory = ims_logics.query_format_cp_inventory(sale_sku, self.warehouse_id, 'A')

        block_res = ims_request.cp_other_out_block(ware_sku_qty_list, cp_kw_ids, self.warehouse_id)
        for (ware_sku, qty), cp_kw_id in zip(ware_sku_qty_list, cp_kw_ids):
            self.expect_inventory[ware_sku][cp_kw_id]['block'] += qty
            self.expect_inventory[ware_sku]['total']['block'] += qty

        after_block_inventory = ims_logics.query_format_cp_inventory(sale_sku, self.warehouse_id)
        assert block_res['code'] == 200
        assert after_block_inventory == self.expect_inventory

        source_no = block_res['data'][0]['sourceNo']
        block_book_id = block_res['data'][0]['blockBookId']

        cancel_res = ims_request.cancel_cp_other_out_block(block_book_id, source_no)
        for (ware_sku, qty), cp_kw_id in zip(ware_sku_qty_list, cp_kw_ids):
            self.expect_inventory[ware_sku][cp_kw_id]['block'] -= qty
            self.expect_inventory[ware_sku]['total']['block'] -= qty
        after_cancel_block_inventory = ims_logics.query_format_cp_inventory(sale_sku, self.warehouse_id)

        assert cancel_res['code'] == 200
        assert after_cancel_block_inventory == self.expect_inventory


if __name__ == '__main__':
    pytest.main()
