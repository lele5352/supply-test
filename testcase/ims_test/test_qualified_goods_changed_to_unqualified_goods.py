import time

import pytest

from testcase.ims_test import *


class TestUnqualifiedGoodsChangedToQualifiedGoods(object):
    """库内管理-库内转次"""

    def setup_class(self):
        self.ims = ims
        self.warehouse_id = delivery_warehouse_id
        self.target_warehouse_id = delivery_warehouse_id
        self.sale_sku_code = sale_sku_code
        self.bom_version = bom_version
        self.bom_detail = bom_detail
        self.sale_sku_count = 2
        self.sj_location_ids = fsj_location_ids
        self.cp_location_id = fcp_location_id
        self.ims.delete_ims_data(self.sale_sku_code, self.warehouse_id)
        self.ims.delete_unqualified_goods_inventory_data(self.sale_sku_code, self.bom_version, self.warehouse_id)
        self.ims.add_stock_by_purchase_into_warehouse(
            self.sale_sku_code,
            self.bom_version,
            self.sj_location_ids,
            self.sale_sku_count,
            self.warehouse_id,
            self.target_warehouse_id
        )
        self.expect_inventory = self.ims.get_current_inventory(
            self.sale_sku_code,
            self.bom_version,
            self.warehouse_id,
            self.target_warehouse_id
        )
        self.expect_unqualified_inventory = self.ims.get_unqualified_inventory(
            self.sale_sku_code,
            self.bom_version,
            self.warehouse_id
        )

    # @pytest.mark.skip(reason='test')
    def test_1_qualified_goods_changed_to_unqualified_goods(self):
        """
        tips：销售sku不能是单品，单品会单件成套，不存在计算成套逻辑
        测试场景：
        先通过采购入库2套销售商品库存，再每套按仓库sku逐件转次；
        """
        mix_list = list(zip(self.sj_location_ids, self.bom_detail.items()))
        for index in range(self.sale_sku_count):
            if (index % 2) != 0:
                mix_list.reverse()
            changed_count = 0
            for location_id, detail in mix_list:
                for count in range(detail[1]):
                    changed_count += 1
                    turn_to_unqualified_goods_res = self.ims.turn_to_unqualified_goods(
                        detail[0],
                        location_id,
                        self.cp_location_id,
                        1,
                        self.warehouse_id,
                        self.target_warehouse_id
                    )

                    # 构造期望库存
                    if changed_count == 1:
                        # 如果是本套的第一件，则中央库存、销售商品总库存、现货库存、仓库商品总库存、库位库存的stock都扣减1
                        self.expect_inventory['central_inventory_stock'] -= 1
                        self.expect_inventory['central_inventory_sale_stock'] -= 1
                        self.expect_inventory['goods_inventory_spot_goods_stock'] -= 1
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
                                    self.cp_location_id: {'stock': 1, 'block': 0},
                                    'total': {'stock': 1, 'block': 0}
                                }
                            }

                        )
                    else:
                        self.expect_unqualified_inventory[detail[0]][self.cp_location_id]['stock'] += 1
                        self.expect_unqualified_inventory[detail[0]]['total']['stock'] += 1

                    # 获取转次后的良品库存
                    current_inventory = self.ims.get_current_inventory(
                        self.sale_sku_code,
                        self.bom_version,
                        self.warehouse_id,
                        self.target_warehouse_id)
                    current_unqualified_inventory = self.ims.get_unqualified_inventory(
                        self.sale_sku_code,
                        self.bom_version,
                        self.warehouse_id
                    )
                    print(current_inventory)
                    print(current_unqualified_inventory)

                    assert turn_to_unqualified_goods_res['code'] == 200
                    assert self.expect_inventory == current_inventory
                    assert self.expect_unqualified_inventory == current_unqualified_inventory


if __name__ == '__main__':
    pytest.main()