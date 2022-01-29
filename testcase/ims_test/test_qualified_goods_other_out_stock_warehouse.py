import pytest

from testcase import *


class TestQualifiedGoodsOtherOutStockWarehouse(object):
    def setup_class(self):
        self.ims = ims
        self.sale_sku_code = sale_sku_code
        self.warehouse_id = stock_warehouse_id
        self.target_warehouse_id = ''
        self.bom_version = bom_version
        self.bom_detail = bom_detail
        self.sale_sku_count = 2
        self.sj_location_ids = bsj_location_ids
        self.ims.delete_ims_data(self.sale_sku_code)
        # 采购入库生成库存
        self.ims.add_stock_by_purchase_into_warehouse(
            self.sale_sku_code, self.bom_version,
            self.sj_location_ids,
            self.sale_sku_count,
            self.warehouse_id,
            self.target_warehouse_id)
        self.expect_inventory = self.ims.get_current_inventory(
            self.sale_sku_code,
            self.bom_version,
            self.warehouse_id,
            self.target_warehouse_id)

    # @pytest.mark.skip(reason='test')
    def test_1_qualified_goods_other_out_delivery_warehouse(self):
        """
        tips：销售sku不能是单品，单品会单件成套，不存在计算成套逻辑
        测试场景：
        构造n套库存，分多次循环执行良品其他出库：
        单次循环内按bom_detail内的仓库sku，每次出库1件，直到每个仓库sku库存都出完；
        双次循环内按bom_detail内的仓库sku进行倒置排序，然后每次出库1件，直到每个仓库sku库存都出完；
        期望：
        每次循环开始出库第一个仓库sku后，中央库存、销售商品总库存、现货库存扣去1套，后续此套内继续出库不扣中央库存、销售商品总库存、现货库存，只扣库位库存，仓库商品总库存
        """
        mix_list = list(zip(self.sj_location_ids, self.bom_detail.items()))
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
                    block_res = self.ims.qualified_goods_other_out_block(
                        ware_sku_list,
                        self.warehouse_id,
                        self.target_warehouse_id)
                    # 调用其他出库预占库存接口后获取库存数据，用于与构造的期望库存数据进行比对
                    after_block_inventory = self.ims.get_current_inventory(
                        self.sale_sku_code,
                        self.bom_version,
                        self.warehouse_id,
                        self.target_warehouse_id)

                    # 构造期望库存
                    if out_count == 1:
                        # 如果是本套的第一件，则预占中央库存、销售商品总库存、现货库存、仓库商品总库存、库位库存
                        self.expect_inventory['central_inventory_block'] += 1
                        self.expect_inventory['central_inventory_sale_block'] += 1
                        self.expect_inventory['goods_inventory_spot_goods_block'] += 1
                        self.expect_inventory[detail[0]][location_id]['block'] += 1
                        self.expect_inventory[detail[0]]['total']['block'] += 1
                    else:
                        # 不是本套第一件只预占仓库商品总库存、库位库存
                        self.expect_inventory[detail[0]][location_id]['block'] += 1
                        self.expect_inventory[detail[0]]['total']['block'] += 1

                    assert block_res['code'] == 200
                    assert after_block_inventory == self.expect_inventory

                    delivery_out_res = self.ims.qualified_goods_other_out_delivered(
                        ware_sku_list,
                        self.warehouse_id,
                        self.target_warehouse_id
                    )
                    after_delivered_inventory = self.ims.get_current_inventory(
                        self.sale_sku_code,
                        self.bom_version,
                        self.warehouse_id,
                        self.target_warehouse_id)
                    if out_count == 1:
                        self.expect_inventory['central_inventory_stock'] -= 1
                        self.expect_inventory['central_inventory_block'] -= 1
                        self.expect_inventory['central_inventory_sale_stock'] -= 1
                        self.expect_inventory['central_inventory_sale_block'] -= 1
                        self.expect_inventory['goods_inventory_spot_goods_stock'] -= 1
                        self.expect_inventory['goods_inventory_spot_goods_block'] -= 1
                        self.expect_inventory[detail[0]][location_id]['stock'] -= 1
                        self.expect_inventory[detail[0]][location_id]['block'] -= 1
                        self.expect_inventory[detail[0]]['total']['stock'] -= 1
                        self.expect_inventory[detail[0]]['total']['block'] -= 1
                    else:
                        self.expect_inventory[detail[0]][location_id]['stock'] -= 1
                        self.expect_inventory[detail[0]][location_id]['block'] -= 1
                        self.expect_inventory[detail[0]]['total']['stock'] -= 1
                        self.expect_inventory[detail[0]]['total']['block'] -= 1

                    assert delivery_out_res['code'] == 200
                    assert after_delivered_inventory == self.expect_inventory


if __name__ == '__main__':
    pytest.main()
