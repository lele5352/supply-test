import pytest

from testcase.ims_test import *


class TestCancelUnqualifiedGoodsOtherOut(object):
    def setup_class(self):
        self.ims = ims
        self.warehouse_id = delivery_warehouse_id
        self.target_warehouse_id = delivery_warehouse_id
        self.ware_sku_code = ware_sku_code

        self.ware_sku_count = 10
        self.sj_location_code = self.ims.wms_api.get_location_codes(1, 5, self.warehouse_id)
        self.sj_location_id = self.ims.wms_api.get_location_id(self.sj_location_code, self.warehouse_id)
        self.cp_location_code = self.ims.wms_api.get_location_codes(1, 6, self.warehouse_id)
        self.cp_location_id = self.ims.wms_api.get_location_id(self.cp_location_code, self.warehouse_id)
        self.ims.delete_unqualified_goods_inventory_data(self.ware_sku_code, self.warehouse_id)
        self.ims.add_unqualified_stock_by_other_in(self.ware_sku_code, self.sj_location_id, self.cp_location_id,
                                                   self.ware_sku_count, self.warehouse_id, self.target_warehouse_id)
        self.expect_inventory = self.ims.get_unqualified_inventory(self.ware_sku_code, self.warehouse_id)

    # @pytest.mark.skip(reason='test')
    def test_1_unqualified_goods_other_out_delivery_warehouse(self):
        """
        tips：销售sku不能是单品，单品会单件成套，不存在计算成套逻辑
        测试场景：

        """
        ware_sku_dict = {
            "qty": self.ware_sku_count,
            "storageLocationId": self.cp_location_id,
            "wareSkuCode": self.ware_sku_code
        }
        block_res = self.ims.unqualified_goods_other_out_block([ware_sku_dict], self.warehouse_id)

        self.expect_inventory[self.ware_sku_code][self.cp_location_id]['block'] += self.ware_sku_count
        self.expect_inventory[self.ware_sku_code]['total']['block'] += self.ware_sku_count

        after_block_inventory = self.ims.get_unqualified_inventory(
            self.ware_sku_code,
            self.warehouse_id
        )
        assert block_res['code'] == 200
        assert after_block_inventory == self.expect_inventory

        source_no = block_res['data'][0]['sourceNo']
        block_book_id = block_res['data'][0]['blockBookId']

        cancel_block_res = self.ims.cancel_unqualified_goods_other_out_block(block_book_id, source_no)
        after_cancel_block_inventory = self.ims.get_unqualified_inventory(
            self.ware_sku_code,
            self.warehouse_id
        )
        self.expect_inventory[self.ware_sku_code][self.cp_location_id]['block'] -= self.ware_sku_count
        self.expect_inventory[self.ware_sku_code]['total']['block'] -= self.ware_sku_count

        assert cancel_block_res['code'] == 200
        assert after_cancel_block_inventory == self.expect_inventory


if __name__ == '__main__':
    pytest.main()