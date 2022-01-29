import pytest

from testcase import *


class TestUnqualifiedGoodsOtherOut(object):
    def setup_class(self):
        self.ims = ims
        self.warehouse_id = delivery_warehouse_id
        self.target_warehouse_id = delivery_warehouse_id
        self.ware_sku_code = ware_sku_code
        self.sale_sku_code = sale_sku_code
        self.bom_version = bom_version
        self.ware_sku_count = 10
        self.sj_location_id = fsj_location_ids[0]
        self.cp_location_id = fcp_location_id
        self.ims.delete_unqualified_goods_inventory_data(self.sale_sku_code, self.bom_version, self.warehouse_id)
        self.ims.add_unqualified_stock_by_other_in(
            self.ware_sku_code,
            self.sj_location_id,
            self.cp_location_id,
            self.ware_sku_count,
            self.warehouse_id,
            self.target_warehouse_id)
        self.expect_inventory = self.ims.get_unqualified_inventory(
            self.sale_sku_code,
            self.bom_version,
            self.warehouse_id)

    # @pytest.mark.skip(reason='test')
    def test_1_unqualified_goods_other_out_delivery_warehouse(self):
        """
        tips：销售sku不能是单品，单品会单件成套，不存在计算成套逻辑
        测试场景：
        先通过其他入库+良转次生成n件指定仓库sku的次品库存；
        然后循环预占再出库发货
        """
        for index in range(self.ware_sku_count):
            ware_sku_dict = {
                "qty": 1,
                "storageLocationId": self.cp_location_id,
                "wareSkuCode": self.ware_sku_code
            }
            block_res = self.ims.unqualified_goods_other_out_block([ware_sku_dict], self.warehouse_id)

            self.expect_inventory[self.ware_sku_code][self.cp_location_id]['block'] += 1
            self.expect_inventory[self.ware_sku_code]['total']['block'] += 1

            after_block_inventory = self.ims.get_unqualified_inventory(
                self.sale_sku_code,
                self.bom_version,
                self.warehouse_id)
            assert block_res['code'] == 200
            assert after_block_inventory == self.expect_inventory

            delivered_res = self.ims.unqualified_goods_other_out_delivered([ware_sku_dict], self.warehouse_id)
            self.expect_inventory[self.ware_sku_code][self.cp_location_id]['block'] -= 1
            self.expect_inventory[self.ware_sku_code]['total']['block'] -= 1
            self.expect_inventory[self.ware_sku_code][self.cp_location_id]['stock'] -= 1
            self.expect_inventory[self.ware_sku_code]['total']['stock'] -= 1

            after_delivered_inventory = self.ims.get_unqualified_inventory(
                self.sale_sku_code,
                self.bom_version,
                self.warehouse_id)

            assert delivered_res['code'] == 200
            assert after_delivered_inventory == self.expect_inventory


if __name__ == '__main__':
    pytest.main()
