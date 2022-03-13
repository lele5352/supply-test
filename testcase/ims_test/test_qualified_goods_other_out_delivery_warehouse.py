import time

import pytest

from testcase import *


class TestQualifiedGoodsOtherOutDeliveryWarehouse(object):
    def setup_class(self):
        self.warehouse_id = delivery_warehouse_id
        self.target_warehouse_id = delivery_warehouse_id

        self.sale_sku_count = 2

    # @pytest.mark.skip(reason='test')
    def test_1_two_suites_multiple_goods_other_out_by_time(self):
        """
        tips：销售sku不能是单品，单品会单件成套，不存在计算成套逻辑
        测试场景：
        构造n套库存，分多次循环执行良品其他出库：
        单次循环内按bom_detail内的仓库sku，每次出库1件，直到每个仓库sku库存都出完；
        双次循环内按bom_detail内的仓库sku进行倒置排序，然后每次出库1件，直到每个仓库sku库存都出完；
        期望：
        每次循环开始出库第一个仓库sku后，中央库存、销售商品总库存、现货库存扣去1套，后续此套内继续出库不扣中央库存、销售商品总库存、现货库存，只扣库位库存，仓库商品总库存
        """
        sj_kw_ids = fsj_kw_ids
        ims.delete_qualified_inventory([sale_sku])
        # 其他入库生成库存
        ims.add_qualified_stock_by_other_in(
            sale_sku,
            bom,
            self.sale_sku_count,
            sj_kw_ids,
            self.warehouse_id,
            self.target_warehouse_id
        )
        self.expect_inventory = ims.get_qualified_inventory(
            sale_sku,
            self.warehouse_id,
            self.target_warehouse_id)
        mix_list = list(zip(sj_kw_ids, bom_detail.items()))
        for index in range(self.sale_sku_count):
            if (index % 2) != 0:
                mix_list.reverse()
            out_count = 0
            for location_id, detail in mix_list:
                for count in range(detail[1]):
                    out_count += 1
                    ware_sku_list = [{
                        "qty": 1,
                        "storageLocationId": location_id,
                        "wareSkuCode": detail[0]
                    }]
                    block_res = ims.qualified_goods_other_out_block(
                        ware_sku_list,
                        self.warehouse_id,
                        self.target_warehouse_id)
                    # 调用其他出库预占库存接口后获取库存数据，用于与构造的期望库存数据进行比对
                    after_block_inventory = ims.get_qualified_inventory(
                        sale_sku,
                        self.warehouse_id,
                        self.target_warehouse_id)
                    print(after_block_inventory)
                    # 构造期望库存
                    if out_count == 1:
                        # 如果是本套的第一件，则销售商品总库存、现货库存、仓库商品总库存、库位总库存、库位库存
                        self.expect_inventory['central_remain'] -= 1
                        self.expect_inventory['spot_goods_remain'] -= 1
                        self.expect_inventory[detail[0]][location_id]['block'] += 1
                        self.expect_inventory[detail[0]]['warehouse_total']['block'] += 1
                        self.expect_inventory[detail[0]]['location_total']['block'] += 1

                    else:
                        # 不是本套第一件只预占仓库商品总库存、库位总库存、库位库存
                        self.expect_inventory[detail[0]][location_id]['block'] += 1
                        self.expect_inventory[detail[0]]['warehouse_total']['block'] += 1
                        self.expect_inventory[detail[0]]['location_total']['block'] += 1

                    assert block_res['code'] == 200
                    assert after_block_inventory == self.expect_inventory

                    delivery_out_res = ims.qualified_goods_other_out_delivered(
                        ware_sku_list,
                        self.warehouse_id,
                        self.target_warehouse_id
                    )
                    after_delivered_inventory = ims.get_qualified_inventory(
                        sale_sku,
                        self.warehouse_id,
                        self.target_warehouse_id)
                    if out_count == 1:
                        self.expect_inventory['central_stock'] -= 1
                        self.expect_inventory['spot_goods_stock'] -= 1
                        self.expect_inventory[detail[0]][location_id]['stock'] -= 1
                        self.expect_inventory[detail[0]][location_id]['block'] -= 1
                        self.expect_inventory[detail[0]]['warehouse_total']['stock'] -= 1
                        self.expect_inventory[detail[0]]['warehouse_total']['block'] -= 1
                        self.expect_inventory[detail[0]]['location_total']['stock'] -= 1
                        self.expect_inventory[detail[0]]['location_total']['block'] -= 1
                    else:
                        self.expect_inventory[detail[0]][location_id]['stock'] -= 1
                        self.expect_inventory[detail[0]][location_id]['block'] -= 1
                        self.expect_inventory[detail[0]]['warehouse_total']['stock'] -= 1
                        self.expect_inventory[detail[0]]['warehouse_total']['block'] -= 1
                        self.expect_inventory[detail[0]]['location_total']['stock'] -= 1
                        self.expect_inventory[detail[0]]['location_total']['block'] -= 1

                    assert delivery_out_res['code'] == 200
                    assert after_delivered_inventory == self.expect_inventory


if __name__ == '__main__':
    pytest.main()
