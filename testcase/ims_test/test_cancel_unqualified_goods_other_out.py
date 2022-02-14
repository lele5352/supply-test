import time

import pytest

from testcase import *


class TestCancelUnqualifiedGoodsOtherOut(object):
    def setup_class(self):
        self.warehouse_id = delivery_warehouse_id
        self.target_warehouse_id = delivery_warehouse_id
        self.ware_sku_count = 10
        self.sj_kw_id = fsj_kw_ids[0]
        self.cp_kw_id = fcp_kw_id

        ims.delete_unqualified_inventory(sale_sku, bom, self.warehouse_id)
        ims.add_unqualified_stock_by_other_in(
            ware_sku,
            self.sj_kw_id,
            self.cp_kw_id,
            self.ware_sku_count,
            self.warehouse_id,
            self.target_warehouse_id)
        self.expect_inventory = ims.get_unqualified_inventory(
            sale_sku,
            bom,
            self.warehouse_id)

    # @pytest.mark.skip(reason='test')
    def test_1_unqualified_goods_other_out_delivery_warehouse(self):
        """
        tips：销售sku不能是单品，单品会单件成套，不存在计算成套逻辑
        测试场景：

        """
        ware_sku_dict = {
            "qty": self.ware_sku_count,
            "storageLocationId": self.cp_kw_id,
            "wareSkuCode": ware_sku
        }
        block_res = ims.unqualified_goods_other_out_block([ware_sku_dict], self.warehouse_id)

        self.expect_inventory[ware_sku][self.cp_kw_id]['block'] += self.ware_sku_count
        self.expect_inventory[ware_sku]['total']['block'] += self.ware_sku_count

        after_block_inventory = ims.get_unqualified_inventory(
            sale_sku,
            bom,
            self.warehouse_id
        )
        assert block_res['code'] == 200
        assert after_block_inventory == self.expect_inventory

        source_no = block_res['data'][0]['sourceNo']
        block_book_id = block_res['data'][0]['blockBookId']
        # time.sleep(15)
        cancel_block_res = ims.cancel_unqualified_goods_other_out_block(block_book_id, source_no)
        after_cancel_block_inventory = ims.get_unqualified_inventory(
            sale_sku,
            bom,
            self.warehouse_id
        )
        self.expect_inventory[ware_sku][self.cp_kw_id]['block'] -= self.ware_sku_count
        self.expect_inventory[ware_sku]['total']['block'] -= self.ware_sku_count

        assert cancel_block_res['code'] == 200
        assert after_cancel_block_inventory == self.expect_inventory


if __name__ == '__main__':
    pytest.main()
