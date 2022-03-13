import pytest

from testcase import *


class TestUnqualifiedGoodsChangedToQualifiedGoods(object):
    """库内管理-库内转良"""

    def setup_class(self):
        self.warehouse_id = delivery_warehouse_id
        self.target_warehouse_id = delivery_warehouse_id
        self.ware_sku_count = 10
        self.sj_kw_id = fsj_kw_ids[0]
        self.cp_kw_id = fcp_kw_id
        ims.delete_unqualified_inventory(sale_sku)
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
        先通过其他入库+良转次生成n件指定仓库sku的次品库存；
        然后循环预占再出库发货
        """
        for index in range(self.ware_sku_count):
            ware_sku_dict = {
                "qty": 1,
                "storageLocationId": self.cp_kw_id,
                "wareSkuCode": ware_sku
            }
            block_res = ims.unqualified_goods_other_out_block([ware_sku_dict], self.warehouse_id)

            self.expect_inventory[ware_sku][self.cp_kw_id]['block'] += 1
            self.expect_inventory[ware_sku]['total']['block'] += 1

            after_block_inventory = ims.get_unqualified_inventory(
                sale_sku,
                bom,
                self.warehouse_id
            )
            assert block_res['code'] == 200
            assert after_block_inventory == self.expect_inventory

            delivered_res = ims.unqualified_goods_other_out_delivered([ware_sku_dict], self.warehouse_id)
            self.expect_inventory[ware_sku][self.cp_kw_id]['block'] -= 1
            self.expect_inventory[ware_sku]['total']['block'] -= 1
            self.expect_inventory[ware_sku][self.cp_kw_id]['stock'] -= 1
            self.expect_inventory[ware_sku]['total']['stock'] -= 1

            after_delivered_inventory = ims.get_unqualified_inventory(
                sale_sku,
                bom,
                self.warehouse_id
            )

            assert delivered_res['code'] == 200
            assert after_delivered_inventory == self.expect_inventory


if __name__ == '__main__':
    pytest.main()
