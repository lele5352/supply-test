import pytest

from testcase import *


class TestUnqualifiedGoodsChangedToQualifiedGoods(object):
    """库内管理-库内转次"""

    def setup_class(self):
        self.warehouse_id = delivery_warehouse_id
        self.target_warehouse_id = delivery_warehouse_id
        self.sale_sku_count = 2
        self.sj_kw_ids = fsj_kw_ids
        self.cp_kw_id = fcp_kw_id
        ims.delete_qualified_inventory([sale_sku])
        ims.delete_unqualified_inventory(sale_sku)
        ims.add_stock_by_purchase_in(
            sale_sku,
            bom,
            self.sj_kw_ids,
            self.sale_sku_count,
            self.warehouse_id,
            self.target_warehouse_id
        )
        self.expect_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.target_warehouse_id
        )
        self.expect_unqualified_inventory = ims.get_unqualified_inventory(
            sale_sku,
            bom,
            self.warehouse_id
        )

    # @pytest.mark.skip(reason='test')
    def test_1_qualified_goods_changed_to_unqualified_goods(self):
        """
        tips：销售sku不能是单品，单品会单件成套，不存在计算成套逻辑
        测试场景：
        先通过采购入库2套销售商品库存，再每套按仓库sku逐件转次；
        """
        mix_list = list(zip(self.sj_kw_ids, bom_detail.items()))
        for index in range(self.sale_sku_count):
            if (index % 2) != 0:
                mix_list.reverse()
            changed_count = 0
            for location_id, detail in mix_list:
                for count in range(detail[1]):
                    changed_count += 1
                    turn_to_unqualified_goods_res = ims.turn_to_unqualified_goods(
                        detail[0],
                        location_id,
                        self.cp_kw_id,
                        1,
                        self.warehouse_id,
                        self.target_warehouse_id
                    )

                    # 构造期望库存
                    if changed_count == 1:
                        # 如果是本套的第一件，则中央库存、销售商品总库存、现货库存、仓库商品总库存、库位库存的stock都扣减1
                        self.expect_inventory['central_inventory_stock'] -= 1
                        self.expect_inventory['central_stock'] -= 1
                        self.expect_inventory['spot_goods_stock'] -= 1
                        self.expect_inventory[detail[0]][location_id]['stock'] -= 1
                        self.expect_inventory[detail[0]]['total']['stock'] -= 1
                    else:
                        # 不是本套第一件只扣减仓库商品总库存、库位库存
                        self.expect_inventory[detail[0]][location_id]['stock'] -= 1
                        self.expect_inventory[detail[0]]['total']['stock'] -= 1
                    # 转次后仓库sku的次品库存对应增加

                    if not self.expect_unqualified_inventory.get(detail[0]):
                        self.expect_unqualified_inventory.update(
                            {
                                detail[0]: {
                                    self.cp_kw_id: {'stock': 1, 'block': 0},
                                    'total': {'stock': 1, 'block': 0}
                                }
                            }
                        )
                    else:
                        self.expect_unqualified_inventory[detail[0]][self.cp_kw_id]['stock'] += 1
                        self.expect_unqualified_inventory[detail[0]]['total']['stock'] += 1

                    # 获取转次后的良品库存
                    current_inventory = ims.get_inventory(
                        sale_sku,
                        bom,
                        self.warehouse_id,
                        self.target_warehouse_id)
                    current_unqualified_inventory = ims.get_unqualified_inventory(
                        sale_sku,
                        bom,
                        self.warehouse_id
                    )
                    assert turn_to_unqualified_goods_res['code'] == 200
                    assert self.expect_inventory == current_inventory
                    assert self.expect_unqualified_inventory == current_unqualified_inventory


if __name__ == '__main__':
    pytest.main()
